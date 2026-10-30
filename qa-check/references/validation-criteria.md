# Validation criteria — QA Check reference

Index: 1. Description and acceptance criteria · 2. Test scenarios · 3. Severity and verdict · 4. Reading the backlog · 5. Proposing what is missing · 6. Manual checklist

The script and the checklist check form. **Judgement is the value here**: a criterion can be well-formed and still untestable, and a scenario can be valid Gherkin and still test nothing. Read each one as the tester who must accept or reject the story.

## 1. Description and acceptance criteria

For each criterion ask, in this order:

| Check | Fails when | Typical severity |
|---|---|---|
| Complete | Given, When or Then is missing, or the criterion is a bare sentence | Major (Blocker if no outcome at all) |
| Testable | a tester cannot accept or reject it without asking ("works correctly", "user-friendly", "secure") | Blocker |
| Observable | the Then is internal state, not what the user sees or receives | Major |
| Measurable | a quality is claimed without a number, limit or message ("fast", "large", "quickly") | Major |
| One behaviour | When or Then hides several actions or outcomes joined by "and" | Major |
| Specific | values are left open ("valid data", "all countries") with no source | Major (and an open question) |
| Consistent | it contradicts another criterion, the description, or another source | Blocker |
| Not implementation | it names tables, endpoints, components, selectors | Minor |
| Not duplicated | it repeats another criterion in other words | Minor |

**Description against criteria.** The description is where the business rules live; the criteria must carry them.

1. List every behaviour, rule, limit and value the description (and the statement) states: "only the owner can remove a listing", "title is mandatory, 120 characters maximum".
2. Match each to a criterion. A rule with **no criterion** is a **Major** finding, quoted from the description, and gets a proposed criterion (§5).
3. The reverse: a criterion that states behaviour the description does not mention is a **Minor** finding when harmless, **Major** when it adds scope or contradicts the description.
4. A value the description gives (a limit, a role) must appear verbatim in the criterion that covers it; a different value is a **Blocker** (contradiction).
5. If the story lists requirements, check that each requirement's behaviour is also covered by a criterion.

Story-level checks: at least two criteria; the main path **and** at least one negative, boundary or permission case; the statement (As a / I want / So that) has all three parts and the *so that* states value; no criterion adds scope the story and description do not mention; non-functional requirements the source names are attached somewhere.

Vague words to challenge: works, correctly, properly, fast, quickly, easy, intuitive, user-friendly, appropriate, valid (without a rule), "etc.", "as expected", "should" without a measurable Then.

**What the source does not say.** Do not fill the gap. Report the criterion, state the most likely reading, and list the missing value as an open question.

## 2. Test scenarios

| Check | Fails when | Typical severity |
|---|---|---|
| Linked | it covers no criterion, or covers one that does not exist | Major |
| Covered | a criterion has no scenario | Major |
| Valid Gherkin | no Given, no When or no Then; a placeholder `<x>` without an Examples column; a Scenario Outline without Examples | Major |
| One behaviour | two Whens, or several unrelated Thens | Minor |
| Observable Then | the Then is "works", "correctly", or internal state | Major |
| Concrete | limits, roles, messages are replaced by "some", "valid", "invalid" where the story gives the value | Minor |
| Declarative | it names buttons, locators, URLs patterns or payloads | Minor |
| Self-contained | it depends on another scenario running first or on a shared Background | Minor |
| Typed | type is not one of happy, alternative, negative, boundary, permission | Minor |
| Not duplicated | two scenarios exercise the same thing | Minor |

Coverage rules to enforce: every criterion exercised by at least one scenario; every story has at least one non-happy scenario; scenario IDs unique across the set; a scenario that needs behaviour no criterion states is a finding on the **criterion** (missing criterion), not an excuse for hidden scope.

**Angles to look for** — a missing one is a finding only when the story actually has the surface:

