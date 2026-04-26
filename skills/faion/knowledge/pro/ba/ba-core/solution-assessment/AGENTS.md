# Solution Assessment

## Summary

Evaluates a solution's ability to meet the business need and deliver expected value across four assessment types: design, implementation, deployment, and post-implementation. Structured five-step framework: define criteria → assess vs requirements → evaluate business value → identify limitations → recommend action.

## Why

Solutions are built but value is not measured. Without structured assessment, the gap between promised and delivered value remains invisible, lessons are not captured, and expensive rework repeats on the next initiative. BABOK Solution Evaluation (KA-6) requires a written limitation register and formal accept/reject recommendation even when the solution is "fine."

## When To Use

- Stage-gate of the BABOK Solution Evaluation knowledge area: "does the solution deliver enterprise value?" against the original business need.
- Design and implementation assessments inside the build phase ("are we still on the right path?").
- Pre go-live deployment readiness review where multiple workstreams must produce one accept/reject row.
- 30/90/365-day post-implementation reviews scoring requirements compliance and benefit realization.
- Solution limitations capture for compliance, audit, or vendor-renewal files.
- Lessons-learned input to the next iteration's strategy analysis (current state → future state).

## When NOT To Use

- Continuous-discovery pre-PMF work where requirements are still being invented every sprint — "REQ-001 met" is meaningless when REQ-001 was wrong.
- Throwaway prototypes, spikes, internal tools used by a handful of people — a 15-minute retro replaces the whole template.
- Pure SRE/platform tuning (latency, cost, capacity) — use SLOs and error budgets.
- When no baseline exists — without a measured "before," the variance column is vibes; back-fill the baseline first.
- When the assessor reports to the project sponsor whose bonus depends on the result — route to an independent reviewer.

## Content

| File | What's inside |
|------|---------------|
| `content/01-assessment-framework.xml` | Four assessment types, five-step framework, assessment criteria categories, when-to-assess triggers. |
| `content/02-assessment-antipatterns.xml` | Common failure modes: no baseline, requirements drift, variance as causation, adoption vs value confusion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solution-assessment-report.md` | Full assessment report with requirements compliance, business value, user feedback, and recommendations. |
| `templates/post-implementation-review.md` | Post-go-live review template covering outcomes, adoption metrics, lessons learned. |
