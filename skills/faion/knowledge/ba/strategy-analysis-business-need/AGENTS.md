# Strategy Analysis — Business Need

## Summary

**One-sentence:** A pre-solution artefact pinning the business problem, evidence, success metric, and do-nothing baseline so downstream solutioning stays anchored to value.

**One-paragraph:** Initiatives drift into solutioning before the problem is named; everyone agrees on the solution, no one agrees on the problem. This methodology produces a business-need spec with: (1) problem statement with named affected stakeholders, (2) primary-source evidence (data, quote, ticket), (3) one quantified success metric, (4) do-nothing baseline, (5) named owner. It is the input to `strategy-analysis-future-state` and `strategy-analysis-gap-analysis`.

**Ефективно для:**

- Pre-kickoff discovery before any RFP / vendor brief.
- Stalled initiatives where 'why are we doing this' is contested.
- Funding requests demanding outcome-driven framing.
- Annual planning cycles with bottom-up proposal review.

## Applies If (ALL must hold)

- no business-need artefact exists yet for the initiative
- a named sponsor exists and is reachable
- primary-source evidence (data, tickets, interview notes) is accessible
- the initiative is not yet in build phase

## Skip If (ANY kills it)

- a current (≤90-day) business-need artefact already exists — refresh it instead
- the initiative is purely compliance-mandated with a fixed scope — go to requirements
- no sponsor — block until one is named

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| initiative trigger (RFP, complaint, OKR) | email / wiki | sponsor |
| primary-source evidence | data export / interview notes / tickets | BA / analyst |
| named sponsor | org chart | executive |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | — |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named problem owner, evidence-cited claims, single quantified success metric, do-nothing baseline, no solution language | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for business-need spec: problem, stakeholders, evidence, metric, baseline, sponsor | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: solution-first framing, anonymous problem, unmeasured metric, sponsorless artefact, baseline missing | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure: capture trigger → gather evidence → quantify metric → document baseline + sponsor sign-off | 600 |
| `content/05-examples.xml` | essential | Worked example: customer-support backlog reduction business-need spec | 500 |
| `content/06-decision-tree.xml` | essential | Tree on sponsor + evidence + existing artefact age | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `evidence_triangulation` | sonnet | Cross-check 2 independent evidence sources. |
| `metric_quantification` | sonnet | Convert qualitative pain into a numeric metric. |
| `baseline_capture` | haiku | Mechanical query of the do-nothing baseline. |
| `spec_assembly` | sonnet | Light judgment compiling the spec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-need-spec.md` | Markdown skeleton with problem/evidence/metric/baseline/sponsor. |
| `templates/evidence-log.csv` | Header for evidence sources with type + retrieved_at. |
| `templates/_smoke-test.md` | Minimum viable business-need spec. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis-business-need.py` | Validates business-need spec against the JSON Schema. | Before sponsor sign-off; pre-commit. |

## Related

- [[strategy-analysis-current-state]]
- [[strategy-analysis-future-state]]
- [[strategy-analysis-gap-analysis]]
- [[stakeholder-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
