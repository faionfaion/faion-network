# Tree Testing

## Summary

Tree testing evaluates the findability of topics in a website's hierarchy by having participants navigate a text-only version of the site structure (no design, no content) to locate answers to scenario tasks. Key metrics are success rate, directness, and first-click correctness. Requires 30-50 participants for statistical confidence and 10-15 tasks covering shallow and deep destinations.

## Why

Navigation problems found after build are expensive to fix; tree testing surfaces them before any visual work. First-click data is the most actionable signal: if first-click-correct is low even when overall success is acceptable, the IA feels wrong to users even when they eventually find the answer. Running a task leak-check (does scenario text contain the destination label?) is mandatory — LLM-generated tasks routinely leak the answer.

## When To Use

- Validating a proposed IA before visual design or build begins.
- Comparing two candidate IAs head-to-head with the same task set.
- Post-card-sort validation: test that users can navigate the structure card sorting produced.
- Pre-redesign baselining: measure findability on current site vs proposed site to quantify lift.

## When NOT To Use

- IA does not yet exist — run a card sort first.
- Testing visual labels, CTAs, or filtering UI — use first-click testing or full usability testing.
- Sites where &gt;50% of traffic enters via search — navigation findability is a weaker signal.
- Single-page apps without hierarchical navigation — there is no tree to test.

## Content

| File | What's inside |
|------|---------------|
| `content/01-methodology.xml` | What tree testing is, key metrics (success, directness, first-click), tree structure rules, task writing rules. |
| `content/02-process.xml` | Six-step process: create tree, write tasks, define answers, run test, analyze, iterate. Success rate interpretation thresholds. |
| `content/03-antipatterns.xml` | Task leak patterns, synthetic LLM participants, aggregation pitfalls, CSV schema differences across tools. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.md` | Tree test plan: objectives, tree structure, task table with correct answers, participant criteria, success criteria. |
| `templates/results-report.md` | Results report: executive summary, per-task path analysis, first-click table, problem areas, recommendations. |
| `templates/metrics-parser.py` | Python script: compute success rate, directness, first-click-correct from Treejack CSV export. |
