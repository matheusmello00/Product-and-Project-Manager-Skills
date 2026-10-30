---
name: qa-check
description: 'Validates the acceptance criteria and test scenarios of the stories in a backlog-creator Markdown file (or stories pasted in the same format): checks each story description against its criteria (every behaviour or rule the description states has a criterion), judges every criterion (testable, observable, one behaviour, complete Given / When / Then, no vague words, no implementation detail, no contradictions) and every Gherkin scenario (covers a criterion, concrete data, the negative, boundary, permission and security-through-the-UI angles the story has), builds the criterion-to-scenario coverage matrix, returns a verdict per story with severity-ranked findings, and proposes the missing criteria and scenarios, always marked as proposed. Proposals come only from what the story says, with open questions for any missing value. It never edits the backlog, writes the backlog (backlog-creator), judges the PRD, executes tests or invents behaviour.'
when_to_use: 'When stories have acceptance criteria and test scenarios and someone must confirm they are good enough: before refinement or sprint planning, after backlog-creator, or when a story keeps bouncing back from development. Serves QA, Product Owner, Product Manager, Business Analyst and Scrum Master.'
maturity: em-validacao
allowed-tools:
- Read
- Write
- Bash
compatibility: 'No dependencies. Input is a backlog-creator Markdown file or stories pasted in the same format. When the backlog-creator script backlog_check.py is present it is used for the form checks; otherwise the manual checklist applies. The output is a Markdown report; no tracker or connector is needed.'
argument-hint: '[path to backlog.md | pasted stories] [optional: roles, test data]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'QA, Product Owner, Product Manager, Business Analyst, Scrum Master'
tags:
- qa
- acceptance-criteria
- test-scenarios
- gherkin
- validation
- stories
---

# QA Check / Acceptance criteria and test scenarios

**You give the backlog. You get a verdict and the missing pieces.** For each story: does every behaviour in the description have an acceptance criterion, are the criteria testable, and do the test scenarios exercise them? The output is a report a team can take to refinement: findings with severity, the exact text that is wrong, why it matters and a suggested fix, plus **proposed** criteria and scenarios for what is missing.

Where it sits: `create-prd` → `backlog-creator` → **`qa-check`** → development. It reads the backlog `backlog-creator` produces, judges it, and hands the report back so the backlog can be fixed (apply the proposals, or re-run `backlog-creator` on the same file). It does not create the backlog or run the tests.

## Requires

A `backlog-creator` backlog (Markdown), or stories pasted in the same shape. Nothing else: no tracker, no connector. See `references/validation-criteria.md` §4.

## What you need before starting

- **The stories**: the `<project>-backlog.md` written by `backlog-creator` (best) or stories pasted in that shape. Any size; large sets are checked in parts.
- Optional: roles/personas to cover, test data constraints, whether you want the merged copy (`complete` mode).

## Flow

1. **Read the stories** from the backlog file (format in `../backlog-creator/references/backlog-schema.md`): statement, description, criteria `AC1…`, scenarios `@TC-01 @type @ACn`, requirements and open questions. Done when every story has its description, criteria and scenarios identified, or is listed as missing them.
2. **Run the form check.** `python ../backlog-creator/scripts/backlog_check.py <file>` if present; otherwise the manual checklist in `references/validation-criteria.md` §6. Reproduce its warnings in the report.
3. **Check the description against the criteria.** List every behaviour, business rule, limit and value the description (and statement) states, and match each to a criterion. A description rule with no criterion is a finding; a criterion that adds scope the description does not mention is a finding. See `references/validation-criteria.md` §1.
4. **Judge each acceptance criterion** against §1: testable, observable, one behaviour, complete Given / When / Then, no vague words, no implementation detail, no contradiction. Quote the exact text of every defect.
5. **Judge each test scenario** against §2: covers at least one criterion, valid Gherkin, one behaviour, concrete data, observable Then, self-contained. Build the **coverage matrix** (criterion → scenarios) and list every criterion with no scenario and every scenario with no criterion.
6. **Look for missing angles** the story actually has: negative, boundary, permission, state, and the security scenarios its surface calls for (`references/security-abuse-cases.md`, UI only).
7. **Propose what is missing**, in the report, never in the backlog: criteria for description rules with no criterion, and scenarios for uncovered criteria and missing angles. Rules in `references/validation-criteria.md` §5. Done when every Major gap of "no criterion" or "no scenario" has a proposal or an open question.
8. **Rank and decide.** Severity and verdict rules are in §3. One verdict per story: **Ready**, **Fix before refinement** or **Not testable**.
9. **Deliver the report** (template below) and save it as `<project>-qa-check.md` beside the backlog. Open questions for the author go in their own section. Only if the user asks (`complete` mode), also write `<project>-qa-checked.md`: a copy of the backlog with the proposals merged in, each tagged proposed. The original is never modified.

