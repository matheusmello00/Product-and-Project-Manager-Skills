# release-notes

Git commits, tickets, changelogs or raw notes turned into user-facing release notes — New features, Improvements, Bug fixes — in the tone you need.

**When to use:** a release, sprint or deploy needs notes for customers, in-app, support or internal channels.
**Not for:** technical changelogs for engineers, deployment runbooks, or announcements/marketing copy. Read-only — it never touches the repo or the tracker.

## Requirements
Pasted text or a file needs nothing. A repository needs `git` (read-only). A tracker connector (MCP) is optional: Atlassian (Jira), Azure DevOps or ClickUp, to enrich commits with ticket titles (mapping in `references/sources.md`).

## Tone
B2B Formal (default), B2C Friendly or Internal. Details and examples in `references/tone-guide.md`.

## Behaviour notes
- Related commits are merged into one item; noise (merges, bumps, CI, invisible refactors) is dropped.
- Changes are never invented. Unclear ones go to a **Needs confirmation** block.
- Internal names, error codes and infrastructure never appear in user-facing sections.
- Output is saved as `release-notes-[version-or-date].md`.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (ticket keys, names, version numbers) are kept untouched.
