# Surveys and Questionnaires

## Summary

A research method for collecting structured data from large user populations through standardized
questions — covering satisfaction (NPS, CSAT, SUS), task ease (SEQ), and feature preference —
to quantify user attitudes and validate qualitative findings at scale.

## Why

Qualitative research (interviews, diary studies) produces rich insight but cannot generalize
across a user base. Surveys close that gap by reaching N≥100 with standardized instruments
whose benchmarks are well-established (SUS average=68, NPS range −100 to +100). Without
surveys, product teams rely on the loudest voices and cannot segment findings by user type
or measure change over time.

## When To Use

- Quantitative validation of qualitative findings at N≥100.
- Tracking standard UX metrics over time: NPS, SUS, CSAT, SEQ.
- Segmenting users (new vs. power, free vs. paid) to measure satisfaction or feature value.
- Pre/post launch comparison of perceived ease, trust, or feature impact.

## When NOT To Use

- You do not yet know which questions to ask — run interviews first; an ill-formed survey produces noise.
- Sample &lt;30 — descriptive statistics are unreliable; use qualitative methods instead.
- You need behavioral data (clicks, time on task) — analytics or usability tests, not self-report.
- High-stakes decisions where social-desirability bias dominates (e.g., willingness-to-pay overestimated 2-4x by surveys).

## Content

| File | What's inside |
|------|---------------|
| `content/01-types-and-process.xml` | Survey types, six-step design process, question types, standard UX metrics (NPS, SUS, CSAT, SEQ). |
| `content/02-rules.xml` | Question quality rules, response-rate factors, analysis guidance, agent-specific gotchas. |
| `content/03-examples.xml` | Good and bad question examples with antipattern explanations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-plan.md` | Survey plan: objective, audience, sample size, question list, success metrics. |
| `templates/survey_metrics.py` | Deterministic NPS and SUS calculator from CSV; run as code, not LLM. |
