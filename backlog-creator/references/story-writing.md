# Story writing — Backlog Creation reference

Index:
1. Starting from the inventory
2. Grouping requirements into epics
3. Slicing an epic into stories
4. INVEST test
5. Acceptance criteria
6. Test scenarios (use cases)
7. Priority (MoSCoW)
8. Dependencies
9. Data cautions

**This is the fragile part of the skill.** The script checks form; it cannot tell a good slice from a bad one. A backlog can pass every check and still be a technical task list in story clothing. The judgement in §2–5 is where the quality is made.

Canonical reference for the user-story format and INVEST: https://www.agilealliance.org/glossary/user-story

## 1. Starting from the inventory

Slicing starts from the **confirmed requirement inventory** built in `source-ingestion.md`, never from a fresh read of the source. The inventory already holds every requirement, use case, non-functional requirement and constraint, with its ID and source reference.

- Work from the inventory IDs verbatim. If the source had none, the prefix (`FR-`, `UC-`, `NFR-`) was assigned at ingestion and declared in the notes.
- Take the **user types** the sources name, and the constraints (regulatory, performance, integrations). Constraints become acceptance criteria or notes, not stories of their own, unless they deliver something a user notices.
- Anything ambiguous, contradictory or untestable ("the system should be intuitive") is already an **open question** in the inventory. Do not decompose what is not understood; ask once, in a batch.
- If there is no confirmed inventory, or it is empty, stop and go back to ingestion. An empty backlog is not a result.

## 2. Grouping requirements into epics

- An epic is a **coherent outcome for a user type**, e.g. "Students publish and manage listings". It is not a layer ("Backend"), a team ("Platform") or a phase ("Sprint 1").
- Each epic has a name, a description (what it delivers and to whom), a **success metric** — how the team will know the epic delivered value — its own **acceptance criteria** (observable outcomes that define "done" for the epic, aligned with the requirements it owns) and an **out of scope** note. If the sources have the metric, use it; if not, propose one and mark it as proposed.
- Cluster requirements by the user journey or functional domain they serve. **Each requirement is owned by exactly one epic**: if it touches several, record it under the epic that owns its main value and mention the others in the notes. A requirement parked in the wrong domain is moved, not duplicated.
- If the requirements inside an epic do not add up to its acceptance criteria, fix the epic boundary before slicing.
- Epics should be independently deliverable, with no or only light dependencies on other epics, and sized so one owner can hold it in their head.
- Sanity checks: one story only → probably a story (or work at epic level and keep the story for tracking); more than about five stories → probably two epics or stories not grouped by outcome; every requirement is assigned to some epic, and none to two.
- **Validate coverage explicitly**: all epics together deliver 100% of the confirmed inventory. Surface any unassigned requirement, overlap, or epic whose criteria do not match its requirements.
- Present the draft epic map (epic → requirements owned → epic criteria) with the coverage check and **get confirmation before slicing**.

## 3. Slicing an epic into stories

A story is a **vertical slice**: it crosses UI, logic and data and delivers something a user can observe. "Create the table" is a task.

**Think outcome, not requirement count.** Ask "what should the user be able to do after this story?", not "which requirements are left?". Several requirements or use cases that serve the same user-facing outcome belong in one story (scanning an item: valid code, invalid code, manual entry — one story). Separate them where there is a real boundary (different actor, different risk, hardware or an external system involved). Target **3–5 stories per epic**; two is fine for a simple epic. The hard constraint is not the number but that each story is a tangible, shippable slice.

Splitting patterns, in the order worth trying:

| Pattern | Example |
|---|---|
| Workflow steps | request a swap → accept → complete → rate |
| Operations | create / edit / remove a listing |
| Business rules | free listing → paid highlight |
| Data or input variations | by course, by campus |
| Interface or channel | web first, mobile later |
| Happy path first, then variations and errors | pay by card → pay by voucher |
| Simple first, then complex | one book per swap → bundles |

