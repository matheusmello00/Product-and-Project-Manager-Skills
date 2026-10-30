# Backlog format — what the check reads

The backlog is a single Markdown file in the shape shown in `SKILL.md` ("Output format"). `scripts/backlog_check.py` reads that file directly; there is no JSON to prepare. This page lists the rules the file must follow so every part is read correctly.

```bash
python scripts/backlog_check.py <project>-backlog.md                     # report
python scripts/backlog_check.py <project>-backlog.md --features features # also write one .feature per story
python scripts/backlog_check.py <project>-backlog.md --json              # report as JSON
```

## Structure

| Part | How it is recognised | Notes |
|---|---|---|
| Project and sources | first `# ` heading (`# Backlog — name · date`) and a `Sources:` line | Echoed in the report. |
| Inventory | `## Requirements inventory`, a table with columns `ID`, `Kind`, `Requirement`, `Source` | An empty `Source` → warning. Without the table, requirement coverage is reported as n/a. |
| Epics | `## Epics`, one `### EP-xx — name` per epic | See fields below. |
| Stories | `## Stories`, grouped under `### EP-xx — name`, one `#### ST-xx — title` per story | The epic of a story is the `###` heading it sits under. |
| Everything else | `## Coverage matrix`, `## Backlog summary`, `## Notes` | Not read; they are for people. |

A file with no `## Stories` section is rejected (exit 2): it is not in this format.

## Fields

Fields are lines that start with `**Label:**`. Labels are matched ignoring case and parentheses, so `**Acceptance criteria (epic):**` and `**Acceptance criteria:**` both work.

**Epic**

| Label | Required | Notes |
|---|---|---|
| `Delivers` (or `Description`) | yes | Missing → issue. |
| `Success metric` | yes | Missing → issue. |
| `Acceptance criteria (epic)` | yes | A bullet list of observable outcomes. Empty → issue. |
| `Requirements owned` | recommended | IDs separated by commas. When epics declare them, each requirement must belong to exactly one epic: two → warning; none → warning. |
| `Out of scope` | optional | Not checked. |

**Story**

| Part | Required | Notes |
|---|---|---|
| Statement line right under the heading: `**As a** …, **I want** …, **so that** ….` | yes | The three bold keywords are what the check looks for; a missing one → issue. |
| `Description` | yes | Expected behaviour and business rules. Missing → issue. |
| `Acceptance criteria` | yes | Bullets of the form `- **Given** … **When** … **Then** …`. Fewer than 2 → issue; a missing keyword → issue; a bullet that cannot be read → warning. |
| `Test scenarios (Gherkin)` | yes | A fenced ` ```gherkin ` block. No scenarios → issue. See below. |
| `Priority` | yes | First word must be `Must`, `Should` or `Could` (a reason may follow). Anything else → issue. |
| `Requirements` | recommended | IDs separated by commas; drives traceability. |
| `Dependencies` | optional | Story IDs, or `None`. Unknown, self or circular → issue. |
| `Open questions` | optional | `None`, a bullet list, or items separated by `;`. Any → warning (story not spec-ready). |
| `Design`, `Estimate` | optional | Not checked. Leave the estimate empty. |

## Gherkin scenarios

```gherkin
@TC-01 @happy @AC1
Scenario: Publish with all mandatory fields
  Given I am signed in
  And I open the new listing form
  When I submit a listing with title, course and condition
  Then the listing appears in search results within 1 minute

@TC-02 @boundary @AC2
Scenario Outline: Title length limits
  Given I am signed in
  When I submit a listing with a title of <length> characters
  Then the listing is <result>
  Examples:
    | length | result                         |
    | 120    | published                      |
    | 121    | rejected with 'Title too long' |
```

- **Tags** on the line before `Scenario`: `@TC-xx` is the scenario ID (unique across the backlog); the type is one of `@happy`, `@alternative`, `@negative`, `@boundary`, `@permission`; `@AC1`, `@AC2` … name the acceptance criteria the scenario covers (`AC1` is the first criterion of the story).
- **Checks**: no title, no `When` or no `Then` → issue; no `Given` → warning; unknown type → issue; `@ACn` pointing to a criterion that does not exist → issue; a criterion no scenario covers → warning; a story with only `@happy` scenarios → warning; vague wording in `Then` → warning; a `<placeholder>` with no `Examples` table or no matching column → issue.
- Keywords stay `Given / When / Then / And / But`; the text after them follows the output language.

## Other checks

Duplicate IDs · story with no epic or an unknown epic · requirements not covered by any story · story not traced to any requirement · epic with no stories, one story, or more than five · more than five criteria in a story · more than 60% of stories as Must (backlog of five or more) · zero stories.

Findings never change the exit code: `0` means the file was read; `2` means a usage error or a file that is not in this format.

## Exporting the scenarios

`--features DIR` writes one `.feature` file per story: the As a / I want / So that statement, description and criteria as comments, each scenario as `Scenario` or `Scenario Outline`, tagged with its ID, type and criteria. The exporter formats what is in the file; run the check first.
