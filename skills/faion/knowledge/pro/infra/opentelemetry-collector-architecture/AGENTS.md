---
slug: opentelemetry-collector-architecture
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Architecture spec for OTel Collector deployment: agent vs gateway tier, receivers/processors/exporters pipeline, batching + retry, mTLS, capacity sizing.
content_id: "4ba70d765be10e4e"
complexity: deep
produces: spec
est_tokens: 4300
tags: [opentelemetry, otel, collector, architecture, infra]
---
# OpenTelemetry Collector Architecture

## Summary

**One-sentence:** Architecture spec for OTel Collector deployment: agent vs gateway tier, receivers/processors/exporters pipeline, batching + retry, mTLS, capacity sizing.

**One-paragraph:** Architecture spec for OTel Collector deployment: agent vs gateway tier, receivers/processors/exporters pipeline, batching + retry, mTLS, capacity sizing. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- 100+ сервісів випускають OTel — без gateway tier upstream вендор тоне в RPS.
- Потрібно >=2 експортерів (metrics → Prom, traces → Tempo, logs → S3) з різними тарифами.
- Безпекова політика вимагає mTLS між agent і gateway — інакше трафік просто заблокують.
- Capacity planning: треба знати скільки RAM / CPU дає collector на 10k spans/sec.

## Applies If (ALL must hold)

- Team is deploying OTel Collector at scale (>=100 services)
- Architecture must decide agent-only vs agent+gateway tier
- Multiple exporters needed (Prometheus + Tempo + S3 / Datadog)
- Network/security constraints require mTLS between tiers

## Skip If (ANY kills it)

- Team uses a vendor agent (Datadog Agent, Splunk UF) — collector not in scope
- Single-service deployment with no aggregation — direct SDK export is fine
- Instrumentation strategy still being chosen — use opentelemetry-instrumentation-playbook first

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
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
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
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-opentelemetry-collector-architecture.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the team deploying OTel Collector at >=100 services with multiple exporters + mTLS?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
