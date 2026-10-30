# PRD writing — Create PRD reference

Index: 1. Gaps and questions · 2. Section craft · 3. Requirements and IDs · 4. Vague words · 5. Final checklist · 6. Contract with backlog-creator

## 1. Gaps and questions

A PRD needs at least: the segment, the problem and its cost, how it is solved today, the intended outcome, one primary metric, and what is out. Compare the input against that list.

- **Blocking** (ask): no identifiable user, no problem (only a solution), no notion of success. Ask them in one batch, at most five questions, each with two or three candidate answers to pick from.
- **Non-blocking** (assume): technical approach, V2 content, secondary metrics, naming. Assume, label in *Assumptions*.
- If the user answers none of the questions, write the PRD with explicit assumptions and mark the PRD `draft`.

## 2. Section craft

- **Problem**: segment + situation + cost. "Ops teams at mid-market SaaS with 50+ integrations lose about a day a week reconciling errors" beats "users struggle with integrations". Put the source of any figure next to it.
- **Target users**: one primary persona. A second one needs its own reason. Trigger = the event that makes them look for a solution.
- **Solution**: say what the user can do afterwards, not how it is built. Flows are numbered and sequential, from trigger to outcome.
- **Exclusions**: pick things stakeholders will plausibly ask for. "No mobile app in MVP" is real; "no unrelated features" is not.
- **Metrics**: one primary (leading or lagging, say which), two or three secondary at most, plus a guardrail if the change can hurt something. Each has baseline, target, date and the data source. Unknown baseline = "unknown" + open question.
- **Scope**: MVP is the smallest thing that tests the main assumption, not the smallest thing that is demo-able. V2 is conditional on the MVP metric.
- **Risks**: product risk first (will they use it?), then technical and dependency risks. Each open question has an owner and a date.

## 3. Requirements and IDs

- One line per capability, in the user's terms: "Student can publish a book with a title and course". No solution words (API, table, screen).
- Prefix `FR-` functional, `NFR-` non-functional (performance, security, accessibility, compliance), `UC-` only if the context already uses use cases. Number in reading order, two digits.
- Each carries: user type, priority (Must / Should / Could), source (where in the input it came from, or "assumed").
- A requirement without a solution element or a flow is scope creep; a solution element without a requirement is a gap. Fix both.
- Keep the table to the MVP; V2 items stay as one line in Scope, without IDs, until they are promoted.
- This table is what `backlog-creator` reads as its requirement inventory; keep it parsable (one row per requirement, no merged cells).

## 4. Vague words to remove

improve, better, easy, intuitive, seamless, robust, fast, scalable, modern, user-friendly, "etc.", "and more", "as needed", "appropriate". Replace each with a behaviour, a number or a deletion.

## 5. Final checklist

1. Problem names a specific segment and a cost.
2. One primary persona and a trigger.
3. At least two real exclusions.
4. Every metric has baseline (or "unknown"), target and date.
5. MVP, V2 and out of scope are distinct; nothing appears in two.
6. Every FR/NFR has user, priority and source; every MVP flow step maps to a requirement.
7. No invented figures; assumptions and open questions are listed with owners.
8. No word from §4.
9. Length within two pages (third page only for the requirements table).

## 6. Contract with backlog-creator

`backlog-creator` reads this file as its requirement source. Keep the contract, or the import falls back to reading prose:

- File name `prd-<product-name>.md`, Markdown, one PRD per file.
- Section headings exactly: `## Problem`, `## Target users`, `## Solution`, `## Success metrics`, `## Scope`, `## Requirements`, `## Risks and open questions`, `## Assumptions`.
- `## Requirements` is one table with columns exactly `ID | Requirement | User | Priority | Source`; IDs `FR-xx` / `NFR-xx`; priority `Must` / `Should` / `Could`; one row per requirement.
- `We are NOT building`, `MVP`, `V2` and `Out of scope` keep those labels, because the backlog uses them as epic exclusions and as what is in or out.
- Open questions are one per line as `question — owner — needed by`.
- Never renumber IDs after the file has been handed over; append new ones.
