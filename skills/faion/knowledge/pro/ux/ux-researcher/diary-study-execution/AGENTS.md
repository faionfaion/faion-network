# Diary Study Execution and Analysis

## Summary

The operational and analytical phase of a running diary study: monitoring participant compliance, detecting low-quality entries, managing drop-off, coding entries against a fixed codebook, computing temporal patterns, and synthesizing findings into a structured report. Lock the codebook before coding begins; adding themes mid-study invalidates cross-participant comparison.

## Why

Diary data is messy by nature: photos, voice notes, free text, sparse entries, copy-paste repetition, emotional venting. Without systematic quality monitoring and a coded pipeline, the expensive longitudinal data collapses into anecdote. Rolling synthesis from day 3 onward (not batch at end) allows follow-up probes while participants are still active.

## When To Use

- Multi-day diary study is already running and entries (text, photo, voice) are flowing into a single store.
- Cross-participant thematic and temporal coding of more than 50 entries with quote extraction and timeline charts.
- Mid-study quality monitoring: flag low-engagement participants, generic copy-paste entries, missed days.
- Producing the final report from already-coded data.

## When NOT To Use

- Recruitment, screening, or onboarding calls — these require human trust and cannot be delegated to agents.
- Real-time participant chat or probing follow-up DMs while study is live (PII handling, emotional sensitivity).
- Studies where entries are voice-only without transcription pipeline or photos without vision/OCR — no usable text signal.
- Fewer than 5 participants — a human reads everything end-to-end faster than setting up the pipeline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-execution.xml` | Monitoring steps, entry quality checks, bias types and mitigations, participant engagement and drop-off strategies. |
| `content/02-analysis.xml` | Codebook requirements, coding pass rules, thematic/temporal/contextual analysis, quantitative metrics, report structure. |
| `content/03-antipatterns.xml` | Common analysis failures: cherry-picking, ignoring outliers, losing context, over-quantifying, confirmation bias. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthesis.md` | Analysis output skeleton: participation summary, theme blocks with verbatim quotes, temporal patterns, recommendations. |
| `templates/qa-monitor.sh` | Bash script flagging participants below 60% completion and suspected copy-paste entries. |
