# blocker-aging

Active impediments of a team and how many business days they have been stuck, with an identified owner and flagging of what passes the limit — so nothing stays blocked in silence.

**When to use:** in the daily, before a sync, at a status point, or in following a continuous Kanban flow.
**Not for:** cross-team dependencies or sprint metrics from an external report; it is a diagnosis of blocking and delivery risk. Read-only — does not resolve or reassign.

## Requirements
A tracker connector (MCP) with read access: Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`). Python 3.9+.

> **Azure DevOps and ClickUp:** to work well outside Jira, add your tool's own fields to the lookup — work item types and states, estimate field, blocked marker, sprint/iteration and acceptance criteria — or tell the skill their names. Without them the search can miss items or misread their status. Mapping in `references/trackers.md`.

## Blocking process
The blocking-marking mechanism (`Flagged`, status, label or custom field) is resolved at runtime. If the team uses `Flagged` with a reason field, `Flagged` without a reason is reported as a governance inconsistency. The skill measures blocking time and escalates risk; it does not replace process governance.

## Script
```bash
python scripts/aging.py impedimentos.json [--json]
python scripts/aging.py --help
```

## Behaviour notes
- Three buckets, with **"Unknown aging" at the top**: a block with no reliable date is not "under control" — it is the one nobody escalates.
- Business days are Mon–Fri minus the **holidays** passed in the input (avoids undue escalations in bridge-day weeks). The holidays applied are echoed in the output.
- The count **includes the day it became blocked**, and escalation is *above* the limit: with the default 3, it escalates on the 4th business day.
- The blocking-marking mechanism is resolved at runtime and is not limited to one status, label or column. If the item is `Flagged` without a reason (when the team uses that field), it is reported as a governance inconsistency.
- The report supports `delivery_model` to distinguish **Scrum** (sprint impact) from **Kanban** (flow / WIP / pull impact).

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (issue keys, names, field values) are kept untouched.
