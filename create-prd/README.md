# create-prd

Turns a product idea (a sentence, notes, a transcript, feedback, a Confluence or Jira page) into a 1-2 page PRD that forces decisions: specific problem and users, solution with real exclusions, measurable metrics, MVP / V2 / out of scope, risks, open questions, and a requirements table with stable IDs (`FR-01`, `NFR-01`) ready for `backlog-creator`.

**When to use:** a feature or product needs a decision document before refinement, or the backlog needs a clean requirement source.
**Not for:** epics and stories (`backlog-creator`), discovery and interviews (`user-interview-prep`, `feedback-analyzer`), technical specs, estimation.

## How to use
1. Give the idea in any form; add audience, deadline or constraints if you know them.
2. Answer the one batch of questions, if any; it only asks what blocks a decision.
3. Receive `prd-[product-name].md`, then hand it to `backlog-creator`.

## Requirements
Nothing. Optional Atlassian connector (read-only) to pull a Confluence or Jira page. No scripts.

## Behaviour notes
- Vague input gets questions first, not a hollow PRD.
- Gaps become labelled assumptions or open questions with an owner; figures, users and quotes are never invented.
- "What we are NOT building" is mandatory and must hold real exclusions.
- Metrics need baseline (or "unknown"), target and date.
- Requirement IDs are stable once shared.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (IDs, keys, names) are kept untouched.
