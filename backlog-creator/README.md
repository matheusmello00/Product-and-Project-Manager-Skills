# backlog-creator

Give it the context — a PRD, a very large document, a Confluence page, a spreadsheet, Jira issues, meeting notes or pasted text — and it returns one Markdown backlog: **epics** (description, acceptance criteria, scope) and **stories** (As a / I want / So that, description, Given / When / Then criteria, priority, dependencies) with **test scenarios in Gherkin** for every story, all traced to the requirements they came from.

**When to use:** requirements exist and the team needs epics and stories with criteria and test scenarios before refinement or sprint planning; an existing backlog must be restructured to INVEST.
**Not for:** writing the PRD (`create-prd`), validating criteria and use cases in depth (`qa-check`), technical specs (`spec-writer`), detailed QA test cases (`qa-scenarios`) or estimation.

## How to use
Upstream: `create-prd` writes `prd-<name>.md`; give that file here and its requirement IDs, users, priorities, exclusions and open questions are imported as they are.

1. Paste the context, point to a file, or share a link. Add user types, release scope or target tracker if you know them.
2. Answer the one batch of questions, if any — only what blocks the work.
3. Receive `<project>-backlog.md`. Ask for the tracker publication or the `.feature` export if you want them.

Nothing to prepare and nothing to run yourself: the skill runs its own check.

## Requirements
A source of requirements: pasted text, a file (Markdown, text, CSV, PDF, Word, Excel) or a Confluence/Jira link (Atlassian connector); Figma links need a Figma reader. How each is read is in `references/source-ingestion.md`. To publish: a tracker connector (MCP) with write access — Atlassian (Jira), Azure DevOps or ClickUp (mapping in `references/trackers.md`). The quality check needs Python 3.9+ and nothing else; without it the skill uses a manual checklist.

> **Azure DevOps and ClickUp:** to publish well outside Jira, tell the skill the names of your work item types, the acceptance-criteria field, the priority field and how epics link to stories.

## The output
- **Inventory** of requirements with their source (so nothing is lost in a large document).
- **Epics:** description, success metric, the requirements it owns, acceptance criteria, out of scope.
- **Stories:** `As a … I want … so that …`, description, Given / When / Then criteria, Gherkin scenarios tagged `@TC-01 @happy @AC1`, priority (Must / Should / Could), requirements, dependencies, open questions, empty estimate.
- **Coverage matrix** (requirement → epic → story → scenarios), summary and notes.

## Script (optional, run by the skill)
```bash
python scripts/backlog_check.py backlog.md                       # report: issues first, then warnings
python scripts/backlog_check.py backlog.md --features features   # also write one .feature file per story
python scripts/backlog_check.py --help
```
One script, no dependencies. It reads the Markdown directly (format in `references/backlog-schema.md`).

## Behaviour notes
- **Two paths.** Normal context: one pass, no confirmation gates. Large or multi-source context: read in parts, confirm the inventory (with what was not read, conflicts and open questions), then the epic map, then slice.
- **Each requirement belongs to exactly one epic**; stories are sliced by outcome (target 3–5 per epic).
- **Criteria and values are never invented.** Where the source is silent, the skill asks (offering candidates) or records an open question on the story.
- **Scenarios exercise the criteria.** Every criterion is covered by at least one scenario; every story has at least one non-happy case; `Scenario Outline` + `Examples` for limits and data variations.
- **The check** reports issues (must fix: missing parts, fewer than two criteria, stories without scenarios, broken dependencies) and warnings (uncovered requirements, vague wording, oversized stories, priority inflation). Findings never change the exit code; exit 2 means the file is not in the expected format.
- **Zero stories is not "done".**
- The estimate is left empty on purpose: sizing belongs to the team.
- The tracker is written **only after approval**, epics first and then their stories linked to them.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. The story statement is always As a / I want / So that and the criteria and scenarios use Given / When / Then. Verbatim items (requirement IDs, issue keys, names, field values) are kept untouched.

## Credits
Story decomposition approach adapted from `bmad-method:bmad-create-epics-and-stories` (MIT, © 2025 BMad Code, LLC). User-story and INVEST concepts: Agile Alliance, https://www.agilealliance.org/glossary/user-story
