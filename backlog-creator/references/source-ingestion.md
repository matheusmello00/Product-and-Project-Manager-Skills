# Source ingestion — Backlog Creation reference

Index:
1. Sources and how to read each
2. Reading a large source in parts
3. What counts as a requirement
4. The requirement inventory
5. Completeness checks
6. Conflicts, duplicates and gaps
7. Data cautions

**This is the fragile part of the skill.** Everything downstream — epics, stories, coverage — is measured against the inventory. `backlog_check.py` can only tell you that a requirement in the inventory has no story; it cannot tell you that a requirement was never extracted. A requirement lost here is lost silently, so this step is slow on purpose and ends with the user confirming the inventory.

## 1. Sources and how to read each

Requirements can come from anywhere, and from several places at once. Resolve each source, read it, and record which source each requirement came from.

| Source | How to read | Watch out for |
|---|---|---|
| Markdown / text / CSV file | `Read` the file; for long files read by line ranges | Truncated reads: check that the end of the file was reached |
| PDF | `Read` with page ranges (a few pages at a time); use the `pdf` skill if the text does not extract cleanly | Scanned pages and tables that extract as noise; say so, do not guess |
| Word (.docx) | Use the `docx` skill to extract text and tables | Tracked changes and comments may hold decisions — read them, report them |
| Excel / CSV requirement tables | Use the `xlsx` skill, or read the CSV; one row is usually one requirement | Several sheets; hidden columns; merged cells |
| Confluence page | Atlassian connector, read the page content; follow child pages only if the user asks | Scope tables inside macros may be incomplete; page version |
| Jira issues | Atlassian connector; a JQL or a list of keys | Existing stories already covering requirements: do not duplicate them |
| Meeting notes / transcripts / pasted text | Read directly | Decisions mixed with discussion: extract only what was decided, put the rest in open questions |
| Figma links | A Figma reader (e.g. the `figma-read` skill), by **node** link | Keep node links; never rely on screenshots pasted into the story |
| Images (diagrams, screenshots) | `Read` the image | State what was read from the image; low confidence is an open question |

Rules:
- If a source cannot be opened, say so and ask for it. Do not work from memory or from its title.
- If several sources overlap, ask which wins when they conflict (default: the most recent approved one) and record the choice in the notes.
- Never fetch content through a channel the session is not allowed to use; if a link is blocked, report it.

## 2. Reading a large source in parts

A large source never has to fit in context at once.

1. **Map first.** Get the structure without reading everything: headings, table of contents, page or sheet count, section sizes. Record it as the reading plan (`section → range → status`).
2. **Read section by section** (or a few pages at a time). After each part, **append to the inventory file** the requirements found there, with their source reference, and mark the part as read. Do not carry the text forward; carry the inventory.
3. **Prefer an order the structure suggests**: requirements sections before narrative, scope tables before background, appendices last. Annexes are read too — they often hold non-functional requirements and rules.
4. **If the source is very large** (hundreds of pages), say how much will be read in this session and which parts are left, rather than quietly reading the first part and stopping. Ask the user to prioritise the parts that matter for the release.
5. **If a read is truncated or fails**, mark that part as **not read** and report it. A part that is not read is not "empty".
6. **Resume from the file.** A later session continues from the reading plan and the inventory, it does not start over.

## 3. What counts as a requirement

Record each of these, tagged by kind:

| Kind | What it is | Becomes |
|---|---|---|
| `functional` | something the product must let a user do or do for a user | stories |
| `use_case` | a described flow with actors, steps, alternatives | stories and test scenarios |
| `non_functional` | performance, security, accessibility, audit, availability | acceptance criteria on the stories they constrain |
| `constraint` | regulatory, legal, technical or budget limit | notes, criteria or open questions |
| `out_of_scope` | explicitly excluded | the Won't list in the notes |
| `open_question` | ambiguous, contradictory or missing | open questions on the story (never guessed) |

Identifiers:
- **Keep the source ID verbatim** (`RF.01`, `UC-012`, `RNF.03`, `FR-01`). The backlog keeps the same IDs so the team can trace back.
- If the source has none, assign them in reading order with a consistent prefix (`FR-`, `UC-`, `NFR-`) and **declare it in the notes**.
- One statement, one requirement. Split compound statements ("the user can register and reset the password") into separate entries, keeping the same source reference.

## 4. The requirement inventory

The inventory is the table at the top of the backlog file (`## Requirements inventory`, see `backlog-schema.md`). For a large source, build it in the file as you read, section by section, so it survives a long session. Each row:

```
| ID | Kind | Requirement | Source |
|---|---|---|---|
| RF.01 | functional | Students publish book listings with title, course and condition | PRD v1.2 §3.1, p.12 |
```

- `Source` is mandatory: file or page plus the section, page, sheet/row or timestamp. `backlog_check.py` warns on a row without it.
- `Requirement` stays close to the source wording. Do not rewrite it into your own interpretation at this stage.

## 5. Completeness checks

Run these before asking the user to confirm the inventory.

- **Coverage of the source**: sections or pages read vs the total; list what was not read and why.
- **Counts per section**: a long section with zero requirements is a signal either that it holds none (background) or that it was skipped — say which.
- **Sampling back**: pick five to ten statements from different parts of the source, at random, and confirm each one is in the inventory. A miss means the extraction in that part is unreliable — re-read it.
- **Cross-check the structure**: if the source lists requirement IDs in a summary table, compare that list with the inventory IDs, ID by ID.
- **Say what cannot be proven**: completeness of an extraction cannot be verified by the script. State the checks done and their limits.

## 6. Conflicts, duplicates and gaps

- **Conflicts** between sources or sections (different limits, different rules): list both versions with their sources, ask which wins, and do not pick silently.
- **Duplicates**: the same requirement stated twice is one entry with two source references.
- **Gaps**: a requirement with no observable outcome, an undefined term, a missing value ("all countries") — keep it, tag it as an `open_question`, and carry it through to the story as an open question. Never fill the gap with a plausible assumption.
- **Dependencies on other teams or systems** are recorded in the notes and raised with the owner.

## 7. Data cautions

- **The inventory is the contract.** Confirm it with the user before slicing; changes after that go through the same confirmation.
- **Not read is not empty.** Report skipped or truncated parts every time.
- **Source wording, not interpretation.** Interpretation belongs to the story, where it is visible and reviewable.
- **Source references travel with the requirement** into the coverage matrix, so a reviewer can open the source and check.
- **Existing work first.** If stories for these requirements already exist in the tracker, report them and ask whether to extend, replace or skip — do not create duplicates.
