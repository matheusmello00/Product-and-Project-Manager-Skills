# feedback-analyzer

Raw user feedback — pasted text, CSV/Excel, survey, NPS/CSAT, reviews, tickets, Jira issues or interview notes — turned into themes, sentiment, urgency, patterns and prioritised recommendations, with verbatim quotes and entry IDs as evidence.

**When to use:** before refinement, prioritisation or a product review, when you need to know what users say, how often and what to do first.
**Not for:** planning interviews (`user-interview-prep`), writing release notes (`release-notes`), market or competitor research, or computing NPS/CSAT from scratch. Read-only on the source.

## How to use
1. Paste the feedback, or give a file path or link. Add product, period or the decision you want to support if you know it.
2. Receive the analysis; the full classified table is saved to a file when it is long.

Nothing to clean or prepare first.

## Requirements
Pasted text or a local file (CSV, TSV, TXT, Markdown, XLSX, JSON). Python 3.9+ is used for Excel and big files (`openpyxl` for XLSX if installed). Jira/Confluence sources go through the available connector (MCP). Details in `references/sources.md`.

## The output
- **Summary:** entries analysed vs received, sentiment split, top theme, source score as reported, confidence.
- **Themes table:** count, %, sentiment, urgency, signal strength and one verbatim quote with its ID.
- **Top 3 patterns** with evidence and signal strength.
- **Recommended actions** (P0/P1/P2) tied to the evidence.
- **Weak signals and open questions**, classified entries, notes.

## Behaviour notes
- Every entry gets an ID; the source's own IDs are kept verbatim.
- Every theme has at least one verbatim quote; quotes are checked against the source.
- Minimum 3 themes; a theme above about 40% of entries is split.
- Small samples are labelled: under 5 entries no conclusions, under 20 counts instead of percentages.
- Single churn or safety statements are surfaced as high-urgency outliers, not buried by volume.
- Large volumes are read in batches with a completeness check; any subset is declared.
- Scores (NPS, CSAT, stars) are reported as given, never recomputed.
- Personal data is not copied into the report.

## Language
Default to English. Always reply in the language the user writes in or explicitly requests (any language, e.g. Portuguese, Spanish). Only the output language changes, not the logic. Verbatim items (quotes, entry IDs, names, field values) are kept untouched.
