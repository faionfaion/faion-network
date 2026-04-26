# Feature Discovery

## Summary

A methodology for identifying, prioritizing, and validating product features before committing engineering effort. The core rule: collect feature signals from 4 sources (customer research, usage analytics, competitive analysis, market trends), classify each using the Kano model, score top candidates with RICE (Reach × Impact × Confidence / Effort), and validate the top-3 with a fake-door or prototype test before building.

## Why

Feature decisions based on loudest-customer requests or competitor copying lead to bloat, unused code, and missed adoption drivers. RICE scoring makes trade-offs explicit and defensible. Kano classification prevents conflating must-have fixes with excitement features. Validating before building eliminates the most common cause of wasted engineering cycles.

## When To Use

- Pre-roadmap planning when the feature backlog has more than ~30 candidates.
- After a noticeable churn or activation drop, to decide between fixing flows and adding capability.
- When stakeholders push competing feature requests and you need a defensible ranking.
- When validating a new feature idea before committing engineering.

## When NOT To Use

- Pre-PMF: run problem-validation first; there is no stable user base to score Reach against.
- Single-feature decisions where the cost of running RICE exceeds the cost of just building.
- Fewer than 5 features in scope — prioritization overhead exceeds value.
- Telemetry is missing — RICE on guessed Reach is theatrical.

## Content

| File | What's inside |
|------|---------------|
| `content/01-sources-and-categorization.xml` | Feature signal sources (4 types), Kano model with quadrant descriptions, Opportunity Scoring (ODI) formula. |
| `content/02-rice-and-validation.xml` | RICE scoring formula, effort sizing table, validation methods with effort/confidence trade-offs, and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-discovery-board.md` | Quarter-level discovery board: active collection sources, feature ideas table, Kano classification, RICE scores, validation plan. |
| `templates/feature-request-log.md` | Per-feature log: metadata, problem statement, impact assessment, validation checkboxes, decision + reasoning. |
| `templates/rice-scorer.py` | Python script: reads CSV of features with Reach/Impact/Confidence/Effort, outputs sorted RICE scores. |
