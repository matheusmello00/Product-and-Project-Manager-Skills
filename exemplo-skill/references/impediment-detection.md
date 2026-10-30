# Impediment detection — Blocker Aging reference

Index:
1. Discovering the marking mechanism
2. JQL variants by mechanism
3. Since when it has been blocked
4. Holidays and business days
5. Script JSON schema
6. Data cautions

**This is the fragile part of the skill.** There is no universal mechanism for marking blocks in Jira: each team uses its own. If the JQL does not cover the real mechanism, the query returns zero and an empty report looks like good news — the most dangerous false negative of this plugin. The script emits a warning when it receives zero impediments, but the responsibility for resolving the mechanism lies with whoever builds the query.

## 1. Discovering the marking mechanism

Never assume. Resolve it at runtime, in this order:

1. **Ask the team**, if you are in a conversation with whoever works on the board: "how do you mark an item as blocked?" It is the fastest and most reliable path.
2. **Inspect real issues.** Pull some in-progress issues with all fields (`getJiraIssue`) and look for: a populated `Flagged` field, a status with a blocking name, labels like `blocked`/`bloqueado`/`impediment`, or a custom blocking field.
3. **Check the available statuses** in the workflow (`getTransitionsForJiraIssue` on an issue of the project): if a `Blocked`, `On Hold` or `Impedido` status exists, it is a likely candidate.
4. **Confirm the coverage.** After building the JQL, compare the number of results with the team's expectation. Zero results on an active board is a sign of wrong JQL, not of a team without blocks.

Record the mechanism found in the report notes. In a following session, the mechanism is the first thing to reconfirm.

## 2. Blocking-reason process (if it exists)

If the team uses `Flagged` + a blocking-reason field (multi-select):

- `Flagged` = item blocked, with one or more reasons selected.
- `Flagged` without a reason filled in: flag as inconsistent.
- Reason filled in without `Flagged`: potential deviation; the state must be corrected.
- The reason values are those defined by the team — ask for them, do not assume them.

## 3. JQL variants by mechanism

### Scrum

| Mechanism | JQL |
|---|---|
| `Flagged` field (the most common) | `project = "<KEY>" AND Flagged = Impediment AND statusCategory != Done` |
| Dedicated status | `project = "<KEY>" AND status IN ("Blocked", "On Hold") AND statusCategory != Done` |
| Label | `project = "<KEY>" AND labels IN (blocked, bloqueado, impediment) AND statusCategory != Done` |
| Custom blocking field | `project = "<KEY>" AND "<Field Name>" IS NOT EMPTY AND statusCategory != Done` |
| Combination (recommended when in doubt) | `project = "<KEY>" AND (Flagged = Impediment OR status IN ("Blocked", "On Hold") OR labels IN (blocked, bloqueado)) AND statusCategory != Done` |

### Kanban / Continuous flow

| Mechanism | JQL |
|---|---|
| Blocking column/status | `project = "<KEY>" AND status IN ("Blocked", "Waiting", "On Hold") AND statusCategory != Done` |
| Flow label | `project = "<KEY>" AND labels IN (blocked, waiting, impediment, fluxo) AND statusCategory != Done` |
| Custom flow field | `project = "<KEY>" AND "<Blocking Field Name>" IS NOT EMPTY AND statusCategory != Done` |
| Kanban combination | `project = "<KEY>" AND (status IN ("Blocked", "Waiting", "On Hold") OR labels IN (blocked, waiting, impediment) OR "<Field>" IS NOT EMPTY) AND statusCategory != Done` |

Notes:
- `Flagged` is often `customfield_10021`, but **do not hardcode the ID** — detect it by name/schema, because it varies between instances.
- `statusCategory != Done` avoids dragging in blocks of already-closed items.
- Sort by `updated ASC` so the most stagnant appear first in the response.
- When in doubt about the mechanism, the combined variant is preferable: a false positive is visible and gets corrected; a false negative passes in silence.
- In Kanban, a “waiting” queue / column is also an impediment signal. Using a sprint for the report is not mandatory.

## 4. Since when it has been blocked

Aging depends on the date the issue **became** blocked, which is not the creation date nor necessarily the `updated` date.

- **With changelog** (`expand=changelog` on `getJiraIssue`, if the tool accepts it): walk the history looking for the transition that activated the mechanism — the `Flagged` field becoming `Impediment`, or the status transition to `Blocked`. The date of that change is the `blocked_since`.
- **Without changelog**: approximate using `updated` and mark `approximate: true` in the input. The report then says the aging is approximate.
- **Without a reliable date**: leave `blocked_since` as `null`. The script puts the item in the **Unknown aging** bucket, which appears at the top of the report — it is what nobody escalates.

Future or invalid dates also fall into Unknown aging, by design: a negative aging would be worse than none.

## 5. Holidays and business days

Aging counts **business days** (Monday to Friday), including the day the issue became blocked, and escalation occurs *above* the limit — with the default of 3, it escalates on the 4th business day.

Pass the holidays in `holidays` so aging is not inflated. Without that, a week with a bridge day generates undue escalations. Relevant Portuguese national holidays: 1 January, Carnival (movable, optional), Good Friday and Easter (movable), 25 April, 1 May, Corpus Christi (movable), 10 June, 15 August, 5 October, 1 November, 1, 8 and 25 December. Add municipal holidays (13 June in Lisbon, 24 June in Porto) and MC's internal bridge days. The holidays applied are echoed in the output.

## 6. Script JSON schema

```json
{
  "board": "Board Exemplo",
  "delivery_model": "scrum",
  "threshold_business_days": 3,
  "today": "2026-07-29",
  "holidays": ["2026-04-25", "2026-05-01"],
  "impediments": [
    {
      "key": "ABC-123",
      "title": "Waiting for access approval",
      "assignee": "Ana",
      "delivery_context": "Sprint 42",
      "note": "waiting for the Infra team",
      "blocked_since": "2026-07-20",
      "approximate": false
    }
  ]
}
```

### Kanban example
```json
{
  "board": "Digital Flow",
  "delivery_model": "kanban",
  "threshold_business_days": 3,
  "today": "2026-07-29",
  "holidays": ["2026-04-25", "2026-05-01"],
  "impediments": [
    {
      "key": "KAN-101",
      "title": "Waiting for endpoint access",
      "assignee": "Bruno",
      "delivery_context": "Waiting / Pull blocked",
      "note": "the queue is waiting for access",
      "blocked_since": "2026-07-20",
      "approximate": false
    }
  ]
}
```

Notes:
- `delivery_model` optional: `scrum` by default or `kanban` when the board is continuous.
- `impediments` is **required**. If missing, the script returns an input error (exit 2) instead of an empty report.
- `impediments: []` is accepted as a legitimate result, but generates a warning: zero can be "nothing to report" or "the JQL found nothing", and the script does not distinguish the two.
- `blocked_since` as `null` or invalid → Unknown aging bucket.
- `approximate: true` when the date was inferred without changelog.
- `threshold_business_days` optional (default 3). `today` optional (default: today's date).
- `delivery_context` replaces the use of `sprint` as the sole field in a delivery context; in Kanban the note should refer to `flow` / `WIP` / `pull`.

## 7. Data cautions

- **Mechanism before numbers.** A report with the wrong mechanism is worse than no report.
- **Zero is not good news** until it is confirmed that the query covers the real mechanism.
- **Approximate aging is stated.** Without a changelog, the number is an estimate and the report declares it.
- **Read-only.** The skill does not resolve, reassign or unflag blocks.
- **Blocks that cross teams** belong to the cross-team dependencies conversation, not only to aging.
