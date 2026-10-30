---
name: user-interview-prep
description: 'Turns a research topic or hypothesis into a ready-to-use interview kit: a single testable research goal, 3-5 hypotheses with falsifiers, a 30-minute interview guide with open-ended, non-leading questions (Mom Test), follow-up prompts, behavioural signals to watch, interviewer anti-patterns, a recruiting screener note and a consent/recording note. Optionally uses existing context (feedback, personas, prior research, analytics) to sharpen the hypotheses. Fits on two printable pages. Does not run the interviews, synthesise findings or validate a solution; it prepares the PM to learn about the problem, not to confirm an idea.'
when_to_use: 'When you are about to talk to users and need a research brief and interview guide: discovery for a new feature, understanding a drop in a metric, exploring a segment, or preparing follow-up interviews after feedback analysis. Serves Product Managers, Product Owners, UX researchers and Agile Coaches.'
maturity: ready
allowed-tools:
- Read
- Write
compatibility: 'No connector or script required. Optional: Read access to local files (feedback exports, personas, prior research notes) passed as context.'
argument-hint: '[research topic or hypothesis] [optional: context file]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Product Manager, Product Owner, UX Researcher, Agile Coach'
tags:
- product
- discovery
- user-research
- interviews
- mom-test
---

# User Interview Prep

Go into interviews with a clear research goal, hypotheses that can be proven wrong, and questions that make people talk about their real past behaviour. The aim is to **learn, not to confirm**. Output is one brief a PM can print and bring to the room.

## Requires

Nothing beyond the conversation. Optional context files (feedback exports, personas, earlier research, analytics notes) are read when provided.

## What you need before starting

- **Research topic or hypothesis** (required). Vague is fine; the skill sharpens it.
- **Who you will interview** (segment, role, recent behaviour). If missing, assume the most likely segment and state it in one line.
- **Optional context:** existing feedback, personas, previous research, metrics. Used only to sharpen hypotheses and probe areas; never quoted as fact without a source.
- **Interview length** (default 30 minutes) and whether it is remote or in person.

If something essential is missing, ask **one** question; otherwise state the assumption and proceed.

## Flow

1. **Read the input and any context.** Note what is already known versus what is assumed.
2. **Write the research goal**: one testable question starting with "Understand…" or "Discover…". Never "Validate…" or "Confirm…". If the input is a solution ("do users want X?"), reframe it as the problem behind it. See `references/interview-craft.md` §1.
3. **Surface 3–5 hypotheses** the PM is likely carrying. For each, define what would show it is true **and** what would show it is false. Call out weak or untestable ones and propose a better one (§2).
4. **Design the 30-minute flow**: warm-up (5), core exploration (20), wrap-up (5), each with a purpose (§3).
5. **Write the questions**: open-ended, about the past and real behaviour, maximum 12 in total, with at least 2 follow-up prompts per core question (§4–5). Run every question through the checks in `references/interview-craft.md` §4.
6. **Add observation notes, anti-patterns, the screener note and the consent note** (§6–8).
7. **Check the output**: question count ≤ 12, no forbidden openers, no questions about the PM's solution, fits two pages.
8. **Save** as `interview-brief-[topic].md` in the working directory and deliver (template in `references/research-brief-template.md`).

## Template

```
# Interview brief — [topic]  ·  [date]

## Research goal
[One sentence: Understand… / Discover…]

## Who to talk to (screener note)
[Segment · must-have recent behaviour · exclusions · suggested n]

## Hypotheses to test
| # | Hypothesis | True if we hear… | False if we hear… |

## Interview guide ([N] min)
**Warm-up (5 min)** — [purpose]
**Core exploration (20 min)** — [purpose]
  Q3 … ↳ follow-ups: …
**Wrap-up (5 min)** — [purpose]

## Things to watch for
## Anti-patterns to avoid
## Consent and recording
## Notes
- [assumptions, context used, weak hypotheses]
```

## Rules

- **Never open a question with "Would you…" or "Do you think…".** They invite hypothetical answers; ask about past behaviour ("Tell me about the last time…").
- **Mom Test:** every question must yield honest, useful data even if you asked your mom. Ask about their life, not your idea.
- **Maximum 12 questions** in total. Each must earn its place.
- **At least 2 follow-up prompts per core question** ("Tell me more about that", "What happened next?").
- **No questions about the PM's product or solution.** This is about understanding the problem.
- **Goal starts with Understand or Discover**, never Validate or Confirm.
- **Be opinionated:** if a hypothesis is weak or untestable, say so and suggest a better one.
- **Context is not evidence.** Hypotheses drawn from feedback or personas cite the source; assumptions are labelled as assumptions.
- **Two pages maximum.** If it overflows, cut questions, not the falsifiers.
- Consent and recording are always mentioned; the skill never assumes permission to record.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (quotes, names, product terms) untouched.

## References

| Read this | Before… |
|---|---|
| `references/interview-craft.md` §1–2 | writing the goal and hypotheses |
| `references/interview-craft.md` §3 | structuring the 30-minute flow |
| `references/interview-craft.md` §4–5 | writing questions and follow-ups, and checking for bias |
| `references/interview-craft.md` §6–8 | observation notes, screener and consent note |
| `references/research-brief-template.md` | assembling and saving the final brief |
