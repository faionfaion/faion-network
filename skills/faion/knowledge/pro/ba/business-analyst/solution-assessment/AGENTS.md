# Solution Assessment

## Summary

A structured evaluation of a solution's ability to meet the business need and deliver expected value. Covers four assessment types (design, implementation, deployment, post-implementation), compares actuals against requirements and success metrics, identifies limitations, and produces a recommendation (accept / accept with conditions / require changes / reject). Run at 30/60/90 days post-deployment, not as a one-shot event.

## Why

Solutions are built but value is never measured; user complaints are unstructured; the gap between promised and delivered remains invisible; lessons are not captured. Structured assessment forces a pre-agreed success baseline, makes variance visible, distinguishes "not met" from "deprecated requirement", and closes the delivery loop by feeding a remediation backlog.

## When To Use

- 30/60/90-day post-launch checkpoints when the business case promised quantified outcomes
- Pre-go-live deployment readiness gate: aggregate QA, ops, support, training, and security signals into a single accept/reject
- Phase-gate reviews on long programs (CRM, ERP, billing migrations) before funding the next phase
- Vendor/SaaS contract renewal — assess deployed solution against original requirements and SLA
- Compliance/audit cycles (SOX, ISO, HIPAA) requiring documented evaluation that requirements were met
- Post-incident assessment: was the failure a missed requirement, implementation gap, or unmeasured non-functional?

## When NOT To Use

- Throwaway prototypes or internal tools with 5 or fewer users — run a 15-minute retrospective instead
- Pre-PMF early-stage startups where requirements change every sprint — use continuous discovery
- When there is no baseline: without a measured "before", variance cannot be computed and the report is meaningless
- As a substitute for ongoing monitoring — a one-shot report that sits until the next audit is the canonical anti-pattern
- When the assessor reports to the project sponsor whose bonus depends on the result — independence is required
- Pure technical performance tuning (latency, throughput) — use SRE/SLO frameworks instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-assessment-types.xml` | Four assessment types, five success criteria categories, step-by-step process, timing triggers |
| `content/02-quality-rules.xml` | Evidence requirements, sample-size rules, variance thresholds for met/partial/not-met, common failure modes |
| `content/03-examples.xml` | CRM implementation assessment (requirements compliance + business value table), user feedback survey analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/solution-assessment-report.md` | Full assessment report: executive summary, requirements compliance table, business value table, user feedback, issues, limitations, recommendations |
| `templates/post-implementation-review.md` | Post-launch review: original business case vs. actual results, adoption metrics, issues log, lessons learned |
| `templates/variance.py` | Python script computing variance %, z-test p-value, and on-track/at-risk/off-track status for business metrics |