Stories are written in the **mandatory** statement "As a `<user type>`, I want `<capability>`, so that `<outcome>`", always in this form whatever the output language. All three parts are required, even if the target tracker's template only asks for a description and criteria — the statement then goes at the top of the Description.

- **As a** — a user type named in the sources, not a generic "user" and not a system.
- **I want** — a capability the user can observe. Avoid solution words (API, table, screen, endpoint).
- **So that** — the value or outcome, not a restatement of the action. If you cannot state the value, the story is probably a task (merge it into the story that makes it visible).

Each story also carries a short **Description**: the expected behaviour from the user and business point of view — the main flow and the business rules — in a few sentences. No technical detail (endpoints, tables, components): that belongs to the spec. The description gives context; the acceptance criteria are what gets tested.

## 4. INVEST test

| Letter | Fails when… | Fix |
|---|---|---|
| Independent | it cannot be delivered without another story in the same sprint | re-slice, or record a real dependency (§7) |
| Negotiable | it dictates the implementation | move the how to the spec |
| Valuable | a user or the business would not notice it | merge into the story that makes it visible |
| Estimable | the team could not size it | clarify, or split off a spike |
| Small | it has more than about five criteria or cannot fit in a sprint | split (§3) |
| Testable | a criterion cannot be accepted or rejected | rewrite the criterion (§5) |

Split or merge **before** writing criteria.

## 5. Acceptance criteria

- **Given** a precondition, **When** one action, **Then** an observable outcome. One behaviour per criterion. The keywords stay Given / When / Then in every output language; the text after them follows the output language.
- **At least two** per story: the main path and at least one negative, boundary or permission case. A story with only a happy path is not tested.
- **Observable and measurable.** Not "it works correctly", "fast", "user-friendly". Say what the user sees ("the form shows 'Title is required' and nothing is published"), with a number where it matters ("appears in search results within 1 minute").
- No implementation detail (table names, endpoints). That belongs to the spec.
- Non-functional requirements from the PRD (performance, accessibility, audit) are attached as criteria to the story they constrain.
- Criteria are independently verifiable: a tester should not need to ask anything to accept or reject.
- Depth of validation (completeness, ambiguity, use-case coverage) belongs to `qa-check`; here the goal is a defensible first version.

**What the source does not say.** Criteria come from the sources, not from imagination.

- Take the observable outcomes from the source's own use cases, flows, rules and Given/When/Then, keeping concrete values verbatim (which countries, which message, which limit).
- Where the source gives no observable outcome or leaves a value open, **stop and ask** the user, offering two or three candidate criteria to choose from or rewrite. A blank the user fills beats a plausible criterion that was invented.
- If it cannot be resolved now, keep the story and record the gap as an **open question** on it. The story is then visibly not spec-ready; it is never shipped as if complete.
- A criterion that contradicts another source (document vs design vs conversation) is the same case: list both versions, ask which wins.

## 6. Test scenarios (use cases)

A scenario is one concrete way a user (or the system) goes through the story, from a starting point to an observable result, written in **Gherkin**. Criteria state the rule; a scenario exercises it with concrete values. This is a **first pass** that lets the team and QA see the shape of the testing before development — full test cases, test data and automation belong to `qa-scenarios`.

Derive scenarios **from the acceptance criteria**, then look for the gaps. Types:

| Type | What it exercises | Example |
|---|---|---|
| `happy` | the main path, valid data, allowed user | publish a listing with all mandatory fields |
| `alternative` | a valid but different route or option | publish without a photo, when the photo is optional |
| `negative` | invalid input or a rejected action | submit without a title → "Title is required" |
| `boundary` | limits of a rule: min, max, just over, empty, duplicate | title with exactly 120 characters, and with 121 |
| `permission` | who may and may not do it | another student tries to edit my listing → permission error |

### Gherkin format

