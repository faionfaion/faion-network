# Solution Assessment

## Summary

**One-sentence:** A 4-stage solution evaluation that locks baselines pre-build, measures variance at 30/60/90 days, and produces an accept / remediate / reject recommendation backed by primary-source evidence.

**One-paragraph:** Solutions are built but value is rarely measured; complaints stay unstructured; the gap between promised and delivered is invisible. Solution assessment forces four staged evaluations — Design, Implementation, Deployment, Post-Implementation (30/60/90 days) — against pre-locked baselines. Each metric verdict cites an evidence URL with timestamp, requires statistical sample size, and triangulates two independent sources. Numeric variance bands (≥0% Met, -15..0% Partial, <-15% Not Met) make verdicts deterministic. Output: an assessment report with per-requirement compliance table, business-value section, deprecated-requirement flags, and a remediation backlog.

**Ефективно для:**

- 30/60/90-day post-launch checkpoints with quantified business case.
- Pre-go-live deployment readiness gates aggregating QA + ops + support + training + security.
- Phase-gate reviews on multi-quarter programs before next-phase funding.
- Vendor/SaaS contract renewal — solution-against-SLA evaluation.
- Compliance/audit cycles (SOX, ISO, HIPAA) requiring documented requirements-met evidence.

## Applies If (ALL must hold)

- the engagement has a signed business case with measurable outcomes
- a baseline measurement exists or can be reconstructed from primary sources
- an independent assessor (not the sponsor) is available to run the evaluation
- the solution has been in production for at least one assessment window (≥30 days for post-impl)

## Skip If (ANY kills it)

- throwaway prototypes or internal tools with ≤5 users — run a 15-minute retro instead
- pre-PMF startups where requirements change every sprint — use continuous discovery
- no baseline exists and cannot be reconstructed — variance is unmeasurable
- as a substitute for ongoing monitoring — one-shot reports are the antipattern
- assessor reports to the sponsor whose bonus depends on the result — independence violated
- pure technical performance tuning (latency, throughput) — use SRE/SLO frameworks

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| signed business case with quantified outcomes | PDF / wiki page | sponsor |
| requirements baseline with IDs | CSV / ALM export | BA team |
| primary-source data exports (analytics, finance, ticketing) | CSV / API | ops / finance / analytics |
| baseline-time query definitions | SQL / KQL | data-engineering |
| survey + adoption telemetry | CSV / dashboard | UX / analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-traceability-full-lifecycle]] | Provides the requirement-to-deliverable mapping the assessment scores. |
| [[scope-drift-early-warning-metrics]] | Drift signals indicate which requirements may be Deprecated by assessment time. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-stage cadence, primary-source evidence, sample-size guard, triangulation, deprecated vs not-met | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for assessment report: per-requirement compliance table, business-value rows, recommendation, remediation backlog | 900 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: missing baseline, survey-only sampling, one-shot cadence, vendor-marked, optimistic verdicts, ignored remediation | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: lock baselines → assess vs requirements → evaluate value → identify limitations → recommend | 700 |
| `content/05-examples.xml` | essential | Worked example: SaaS billing migration 90-day assessment with verdict + remediation backlog | 600 |
| `content/06-decision-tree.xml` | essential | Tree on baseline availability + independence + window age | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `baseline_lock_audit` | sonnet | Verify baselines are query-reproducible. |
| `per_requirement_verdict` | sonnet | Apply variance band to evidence per requirement. |
| `triangulation_check` | haiku | Mechanical two-source cross-check. |
| `recommendation_narrative` | opus | Cross-section synthesis; high stakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solution-assessment-report.md` | Markdown skeleton with all assessment-report sections. |
| `templates/requirement-compliance-table.csv` | Header row for per-requirement compliance table. |
| `templates/business-value-rows.csv` | Header row for business-value metric rows. |
| `templates/_smoke-test.md` | Minimum viable filled-in assessment. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solution-assessment.py` | Validates assessment report against the JSON Schema in 02-output-contract.xml. | Before report sign-off; pre-commit on the report repo. |

## Related

- [[requirements-traceability-full-lifecycle]]
- [[scope-drift-early-warning-metrics]]
- [[use-case-modeling]]
- [[strategy-analysis-future-state]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
