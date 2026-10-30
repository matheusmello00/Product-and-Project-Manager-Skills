---
name: backlog-creator
description: 'Give it the context — a PRD, a very large document, a Confluence page, a spreadsheet, Jira issues, meeting notes or just pasted text — and it returns one Markdown backlog: Epics (description, acceptance criteria, scope), User Stories in the As a / I want / So that format (description, Given/When/Then acceptance criteria, MoSCoW priority, dependencies) and, for every story, test scenarios written in Gherkin (happy path, alternative, negative, boundary, permission), all traced back to the requirements they came from. Large sources are read in parts and checked for completeness; a built-in check catches missing criteria, uncovered requirements and broken dependencies before delivery. Does not write the PRD, does not estimate, does not write detailed QA test cases, never invents criteria, and does not push to a tracker without explicit approval.'
when_to_use: 'When requirements exist — in a PRD, one-pager, large specification, Confluence page, workshop notes or a change request — and the team needs epics and stories with criteria and test scenarios before refinement or sprint planning; when an existing backlog must be restructured to INVEST; or when a retro found missing or vague acceptance criteria. Serves Product Manager, Product Owner, Business Analyst and Scrum Master.'
maturity: draft
allowed-tools:
- Bash
- Read
- Write
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'Reads requirements from pasted text, files (Markdown, text, CSV, PDF, Word, Excel), and Confluence/Jira through the Atlassian connector; Figma links only through a Figma reader. Needs nothing else: the output is a Markdown file. The optional quality check is one standard-library Python 3 script, run by the skill itself; a tracker connector (MCP) is needed only to publish.'
argument-hint: '[context: text | path | link]'
metadata:
  author: Matheus Mello
  version: '0.3.0'
audience: 'Product Manager, Product Owner, Business Analyst, Scrum Master'
tags:
- product
- backlog
- epics
- user-stories
- acceptance-criteria
- gherkin
- test-scenarios
- requirements
- invest
- moscow
- jira
---

# Backlog Creation / Epics, Stories, Criteria and Test Scenarios

**You give the context. You get the backlog.** One Markdown file with, for each epic, its description and acceptance criteria, and for each story its **As a / I want / So that**, description, **Given / When / Then** criteria and **Gherkin** test scenarios — every item traced to the requirement it came from. There is nothing to prepare and nothing to run yourself: the skill reads the context, does the work, checks it, and hands back the file.

## Quick start

- Paste the context, point to a file, or share a link. Any size, any mix of sources. A PRD written by `create-prd` (`prd-*.md`) is imported as it is: its requirements table becomes the inventory.
- Add what you know: user types, release scope, target tracker. Nothing else is required.
- The skill asks **at most one batch of questions**, only for what blocks the work, and lists the rest as open questions in the file.
- You get `<project>-backlog.md`. Publishing to Jira (or another tracker) and exporting the scenarios as `.feature` files happen only if you ask.

## Two paths

- **Normal context** (pasted text, a few pages, one document): the skill does everything in one pass and shows the inventory of requirements inside the file. No confirmation gates.
- **Large or multi-source context** (hundreds of pages, several documents, conflicting sources): the skill reads in parts, builds the requirement inventory first and **asks you to confirm it** — with what was not read, conflicts and open questions — before writing epics, and confirms the epic map before slicing. See `references/source-ingestion.md`.

## Flow

1. **Read the context.** If a source is a `create-prd` PRD, import it instead of re-extracting it (`references/source-ingestion.md` §7). Every source, in parts if it is large; keep the requirements in the file as you go, not in memory. Say what could not be read. See `references/source-ingestion.md` §1–2.
2. **Build the requirement inventory** — every requirement, use case, non-functional requirement and constraint, with its source ID verbatim (or an assigned one) and where it came from. Large sources: confirm it with the user. See `references/source-ingestion.md` §3–6.
3. **Group requirements into epics by user value**, not by layer or team. Each requirement belongs to **exactly one** epic. Each epic gets a description, a success metric, its own acceptance criteria and what is out of scope. See `references/story-writing.md` §2.
4. **Slice each epic into stories by outcome** — 3–5 vertical slices, each in the mandatory **As a / I want / So that** statement plus a short **Description** (expected behaviour and business rules, no technical detail). See `references/story-writing.md` §3–4.
5. **Write the acceptance criteria** in **Given / When / Then**: at least two per story, covering the main path and a negative or boundary case, observable and never invented — where the source is silent, ask (offering two or three candidates) or record an open question. See `references/story-writing.md` §5.
6. **Write the test scenarios in Gherkin**, derived from the criteria: every criterion is exercised by at least one scenario and every story has at least one non-happy case. See `references/story-writing.md` §6.
7. **Set priority and dependencies** — Must / Should / Could with a reason for each Must; dependencies by story ID, only real blockers. See `references/story-writing.md` §7–8.
8. **Check it.** Save the Markdown and run `python scripts/backlog_check.py <file>`; fix every issue and weigh every warning. If Python is not available, go through the manual checklist below instead. See `references/backlog-schema.md`.
9. **Deliver the file** with a short summary: epics, stories, scenarios, coverage, open questions. Offer the tracker publication and the `.feature` export — do not do either unprompted. Publishing follows `references/trackers.md`, **only after explicit approval**.

## Output format

Write the backlog exactly in this shape — the check reads it directly. Full rules in `references/backlog-schema.md`.

