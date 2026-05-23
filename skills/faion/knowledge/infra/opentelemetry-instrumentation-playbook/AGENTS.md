# OpenTelemetry Instrumentation Playbook

## Summary

**One-sentence:** Step-by-step instrumentation playbook: auto-instrumentation vs manual, semantic-convention tags, trace context propagation, sampling, baggage, PII scrubbing.

**One-paragraph:** Step-by-step instrumentation playbook: auto-instrumentation vs manual, semantic-convention tags, trace context propagation, sampling, baggage, PII scrubbing. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Сервіс - candidate на auto-instrumentation (Python/Go/Java/Node) — треба правильна послідовність.
- Trace context зникає між сервісами — propagation тестується тільки в production.
- HTTP body містить PII (email, токени) — треба scrubbing до експорту.
- Метрика 'spans per second per service' відома; треба обрати sampling % щоб не вибити бюджет.

## Applies If (ALL must hold)

- Service is a candidate for OTel SDK instrumentation (auto or manual)
- Trace context must propagate across at least one network hop
- PII risk exists (HTTP body, query params) and must be scrubbed before export
- Sampling decisions needed (head-based vs tail-based) to control cost

## Skip If (ANY kills it)

- Service is already fully instrumented and stable — no work needed
- Service uses a vendor-only SDK (Datadog, New Relic) — no OTel migration planned
- Team blocked by collector architecture — resolve opentelemetry-collector-architecture first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step.md` | working skeleton matching the `produces=playbook-step` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-opentelemetry-instrumentation-playbook.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the team instrumenting a service with OTel where context propagation + PII scrubbing + sampling matter?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
