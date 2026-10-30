# PRD — BookSwap  ·  2026-10-30  ·  v0.1 draft

## Problem
- Who: students of two faculties who buy textbooks every semester
- How they solve it today: WhatsApp groups and flyers
- Why that hurts: books are hard to find; no one tracks swaps (baseline unknown)

## Target users
- Primary: undergraduate student, uses the app weekly
- Trigger: start of semester

## Solution
- We are building: a web app to publish books and request swaps
- We are NOT building: payments, shipping, a mobile app
- Key flows: 1. Student publishes a book. 2. Another student searches by course. 3. They request a swap; the owner accepts or declines.

## Success metrics
| Metric | Type | Baseline | Target | By when |
|---|---|---|---|---|
| Completed swaps per semester | Primary | unknown | 200 | end of pilot |

## Scope
- MVP: publish, search by course, request and decide swaps
- V2: search by ISBN
- Out of scope: payments, shipping

## Requirements
| ID | Requirement | User | Priority | Source |
|---|---|---|---|---|
| FR-01 | Student publishes a book with title (mandatory), course and condition | Student | Must | notes 12 Oct |
| FR-02 | Student searches listings by course | Student | Must | notes 12 Oct |
| FR-03 | Only the owner can remove their listing | Student | Must | notes 12 Oct |
| NFR-01 | Search results appear within 2 seconds | Student | Should | assumed |

## Risks and open questions
- Product: will students trust unknown swappers?
- Open questions: What counts as a valid course? — Ana — before refinement

## Assumptions
- Pilot limited to two faculties
