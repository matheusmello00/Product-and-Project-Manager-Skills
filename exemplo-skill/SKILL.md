---
name: blocker-aging
description: 'Maps the active impediments of a team and how long each has been stuck, so nothing stays blocked in silence: pulls flagged, blocked or waiting/on-hold issues from Jira, computes aging in business days (configurable holidays), identifies the owner, and separates over-the-limit items from those of unknown age. Runs in the daily, before a sync, at a status point, or in continuous Kanban flow follow-up. Does not manage cross-team dependencies and does not depend on a sprint-specific skill; it uses the board context and Jira data directly, and is read-only: it never resolves or reassigns.'
when_to_use: 'When you need to see what is blocked and for how many days, decide what to escalate, prepare the impediments part of the daily, follow the Kanban flow, or assess delivery risk from blockers. Serves Scrum Master, PMO, Agile Coach and continuous-flow teams.'
maturity: ready
allowed-tools:
- Bash
- Read
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Requires a tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp; Confluence only for the version to be published, optional. Scripts in standard-library Python 3, with no external dependencies.'
argument-hint: '[board] [days-limit]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Scrum Master, PMO, Agile Coach, Kanban Leads and continuous-flow teams'
tags:
- agile
- scrum
- kanban
- jira
- azure-devops
- clickup
- impediments
---

# Blocker Aging / Flow Blockers

Makes visible what is blocked and, above all, **for how long**. A 1-day impediment is normal; a 6-day one is a delivery risk nobody has escalated. It gives the list ordered by age and flags what has already gone past what is acceptable — and what has **unknown** age, which is what most easily slips through. For Kanban, the same diagnosis takes on the language of flow: impact on WIP, work queue and continuous waiting time.

## Requires

A tracker connector (MCP): Atlassian (Jira), Azure DevOps or ClickUp — see `references/trackers.md`. Read-only by default — it only reads and reports.

## What you need before starting

- **Board / project / team** to analyse.
- **Aging limit** (default: 3 business days). Escalation occurs **above** the limit (with the default 3, on the 4th business day), counting the day it became blocked.
- **Holidays** (optional): list of dates not to count as business days (national holidays/bridge days), so aging is not inflated.

## Blocking process

The blocking-marking mechanism varies by team and is resolved at runtime (see `references/impediment-detection.md` §1–2). If the team uses `Flagged` with a blocking-reason field, these validation rules apply:

- A `Flagged` item must have reason(s) filled in; without a reason, record it as inconsistent / pending governance.
- A reason filled in without `Flagged` is a potential deviation and must be flagged.
- The card's real status stays unchanged: the item does not change workflow just because it is blocked.
- The accepted reason values are those defined by the team; do not assume a fixed list.

## Flow

1. **Resolve the marking mechanism and pull the active impediments.** If the JQL does not cover the team's real mechanism (e.g. `Flagged` + reason field), it may silently return zero. See `references/impediment-detection.md` §1–2 to confirm the team's real mechanism and for the JQL variants, in both Scrum and Kanban.

2. **Determine since when each issue has been blocked** — see `references/impediment-detection.md` §3. Without a changelog, approximate and mark `approximate`; without a reliable date, the item falls into the "Unknown aging" bucket. When the item is `Flagged` but has no reasons filled in, record it as inconsistent and treat this condition as a pending-governance signal.
3. **Collect** owner (assignee), type, delivery context (sprint / flow), column/status in Kanban, and a short note on the block.
4. **Normalise** and run:
   ```bash
   python scripts/aging.py impedimentos.json
   ```
   The script counts business days (minus holidays), flags those past the limit, and separates those of unknown aging.
5. **Build the report** with the template below.

## Template

```
# Impediments — [board]  ·  [today's date]

## Unknown aging — verify
- [KEY] [title] — no reliable date · owner: [assignee]

## To escalate (above [N] business days, counting the day it became blocked)
- [KEY] [title] — [days]d stuck · owner: [assignee] · impact: [sprint/flow] · [block note]

## Active (within the limit)
- [KEY] [title] — [days]d · owner: [assignee]

## Notes
- [holidays applied; aging approximated for lack of changelog; delivery context: sprint/flow; impact on WIP or pull]
```

## Rules

- **Aging is the value.** Sort by age; highlight what has passed the limit. The **"Unknown aging"** bucket goes at the top — a block of unknown age is not "under control"; it is the item nobody escalates.
- **Only state what you know** — without a changelog, aging is approximate and that is said.
- **Read-only** — does not resolve or reassign without a request.
- **Validate the blocking process** — if the team uses a blocking-reason field, `Flagged` must come with it; if it is empty, flag it as an inconsistency.
- **Propagate the warnings and do not swallow errors.** If the script returns a `WARNINGS` block, reproduce those warnings in the report you deliver — the warning serves the reader, not the script. If the script ends with **exit 2**, the input does not match the schema: fix the normalisation and run again, never report a result from a rejected input.
- **Business days, minus holidays** — to avoid triggering undue escalations in holiday weeks.
- **Supports the Scrum and Kanban delivery models**: in Scrum the impact is attributed to the sprint; in Kanban the impact is attributed to the flow, column, WIP or pull.
- Issue keys and names verbatim.
- If an impediment involves another team, link it to the cross-team dependencies conversation.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (issue keys, names, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/impediment-detection.md` §1–2 | finding out how the team marks blocks and building the JQL |
| `references/impediment-detection.md` §3 | determining since when each issue has been stuck |
| `references/impediment-detection.md` §4 | applying holidays and interpreting the escalation limit |
| `references/impediment-detection.md` §5 | normalising the JSON before running `aging.py` |
| `references/trackers.md` | pulling data from Azure DevOps or ClickUp instead of Jira (query and field mapping) |
