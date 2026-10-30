# Input sources

All access is **read-only**.

## Git
- `git log --oneline v2.2..v2.3` (range by tags), or `git log --oneline --since="2 weeks ago"`.
- Terse messages: `git log --no-merges --format="%h %s%n%b" <range>`.
- Latest tag for the version: `git describe --tags --abbrev=0`; date: `git log -1 --format=%cs <tag>`.
- Conventional prefixes (`feat:`, `fix:`, `perf:`, `refactor:`, `chore:`, `docs:`) help classification but are not proof of user impact.
- Never run commit, tag, push, checkout or reset.

## Pasted text / files
Changelogs, CSV exports, release drafts or notes: read as given. One entry per line or paragraph.

## Trackers (optional connector)
Use ticket keys found in commits (`ABC-123`) to read the title and description for user-facing wording.

| Tracker | Lookup |
|---|---|
| Jira | `key in (...)` or JQL on `fixVersion` |
| Azure DevOps | work item IDs, or WIQL on iteration/tag |
| ClickUp | task IDs, or filtered list by tag/status |

If no connector is available, work from the commit/ticket text and say the tickets were not enriched. Never write to the tracker.

## Gaps
Missing version, date, or unclear impact → ask once, or list under Needs confirmation. Do not guess.
