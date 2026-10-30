# Tone guide

## Choosing the tone
Use the tone the user names. Otherwise infer: enterprise customers / changelog page → B2B Formal; consumer app / in-app → B2C Friendly; Slack, wiki, support briefing → Internal. If still unclear, default to B2B Formal and state it.

## B2B Formal
Professional, clear, concise. "We've introduced…", "This release includes…". For enterprise customers and changelog pages.

## B2C Friendly
Warm, conversational, benefit-focused. "You can now…", "We fixed a bug that…". For consumer apps and in-app changelogs. No jargon.

## Internal
Direct, technical context allowed: ticket keys, feature flags, team names, rollout %. For Slack, wikis, support and CSM briefings.

## Translating technical changes

| Raw change | User-facing |
|---|---|
| Fixed null pointer exception in auth service | Fixed an issue where some users couldn't log in. |
| Add index on orders.created_at | Order history now loads noticeably faster. |
| Refactor payment module | (omit — or Improvement only if users notice something) |
| Bump lodash 4.17.20 → 4.17.21 | (omit — Internal Notes) |
| feat: CSV export for reports | You can now export any report as a CSV file. |

## Checks per item
- Does it say what the user can do or notice? Does it answer "why should I care?"
- No internal system names, error codes, hostnames, credentials or customer names.
- Breaking change or deprecation? State it and what the user must do.
- Do not promise what the input does not say (dates, availability, plans).
