# Backlog — BookSwap Campus  ·  2026-10-30
Sources: docs/prd-bookswap-v1.md

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| FR-01 | functional | FR-01 (see source) | PRD (section n/a) |
| FR-02 | functional | FR-02 (see source) | PRD (section n/a) |
| FR-03 | functional | FR-03 (see source) | PRD (section n/a) |
| FR-04 | functional | Moderation of reported listings |  |
| FR-05 | functional | FR-05 (see source) | PRD (section n/a) |

## Epics

### EP-01 — Book listing
**Delivers:** Lets students publish and manage the books they want to swap.
**Success metric:** 70% of registered students publish at least one listing in the first month.
**Requirements owned:** FR-01, FR-02
**Acceptance criteria (epic):**
- A student can publish, find and manage listings end to end
- Only the owner can change or remove a listing

### EP-02 — Notifications
**Delivers:** Keeps students informed about activity on their listings.
**Success metric:** 80% of swap requests are answered within 48 hours.
**Requirements owned:** FR-01, FR-03
**Acceptance criteria (epic):**
- A student can request a swap and the owner is notified
- A reserved listing cannot receive new requests

## Stories

### EP-01 — Book listing

#### ST-01 — Publish a book listing
**As a** student, **I want** to publish a listing, **so that** other students can find my book.

**Description:** The student can publish a listing. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I am signed in **When** I submit a valid listing **Then** it appears in search results
- **Given** I am signed in **When** I submit an invalid listing **Then** the form shows the missing fields

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: I submit a valid listing
  Given I am signed in
  When I submit a valid listing
  Then it appears in search results

@TC-02 @negative @AC2
Scenario: I submit an invalid listing
  Given I am signed in
  When I submit an invalid listing
  Then the form shows the missing fields
```

**Priority:** Must
**Requirements:** FR-01
**Dependencies:** None
**Open questions:** None
**Estimate:** 

#### ST-02 — Search listings by course
**As a** student, **I want** to filter listings by course, **so that** I find books for my subjects.

**Description:** The student can filter listings by course. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** listings exist for several courses **When** I filter by one course **Then** only listings of that course are shown
- **Given** no listing matches **When** I filter by a course **Then** the page shows 'No listings found'

**Test scenarios (Gherkin):**

```gherkin
@TC-03 @happy @AC1
Scenario: I filter by one course
  Given listings exist for several courses
  When I filter by one course
  Then only listings of that course are shown

@TC-04 @negative @AC2
Scenario: I filter by a course
  Given no listing matches
  When I filter by a course
  Then the page shows 'No listings found'
```

**Priority:** Must
**Requirements:** FR-02
**Dependencies:** None
**Open questions:** None
**Estimate:** 

#### ST-03 — Report a listing
**As a** student, **I want** to report an inappropriate listing, **so that** the catalogue stays safe.

**Description:** The student can report an inappropriate listing. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** a listing is visible **When** I report it with a reason **Then** a moderator receives the report
- **Given** I already reported a listing **When** I report it again **Then** the system tells me it was already reported

**Test scenarios (Gherkin):**

```gherkin
@TC-05 @happy @AC1
Scenario: I report it with a reason
  Given a listing is visible
  When I report it with a reason
  Then a moderator receives the report

@TC-06 @negative @AC2
Scenario: I report it again
  Given I already reported a listing
  When I report it again
  Then the system tells me it was already reported
```

**Priority:** Could
**Dependencies:** None
**Open questions:** None
**Estimate:** 

