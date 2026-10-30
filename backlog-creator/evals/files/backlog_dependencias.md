# Backlog — BookSwap Campus  ·  2026-10-30
Sources: docs/prd-bookswap-v1.md

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| FR-01 | functional | FR-01 (see source) | PRD (section n/a) |
| FR-02 | functional | FR-02 (see source) | PRD (section n/a) |
| FR-03 | functional | FR-03 (see source) | PRD (section n/a) |

## Epics

### EP-01 — Swap flow
**Delivers:** Lets two students agree and complete a swap.
**Success metric:** 60% of accepted swaps are marked as completed.
**Acceptance criteria (epic):**
- A student can publish, find and manage listings end to end
- Only the owner can change or remove a listing

## Stories

### EP-01 — Swap flow

#### ST-01 — Request a swap
**As a** student, **I want** to request a swap, **so that** I can get the book I need.

**Description:** The student can request a swap. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** a listing is active **When** I request a swap **Then** the owner is notified
- **Given** a listing is reserved **When** I request a swap **Then** the system blocks the request

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: I request a swap
  Given a listing is active
  When I request a swap
  Then the owner is notified

@TC-02 @negative @AC2
Scenario: I request a swap
  Given a listing is reserved
  When I request a swap
  Then the system blocks the request
```

**Priority:** Must
**Requirements:** FR-01
**Dependencies:** ST-02
**Open questions:** None
**Estimate:** 

#### ST-02 — Accept a swap
**As a** student, **I want** to accept a swap request, **so that** we can arrange the exchange.

**Description:** The student can accept a swap request. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** I received a request **When** I accept it **Then** both students see the swap as accepted
- **Given** I received a request **When** I decline it **Then** the requester is notified of the refusal

**Test scenarios (Gherkin):**

```gherkin
@TC-03 @happy @AC1
Scenario: I accept it
  Given I received a request
  When I accept it
  Then both students see the swap as accepted

@TC-04 @negative @AC2
Scenario: I decline it
  Given I received a request
  When I decline it
  Then the requester is notified of the refusal
```

**Priority:** Must
**Requirements:** FR-02
**Dependencies:** ST-01
**Open questions:** None
**Estimate:** 

#### ST-03 — Rate the other student
**As a** student, **I want** to rate my swap partner, **so that** others can trust the community.

**Description:** The student can rate my swap partner. Business rules are given by the acceptance criteria below.

**Acceptance criteria:**
- **Given** a swap is completed **When** I submit a rating from 1 to 5 **Then** the rating is stored on the partner's profile
- **Given** a swap is not completed **When** I try to rate **Then** the system blocks the action

**Test scenarios (Gherkin):**

```gherkin
@TC-05 @happy @AC1
Scenario: I submit a rating from 1 to 5
  Given a swap is completed
  When I submit a rating from 1 to 5
  Then the rating is stored on the partner's profile

@TC-06 @negative @AC2
Scenario: I try to rate
  Given a swap is not completed
  When I try to rate
  Then the system blocks the action
```

**Priority:** Should
**Requirements:** FR-03
**Dependencies:** ST-09
**Open questions:** None
**Estimate:** 

