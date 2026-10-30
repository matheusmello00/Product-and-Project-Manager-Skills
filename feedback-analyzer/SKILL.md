---
name: feedback-analyzer
description: 'Turns raw user feedback into themes, sentiment, urgency and prioritised recommendations a PM can act on: reads pasted text or exports (CSV, Excel, survey and NPS/CSAT exports, app-store reviews, support tickets, Jira issues, interview notes), gives every entry an ID, classifies each one (theme, sentiment, urgency, type), aggregates patterns with counts, backs every theme with verbatim quotes and entry IDs, and says how strong each signal is. Reads large volumes in parts. Never invents entries, numbers or quotes, and is read-only on the source.'
when_to_use: 'When you have a pile of feedback and need to know what users are really saying, what comes up most, what is urgent, and what to do first. Serves Product Managers, Product Owners, UX researchers, CSMs and Agile Coaches preparing refinement, prioritisation or a product review.'
maturity: ready
allowed-tools:
- Read
- Write
- Bash
- Glob
- Grep
compatibility: 'Works with pasted text or local files (CSV, TSV, TXT, Markdown, XLSX, JSON). Excel and large CSVs are read with Python 3 (standard library for CSV; openpyxl for XLSX if installed). Jira, Confluence or other sources are read through whichever connector (MCP) is available in the session.'
argument-hint: '[paste feedback | path to file] [optional: product / period / what you want to decide]'
metadata:
  author: Matheus Mello
  version: '0.1.0'
audience: 'Product Manager, Product Owner, UX Researcher, CSM, Agile Coach'
tags:
- product
- discovery
- feedback
- sentiment
- themes
- nps
- csat
---

# Feedback Analyzer

You give the feedback. You get the patterns: what users say, how often, how strongly, and what to do first. Every claim is backed by real words and entry IDs, and a thin signal is called thin.

## Requires

Nothing beyond the feedback itself. Pasted text works as is. For files see `references/sources.md` (formats and how each is read). Read-only: the source is never changed.

## What you need before starting

- **The feedback**: pasted, a file path, or a link/connector reference. Nothing to prepare or clean first.
- **Optional context** (use it if given, never block on it): product or feature, period, segment, and the decision the analysis should support. If the decision is known, the recommendations target it.
- **Language**: the feedback may be in any language. Quotes stay in the original language; the analysis follows the output language (see Language).

## Flow

