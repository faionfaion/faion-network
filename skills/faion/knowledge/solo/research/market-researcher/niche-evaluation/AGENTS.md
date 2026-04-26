# Niche Evaluation

## Summary

Six-step framework to assess whether a market segment is viable: define the niche with a one-sentence
formula, estimate TAM/SAM/SOM with cited sources, map competitors on a quality-vs-players matrix,
score audience accessibility, evaluate monetization potential, and rate personal fit. Produces a
weighted score (0-5) with a decision band; final go/no-go is always human.

## Why

Solopreneurs pick niches too broad (competing with giants) or too small (no revenue) based on gut
feeling. The two-phase evidence-before-score discipline — gather citations first, score only from
evidence — prevents the #1 agent failure: hallucinated TAM/SAM numbers. Personal fit is the only
criterion that cannot be delegated to an agent; any niche with founder fit below 3 fails regardless
of score.

## When To Use

- After `idea-generation` produces 5-10 candidate niches; need to score and short-list.
- Pivoting: benchmarking new candidate against current niche performance.
- Product-line expansion: evaluating adjacent niche for second product.
- Investor/board ask requiring defensible market-sizing with cited sources.

## When NOT To Use

- Already shipping with paying customers — churn data beats any scoring model.
- Pure curiosity research — the framework is decision-forcing, not exploratory.
- Hyper-local services (plumber, dentist) — catchment-area metrics apply, not TAM/SAM/SOM.

## Content

| File | What's inside |
|------|---------------|
| `content/01-definition-and-market.xml` | Niche definition formula, TAM/SAM/SOM calculation, validation signals (Trends, keyword volume). |
| `content/02-competition-and-access.xml` | Competitor quality-vs-players matrix, audience accessibility scoring, long-tail competitor scan. |
| `content/03-scoring.xml` | Weighted scoring formula, decision thresholds, personal-fit override rule, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/niche-scorecard.md` | Full Niche Evaluation Scorecard with all 5 criteria, source columns, and decision block. |
| `templates/prompt-niche-research.txt` | Phase-1 evidence-gathering agent prompt (no scoring; citations required). |
| `templates/prompt-niche-score.txt` | Phase-2 scoring agent prompt (evidence-only, refuse-without-source rule). |