````
# Backlog — [project]  ·  [date]
Sources: [paths / links] · Version: [x.y] · Author: [name]

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| RF.01 | functional | [statement, close to the source wording] | [document §section, page] |

## Epics

### EP-01 — [name]
**Delivers:** [description: what it delivers and to whom]
**Success metric:** [how completion is measured]
**Requirements owned:** [RF.01, RF.02]
**Acceptance criteria (epic):**
- [observable outcome that defines "done" for the epic]
**Out of scope:** [what does not belong here]

## Stories

### EP-01 — [name]

#### ST-01 — [title]
**As a** [user type], **I want** [capability], **so that** [outcome].

**Description:** [expected behaviour from the user/business point of view: main flow and business rules; no technical detail]

**Acceptance criteria:**
- **Given** [precondition] **When** [action] **Then** [observable outcome]
- **Given** [precondition] **When** [action] **Then** [observable outcome]

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: [title]
  Given [precondition]
  And [another precondition, if needed]
  When [action]
  Then [observable outcome]

@TC-02 @boundary @AC2
Scenario Outline: [title]
  Given [precondition]
  When [action with <value>]
  Then [outcome with <result>]
  Examples:
    | value | result |
    | …     | …      |
```

**Priority:** [Must / Should / Could] — [reason if Must]
**Requirements:** [RF.01]
**Design:** [Figma node links, if any]
**Dependencies:** [ST-xx or None]
**Open questions:** [list separated by ";" or None]
**Estimate:** [left empty — to be filled by the team]

## Coverage matrix
| Requirement | Source | Epic | Stories | Scenarios |
|---|---|---|---|---|
| RF.01 | [section / page] | EP-01 | ST-01 | TC-01, TC-02 |

## Backlog summary
Epics: [N] · Stories: [N] · Scenarios: [N] · Must / Should / Could: [N / N / N] · Requirement coverage: [N%] · Open questions: [N]

## Notes
- [IDs assigned by the skill; parts not read; conflicts between sources; Won't (out of scope); assumptions; check results reproduced]
````

## Manual checklist (when Python is not available)

Every requirement owned by exactly one epic and covered by at least one story · every epic has description, metric and acceptance criteria · every story has As a, I want, So that, a description and at least two Given/When/Then criteria · every criterion is covered by a scenario and every story has a non-happy scenario · every Scenario Outline placeholder has an Examples column · every priority is Must, Should or Could · dependencies point to existing stories and have no cycles · open questions are listed, not hidden.

## Rules

- **The Markdown file is the backlog.** One deliverable, in the format above. No JSON or intermediate files for the user to handle.
- **Inventory before slicing.** Say plainly what was not read or not understood; never present an inventory as complete when parts of a source were skipped or truncated. For large or multi-source contexts, the user confirms the inventory before epics are written.
- **Traceability is the value.** Every requirement is owned by exactly one epic, covered by at least one story, and carries its source reference; an uncovered requirement is reported, never silently dropped.
- **Story statement: always As a / I want / So that**, all three parts, whatever the output language and even if the tracker template does not require it. The **so that** states the value, not a restatement of the action. Each story also has a short **Description**.
- **Acceptance criteria always Given / When / Then**, at least two per story, observable. No "works correctly" or "fast"; use the concrete values (which countries, which message, which limit).
- **Never invent a criterion or a value.** Where the source gives none, ask once with two or three candidates, or record an open question on the story so it is visibly not spec-ready. No open question ships silently.
- **Test scenarios are Gherkin**: one behaviour each, Given = state, When = one action, Then = observable result, `Scenario Outline` + `Examples` for limits and data variations, tagged `@TC-01 @happy @AC1` (ID, type, criterion covered). They exercise the criteria; they add no scope — a needed behaviour with no criterion gets a criterion or an open question. They are a first pass; detailed test data and regression belong to `qa-scenarios`.
- **Vertical slices, by outcome.** A story is something a user can do, not "build the API". Several requirements serving one outcome are one story. An epic with one story is probably a story; more than about five usually hides two epics.
- **Do not estimate.** Leave the estimate empty.
- **Design by link**, never screenshots: keep Figma node links on the story.
- **Do not swallow the check.** Fix every issue it reports; reproduce unresolved warnings in the Notes. If it exits with an error, the file is not in the expected format — fix the file and run again, never report from a rejected input.
- **An empty backlog is not done.** If no requirements were found, say so and ask for the source.
- **Publish only on request and approval.** Before the first write ask once for the project's conventions (parent of the epics, mandatory labels, initial status, required fields), discover required fields from the tracker, avoid duplicates, and never edit or delete existing items.
- Requirement IDs, ticket keys, names and field values verbatim.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (requirement IDs, issue keys, names, field values) untouched. The story statement is always **As a / I want / So that**; criteria and scenarios always use the Gherkin keywords Given / When / Then (And), with the text after them in the output language. Content created in a tracker follows the language of the sources.

## References

| Read this | Before… |
|---|---|
| `references/source-ingestion.md` §1–6 | reading the context — any type, any size — and building or confirming the inventory |
| `references/source-ingestion.md` §7 | the input is a `prd-*.md` produced by `create-prd` (import its requirements table, scope, exclusions and open questions) |
| `references/story-writing.md` | grouping epics, slicing stories, writing criteria and Gherkin scenarios, setting priority and dependencies |
| `references/backlog-schema.md` | saving the file in the format the check reads, and running the check or the `.feature` export |
| `references/trackers.md` | publishing to Jira, Azure DevOps or ClickUp (hierarchy, fields, conventions) |
