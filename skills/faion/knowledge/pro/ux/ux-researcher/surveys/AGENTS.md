# Surveys and Questionnaires

## Summary

Structured data collection from many users through standardized questions that quantify attitudes, preferences, and experiences. Four survey types: satisfaction (CSAT, NPS), task-based (SUS, SEQ), preference (A vs B), and exploratory (usage patterns). Standard metrics require exact question wording and order — any deviation invalidates benchmarking against published norms.

## Why

Qualitative research (interviews, diary studies) reveals "why" but cannot generalize to the full user base. Surveys provide statistical confidence and enable tracking changes over time. NPS, SUS, and CSAT are industry-standard benchmarks; using the exact published wording lets you compare your product against 10,000+ published scores. Surveys are also the fastest way to triage: which segments are unhappy, which features matter most.

## When To Use

- Validating qualitative findings at scale after interviews or diary studies.
- Tracking standardized UX metrics over time: NPS, CSAT, SUS, SEQ, CES — quarterly cohorts vs baseline.
- Post-task micro-surveys (1-2 questions) embedded in product after key flows.
- Segmenting a large user base: screener surveys to recruit participants for deeper qualitative work.
- Quantifying feature value across the full user base.

## When NOT To Use

- "Why" questions — surveys give "what" and "how much"; interviews give "why".
- Sample below 100 — confidence intervals are too wide; do interviews instead.
- Highly emotional or sensitive topics — social desirability bias dominates self-report.
- Concept testing where artifact context matters — closed questions cannot substitute for showing the design.
- When results cannot drive action — running surveys you will ignore burns respondent trust permanently.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Survey types, when-to/not-to use, process steps from objective to analysis. |
| `content/02-standard-metrics.xml` | NPS, SUS, CSAT, SEQ: exact question wording, scoring formulas, benchmarks, when to use each. |
| `content/03-question-design.xml` | Question types, bias rules (leading, double-barreled, vague), good vs bad question examples, response-rate factors. |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-plan.md` | Survey planning template: objective, audience, sample size, questions with types, success metrics. |
| `templates/standard-survey.md` | Ready-to-use satisfaction + feature + open-ended survey with NPS, usability, and demographic questions. |
| `templates/nps-segments.py` | NPS calculation with per-segment cut (pandas); includes open-ended coding hook. |
