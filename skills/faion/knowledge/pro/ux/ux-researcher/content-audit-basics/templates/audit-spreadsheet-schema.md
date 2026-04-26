# Content Audit Spreadsheet Schema

Column definitions for the content audit inventory. Use as Google Sheets, Airtable, or CSV.

## Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | int | Unique row identifier | 001 |
| url_hash | str | MD5 of canonical URL (join key) | a3f8... |
| url | str | Full canonical URL after redirect | /blog/article-name |
| title | str | Page/content title | "How to..." |
| content_type | str | Blog, Product, Help, Legal, Gallery | Blog |
| author | str | Content owner (team or person) | jane.smith |
| date_published | date | ISO creation date | 2024-01-15 |
| date_modified | date | ISO last modification | 2024-06-20 |
| word_count | int | Approximate word count | 1500 |
| has_images | bool | Page value primarily visual? | false |
| age_days | int | Days since published (audit date - date_published) | 180 |

## Analytics Columns (join from GSC + GA4)

| Column | Type | Description |
|--------|------|-------------|
| gsc_clicks_90d | int | GSC clicks last 90 days |
| gsc_impressions_90d | int | GSC impressions last 90 days |
| ga4_sessions_90d | int | GA4 sessions last 90 days |
| ga4_bounce_rate | float | Bounce rate 0.0-1.0 |
| ga4_avg_time_s | int | Average time on page in seconds |

## Scoring Columns (LLM + human)

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| score_accuracy | float | Is content correct? | 1-5 |
| score_relevance | float | Do users need this? | 1-5 |
| score_quality | float | Is writing clear/complete? | 1-5 |
| score_overall | float | Average of three scores | 1-5 |
| scored_by | str | "llm-haiku" / "llm-opus" / "human" | — |
| score_model_version | str | Model ID used for scoring | claude-haiku-4-5 |

## Action Columns (final decisions)

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| action | str | Recommended action | keep / update / consolidate / remove |
| action_priority | str | Urgency | high / medium / low |
| action_owner | str | Person responsible | — |
| action_notes | str | Additional context | "Needs new screenshots" |
| human_reviewed | bool | Human sign-off on action? | false |
