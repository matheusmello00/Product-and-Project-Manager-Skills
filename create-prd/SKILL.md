---
name: create-prd
description: 'Turns a product idea, feature description, workshop notes, feedback or a Confluence/Jira page into a concise PRD of 1-2 pages that forces decisions: specific problem and users, solution with real exclusions, measurable success metrics, MVP / V2 / out-of-scope, risks and open questions, plus a short requirements table with stable IDs (FR-xx / NFR-xx) that backlog-creator can consume directly. When the input is too vague it lists the blocking questions before writing; it never invents numbers, users or facts. Does not create epics or stories (backlog-creator), does not run discovery or interviews, does not write technical specs, and does not estimate.'
when_to_use: 'When a product idea or feature needs to become a decision document before refinement: starting a new product or feature, aligning stakeholders on scope, or preparing the input for the backlog. Serves Product Manager, Product Owner, Business Analyst and Agile Coach.'
maturity: em-validacao
allowed-tools:
- Read
- Write
- mcp__atlassian
compatibility: 'No dependencies for pasted text or local files. Confluence or Jira context is read through the Atlassian connector when available, read-only. The output is a Markdown file; no scripts.'
argument-hint: '[product idea | feature description | path | link] [optional: audience, deadline]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Product Manager, Product Owner, Business Analyst, Agile Coach'
tags:
- product
- prd
- requirements
- scope
- metrics
---

# Create PRD

A sharp, actionable Product Requirements Document that fits in 1-2 pages. It is short on purpose: every section forces a decision, and the requirement IDs let `backlog-creator` turn it into epics and stories without re-reading prose.

## Requires

Nothing beyond the idea. Optional context (notes, feedback analysis, interview findings, a Confluence or Jira page) makes the PRD more specific; it is read, never changed.

## What you need before starting

- **The idea or feature**, in any form: a sentence, notes, a transcript, a link or a file.
- Optional: audience of the PRD, deadline, known constraints, existing metrics.

## Flow

1. **Read all the context given.** Done when you can state the problem, the user and the intended outcome in one sentence each. If you cannot, go to step 2.
2. **Close the gaps.** List what the PRD needs and the input does not say (see `references/prd-writing.md` §1). Ask **one batch** of questions only about what blocks a decision (who, what problem, what success means). For everything else, assume the most reasonable option and record it under *Assumptions*. If the input is too vague to write anything defensible, return the questions and stop; do not write a hollow PRD.
3. **Write the PRD** with the template below, in this order: problem → users → solution and exclusions → metrics → scope → requirements → risks. Done when no section contains a word from the vague list in `references/prd-writing.md` §4.
4. **Number the requirements.** Each MVP capability gets a one-line requirement with an ID (`FR-01…`, `NFR-01…`), the user type it serves and its priority (Must / Should / Could) — see `references/prd-writing.md` §3.
5. **Check before delivering** against the checklist in `references/prd-writing.md` §5 (specific, measurable, exclusions real, every requirement traceable to the solution, length). Fix, do not just report.
6. **Save** as `prd-[product-name].md` and tell the user the open questions that still need an owner.
7. **Hand off.** Say the file is ready for `backlog-creator`: it imports the Requirements table as its inventory, so nothing needs to be re-typed. See the contract in `references/prd-writing.md` §6.

## Template

```
# PRD — [product / feature]  ·  [date]  ·  v0.1 draft

## Problem
- Who: [specific segment, not "users"]
- How they solve it today: ...
- Why that hurts: [concrete cost: time, money, errors; with number or source]

## Target users
- Primary: [role, company size, technical level, frequency of use]
- Trigger: [what makes them need this now]

## Solution
- We are building: [concrete and specific]
- We are NOT building: [real exclusions, at least two]
- Key flows: 1. ... 2. ...

## Success metrics
| Metric | Type | Baseline | Target | By when |
|---|---|---|---|---|
| [one number] | Primary | [value or "unknown"] | ... | ... |

## Scope
- MVP: [smallest thing that delivers value]
- V2: [next, if MVP succeeds]
- Out of scope: [will come up, explicitly deferred]

## Requirements
| ID | Requirement | User | Priority | Source |
|---|---|---|---|---|
| FR-01 | ... | ... | Must | [section / person / doc] |
| NFR-01 | ... | ... | Should | ... |

## Risks and open questions
- Technical: ...
- Product (will users want this?): ...
- Dependencies: ...
- Open questions: [question — owner — needed by]

## Assumptions
- [each assumption made in step 2, marked as such]
```

## Rules

- **Max 2 pages**; a third only for the requirements table. If it is longer, decisions are missing.
- **No fluff.** Every sentence adds information or makes a decision. "Improve user experience" is not specific.
- **"We are NOT building" is mandatory** and holds real exclusions, not "anything else".
- **Metrics are numbers with a target and a date.** "Improve retention" is not a metric. If the baseline is unknown, write "unknown" and add the question; never invent it.
- **Never invent** users, figures, quotes, competitors or constraints. What the input does not give becomes an assumption or an open question, labelled.
- **Concrete over abstract**: use examples and named segments.
- **Requirement IDs are stable** once shared; new ones are appended, retired ones are marked, never renumbered.
- **Vague input**: questions first, PRD second.
- Keep source references verbatim (page names, ticket keys, people).
- Does not create epics, stories or estimates; hand the saved file to `backlog-creator`.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (IDs, keys, names) untouched.

## References

| Read this | Before… |
|---|---|
| `references/prd-writing.md` §1 | deciding what to ask and what to assume |
| `references/prd-writing.md` §2 | writing problem, users, metrics and scope |
| `references/prd-writing.md` §3 | numbering requirements for `backlog-creator` |
| `references/prd-writing.md` §4–5 | the final check |
| `references/prd-writing.md` §6 | saving the file so `backlog-creator` can import it |
