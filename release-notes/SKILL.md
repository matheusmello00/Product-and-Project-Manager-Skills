---
name: release-notes
description: 'Turns git commits, tickets (Jira, Azure DevOps, ClickUp), changelogs or raw notes into user-facing release notes, grouped into New features, Improvements and Bug fixes, with an adjustable tone (B2B Formal, B2C Friendly, Internal). Translates every change into user impact, merges related commits into one item, omits internal refactors from user-facing sections, never exposes internal names, error codes or infrastructure, and never invents a change that is not in the input. Saves the result as release-notes-[version-or-date].md. Read-only: it never alters the repository or the tracker.'
when_to_use: 'When a release, sprint or deploy needs notes for users, customers, support or internal channels: "write the release notes", "changelog for v2.3", "what shipped this sprint", "turn these commits into notes". Serves PMs, Product Owners, Scrum Masters and release managers.'
maturity: ready
allowed-tools:
- Read
- Write
- Bash
- mcp__atlassian
- mcp__azure-devops
- mcp__clickup
compatibility: 'No dependencies for pasted text or files. Git (read-only) for commit history. A tracker connector (MCP) with read access — Atlassian (Jira), Azure DevOps or ClickUp — is optional, to enrich commits with ticket titles and descriptions.'
argument-hint: '[paste commits/tickets | path to file | repo path + range] [tone]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Product Manager, Product Owner, Scrum Master, release manager'
tags:
- product
- release
- changelog
- communication
- git
- jira
---

# Release Notes

Transforms raw engineering artifacts into release notes written for **users, not engineers**. Every item answers "why should the user care?". What has no user impact is left out of the user-facing sections.

## Requires

Nothing for pasted text or a file. For a repository: `git` (read-only). A tracker connector is optional — see `references/sources.md`.

## What you need before starting

- **Input:** pasted commits/tickets, a file path (changelog, CSV, export) or a repo path with a range (`v2.2..v2.3`, `--since`).
- **Tone** (optional): B2B Formal (default), B2C Friendly or Internal — see `references/tone-guide.md`. If unclear from context, default to B2B Formal and say so.
- **Version and date** (optional): taken from the input or the latest tag; if absent, use today's date.
- **Audience note** (optional): who reads it (customers, in-app, support).

## Flow

1. **Read the input.** File path → read it. Repo → `git log --oneline <range>` (add `--no-merges` and body with `--format` when messages are terse); never run a command that writes to the repo. Tickets → use the connector if available, else the pasted text. See `references/sources.md`.
2. **Inventory the changes** — one line per commit/ticket, keeping keys (`ABC-123`, hashes) for traceability.
3. **Drop noise:** merge commits, version bumps, CI, formatting, dependency updates and refactors with no visible effect → candidates for Internal Notes.
4. **Group** related changes into one item (five commits on one feature = one bullet), then classify: New features, Improvements, Bug fixes.
5. **Translate** each item into user impact (what the user can do, notice or no longer suffers). See `references/tone-guide.md` for before/after examples.
6. **Flag what you cannot resolve:** a change whose user impact is unclear, a commit message like "fix stuff", a breaking change, a missing date. Put these in the **Needs confirmation** block instead of guessing.
7. **Apply the tone** and write the notes with the template below.
8. **Save** to `release-notes-[version-or-date].md` in the working directory and show the result.

## Template

```
### [Release title — descriptive, not just a version number]
**Version:** [if applicable]
**Date:** [release date]

---

#### New Features
- **[Feature name]** — what it does and why it matters to the user.

#### Improvements
- **[What improved]** — what the user will notice is better.

#### Bug Fixes
- **[What was fixed]** — the problem the user experienced, not the root cause.

---

#### Internal Notes (only if requested)
- Details for support, CSMs or stakeholders: migration notes, feature flags, rollout %, known issues not fixed. Ticket keys allowed.

#### Needs confirmation (only if there are open points)
- [KEY / hash] [change] — why it is unclear and what is needed.
```

Omit empty categories.

## Rules

- **Write for users.** Translate every change into user impact: "Fixed null pointer exception in auth service" → "Fixed an issue where some users couldn't log in."
- **Never invent.** Only describe changes present in the input. If the impact is not clear, ask or list it under Needs confirmation; do not embellish.
- **Refactors** become an Improvement only if users notice something; otherwise omit them (Internal Notes if requested).
- **Group related commits** into a single item.
- **Never expose** internal system names, error codes, infrastructure, hostnames, credentials, customer names or personal data in user-facing sections. Redact and say you did.
- **Breaking changes and deprecations** are always stated, with what the user must do.
- **Default tone is B2B Formal** when not specified.
- **Read-only:** never commit, tag, push, or edit tickets.
- **Every item answers:** "Why should the user care?"
- Keep ticket keys and version numbers verbatim; keep Internal Notes out of user-facing sections.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (ticket keys, names, version numbers, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/sources.md` | reading git, Jira, Azure DevOps, ClickUp, a changelog or raw notes |
| `references/tone-guide.md` | choosing the tone and translating technical changes into user language |
