# Survey Design

## Summary

Survey design is the methodology for creating quantitative research instruments that yield valid, actionable data. The core rule: conduct at least 10 interviews before building a survey — surveys quantify known patterns, they cannot discover unknown problems. Every question must be specific, single-concept, and neutrally worded; surveys fail when they ask hypotheticals instead of facts or exceed 7 minutes in length.

## Why

Surveys without methodology training produce misleading data. Leading questions bias responses, double-barreled items confuse respondents, hypothetical questions over-predict intent by 2-5x, and self-selection on distribution channels distorts the sample. Systematic design eliminates these failure modes before fielding.

## When To Use

- After 10+ qualitative interviews have surfaced patterns worth quantifying
- Pricing sensitivity studies (Van Westendorp, Gabor-Granger) where N >= 100 is realistic
- Feature prioritization across an installed user base (MaxDiff, Kano, importance/satisfaction matrix)
- Periodic NPS/CSAT tracking against a stable cohort
- Screener-driven recruitment funnels for follow-up interviews

## When NOT To Use

- Discovery of unknown problems — interviews and observation reveal what surveys cannot ask about
- Sample sizes below ~30 — stick to interviews; quantitative claims are not defensible
- Predicting future behavior ("would you pay X?") — use price-anchored conjoint or pre-orders
- B2B segments where the named buyer is gated — 1:1 outreach beats panel surveys
- Internal stakeholder alignment — use a workshop, not a survey

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-process.xml` | Six-step survey design process: objective, question types, writing rules, structure, testing, analysis |
| `content/02-rules-and-antipatterns.xml` | Concrete question-writing rules, common mistakes, and AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-design-doc.md` | Full survey design document template with objective, screener, core questions, demographics, and distribution plan |
| `templates/question-bank.md` | Per-research-type question banks: pricing (Van Westendorp), satisfaction (NPS/matrix), feature prioritization (MaxDiff) |
| `templates/bias-linter.py` | Python pre-filter that detects leading, hypothetical, absolutist, and double-barrel questions before LLM review |
