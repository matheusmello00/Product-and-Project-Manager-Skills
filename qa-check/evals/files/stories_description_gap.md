# Backlog — BookSwap Campus  ·  2026-10-30
Sources: prd-bookswap.md

## Requirements inventory
| ID | Kind | Requirement | Source |
|---|---|---|---|
| FR-01 | functional | Student publishes a book with title (mandatory, max 120 characters), course and condition | prd-bookswap.md §Requirements |
| FR-02 | functional | Only the owner can remove a listing | prd-bookswap.md §Requirements |

## Epics

### EP-01 — Book listing
**Delivers:** Students publish and manage the books they want to swap.
**Success metric:** 70% of registered students publish a listing in the first month.
**Requirements owned:** FR-01, FR-02
**Acceptance criteria (epic):**
- A student can publish and remove their own listings
- Nobody else can remove a listing

**Out of scope:** payments, shipping

## Stories

### EP-01 — Book listing

#### ST-01 — Publish a book listing
**As a** student, **I want** to publish a listing with title, course and condition, **so that** other students can find my book.

**Description:** The title is mandatory and has a maximum of 120 characters. The course and the condition are chosen from a list. A published listing appears in the course search results.

**Acceptance criteria:**
- **Given** I am signed in **When** I submit a listing with title, course and condition **Then** the listing appears in the search results for that course
- **Given** I am signed in **When** I submit a listing without a title **Then** the form shows "Title is required" and nothing is published

**Test scenarios (Gherkin):**

```gherkin
@TC-01 @happy @AC1
Scenario: Publish with all fields
  Given I am signed in
  When I submit a listing with title, course and condition
  Then the listing appears in the search results for that course

@TC-02 @negative @AC2
Scenario: Publish without a title
  Given I am signed in
  When I submit a listing without a title
  Then the form shows "Title is required" and nothing is published
```

**Priority:** Must — core flow
**Requirements:** FR-01

#### ST-02 — Remove my listing
**As a** student, **I want** to remove one of my listings, **so that** the book no longer appears once I have swapped it.

**Description:** Only the owner can remove a listing. Removing it takes it out of the search results immediately.

**Acceptance criteria:**
- **Given** I own a listing **When** I remove it **Then** it no longer appears in the search results
- **Given** I own a listing **When** I remove it **Then** it works correctly

**Test scenarios (Gherkin):**

```gherkin
@TC-03 @happy @AC1
Scenario: Owner removes a listing
  Given I own a listing
  When I remove it
  Then it no longer appears in the search results
```

**Priority:** Must — core flow
**Requirements:** FR-02

## Coverage matrix
| Requirement | Epic | Stories | Scenarios |
|---|---|---|---|
| FR-01 | EP-01 | ST-01 | TC-01, TC-02 |
| FR-02 | EP-01 | ST-02 | TC-03 |

## Backlog summary
2 stories, 3 scenarios.

## Notes
- Estimates left empty.
