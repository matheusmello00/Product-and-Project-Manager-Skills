#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Check a backlog written in Markdown: epics, stories, acceptance criteria and Gherkin scenarios.

The Markdown file IS the backlog (see references/backlog-schema.md for the format). This script reads it
directly — there is no JSON to prepare — and reports what is missing or inconsistent before the backlog
is baselined or pushed to a tracker. Optionally it exports the scenarios as Gherkin `.feature` files.

Interface:
    python scripts/backlog_check.py backlog.md                       # human-readable report (stdout)
    python scripts/backlog_check.py backlog.md --features features   # also write one .feature per story
    python scripts/backlog_check.py backlog.md --json                # report as JSON only
    python scripts/backlog_check.py --help

What it checks (deterministic, no judgement on business value):
  ISSUES   (must fix before the backlog is baselined)
    - duplicate IDs; story without epic or pointing to an unknown epic
    - story with an incomplete As a / I want / So that, or without a description
    - fewer than 2 acceptance criteria, or a criterion missing Given / When / Then
    - priority outside Must / Should / Could
    - story with no test scenarios; scenario (Gherkin) without a title, When or Then;
      scenario with an unknown type or covering a criterion that does not exist;
      <placeholder> in the steps with no Examples table or column
    - dependency on an unknown story, on itself, or forming a cycle
    - epic without name, description, success metrics or acceptance criteria
  WARNINGS (review, may be legitimate)
    - requirement not covered by any story; story with no traceability
    - requirement not assigned to any epic, or owned by more than one epic
    - requirement in the inventory with no source reference
    - story with open questions (not spec-ready)
    - vague wording in a criterion's or a scenario's "Then" (works, correctly, fast, easy ...)
    - acceptance criterion not covered by any scenario; story with only happy-path scenarios;
      scenario with no Given or not linked to any criterion
    - story with many criteria (possibly too big); epic with 1 or too many stories; epic with no stories
    - Must stories above 60% of the backlog (priority inflation)
    - zero stories; parts of the file the script could not read

