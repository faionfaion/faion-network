# Annual Planning Templates

## Summary

A set of fill-in-the-blank Markdown templates for the annual planning lifecycle: Annual Plan (vision, goals, strategic priorities, quarterly breakdown, budget, not-doing list), Quarterly Review (results vs goals, wins, misses, learnings, adjustments), Annual Review (executive summary, year-by-numbers, accomplishments, personal reflection), Monthly Plan (focus, metrics, weekly breakdown), OKR template (objective, key results with baseline and target, initiatives), and Year-in-Review. Templates are content scaffolds — strategy must come from the human; agents fill only what is grounded in provided data.

## Why

Planning templates enforce structural discipline: the "Not Doing This Year" section prevents scope creep, the OKR format with Current/Target fields forces measurability, the budget table pairs goals with resources. Without a template, LLM-generated plans drift into aspirational prose with no accountability mechanism. Templates also make quarterly amendments traceable (diff the doc) and force a personal-reflection pass that solo founders systematically skip.

## When To Use

- End-of-year planning cycle: produce annual plan, OKRs, quarterly breakdown, budget
- Quarterly/monthly review cycles: assemble results-vs-goals into standard format
- Generating a year-in-review artifact for personal reflection or stakeholder communication
- Scaffolding a planning document for a brainstorm session
- Aligning multiple workstreams onto shared OKRs with consistent format

## When NOT To Use

- Strategic ideation phase — templates assume strategy exists; for upstream brainstorming use faion-brainstorm
- Daily/weekly task management — overkill; use Linear/Asana/Notion native tooling
- Detailed financial modeling — use ops-financial-planning for scenarios and sensitivity analysis
- Crisis or pivot replanning — annual templates assume baseline stability
- Org-wide planning at more than 20 people — use PM-traditional or PM-agile methodologies

## Content

| File | What's inside |
|------|---------------|
| `content/01-template-guide.xml` | Template inventory, fill-order rules, required vs optional sections, OKR validation criteria |
| `content/02-agent-rules.xml` | Agent safety rules: no invented metrics, OKR activity-vs-outcome validator, "not doing" enforcement, privacy gate on year-in-review |

## Templates

| File | Purpose |
|------|---------|
| `templates/annual-plan.md` | Full annual plan: vision, theme, goals table, priorities, Q1-Q4 breakdown, budget, not-doing list, review schedule |
| `templates/quarterly-review.md` | Quarterly review: results vs goals, wins, misses, learnings, adjustments, next-quarter focus |
| `templates/annual-review.md` | Annual review: executive summary, year-by-numbers, accomplishments, challenges, personal reflection |
| `templates/monthly-plan.md` | Monthly plan: goal, metrics table, week-by-week breakdown, blockers |
| `templates/okr-template.md` | OKR template: objective + why + 3 key results with baseline/target + initiatives |
| `templates/year-in-review.md` | Year-in-review: wins, challenges, metrics summary, surprises, key takeaways |
| `templates/okr-validator.py` | OKR sanity check: flags activity KRs, missing numeric targets, missing baseline/target fields |
