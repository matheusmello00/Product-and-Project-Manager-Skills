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
- **Given** I am signed in **When** I submit a valid listing **Then** it appears in search results within 1 minute
- **Given** I am signed in **When** I submit a listing without a title **Then** the form shows 'Title is required'

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: Publish with all mandatory fields
  Given I am signed in
  And I open the new listing form
  When I submit a listing with all mandatory fields
  Then the listing appears in search results within 1 minute

@TC-02 @smoke @AC5
Scenario: Publish and check it works properly
  Then it works properly
```

**Priority:** Must
**Requirements:** FR-01
**Dependencies:** None
**Open questions:** None
**Estimate:** 

#### ST-02 — Remove my listing
**As a** student, **I want** to remove my own listing, **so that** the catalogue only shows available books.

**Description:** The student can remove my own listing. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I own an active listing **When** I remove it **Then** it no longer appears in search results
- **Given** another student owns a listing **When** I try to remove it **Then** the system rejects the action with a permission error

**Test scenarios (Gherkin):**

```gherkin

```

**Priority:** Should
**Requirements:** FR-02
**Dependencies:** ST-01
**Open questions:** None
**Estimate:** 

#### ST-03 — Search listings by course
**As a** student, **I want** to filter listings by course, **so that** I find books for my subjects.

**Description:** The student can filter listings by course. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** listings exist for several courses **When** I filter by one course **Then** only listings of that course are shown
- **Given** no listing matches **When** I filter by a course **Then** the page shows 'No listings found'

**Test scenarios (Gherkin):**

```gherkin
@TC-03 @happy @AC1
Scenario: Filter by an existing course
  Given listings exist for several courses
  When I filter by one course
  Then only listings of that course are shown

@TC-04 @alternative @AC2
Scenario Outline: Filter with several courses
  Given listings exist for <course>
  When I filter by <course>
  Then only <expected> listings are shown
  Examples:
    | course |
    | Maths |
```

**Priority:** Could
**Requirements:** FR-01
**Dependencies:** None
**Open questions:** Which courses are supported in the first release?
**Estimate:** 