- roles or owned records → permission
- free text or numbers → negative and boundary
- states (reserved, expired, empty) → alternative
- lists → filter, sort, empty state, pagination actually filters the results
- dates → formats, defaults, recalculation
- forms → each required field checked individually, cancel and keep-editing branches
- login, tenant or personal data, file or free-text input → security abuse cases (`security-abuse-cases.md`)

## 3. Severity and verdict

- **Blocker** — the story cannot be tested or accepted as written: no criteria, an untestable or contradictory criterion, no outcome.
- **Major** — the story can be tested but important behaviour is wrong or missing: incomplete criterion, unmeasurable quality, uncovered criterion, missing negative/permission case, scenario with no linked criterion.
- **Minor** — wording and hygiene: implementation detail, duplicates, non-concrete data, style.

Verdict per story: **Not testable** if any Blocker; **Fix before refinement** if no Blocker and at least one Major; **Ready** otherwise (Minors listed, not blocking). Never call a set ready because it passed a script; the verdict comes from the findings.

Be proportionate: do not pad the report with Minors to look thorough. Lead with Blockers, then Majors.

## 4. Reading the backlog

- **Input**: the `<project>-backlog.md` written by `backlog-creator`. Stories are under `#### ST-xx`; criteria are `- **Given** … **When** … **Then** …` bullets, numbered AC1…; scenarios are Gherkin blocks tagged `@TC-01 @happy @AC1`; each story lists its requirements and open questions. Format rules: `../backlog-creator/references/backlog-schema.md`.
- **Requirements**: the backlog's inventory and coverage matrix tell which requirement each story serves; use them to check that a criterion does not add scope and that no requirement lost its criteria.
- **Pasted stories**: accepted if they follow the same shape (statement, criteria, scenarios). If a story has no recognisable criteria or scenarios section, list it as missing them rather than guessing; if the boundary between stories is unclear, ask once.
- **Not the right format**: if the file is not a backlog (the script exits 2, or there is no `## Stories` section), say so and point to `backlog-creator`; never report from a rejected input.
- **Large sets**: check in parts of about 10–15 stories, write findings to the report as you go, and say which stories were not checked.
- **Closing the loop**: findings use the story and criterion IDs, so the author can apply the fixes in the backlog file and re-run `qa-check` until every story is Ready.

## 5. Proposing what is missing

Proposals are part of every report; they are suggestions, never changes to the backlog.

**Proposed criteria** — for each description rule with no criterion, and for a story whose criteria lack the main path or a negative, boundary or permission case the description implies:

- Write it as **Given / When / Then**, one behaviour, observable, using the description's own words and values.
- Continue the story's AC numbering and mark it `(proposed)`; cite the description sentence it came from.
- Where the description gives no value (a limit, a message, a role), write the outcome without it, mark `needs the author's value` and add an open question. Never fill a number or a message in.
- If the description states no behaviour at all (title only), propose nothing: the story is Not testable and goes back to the author.

**Proposed scenarios** — for each criterion with no scenario (existing or proposed) and each missing angle (§2):

- Gherkin in the story's own format, one behaviour, concrete values only from the story, tagged `@TC-xx @type @ACn @proposed`, with new unique IDs continuing the existing ones.
- Where a value is missing, describe the outcome and add an open question.
- Keep it proportionate: typically one to three per story; do not pad.

**Merged copy** (only when the user asks for `complete` mode): write `<project>-qa-checked.md` beside the backlog with the proposals inserted in their stories, each tagged proposed, and re-run the form check on it. The original file is never touched. The author removes the `proposed` marks after reviewing, or rejects the proposals by deleting them.

## 6. Manual checklist (when the script is unavailable)

1. Every story has the three-part statement and a description; every rule in the description has a criterion.
2. Every story has at least two criteria, each with Given, When and Then.
3. Every criterion is covered by a scenario; every scenario names the criteria it covers.
4. Every story has at least one non-happy scenario.
5. Every Scenario Outline placeholder has an Examples column.
6. Scenario and story IDs are unique; dependencies point to existing stories.
7. No criterion or Then contains a word from the vague list in §1.
