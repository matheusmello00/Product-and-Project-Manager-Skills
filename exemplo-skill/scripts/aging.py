#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Aging of active impediments, in business days, with a bucket for those of unknown age.

Interface:
    python scripts/aging.py impedimentos.json          # human-readable summary (stdout)
    python scripts/aging.py impedimentos.json --json    # JSON only (stdout)
    python scripts/aging.py --help

Buckets: Unknown aging (missing/invalid/future date), To escalate (above the limit),
Active (within the limit). Business days are Mon-Fri minus the holidays passed in the input, and the
count includes the day it became blocked. Exit codes: 0 = OK; 2 = usage error or invalid input.
"""

import json
import sys
from datetime import date, datetime, timedelta


def parse_date(value):
    if not value:
        return None
    if isinstance(value, (date, datetime)):
        return value.date() if isinstance(value, datetime) else value
    s = str(value).strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def business_days(start, end, holidays):
    """Business days from start to end (inclusive), excluding weekends and holidays."""
    if not start or not end or end < start:
        return None
    days = 0
    d = start
    while d <= end:
        if d.weekday() < 5 and d not in holidays:
            days += 1
        d += timedelta(days=1)
    return days


def require_schema(data, known, main_key, ctx):
    """Two-layer input guard.

    1. If no recognised key is present, the payload does not match
       the schema -> ValueError (exit 2). Catches the case where the layer that
       normalises the Jira data produces an object with the wrong keys.
    2. If the main collection is missing, it is likewise a schema error.
       If it is present and empty, it is a legitimate result, but returns a warning:
       zero results may mean "nothing to report" or "the query found
       nothing", and the script cannot tell the two apart.
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


def analyse(data):
    warnings = require_schema(
        data, {"board", "delivery_model", "threshold_business_days", "today", "holidays", "impediments"},
        "impediments", "blocker-aging")
    delivery_model = str(data.get("delivery_model") or "scrum").lower()
    if delivery_model not in {"scrum", "kanban"}:
        delivery_model = "scrum"
        warnings.append("Unknown delivery model; assumed `scrum` for compatibility.")

    today = parse_date(data.get("today")) or date.today()
    threshold = data.get("threshold_business_days", 3)
    holidays = set(filter(None, (parse_date(h) for h in (data.get("holidays") or []))))
    items = data.get("impediments", []) or []
    if not items:
        # The most dangerous false negative of this skill: an empty list looks like good
        # news. The marking mechanism varies by team (Flagged field,
        # Blocked status, label), and a JQL that does not cover it returns zero.
        warnings.append(
            "Zero impediments in the input. DO NOT report as a good sign without confirming that the query covers the "
            "team's real marking mechanism (Flagged field, Blocked status or label). "
            "See references/impediment-detection.md."
        )

    rows = []
    for it in items:
        since = parse_date(it.get("blocked_since"))
        age = business_days(since, today, holidays) if since else None
        rows.append({
            "key": it.get("key"), "title": it.get("title"), "assignee": it.get("assignee"),
            "delivery_context": it.get("delivery_context") or it.get("sprint") or "n/a",
            "note": it.get("note"),
            "blocked_since": since.isoformat() if since else None,
            "age_business_days": age,
            "approximate": bool(it.get("approximate")),
            "age_known": age is not None,
            "delivery_model": delivery_model,
        })

    unknown = [r for r in rows if not r["age_known"]]
    known = [r for r in rows if r["age_known"]]
    known.sort(key=lambda r: -(r["age_business_days"] or 0))
    to_escalate = [r for r in known if r["age_business_days"] > threshold]
    within = [r for r in known if r["age_business_days"] <= threshold]

    return {
        "board": data.get("board"), "today": today.isoformat(),
        "delivery_model": delivery_model,
        "threshold_business_days": threshold,
        "holidays_applied": sorted(h.isoformat() for h in holidays),
        "summary": {"total": len(rows), "to_escalate": len(to_escalate), "unknown_age": len(unknown)},
        "unknown_age": unknown, "to_escalate": to_escalate, "within_limit": within, "all": rows,
        "warnings": warnings,
    }


def _line(r):
    age = f"{r['age_business_days']}d" if r["age_known"] else "?d"
    approx = " (approx.)" if r["approximate"] else ""
    who = r["assignee"] or "no owner"
    ctx = r.get("delivery_context") or "n/a"
    note = f" · {r['note']}" if r.get("note") else ""
    return f"- {r['key']} {r['title'] or ''} — {age}{approx} stuck · owner: {who} · context: {ctx}{note}".rstrip()


def render(res):
    lines = []
    lines.append(f"IMPEDIMENTS — {res.get('board') or '(board)'}  ·  {res['today']}")
    s = res["summary"]
    lines.append(f"Total: {s['total']}  ·  To escalate (> {res['threshold_business_days']} business d): {s['to_escalate']}  ·  Unknown aging: {s['unknown_age']}  ·  Model: {res.get('delivery_model') or 'scrum'}")
    if res["holidays_applied"]:
        lines.append(f"(holidays applied: {', '.join(res['holidays_applied'])})")
    lines.append("")

    if res.get("warnings"):
        lines.append("WARNINGS — read before reporting")
        for w in res["warnings"]:
            lines.append(f"  !! {w}")
        lines.append("")

    lines.append("UNKNOWN AGING — verify")
    for r in res["unknown_age"]:
        lines.append(_line(r))
    if not res["unknown_age"]:
        lines.append("- (none)")
    lines.append("")

    lines.append(f"TO ESCALATE (> {res['threshold_business_days']} business days)")
    for r in res["to_escalate"]:
        lines.append(_line(r))
    if not res["to_escalate"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("ACTIVE (within the limit)")
    for r in res["within_limit"]:
        lines.append(_line(r))
    if not res["within_limit"]:
        lines.append("- (none)")
    return "\n".join(lines)


USAGE = """aging.py — aging of active impediments.

Usage:
    python scripts/aging.py impedimentos.json [--json]

Arguments:
    impedimentos.json   impediments, limit in business days and optional holidays

Options:
    --json       write only the JSON to stdout
    -h, --help   show this help

Exit codes:
    0  success
    2  usage error or invalid input
"""


def main(argv):
    args = argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE.strip())
        return 0
    as_json = "--json" in args
    unknown = [a for a in args if a.startswith("-") and a != "--json"]
    if unknown:
        print(f"Error: unknown option: {unknown[0]}", file=sys.stderr)
        print("Expected: --json or --help. Run with --help for the interface.", file=sys.stderr)
        return 2
    positional = [a for a in args if not a.startswith("-")]
    if len(positional) != 1:
        print(f"Error: expected 1 input file, received {len(positional)}.", file=sys.stderr)
        print("Try: python scripts/aging.py impedimentos.json   (--help for the interface)", file=sys.stderr)
        return 2

    path = positional[0]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path} (line {exc.lineno}, column {exc.colno}): {exc.msg}", file=sys.stderr)
        print("Expected: a JSON object matching the schema in the skill reference.", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print(f"Error: the input must be a JSON object, received {type(data).__name__}.", file=sys.stderr)
        return 2

    try:
        result = analyse(data)
    except ValueError as exc:
        print(f"Error: invalid input. {exc}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
