# Tracker support — Jira, Azure DevOps, ClickUp

This skill is tracker-agnostic. It builds the backlog in Markdown first, and writes to whichever connector (MCP) is available in the session — **Atlassian (Jira)**, **Azure DevOps** or **ClickUp** — only after the user approves. Wherever the skill says "epic", "story" or "issue", read it as the equivalent in the active tracker, using the mapping below. Nothing changes in the logic or the template.

## Resolve the tracker first

1. Use the connector the user names. If they don't, use the one that is available; if several are, ask which one holds the team's board (one question).
2. Never assume field names or IDs: they vary per instance, project and process template. Inspect one existing epic and one existing story, confirm with the team, and record the mapping in the notes.
3. **Write only after approval.** Create epics first, then stories linked to them; never edit or delete existing items without an explicit request.
4. Check for duplicates before creating (search by title and by the requirement ID in the description).
5. If no tracker connector is available, deliver the Markdown file and say the backlog was not published.

## Common mapping

| Concept | Jira | Azure DevOps | ClickUp |
|---|---|---|---|
| Query language | JQL | WIQL (or the connector's search tools) | Task search / filtered list queries (no JQL) |
| Epic | Issue type Epic | Work item type Epic (or Feature, depending on the process) | A parent task, or a task type "Epic" if the workspace has one |
| Story | Issue type Story | User Story (Agile / CMMI) or Product Backlog Item (Scrum) | Task (child of the epic task) |
| Epic ↔ story link | Parent / epic link (varies by project type) | Parent–Child relation | Subtask or task relationship |
| Board / scope | Board, project | Project + Team + Area Path | Space / Folder / List |
| Item key | `ABC-123` | Numeric work item ID | Task ID (e.g. `86abc123`) or custom ID |

## This skill: Backlog creation — where each part of a story goes.

| Concept | Jira | Azure DevOps | ClickUp |
|---|---|---|---|
| Story statement (As a / I want / So that) | Summary = title; statement at the top of Description — kept even if the project's own template does not require it | Title + statement at the top of Description | Name + statement at the top of Description |
| Acceptance criteria | A dedicated *Acceptance Criteria* field if the project has one; otherwise a section in Description | `Microsoft.VTS.Common.AcceptanceCriteria` | A checklist, or a section in Description |
| Test scenarios (use cases) | A "Test scenarios" section in Description with the Gherkin text by default (or the `.feature` files exported with `--features` attached); linked Test issues only if the team uses X-ray (or similar) and asks for it | A Gherkin section in Description by default; Test Case work items linked with *Tested By* only on request | A Gherkin section in Description or a checklist |
| Priority (Must / Should / Could) | Priority field mapped by the team (e.g. Must → High), or a label `must` / `should` / `could` | `Microsoft.VTS.Common.Priority` or a tag | Priority field or a tag |
| Dependencies | Issue link "is blocked by" | Predecessor / Successor link | *Waiting on* / *Blocking* dependency |
| Requirement traceability (FR-xx) | Label or text in Description (do not overload a custom field) | Tag or text in Description | Tag or text in Description |
| Estimate | Left empty | Left empty | Left empty |

## Team conventions — ask, never assume

Before the first write, ask once for the conventions of the target project and record them in the notes:

- **Parent of the epics** — an Initiative / Feature / Goal the epics must hang from. If the tracker enforces one and it does not exist yet, stop and resolve that first; do not create orphan epics.
- **Mandatory labels or tags** (for example one that marks AI-assisted items), applied to every epic and story created.
- **Initial status** of new items (usually the first "to do" state).
- **Required fields** — discover them from the tracker's field metadata before creating; do not pass unvalidated optional fields (priority, components) as they can be rejected.
- **Language** of the content created in the tracker (default: the language of the sources).
- **Write-back**: offer to record the created keys in the requirement table of the source document, only on approval and only that column, so a later sync can match items to issues.
- **Duplicates**: search for existing epics and stories for the same requirements before creating, and ask whether to extend, replace or skip.

## Honest limits

- A missing capability (no acceptance-criteria field, no link type, no priority field) is reported and the content goes to the description — never invented as a new field.
- The priority mapping (Must / Should / Could → the tracker's priorities) is the team's decision; ask once and record it.
- Connector tool names differ by server; pick the write tools that match the capability you need rather than a fixed tool name.
- Keep requirement IDs, keys, names and field values verbatim in the output.
