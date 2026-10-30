# Sources — Feedback Analyzer reference

Index:
1. Sources and how to read each
2. Normalising to one entry list
3. Reading large volumes in parts
4. Cautions

## 1. Sources and how to read each

| Source | How to read | Watch for |
|---|---|---|
| Pasted text | Split by line, blank line or bullet; one entry each | Quoted multi-paragraph entries; signatures and email threads |
| CSV / TSV | Python `csv` module (`csv.Sniffer` for the delimiter); inspect headers and 5 rows first | Encoding (try `utf-8-sig`, then `latin-1`), multiline cells, delimiter `;` |
| Excel (XLSX) | `openpyxl` (read-only) or `pandas` if installed; list sheets first | Several sheets (one per channel?), header not on row 1, merged cells |
| Survey / NPS / CSAT export | Find the score column and the free-text column(s) | Report the score as given; text-only analysis of comments; many blank comments are normal |
| App-store / review export | Rating, text, date, version, language | Version drift (an old bug raised after a fix), non-English reviews |
| Support tickets | Subject + first customer message; ignore agent replies unless asked | Duplicates of the same incident, auto-generated text |
| Jira / issue tracker | Via the connector: summary, description, comments from reporters | One user, many tickets; internal comments are not user feedback |
| Interview notes / transcripts | Treat each distinct statement as an entry, speaker-tagged | Interviewer's words are not feedback; paraphrase vs verbatim |
| Chat / Slack / email dumps | One message or thread per entry | Threads where only one message is feedback |
| JSON | Locate the array of entries and the text field | Nested structures |

If a column is ambiguous, say which one you used (e.g. "text taken from `comment`, score from `nps`") in the Notes.

## 2. Normalising to one entry list

Whatever the source, build this working list before classifying:

`ID · text · optional: date · score · channel · segment/plan · language`

- IDs: keep the source's own ID (ticket key, review ID) verbatim; otherwise number rows `F-001…` in source order and say so.
- Drop only what carries no feedback (empty, "N/A", test rows, exact duplicates). Count and list the drops; keep near-duplicates (the repetition is signal).
- Keep the original text untouched; never correct spelling inside a quote.
- Remove personal data (names, emails, phones) from anything copied into the report.

## 3. Reading large volumes in parts

- Check size first (`wc -l`, row count). Up to about 200 entries: read everything in one pass. Above that: batches of about 100.
- For each batch: classify, then append to a working file (`feedback-working-[date].csv` in the working directory) and update a running theme tally. Re-use theme names across batches; add a new theme only when an entry fits none.
- After the last batch, re-read the theme list once: merge near-duplicates, rename for clarity, then re-assign entries of merged themes.
- **Completeness check:** total entries = sum of dominant-theme counts; spot-check at least 10 random entries (or 5% if larger) back against their classification; confirm the quotes exist in the source.
- If you cannot classify everything (time, size), say exactly what was covered and how the subset was chosen (e.g. "most recent 500", "random 300 with seed 1"). A subset is never presented as the whole.

## 4. Cautions

- A score and its comment can disagree (9/10 with a complaint). Classify the text; note the mismatch as an insight.
- Mixed-language sources: classify in the original language, name themes in the output language, keep quotes original.
- Export artefacts (HTML tags, "Sent from my iPhone", ticket templates) are not feedback.
- Feedback from internal staff or testers is flagged, not mixed silently with customer feedback.
