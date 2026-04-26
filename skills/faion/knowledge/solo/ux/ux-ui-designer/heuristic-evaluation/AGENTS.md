# Heuristic Evaluation

## Summary

A structured usability inspection method where 3-5 evaluators independently review an interface against Nielsen's 10 heuristics and rate each issue on a 0-4 severity scale (0=not a problem, 4=catastrophic). Evaluators work independently first, then findings are compiled and deduplicated. One pass per heuristic yields ~3x more findings than a single omnibus pass. Severity 4 blocks release; severity 3 is sprint-level; severity 1-2 goes to polish backlog.

## Why

Full usability testing is expensive and time-consuming. Heuristic evaluation finds obvious violations at near-zero cost — 3-5 evaluators catch ~75% of issues vs ~35% for one evaluator. Expert review before user testing ensures test sessions surface real user struggles, not violations any UX professional would catch. The method also serves as a forcing function for design documentation: evaluators need to know intended behavior to judge violations.

## When To Use

- Before a usability test — eliminate obvious violations so testing resources address real user behavior
- When no user research budget is available — gives actionable findings at near-zero cost
- After a design sprint or major redesign — rapid expert review before development handoff
- Code review for UI components — catching violations in PRs prevents regressions
- Competitive analysis: apply the same heuristics to competitors to score relative quality

## When NOT To Use

- As a replacement for usability testing — finds expert-visible violations, not real user struggles with domain tasks
- After launch as the sole quality gate — too late for design changes; use for iterative improvements
- When quantitative data is needed to justify decisions — heuristic evaluation produces qualitative expert opinions
- On expert-user products where violations are worked around via muscle memory — disrupting their efficiency is worse

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step process, Nielsen's 10 heuristics with core question per heuristic, evaluator selection rationale, severity scale (0-4) |
| `content/02-examples.xml` | Example findings with location/heuristic/severity/recommendation, severity rating examples, heuristic evaluation vs usability testing comparison |

## Templates

| File | Purpose |
|------|---------|
| `templates/evaluation-form.md` | Per-evaluator form: scope, findings (location/heuristic/problem/severity/recommendation), summary table |
| `templates/compiled-report.md` | Compiled report: executive summary, methodology, findings by severity (4→1), findings by heuristic, statistics, recommendations |
| `templates/heuristic-precheck.sh` | Bash script: automated pre-check with axe-core + Lighthouse covering heuristics #1, #4, #5, #9 |
