# Classification — Feedback Analyzer reference

Index:
1. Building the theme list
2. Sentiment
3. Type
4. Urgency
5. Insights
6. Signal strength

## 1. Building the theme list

- Bottom-up: read a first batch, cluster by what the user is talking about, then name the clusters. Do not start from a fixed taxonomy.
- Name by user experience ("Cannot find past orders"), not by team or component ("Search service").
- Typical top-level themes (use only if the data supports them): Onboarding, Pricing and billing, Performance, Reliability and bugs, Usability, Missing feature, Support experience, Integrations, Content/data quality.
- Minimum 3 themes. A theme with more than about 40% of the entries gets split into sub-themes; themes with 1 entry are folded into "Other" unless High urgency.
- One dominant theme per entry for counting; a secondary theme is noted, not counted.

## 2. Sentiment

| Value | Use when |
|---|---|
| Positive | the user expresses satisfaction, praise or gratitude, with no unresolved complaint |
| Neutral | factual, a question, or a request without emotion |
| Negative | frustration, disappointment, a complaint or a failure described |

- Mixed ("love X, but Y is broken"): classify by the part that is the main point of the message; note the secondary theme with its own sentiment.
- Sarcasm: classify by the intended meaning and note it as such in the Notes if it changed the result.
- Scores are context, not sentiment. Classify the text.

## 3. Type

| Value | Use when |
|---|---|
| Bug report | something that should work does not |
| Feature request | asks for something that does not exist |
| Complaint | dissatisfaction without a concrete defect or ask |
| Praise | positive statement about the product |
| Question | asks how to do something or what something means |

One type per entry. A "Question" that reveals a usability problem stays a Question; the usability issue is the secondary theme.

## 4. Urgency

Based on language intensity and frequency, never on your view of importance.

| Level | Signals |
|---|---|
| High | blocking or loss language: "broken", "can't use", "blocking", "lost data", "charged twice", "cancelling", "switching to"; or the same issue from many users |
| Medium | clear friction with a workaround: "annoying", "confusing", "takes too long" |
| Low | nice-to-have, mild preference, praise, general question |

- Frequency raises urgency by one level when one theme recurs across at least 10% of entries and 5 users.
- Safety, privacy, money or legal language ("charged", "data leak", "GDPR") is High and flagged, regardless of volume.
- A single churn statement is a **High-urgency outlier**: report it separately even if the theme count is 1.

## 5. Insights

Look for what the counts alone do not show:

- Themes that co-occur (e.g. "Onboarding" with "Missing feature" suggests users do not find what exists).
- Differences by segment, plan, channel, version or period (sentiment dropping after a release date).
- Score vs text mismatch.
- Praise that names a feature worth protecting.
- Workarounds users describe (a signal for a missing feature).
- Churn-risk or expansion language.

Each insight: what it is, evidence (entry IDs), why it matters. If it rests on fewer than 3 entries, label it a weak signal.

## 6. Signal strength

| Level | Rule of thumb |
|---|---|
| Strong | at least 10 entries or 10% of the set, from several users and, if known, more than one channel or segment; consistent wording |
| Moderate | 4–9 entries, or strong volume from a single channel or segment only |
| Weak | 1–3 entries, a single user, or contradictory entries |

- Below 20 entries total, show counts instead of percentages.
- Below 5 entries total, no pattern is Strong; say the sample is too small to conclude.
- Strength describes the evidence, not the importance: a Weak signal can still be High urgency (see §4).