```gherkin
@TC-01 @happy @AC1
Scenario: Publish with all mandatory fields
  Given I am signed in
  And I open the new listing form
  When I submit a listing with title, course and condition
  Then the listing appears in search results within 1 minute

@TC-07 @boundary @AC2
Scenario Outline: Title length limits
  Given I am signed in
  When I submit a listing with a title of <length> characters
  Then the listing is <result>
  Examples:
    | length | result                         |
    | 120    | published                      |
    | 121    | rejected with 'Title too long' |
```

- **Given** is the state (setup), **When** is **one** action, **Then** is an observable result. `And` / `But` continue the previous step. The first step of each kind takes the keyword; the following ones use `And`.
- **One behaviour per scenario.** Two Whens usually mean two scenarios.
- **Declarative, not procedural**: say what the user does and sees ("I submit a listing without a title"), not which button or locator. No UI selectors, no implementation detail.
- **Use `Scenario Outline` with `Examples`** for limits and data variations; every `<placeholder>` needs an `Examples` column. Keep the table short and meaningful — boundaries and one representative per class, not every value.
- **Tag each scenario** with its ID, type and the criteria it covers: `@TC-01 @happy @AC1`. `AC1` means the first acceptance criterion of the story.
- **Self-contained**: no shared `Background` and no dependence on another scenario having run first.
- **Concrete values** where they matter (limits, messages, roles). Where the source does not give the value, it is an open question, not an invented number.
- The text after the keywords follows the output language; the keywords stay Given / When / Then / And.

### Coverage rules

- **Every criterion is exercised by at least one scenario**, and each scenario lists the criteria it covers. The script warns on a criterion with no scenario.
- **At least one non-happy scenario per story.** A story tested only on the happy path is not tested.
- **Attach the angles the story actually has**: roles and owned records → permission; free text or numbers → boundary and negative; states (reserved, expired) → alternative; third-party calls → failure/timeout as negative.
- **No new scope.** If a scenario needs behaviour no criterion states, add the criterion (or an open question); do not leave tested behaviour unwritten.
- Keep it short: typically 2–5 scenarios per story. More suggests the story is too big (§4).
- Scenario IDs (`TC-01…`) are unique across the backlog.
- `python scripts/backlog_check.py <file> --features features` turns the scenarios into `.feature` files, one per story, for QA or automation tools.

## 7. Priority (MoSCoW)

- **Must** — the release is not viable without it. Every Must needs a **rationale** traceable to the PRD (goal, regulation, dependency of the core flow).
- **Should** — high value, include if possible.
- **Could** — nice to have, drop first if capacity falls.
- **Won't (this release)** — not a story priority in the backlog: list it in the notes so the exclusion is explicit.
- Be suspicious of a backlog where more than about 60% is Must: that is not prioritisation. The script warns above that ratio.

## 8. Dependencies

- Record a dependency by story ID only when story B **cannot be started or accepted** without story A. Preference, convenience and "same area" are not dependencies.
- Prefer re-slicing to chains. A long chain of dependencies is a sign of horizontal slicing.
- No cycles; the script reports them.
- A dependency on another team or an external system is recorded in the notes and raised with the owner — it is not hidden as a story ID.

## 9. Data cautions

- **Form before substance.** Passing the script means the backlog is well-formed, not that it is right.
- **Requirements before stories.** A story that traces to no requirement is either scope creep or a missing requirement; ask which.
- **Source before invention.** User types, rules, values and criteria come from the sources; what is missing becomes an open question, not an assumption.
- **Design by link.** Keep Figma node links on the story; never replace them with screenshots.
- **Proposed is marked proposed.** Epic metrics, user types or rules not in the PRD are labelled as proposed, never presented as fact.
- **Estimates stay empty.** Do not size stories on the team's behalf.
- **Scenario count is not quality.** Ten happy-path variations do not replace one permission and one boundary case.
