# Idea Generation Methods

## Summary

A bundle of four complementary pre-validation methods for solopreneur idea discovery: the 7P
framework (Pain/Passion/Profession/Process/Platform/People/Product), Paul Graham's four diagnostic
questions, systematic pain-point mining (complaint audit + workaround inventory), and a 5-dimension
niche scoring matrix. Output: 3 prioritized candidate niches for downstream validation.

## Why

Self-generated ideas without structure over-index on personal bias, generic startup tropes, and
currently trending topics. The 7P + PG + pain-audit sequence forces divergence from multiple angles;
the scoring matrix filters to highest-signal candidates without hallucinated market data. Running
all four in sequence takes more time but produces substantially less mode-collapsed output than a
single brainstorm.

## When To Use

- Earliest exploratory stage: founder with no concrete product target.
- After a project shutdown or pivot — regenerating a fresh idea pool grounded in current pains.
- Periodic side-project ideation: refilling the funnel (idea → niche-evaluation → problem-validation).
- Structured diverge phase before using `faion-brainstorm` skill.

## When NOT To Use

- After committing to a niche — switch to feature-discovery and problem-validation.
- For agency/consulting work where the idea is set by the client.
- For incremental optimization on an existing product — wrong scope.
- When founder cannot dedicate a week to ideation and follow-up; one-shot brainstorms decay.

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | 7P method, PG questions, pain-point mining techniques with scoring weights. |
| `content/02-scoring.xml` | 5-dimension niche scorecard, decision thresholds, fabrication risk rules. |
| `content/03-gotchas.xml` | Mode-collapse antipatterns, agent bias patterns, human-in-loop checkpoints. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ideation-worksheet.md` | Per-P idea capture + scoring rows, top-3 section. |
| `templates/pain-log.md` | Complaint audit table: date/complaint/category/frequency/intensity. |
| `templates/scoring-matrix.md` | 5-dimension scoring matrix with decision band table. |
| `templates/prompt-diverge.txt` | Divergent-ideation agent prompt (7P + PG, JSON output, high-temperature instructions). |
| `templates/prompt-score.txt` | Convergence-scorer agent prompt with missing-data flag requirement. |