## Template

```
# QA Check — [scope]  ·  [date]
Source: [backlog file] · Stories checked: N

## Verdict
| Story | Criteria | Scenarios | Blockers | Majors | Minors | Verdict |
|---|---|---|---|---|---|---|
| ST-01 | 3 | 4 | 0 | 1 | 2 | Fix before refinement |

## Findings
### ST-01 — [title]
| # | Where | Severity | Problem (quoted) | Why it matters | Suggested fix |
|---|---|---|---|---|---|
| F1 | AC2 | Major | "the page loads fast" | not measurable | "... within 2 seconds" — needs the author's value |
| F2 | Description | Major | "only the owner can remove a listing" | no criterion states it | see proposed AC3 |

## Coverage matrix
| Story | Criterion | Scenarios | Gap |
|---|---|---|---|
| ST-01 | AC1 | TC-01 | — |
| ST-01 | AC2 | — | no scenario |

## Proposed criteria (not in the backlog)
### ST-01
- **AC3 (proposed)** — **Given** [...] **When** [...] **Then** [...]   · from: description, "only the owner can remove a listing" · needs the author's value: [...]

## Proposed scenarios (not in the backlog)
### ST-01
```gherkin
@TC-09 @permission @AC3 @proposed
Scenario: Another student cannot remove my listing
  Given [...]
  When [...]
  Then [...]
```

## Open questions for the author
- [question] — [story / criterion]

## Notes
- [form-check warnings reproduced; stories not checked; assumptions]
```

## Rules

- **The backlog is never modified.** The fix is a suggestion the author applies. Files written: the report and, only on request, the merged copy `<project>-qa-checked.md`.
- **Quote, don't paraphrase.** Every finding cites the exact text and its location (story, description, `AC2`, `TC-03`).
- **Never invent.** Proposals come only from what the story says: its description, statement, criteria and requirements. A value, number, message or role the story does not give is marked *needs the author's value* and added to the open questions.
- **Proposed is always marked proposed**, in the report and in the merged copy (`(proposed)` on criteria, `@proposed` on scenarios), with the source text it came from.
- **No criteria and no description behaviour** (title only): the story is **Not testable**, with no proposals; point to `backlog-creator`.
- **A story with a description but no criteria** is still **Not testable** until the author accepts criteria; the proposals are drafts.
- **Ambiguity is a finding with a most-likely reading**, not a reason to skip the criterion. State the reading you used.
- **Behaviour, not implementation**: flag selectors, endpoints, component names and table names as Minor.
- **Security through the UI only**, and only for surfaces the story names; anything needing an API client or tokens is an open question for the developer.
- **Propagate warnings, never swallow errors.** If `backlog_check.py` returns warnings, reproduce them; if it exits 2 the input is not in the expected format: fix the reading or fall back to the manual checklist, never report from a rejected input.
- Proposed scenarios use new unique TC IDs continuing the existing ones; proposed criteria continue the AC numbering.
- Keep keys, IDs, names and field values verbatim.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (keys, IDs, names, field values, Given / When / Then and Gherkin keywords) untouched.

## References

| Read this | Before… |
|---|---|
| `references/validation-criteria.md` §1–2 | judging description, criteria and scenarios |
| `references/validation-criteria.md` §3 | setting severity and the verdict |
| `references/validation-criteria.md` §4 | reading the backlog file and handling large sets |
| `references/validation-criteria.md` §5 | proposing criteria and scenarios, and the merged copy |
| `references/validation-criteria.md` §6 | the manual checklist when the script is unavailable |
| `references/security-abuse-cases.md` | judging or proposing security scenarios a UI tester can run |
