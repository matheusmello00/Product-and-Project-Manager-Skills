# Tracker support — Jira, Azure DevOps, ClickUp

This skill is tracker-agnostic. It reads the team's work from whichever connector (MCP) is available in the session — **Atlassian (Jira)**, **Azure DevOps** or **ClickUp** — and normalizes it into the input the skill expects. Wherever the skill says "Jira", "JQL", "issue" or "sprint", read it as the equivalent in the active tracker, using the mapping below. Nothing changes in the logic, the scripts or the report template.

## Resolve the tracker first

1. Use the connector the user names. If they don't, use the one that is available; if several are, ask which one holds the team's board (one question).
2. Never assume field names or IDs: they vary per instance, project and process template. Inspect a few real items, confirm with the team, and record the mapping in the report notes.
3. Read-only by default. Create or change items only on explicit request and approval.
4. If no tracker connector is available, ask the user for an export (CSV/JSON) and normalize it the same way.

## Common mapping

| Concept | Jira | Azure DevOps | ClickUp |
|---|---|---|---|
| Query language | JQL | WIQL (or the connector's search tools) | Task search / filtered list queries (no JQL) |
| Work item | Issue (Story, Task, Bug, Epic…) | Work item (User Story / PBI, Task, Bug, Feature, Epic…) | Task (with optional task types) and subtasks |
| Board / scope | Board, project | Project + Team + Area Path | Space / Folder / List |
| Item key | `ABC-123` | Numeric work item ID | Task ID (e.g. `86abc123`) or custom ID |

## This skill: Blocker aging: how a block is marked and since when.

| Concept | Jira | Azure DevOps | ClickUp |
|---|---|---|---|
| Blocked marker | `Flagged`, a blocked status, a label or a custom field | A `Blocked` field/tag/state — depends on the process template; resolve at runtime | A `Blocked` status, a tag, or a *waiting on / blocked by* task dependency |
| Since when | Changelog (flag/status change date) | Work item revisions (history of the field/state change) | Task activity/history if the connector exposes it; otherwise approximate |
| Owner | Assignee | `System.AssignedTo` | Assignees |
| Open vs done | `statusCategory` | State category (Proposed / InProgress / Resolved / Completed) | Status type (open / custom / done / closed) |

## Honest limits

- A missing capability (no history, no estimate field, no capacity) is reported as unavailable or approximate — never invented.
- Connector tool names differ by server; pick the read tools that match the capability you need rather than a fixed tool name.
- Keep issue keys, IDs, names and field values verbatim in the output.
