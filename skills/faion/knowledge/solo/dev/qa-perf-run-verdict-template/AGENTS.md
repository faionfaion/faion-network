---
slug: qa-perf-run-verdict-template
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Records a perf run verdict: baseline + current p50/p95/p99, error rate, sample size, environment, and a binary pass/fail against pre-declared SLOs.
content_id: "f387d7bb35f2c0d1"
complexity: medium
produces: report
est_tokens: 5000
tags: [qa, performance, verdict, p95, regression]
---
# QA Performance Run Verdict Template

## Summary

**One-sentence:** Records a perf run verdict: baseline + current p50/p95/p99, error rate, sample size, environment, and a binary pass/fail against pre-declared SLOs.

**One-paragraph:** Records a perf run verdict: baseline + current p50/p95/p99, error rate, sample size, environment, and a binary pass/fail against pre-declared SLOs. Verdict is binary, anchored on pre-declared SLOs. Includes baseline ref, sample size sanity, environment fingerprint, and a release-decision recommendation. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Release candidate has a perf gate before promotion.
- Team has historical baselines and an SLO definition per critical path.
- Need a reviewable artefact to attach to the release ticket.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Release candidate has a perf gate before promotion.
- Team has historical baselines and an SLO definition per critical path.
- Need a reviewable artefact to attach to the release ticket.

## Skip If (ANY kills it)

- No SLOs defined yet — write SLOs first (see perf-test-basics).
- Pre-MVP product with no users — perf gating is premature.
- Internal tool used by one team where slowness is tolerable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Perf run results | k6/locust JSON | perf CI |
| Baseline metrics | JSON | previous green run |
| SLO definition | YAML | ops/slo.yaml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[perf-test-basics]] | Underlying perf-test methodology. |
| [[qa-rollback-trigger-canon]] | Rollback triggers consume this verdict. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diff-baselines` | haiku | Mechanical: percentile diffs vs baseline. |
| `apply-slo` | sonnet | Binary pass/fail per SLO. |
| `draft-recommendation` | sonnet | Release/hold/rollback recommendation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verdict.json` | JSON template scaffolding the artefact contract. |
| `templates/slo.yaml` | YAML configuration scaffolding the artefact. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-perf-run-verdict-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[perf-test-basics]]
- [[perf-test-tools]]
- [[qa-rollback-trigger-canon]]
- [[qa-rc-smoke-pack-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a perf gate with declared SLOs blocking release promotion?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
