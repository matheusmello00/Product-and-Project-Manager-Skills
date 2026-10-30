# Backlog — BookSwap Campus  ·  2026-10-30
Sources: docs/prd-bookswap-v1.md

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| FR-01 | functional | Students publish book listings | PRD §3.1 (p.12) |
| FR-02 | functional | Students edit or remove their listing | PRD §3.2 (p.14) |
| FR-03 | functional | Students request a swap | PRD §4.1 (p.18) |

## Epics

### EP-01 — Book listing
**Delivers:** Lets students publish and manage the books they want to swap.
**Success metric:** 70% of registered students publish at least one listing in the first month.
**Requirements owned:** FR-01, FR-02
**Acceptance criteria (epic):**
- A student can publish, find and manage listings end to end
- Only the owner can change or remove a listing

### EP-02 — Swap requests
**Delivers:** Lets students request and agree a swap with another student.
**Success metric:** 50% of listings receive at least one swap request within 14 days.
**Requirements owned:** FR-03
**Acceptance criteria (epic):**
- A student can request a swap and the owner is notified
- A reserved listing cannot receive new requests

## Stories

### EP-01 — Book listing

#### ST-01 — Publish a book listing
**As a** student, **I want** to publish a listing with title, course and condition, **so that** other students can find my book.

**Description:** The student can publish a listing with title, course and condition. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I am signed in **When** I submit a listing with all mandatory fields **Then** the listing appears in search results within 1 minute
- **Given** I am signed in **When** I submit a listing without a title **Then** the form shows 'Title is required' and nothing is published

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: I submit a listing with all mandatory fields
  Given I am signed in
  When I submit a listing with all mandatory fields
  Then the listing appears in search results within 1 minute

@TC-02 @negative @AC2
Scenario: I submit a listing without a title
  Given I am signed in
  When I submit a listing without a title
  Then the form shows 'Title is required' and nothing is published

@TC-07 @boundary @AC2
Scenario Outline: Title length limits
  Given I am signed in
  When I submit a listing with a title of <length> characters
  Then the listing is <result>
  Examples:
    | length | result |
    | 120 | published |
    | 121 | rejected with 'Title too long' |
```

**Priority:** Must
**Requirements:** FR-01
**Dependencies:** None
**Open questions:** None
**Estimate:** 

#### ST-02 — Edit or remove my listing
**As a** student, **I want** to edit or remove my own listing, **so that** the catalogue only shows books that are still available.

**Description:** The student can edit or remove my own listing. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I own an active listing **When** I remove it **Then** it no longer appears in search results
- **Given** another student owns a listing **When** I try to edit it **Then** the system rejects the action with a permission error

**Test scenarios (Gherkin):**

```gherkin
@TC-03 @happy @AC1
Scenario: I remove it
  Given I own an active listing
  When I remove it
  Then it no longer appears in search results

@TC-04 @negative @AC2
Scenario: I try to edit it
  Given another student owns a listing
  When I try to edit it
  Then the system rejects the action with a permission error
```

**Priority:** Should
**Requirements:** FR-02
**Dependencies:** ST-01
**Open questions:** None
**Estimate:** 

### EP-02 — Swap requests

#### ST-03 — Request a swap
**As a** student, **I want** to request a swap for a listed book, **so that** I can get the book I need.

**Description:** The student can request a swap for a listed book. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** a listing is active **When** I request a swap offering one of my listings **Then** the owner receives a notification with my offer
- **Given** a listing is already reserved **When** I request a swap **Then** the system blocks the request and shows 'Already reserved'

**Test scenarios (Gherkin):**

```gherkin
@TC-05 @happy @AC1
Scenario: I request a swap offering one of my listings
  Given a listing is active
  When I request a swap offering one of my listings
  Then the owner receives a notification with my offer

@TC-06 @negative @AC2
Scenario: I request a swap
  Given a listing is already reserved
  When I request a swap
  Then the system blocks the request and shows 'Already reserved'
```

**Priority:** Must
**Requirements:** FR-03
**Dependencies:** ST-01
**Open questions:** None
**Estimate:** 