1. **Ingest and number.** Read the source (`references/sources.md`). Give every entry a stable ID (`F-001…`, or the source's own ID / row number, kept verbatim). One entry = one piece of feedback; split a long entry that raises distinct issues into sub-entries (`F-014a`, `F-014b`). Report how many entries were read, how many were skipped (empty, duplicates, spam) and why.
2. **Large volumes: read in parts.** Above about 200 entries or any file too large to read at once, process in batches (about 100 entries), keep a running tally of themes in a working file, and finish with a completeness check. Never sample silently: if only part was classified, say which part and how it was chosen. See `references/sources.md` §3.
3. **Build the theme list.** Draft themes bottom-up from the entries, at least 3, named by what the user experiences ("Slow checkout"), not by internal team ("Backend"). Merge near-duplicates, split a theme that swallows more than about 40% of the entries into sub-themes. See `references/classification.md` §1.
4. **Classify every entry**: dominant **Theme** (plus secondary if relevant), **Sentiment** (Positive / Neutral / Negative), **Urgency** (High / Medium / Low), **Type** (Bug report / Feature request / Complaint / Praise / Question). Definitions and edge cases in `references/classification.md` §2–4. Classify what the user said, not what they might have meant.
5. **Aggregate.** Counts per theme, sentiment distribution, urgency mix, type mix; use the source's own metadata when present (score, plan, segment, date, channel). Where a score exists (NPS, CSAT, stars), report it as given and never recompute it from your classification.
6. **Surface insights.** Look for what is not obvious: themes that co-occur, sentiment that differs by segment or period, signals of churn risk or expansion, mismatch between score and text. Each insight cites entry IDs. See `references/classification.md` §5.
7. **Rate signal strength** per theme and per pattern: Strong / Moderate / Weak, from volume, spread (different users and channels) and consistency. See `references/classification.md` §6.
8. **Recommend.** Concrete next steps for a PM, in priority order, each tied to the themes and entry IDs it rests on. Say what to do first and why.
9. **Self-check, then deliver** (below). Save the full classified table to a file when it is long.

### Self-check before delivering

- Entry count in the summary equals the sum of theme counts (a secondary theme is not counted twice).
- Every theme has at least one verbatim quote, and each quote appears in the source word for word.
- Every pattern and recommendation lists entry IDs that exist.
- Percentages add up to about 100% and use the stated denominator.
- No number, date or segment was invented; unknowns are marked unknown.

## Template

```
# Feedback analysis — [product / source]  ·  [date]

## Summary
- Entries analysed: [N] of [M] received ([skipped and why])
- Sentiment: [x]% positive · [x]% neutral · [x]% negative
- Top theme: [theme] ([n] entries) · Period: [range or "not available"]
- Source score, if any: [NPS / CSAT / avg stars, as reported]
- Confidence: [overall note: volume, spread, caveats]

## Themes
| Theme | Count | % | Sentiment | Urgency | Signal | Example quote (ID) |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | Strong/Moderate/Weak | "..." (F-004) |

## Top 3 patterns
1. **[Pattern]** — what it is · why it matters · evidence: [IDs] · signal: [Strong/Moderate/Weak]

## Recommended actions
| Priority | Action | Based on (themes / IDs) | Expected impact |
|---|---|---|---|
| P0 | ... | ... | ... |

## Weak signals and open questions
- [thin or contradictory signals, what extra data would settle them]

## Classified entries
[Full table if fewer than 50 entries: ID · Theme (secondary) · Sentiment · Urgency · Type · Quote or short excerpt]
[Otherwise: saved to `feedback-classified-[date].csv`, path stated here]

## Notes
- [assumptions, skipped entries, parts not read, how themes were merged or split]
```

## Rules

- **Do not editorialise.** Classify what users said, not what you think they meant. No guessing of motives.
- **Real words beat summaries.** At least one verbatim quote per theme, with its entry ID. Quotes are never edited or translated inside quotation marks.
- **Never invent.** No entries, quotes, counts, dates, segments or scores that are not in the source. Missing data is stated as missing.
- **Dominant theme counts once.** If an entry touches several themes, assign the dominant one for the counts and note the secondary one.
- **Urgency comes from language and frequency**, not from your opinion of importance. "Broken", "can't use", "blocking", "cancelling" = High. See `references/classification.md` §4.
- **Minimum 3 themes.** If everything collapses into one, split it into sub-themes.
- **Small samples are said to be small.** Fewer than 5 entries: no conclusions, list everything as weak signals. 5–19: patterns are indicative only. Percentages are replaced by counts below 20 entries.
- **Volume is not importance.** A single "I'm cancelling because of X" outweighs five mild mentions; flag it as a high-urgency outlier instead of burying it.
- **Be opinionated in recommendations.** Say what to do first and why; do not just list options. Tie each to evidence.
- **Report what was not analysed.** Skipped, unreadable or unread parts go in the Notes, never silently dropped.
- **Keep the analysis part under 2 pages.** The classified table may be longer or live in a file.
- **Personal data.** Do not copy names, emails or phone numbers into the report; keep the entry ID instead.
- Read-only: the source is never modified; files are written beside it or in the working directory.
- Do not turn recommendations into tracker items unless asked.

## Language

Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Keep verbatim items (quotes, entry IDs, names, field values) untouched.

## References

| Read this | Before… |
|---|---|
| `references/sources.md` §1–2 | reading a CSV, Excel, survey, NPS/CSAT, review, ticket, Jira or interview-notes source |
| `references/sources.md` §3 | processing a large volume in parts and running the completeness check |
| `references/classification.md` §1 | building the theme list |
| `references/classification.md` §2–4 | classifying sentiment, type and urgency, including edge cases |
| `references/classification.md` §5–6 | writing insights and rating signal strength |
