# Backlog — BookSwap Campus  ·  2026-10-30
Sources: docs/prd-bookswap-v1.md

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| FR-01 | functional | FR-01 (see source) | PRD (section n/a) |
| FR-02 | functional | FR-02 (see source) | PRD (section n/a) |

## Epics

### EP-01 — Book listing
**Delivers:** Lets students publish and manage the books they want to swap.
**Success metric:** 70% of registered students publish at least one listing in the first month.
**Acceptance criteria (epic):**
- A student can publish, find and manage listings end to end
- Only the owner can change or remove a listing

## Stories

### EP-01 — Book listing

#### ST-01 — Publish a book listing
**As a** student, **I want** to publish a listing, **so that** other students can find my book.

**Description:** The student can publish a listing. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I am signed in **When** I submit a listing **Then** it works correctly

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: I submit a listing
  Given I am signed in
  When I submit a listing
  Then it works correctly
```

**Priority:** Must
**Requirements:** FR-01
**Dependencies:** None
**Open questions:** None
**Estimate:** 

#### ST-02 — Edit my listing
**As a** student, **I want** to edit my listing, **so that** .

**Acceptance criteria:**
- **Given** I own a listing **When**  **Then** the changes are saved
- **Given** I own a listing **When** I edit the price **Then** the page loads fast

**Test scenarios (Gherkin):**

```gherkin
@TC-02 @happy @AC1
Scenario: The changes are saved
  Given I own a listing
  Then the changes are saved

@TC-03 @negative @AC2
Scenario: I edit the price
  Given I own a listing
  When I edit the price
  Then the page loads fast
```

**Priority:** Urgent
**Requirements:** FR-02
**Dependencies:** None
**Open questions:** None
**Estimate:** 