Exit codes: 0 = OK (findings do not change the exit code); 2 = usage error or unreadable input.
"""

import json
import re
import sys

PRIORITIES = ("Must", "Should", "Could")
SCENARIO_TYPES = ("happy", "alternative", "negative", "boundary", "permission")
NON_HAPPY_TYPES = {"alternative", "negative", "boundary", "permission"}
MAX_AC_PER_STORY = 5
MAX_STORIES_PER_EPIC = 5
MUST_RATIO_LIMIT = 0.6
VAGUE_TERMS = [
    "correctly", "properly", "works", "work as expected", "as expected", "fast", "quickly",
    "easy", "easily", "user-friendly", "intuitive", "appropriate", "seamless", "etc",
]
_VAGUE_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in VAGUE_TERMS) + r")\b", re.IGNORECASE)


def _s(value):
    return str(value).strip() if value is not None else ""


def _lines(value):
    """A Gherkin step field: one string, or a list of strings (first = Given/When/Then, rest = And/But)."""
    if isinstance(value, (list, tuple)):
        return [_s(v) for v in value if _s(v)]
    return [_s(value)] if _s(value) else []


def require_schema(data, known, main_key, ctx):
    """Two-layer input guard.

    1. If no recognised key is present, the payload does not match the schema
       -> ValueError (exit 2). Catches a normalisation step that produced the wrong keys.
    2. If the main collection is missing, it is likewise a schema error. If it is present
       and empty, it is a legitimate result but returns a warning: zero stories may mean
       "nothing to decompose" or "the PRD was not read", and the script cannot tell them apart.
    """
    present = [k for k in known if k in data]
    if not present:
        raise ValueError(
            f"the payload does not match the schema of {ctx}. "
            f"Keys received: {sorted(data.keys()) or 'none'}. "
            f"Expected (at least one): {sorted(known)}."
        )
    if main_key not in data:
        raise ValueError(
            f"missing required key '{main_key}' in the input of {ctx}. "
            f"Keys received: {sorted(data.keys())}."
        )
    return []


def _find_cycle(graph):
    """Return one dependency cycle as a list of IDs, or None."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    stack = []

    def visit(n):
        color[n] = GREY
        stack.append(n)
        for m in graph.get(n, ()):
            if m not in color:
                continue
            if color[m] == GREY:
                return stack[stack.index(m):] + [m]
            if color[m] == WHITE:
                found = visit(m)
                if found:
                    return found
        stack.pop()
        color[n] = BLACK
        return None

    for node in list(graph):
        if color[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


def analyse(data):
    warnings = require_schema(
        data, {"project", "source_prd", "requirements", "epics", "stories"},
        "stories", "backlog-creator")
    warnings.extend(data.get("_parse_warnings") or [])
    issues = []

    epics = data.get("epics") or []
    stories = data.get("stories") or []
    # `requirements` is the inventory: plain IDs ("RF.01") or objects {id, kind, text, source}.
    requirements = []
    for r in (data.get("requirements") or []):
        rid = _s(r.get("id")) if isinstance(r, dict) else _s(r)
        if not rid:
            continue
        requirements.append(rid)
        if isinstance(r, dict) and not _s(r.get("source")):
            warnings.append(f"{rid}: requirement has no source reference (where in the document it came from).")

    if not stories:
        warnings.append(
            "Zero stories in the input. DO NOT report an empty backlog as done: confirm the PRD was read "
            "and that its functional requirements were extracted. See references/story-writing.md §1."
        )

    # --- IDs -----------------------------------------------------------------------------
    epic_ids, seen = set(), set()
    for e in epics:
        eid = _s(e.get("id"))
        if not eid:
            issues.append("An epic has no id.")
            continue
        if eid in seen:
            issues.append(f"{eid}: duplicate id.")
        seen.add(eid)
        epic_ids.add(eid)

    story_ids = set()
    for st in stories:
        sid = _s(st.get("id"))
        if not sid:
            issues.append(f"Story '{_s(st.get('title')) or '(untitled)'}' has no id.")
            continue
        if sid in seen:
            issues.append(f"{sid}: duplicate id.")
        seen.add(sid)
        story_ids.add(sid)

    # --- epics ---------------------------------------------------------------------------
    stories_by_epic = {eid: [] for eid in epic_ids}
    for st in stories:
        eid = _s(st.get("epic"))
        sid = _s(st.get("id")) or "(no id)"
        if not eid:
            issues.append(f"{sid}: story has no epic.")
        elif eid not in epic_ids:
            issues.append(f"{sid}: points to unknown epic {eid}.")
        else:
            stories_by_epic[eid].append(sid)

    for e in epics:
        eid = _s(e.get("id")) or "(no id)"
        missing = [lbl for key, lbl in (("name", "name"), ("description", "description"),
                                        ("success_metrics", "success metrics")) if not _s(e.get(key))]
        if missing:
            issues.append(f"{eid}: epic is missing {', '.join(missing)}.")
        if not [a for a in (e.get("acceptance_criteria") or []) if _s(a)]:
            issues.append(f"{eid}: epic has no acceptance criteria.")
        n = len(stories_by_epic.get(eid, []))
        if n == 0:
            warnings.append(f"{eid}: epic has no stories.")
        elif n == 1:
            warnings.append(f"{eid}: epic has a single story — probably a story, not an epic (or work at epic level).")
        elif n > MAX_STORIES_PER_EPIC:
            warnings.append(f"{eid}: epic has {n} stories (target 3–{MAX_STORIES_PER_EPIC}) — group by outcome or split the epic.")

    # Requirement ownership: each requirement belongs to exactly one epic (only checked when
    # the epics declare their requirements).
    owners = {}
    for e in epics:
        for r in (e.get("requirements") or []):
            if _s(r):
                owners.setdefault(_s(r), []).append(_s(e.get("id")) or "(no id)")
    if owners:
        for r, es in owners.items():
            if len(es) > 1:
                warnings.append(f"{r}: requirement is owned by more than one epic ({', '.join(es)}) — assign it to exactly one.")
        for r in requirements:
            if r not in owners:
                warnings.append(f"{r}: requirement is not assigned to any epic.")

    # --- stories -------------------------------------------------------------------------
    graph = {}
    covered = set()
    counts = {p: 0 for p in PRIORITIES}
    invalid_priority = 0
    scenario_total = 0
    open_total = 0

    for st in stories:
        sid = _s(st.get("id")) or "(no id)"

        missing = [lbl for key, lbl in (("as_a", "As a"), ("i_want", "I want"), ("so_that", "So that"))
                   if not _s(st.get(key))]
        if missing:
            issues.append(f"{sid}: incomplete story statement — missing {', '.join(missing)}.")
        if not _s(st.get("description")):
            issues.append(f"{sid}: story has no description (expected behaviour and business rules).")

        ac = st.get("acceptance_criteria") or []
        if len(ac) < 2:
            issues.append(f"{sid}: {len(ac)} acceptance criteria (minimum 2).")
        elif len(ac) > MAX_AC_PER_STORY:
            warnings.append(f"{sid}: {len(ac)} acceptance criteria (> {MAX_AC_PER_STORY}) — story may be too big to be Small.")
        for i, c in enumerate(ac, 1):
            c = c if isinstance(c, dict) else {}
            gaps = [k.capitalize() for k in ("given", "when", "then") if not _s(c.get(k))]
            if gaps:
                issues.append(f"{sid}: criterion {i} is missing {', '.join(gaps)}.")
            vague = _VAGUE_RE.search(_s(c.get("then")))
            if vague:
                warnings.append(
                    f"{sid}: criterion {i} has vague wording in Then ('{vague.group(1)}') — make it observable and testable.")

        open_q = [q for q in (st.get("open_questions") or []) if _s(q)]
        if open_q:
            open_total += len(open_q)
            warnings.append(f"{sid}: {len(open_q)} open question(s) — not spec-ready until resolved: {'; '.join(_s(q) for q in open_q)}")

        scenarios = st.get("scenarios") or []
        if not scenarios:
            issues.append(f"{sid}: no test scenarios.")
        covered_ac, seen_types = set(), set()
        for j, sc in enumerate(scenarios, 1):
            sc = sc if isinstance(sc, dict) else {}
            scenario_total += 1
            label = f"{sid}/{_s(sc.get('id')) or f'scenario {j}'}"
            given, when, then = _lines(sc.get("given")), _lines(sc.get("when")), _lines(sc.get("then"))
            if not _s(sc.get("title")):
                issues.append(f"{label}: scenario is missing a title.")
            if not when:
                issues.append(f"{label}: scenario has no When step.")
            if not then:
                issues.append(f"{label}: scenario has no Then step.")
            if not given:
                warnings.append(f"{label}: scenario has no Given step (precondition).")
            placeholders = set(re.findall(r"<([^<>]+)>", " ".join(given + when + then)))
            examples = sc.get("examples") or []
            if placeholders and not examples:
                issues.append(f"{label}: uses placeholders ({', '.join(sorted(placeholders))}) but has no Examples table.")
            elif examples:
                rows = [x for x in examples if isinstance(x, dict)]
                if not rows:
                    issues.append(f"{label}: Examples must be a list of rows (objects with one value per column).")
                else:
                    cols = set(rows[0].keys())
                    absent = placeholders - cols
                    if absent:
                        issues.append(f"{label}: placeholders without an Examples column: {', '.join(sorted(absent))}.")
                    if any(set(r.keys()) != cols for r in rows):
                        warnings.append(f"{label}: Examples rows do not all have the same columns.")
                    if not placeholders:
                        warnings.append(f"{label}: has Examples but no <placeholder> in the steps.")
            stype = _s(sc.get("type")).lower()
            if stype in SCENARIO_TYPES:
                seen_types.add(stype)
            else:
                issues.append(f"{label}: type '{_s(sc.get('type')) or 'empty'}' is not one of {', '.join(SCENARIO_TYPES)}.")
            links = sc.get("covers") or []
            if not links:
                warnings.append(f"{label}: scenario is not linked to any acceptance criterion.")
            for ref in links:
                try:
                    n = int(ref)
                except (TypeError, ValueError):
                    n = 0
                if 1 <= n <= len(ac):
                    covered_ac.add(n)
                else:
                    issues.append(f"{label}: covers criterion '{ref}', which does not exist (story has {len(ac)}).")
            vague = _VAGUE_RE.search(" ".join(then))
            if vague:
                warnings.append(f"{label}: vague wording in Then ('{vague.group(1)}') — make it observable.")
        if scenarios:
            for n in range(1, len(ac) + 1):
                if n not in covered_ac:
                    warnings.append(f"{sid}: acceptance criterion {n} is not covered by any scenario.")
            if not (seen_types & NON_HAPPY_TYPES):
                warnings.append(f"{sid}: only happy-path scenarios — add a negative, boundary, permission or alternative case.")

        prio = _s(st.get("priority")).capitalize()
        if prio in PRIORITIES:
            counts[prio] += 1
        else:
            invalid_priority += 1
            issues.append(f"{sid}: priority '{_s(st.get('priority')) or 'empty'}' is not Must / Should / Could.")

        reqs = [_s(r) for r in (st.get("requirements") or []) if _s(r)]
        if requirements:
            if not reqs:
                warnings.append(f"{sid}: story is not traced to any requirement.")
            for r in reqs:
                if r not in requirements:
                    warnings.append(f"{sid}: references {r}, which is not in the requirements list.")
        covered.update(reqs)

        deps = [_s(d) for d in (st.get("dependencies") or []) if _s(d)]
        graph[sid] = []
        for d in deps:
            if d == sid:
                issues.append(f"{sid}: depends on itself.")
            elif d not in story_ids:
                issues.append(f"{sid}: depends on unknown story {d}.")
            else:
                graph[sid].append(d)

    cycle = _find_cycle(graph)
    if cycle:
        issues.append("Dependency cycle: " + " -> ".join(cycle) + ".")

    uncovered = [r for r in requirements if r not in covered]
    for r in uncovered:
        warnings.append(f"{r}: requirement is not covered by any story.")

    total = len(stories)
    if total >= 5 and counts["Must"] / total > MUST_RATIO_LIMIT:
        warnings.append(
            f"Must stories are {counts['Must']} of {total} ({counts['Must'] * 100 // total}%) — "
            f"priority inflation; revisit what is truly release-blocking.")

    coverage = None
    if requirements:
        coverage = round(100 * (len(requirements) - len(uncovered)) / len(requirements))

    return {
        "project": data.get("project"), "source_prd": data.get("source_prd"),
        "summary": {
            "epics": len(epics), "stories": total, "scenarios": scenario_total, "open_questions": open_total,
            "must": counts["Must"], "should": counts["Should"], "could": counts["Could"],
            "invalid_priority": invalid_priority,
            "requirements": len(requirements), "uncovered_requirements": len(uncovered),
            "coverage_pct": coverage,
            "issues": len(issues), "warnings": len(warnings),
        },
        "issues": issues, "warnings": warnings, "uncovered_requirements": uncovered,
        "stories_by_epic": stories_by_epic,
    }



# ----------------------------------------------------------------------------------------------
# Markdown reader: turns the backlog file into the structure analyse() works on.
# ----------------------------------------------------------------------------------------------

_FIELD_RE = re.compile(r"^\*\*\s*([^*:]+?)\s*:\s*\*\*\s*(.*)$|^\*\*\s*([^*:]+?)\s*\*\*\s*:\s*(.*)$")
_FIELD_KEYS = {
    "delivers": "description", "description": "description",
    "success metric": "success_metrics", "success metrics": "success_metrics",
    "requirements owned": "requirements", "requirements": "requirements",
    "acceptance criteria": "ac", "out of scope": "out_of_scope",
    "test scenarios": "scenarios", "priority": "priority", "dependencies": "dependencies",
    "open questions": "open_questions", "estimate": "estimate", "design": "design",
}
_NONE = {"", "none", "n/a", "-", "—"}


def _split_blocks(text, level):
    """Split text on markdown headings of exactly `level` (#): [(heading, [lines])]. Ignores fenced code."""
    mark = "#" * level + " "
    blocks, cur, fence = [], None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        if not fence and line.startswith(mark):
            cur = (line[len(mark):].strip(), [])
            blocks.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return blocks


def _fields(lines):
    """Split a block into (pre, {field: [lines]}). Field labels look like **Label:** and are ignored inside fences."""
    pre, fields, key, fence = [], {}, None, False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
        m = None if fence or stripped.startswith("```") else _FIELD_RE.match(stripped)
        if m:
            label = (m.group(1) or m.group(3) or "").lower()
            label = re.sub(r"\s*\(.*?\)", "", label).strip()
            rest = m.group(2) if m.group(1) else m.group(4)
            key = _FIELD_KEYS.get(label)
            if key is None:
                key = "_other"
            fields.setdefault(key, [])
            if rest.strip():
                fields[key].append(rest.strip())
        elif key is None:
            pre.append(line)
        else:
            fields[key].append(line)
    return pre, fields


def _text(lines):
    return " ".join(l.strip() for l in lines if l.strip())


def _bullets(lines):
    items = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith("```"):
            continue
        m = re.match(r"^[-*+]\s+(?:\[[ xX]\]\s*)?(.*)$", s)
        if m:
            items.append(m.group(1).strip())
        elif items:
            items[-1] += " " + s
        else:
            items.append(s)
    return items


def _tokens(lines):
    """IDs separated by commas, semicolons or spaces; 'None' means empty."""
    raw = _text(lines).replace("`", "")
    if raw.lower().strip(" .") in _NONE:
        return []
    out = []
    for tok in re.split(r"[,;\s]+", raw):
        tok = tok.strip("[]().,;")
        if tok and tok.lower() not in _NONE:
            out.append(tok)
    return out


def _statement(pre):
    text = _text(pre)
    names = {"as a": "as_a", "i want": "i_want", "so that": "so_that"}
    found = list(re.finditer(r"\*\*\s*(As a|I want|So that)\s*\*\*", text, re.I))
    out = {"as_a": "", "i_want": "", "so_that": ""}
    for i, m in enumerate(found):
        seg_end = found[i + 1].start() if i + 1 < len(found) else len(text)
        out[names[m.group(1).lower()]] = text[m.end():seg_end].strip(" ,.;")
    if not found:
        m = re.match(r"^\s*As a\s+(.+?),\s*I want\s+(.+?),\s*so that\s+(.+?)\.?\s*$", text, re.I)
        if m:
            out = {"as_a": m.group(1).strip(), "i_want": m.group(2).strip(), "so_that": m.group(3).strip()}
    return out


def _criterion(text):
    """'**Given** a **When** b **Then** c' -> {given, when, then}; a missing keyword leaves its part empty."""
    pat = r"\*\*\s*(Given|When|Then)\s*\*\*" if re.search(r"\*\*\s*(Given|When|Then)\s*\*\*", text) \
        else r"\b(Given|When|Then)\b"
    found = list(re.finditer(pat, text))
    out = {"given": "", "when": "", "then": ""}
    for i, m in enumerate(found):
        seg_end = found[i + 1].start() if i + 1 < len(found) else len(text)
        out[m.group(1).lower()] = text[m.end():seg_end].strip(" ,;")
    return out, bool(found)


def _gherkin(lines):
    """Parse fenced Gherkin (Scenario / Scenario Outline, Given/When/Then/And/But, Examples) into scenario dicts."""
    scenarios, cur, tags, last, in_ex, cols = [], None, [], None, False, None
    for raw in lines:
        l = raw.strip()
        if not l or l.startswith("#") or l.startswith("```"):
            continue
        if l.startswith("@"):
            tags += l.split()
            continue
        m = re.match(r"^(Scenario Outline|Scenario Template|Scenario)\s*:\s*(.*)$", l, re.I)
        if m:
            cur = {"title": m.group(2).strip(), "given": [], "when": [], "then": [], "examples": [], "_tags": tags}
            scenarios.append(cur)
            tags, last, in_ex, cols = [], None, False, None
            continue
        if cur is None:
            continue
        if re.match(r"^Examples\s*:", l, re.I):
            in_ex, cols = True, None
            continue
        if in_ex and l.startswith("|"):
            cells = [c.strip() for c in l.strip("|").split("|")]
            if cols is None:
                cols = cells
            else:
                cur["examples"].append(dict(zip(cols, cells)))
            continue
        m = re.match(r"^(Given|When|Then|And|But)\s+(.*)$", l, re.I)
        if m:
            kw = m.group(1).lower()
            if kw in ("and", "but"):
                if last:
                    cur[last].append(m.group(2).strip())
            else:
                last = kw
                cur[kw].append(m.group(2).strip())
    for sc in scenarios:
        ids, covers, other = "", [], []
        for t in sc.pop("_tags"):
            name = t.lstrip("@")
            ac = re.fullmatch(r"AC(\d+)", name, re.I)
            if ac:
                covers.append(int(ac.group(1)))
            elif name.upper().startswith("TC") and not ids:
                ids = name
            else:
                other.append(name)
        sc["id"], sc["covers"], sc["type"] = ids, covers, (other[0].lower() if other else "")
        if not sc["examples"]:
            sc.pop("examples")
    return scenarios


def _heading(h):
    m = re.match(r"^(\S+)\s+[—–\-]+\s+(.+?)\s*$", h)
    return (m.group(1), m.group(2)) if m else (h.split()[0] if h.split() else "", h)


def parse_markdown(text):
    """Read the backlog Markdown into the structure used by analyse(). Raises ValueError if it is not a backlog."""
    notes = []
    data = {"project": None, "source_prd": None, "requirements": [], "epics": [], "stories": []}

    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    if h1:
        name = re.sub(r"^Backlog\s*[—–\-]\s*", "", h1.group(1)).split("·")[0].strip()
        data["project"] = name or None
    src = re.search(r"^\**Sources?:?\**:?\s*(.+)$", text, re.M | re.I)
    if src:
        data["source_prd"] = src.group(1).split("·")[0].strip()

    sections = {}
    for title, lines in _split_blocks(text, 2):
        t = title.lower()
        key = "inventory" if "inventory" in t else "epics" if t.startswith("epic") else "stories" if t.startswith("stor") else None
        if key:
            sections[key] = lines
    if "stories" not in sections:
        raise ValueError("no '## Stories' section found — this does not look like a backlog in the expected format "
                         "(see references/backlog-schema.md).")

    # inventory table
    rows, header = [], None
    for line in sections.get("inventory", []):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        row = dict(zip(header, cells))
        rid = row.get("id", "").strip("` ")
        if rid:
            req = {"id": rid, "kind": row.get("kind", ""), "text": row.get("requirement", row.get("text", ""))}
            if row.get("source", "").strip():
                req["source"] = row["source"].strip()
            rows.append(req)
    data["requirements"] = rows

    # epics
    for heading, lines in _split_blocks("\n".join(["## x"] + sections.get("epics", [])), 3):
        eid, ename = _heading(heading)
        _, f = _fields(lines)
        data["epics"].append({
            "id": eid, "name": ename, "description": _text(f.get("description", [])),
            "success_metrics": _text(f.get("success_metrics", [])),
            "requirements": _tokens(f.get("requirements", [])),
            "acceptance_criteria": _bullets(f.get("ac", [])),
            "out_of_scope": _text(f.get("out_of_scope", [])),
        })

    # stories (grouped under '### EP-xx — name' headings, each story is '#### ST-xx — title')
    for epic_heading, epic_lines in _split_blocks("\n".join(["## x"] + sections["stories"]), 3):
        epic_id, _ = _heading(epic_heading)
        for heading, lines in _split_blocks("\n".join(["### x"] + epic_lines), 4):
            sid, title = _heading(heading)
            pre, f = _fields(lines)
            st = {"id": sid, "epic": epic_id, "title": title, **_statement(pre),
                  "description": _text(f.get("description", []))}
            acs = []
            for item in _bullets(f.get("ac", [])):
                crit, ok = _criterion(item)
                if not ok:
                    notes.append(f"{sid}: could not read this acceptance criterion (expected Given / When / Then): {item[:80]}")
                acs.append(crit)
            st["acceptance_criteria"] = acs
            st["scenarios"] = _gherkin(f.get("scenarios", []))
            pm = re.match(r"\s*\[?([A-Za-z]+)", _text(f.get("priority", [])))
            st["priority"] = pm.group(1) if pm else ""
            st["requirements"] = _tokens(f.get("requirements", []))
            st["dependencies"] = _tokens(f.get("dependencies", []))
            oq = [q for q in _bullets(f.get("open_questions", [])) if q.lower().strip(" .") not in _NONE]
            if len(oq) == 1 and ";" in oq[0]:
                oq = [x.strip() for x in oq[0].split(";") if x.strip()]
            st["open_questions"] = oq
            data["stories"].append(st)
    data["_parse_warnings"] = notes
    return data


# ----------------------------------------------------------------------------------------------
# Gherkin export
# ----------------------------------------------------------------------------------------------

def _tag(text):
    return "@" + re.sub(r"[^\w.\-]+", "-", _s(text)).strip("-")


def _slug(text, limit=40):
    return re.sub(r"[^a-z0-9]+", "-", _s(text).lower()).strip("-")[:limit].strip("-")


def feature_text(story, epic_name=None):
    sid = _s(story.get("id"))
    tags = [_tag(story["epic"])] if _s(story.get("epic")) else []
    tags.append(_tag(sid))
    if _s(story.get("priority")):
        tags.append(_tag(_s(story["priority"]).lower()))
    tags += [_tag(r) for r in (story.get("requirements") or []) if _s(r)]
    out = [" ".join(tags), f"Feature: {sid} — {_s(story.get('title'))}"]
    if epic_name:
        out.append(f"  # Epic: {story.get('epic')} — {epic_name}")
    out += [f"  As a {_s(story.get('as_a'))},", f"  I want {_s(story.get('i_want'))},", f"  so that {_s(story.get('so_that'))}."]
    if _s(story.get("description")):
        out.append(f"  # Description: {_s(story['description'])}")
    out.append("")
    for n, c in enumerate(story.get("acceptance_criteria") or [], 1):
        out.append(f"  # AC{n}: Given {_s(c.get('given'))} · When {_s(c.get('when'))} · Then {_s(c.get('then'))}")
    for q in story.get("open_questions") or []:
        out.append(f"  # OPEN QUESTION: {_s(q)}")
    for sc in story.get("scenarios") or []:
        out.append("")
        stags = ([_tag(sc["id"])] if _s(sc.get("id")) else []) + ([_tag(sc["type"])] if _s(sc.get("type")) else [])
        stags += [f"@AC{n}" for n in (sc.get("covers") or [])]
        if stags:
            out.append("  " + " ".join(stags))
        rows = [r for r in (sc.get("examples") or []) if isinstance(r, dict)]
        out.append(f"  {'Scenario Outline' if rows else 'Scenario'}: {_s(sc.get('title'))}")
        for kw, key in (("Given", "given"), ("When", "when"), ("Then", "then")):
            for i, step in enumerate(_lines(sc.get(key))):
                out.append(f"    {kw if i == 0 else 'And'} {step}")
        if rows:
            cols = list(rows[0].keys())
            table = [cols] + [[_s(r.get(c)) for c in cols] for r in rows]
            w = [max(len(row[i]) for row in table) for i in range(len(cols))]
            out += ["", "    Examples:"] + ["      | " + " | ".join(c.ljust(w[i]) for i, c in enumerate(row)) + " |" for row in table]
    return "\n".join(out) + "\n"


def export_features(data, outdir):
    import os
    epics = {_s(e.get("id")): _s(e.get("name")) for e in data.get("epics") or []}
    os.makedirs(outdir, exist_ok=True)
    written = []
    for st in data.get("stories") or []:
        name = f"{_slug(st.get('id'), 20)}-{_slug(st.get('title'))}.feature".strip("-")
        target = os.path.join(outdir, name)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(feature_text(st, epics.get(_s(st.get("epic")))))
        written.append(target)
    return written


def render(res):
    s = res["summary"]
    lines = [f"BACKLOG CHECK — {res.get('project') or '(project)'}"]
    if res.get("source_prd"):
        lines.append(f"Source: {res['source_prd']}")
    cov = f"{s['coverage_pct']}%" if s["coverage_pct"] is not None else "n/a (no inventory table)"
    lines.append(f"Epics: {s['epics']}  ·  Stories: {s['stories']}  ·  Scenarios: {s['scenarios']}  ·  Must/Should/Could: "
                 f"{s['must']}/{s['should']}/{s['could']}  ·  Requirement coverage: {cov}")
    lines.append(f"Open questions: {s['open_questions']}  ·  Issues: {s['issues']}  ·  Warnings: {s['warnings']}")
    lines.append("")

    lines.append("ISSUES — fix before baselining")
    for i in res["issues"]:
        lines.append(f"  !! {i}")
    if not res["issues"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("WARNINGS — read before reporting")
    for w in res["warnings"]:
        lines.append(f"  ?? {w}")
    if not res["warnings"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("STORIES BY EPIC")
    for eid, sids in res["stories_by_epic"].items():
        lines.append(f"- {eid}: {', '.join(sids) if sids else '(none)'}")
    return "\n".join(lines)


USAGE = """backlog_check.py — check a backlog written in Markdown (epics, stories, criteria, Gherkin scenarios).

Usage:
    python scripts/backlog_check.py backlog.md [--features DIR] [--json]

Arguments:
    backlog.md        the backlog, in the format described in references/backlog-schema.md

Options:
    --features DIR    also write the scenarios as Gherkin .feature files, one per story, into DIR
    --json            write only the report as JSON to stdout
    -h, --help        show this help

Exit codes:
    0  success (findings are reported, they do not change the exit code)
    2  usage error or unreadable input
"""


def main(argv):
    args = argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE.strip())
        return 0
    as_json, features_dir, positional, i = False, None, [], 0
    while i < len(args):
        a = args[i]
        if a == "--json":
            as_json = True
        elif a == "--features":
            if i + 1 >= len(args) or args[i + 1].startswith("-"):
                print("Error: --features needs an output folder.", file=sys.stderr)
                return 2
            features_dir = args[i + 1]
            i += 1
        elif a.startswith("-"):
            print(f"Error: unknown option: {a}", file=sys.stderr)
            print("Expected: --features DIR, --json or --help. Run with --help for the interface.", file=sys.stderr)
            return 2
        else:
            positional.append(a)
        i += 1
    if len(positional) != 1:
        print(f"Error: expected 1 backlog file, received {len(positional)}.", file=sys.stderr)
        print("Try: python scripts/backlog_check.py backlog.md   (--help for the interface)", file=sys.stderr)
        return 2

    path = positional[0]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print(f"Error: {path} is not a UTF-8 text file.", file=sys.stderr)
        return 2

    try:
        data = parse_markdown(text)
        result = analyse(data)
    except ValueError as exc:
        print(f"Error: invalid input. {exc}", file=sys.stderr)
        return 2

    if features_dir:
        written = export_features(data, features_dir)
        if not as_json:
            for w in written:
                print(f"wrote {w}", file=sys.stderr)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
