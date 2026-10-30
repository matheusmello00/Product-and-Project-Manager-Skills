# qa-check

Validates the stories of a `backlog-creator` backlog: checks each description against its acceptance criteria (every rule in the description has a criterion), judges every criterion (testable, observable, one behaviour, complete Given / When / Then, no vague words) and every Gherkin scenario (linked to a criterion, concrete, covers the negative, boundary, permission and security-through-the-UI angles the story has), builds the criterion-to-scenario coverage matrix, returns a verdict per story with severity-ranked findings, and **proposes the missing criteria and scenarios**, always marked as proposed.

**When to use:** right after `backlog-creator`, before refinement or sprint planning, or whenever a story keeps bouncing back.
**Not for:** writing the backlog (`backlog-creator`), writing the PRD (`create-prd`), executing tests, estimation. Read-only: it never rewrites the stories.

## How to use
1. Give the backlog written by `backlog-creator` (or stories pasted in the same shape). Add roles or test data if you know them.
2. Receive the report: verdict per story, findings, coverage matrix, missing angles, open questions.
3. Apply the proposals you accept (or ask for `complete` mode to get a merged copy), fix the rest in the backlog, and run `qa-check` again until every story is Ready.

## Requirements
A backlog in the `backlog-creator` format. Nothing else: no tracker, no connector. For its form checks it uses `../backlog-creator/scripts/backlog_check.py` (Python 3.9+) when present; otherwise the manual checklist in `references/validation-criteria.md` §6.

## Output
Verdict table (**Ready** / **Fix before refinement** / **Not testable**), findings by story with severity (Blocker / Major / Minor), exact quoted text, why it matters and a suggested fix, coverage matrix, **proposed criteria**, **proposed scenarios** (Gherkin), open questions for the author.

## Behaviour notes
- Findings quote the exact text and location (story, `AC2`, `TC-03`); suggestions never invent values — they are marked *needs the author's value*.
- It speaks the backlog-creator vocabulary (ST-xx, AC1, TC-xx, FR-xx), so findings can be applied straight to the backlog and re-checked.
- Stories with no criteria are **Not testable**, not a prompt to invent some.
- Security scenarios are judged only for surfaces the story names, UI only; API-level checks are open questions for the developer.
- **Description vs criteria:** a rule stated in the description with no criterion is a finding, and a criterion is proposed for it, in Given / When / Then, from the description's own words.
- **Proposals** (criteria and scenarios) come only from what the story says; a missing value is marked *needs the author's value* and becomes an open question. Everything proposed is marked `proposed`.
- A story with no criteria and no description behaviour is **Not testable** and gets no proposals.
- `complete` mode writes `<project>-qa-checked.md`, a copy of the backlog with the proposals merged in; your file is never edited.
- Writes only the report (`<project>-qa-check.md`) and, on request, the merged copy.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (keys, IDs, names, Given / When / Then and Gherkin keywords) are kept untouched.
