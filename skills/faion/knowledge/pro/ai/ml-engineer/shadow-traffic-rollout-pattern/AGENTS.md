---
slug: shadow-traffic-rollout-pattern
tier: pro
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Mirrors production traffic to a candidate model/prompt in parallel (no user-facing impact), captures per-request diff vs baseline, blocks promotion until joint quality + latency + cost gates stay within named thresholds across a representative window.
content_id: "ce7003f72c2a4527"
complexity: deep
produces: config
est_tokens: 5500
tags: [ai, rollout, shadow-traffic, ml-ops, deployment]
---
# Shadow Traffic Rollout Pattern

## Summary

**One-sentence:** Mirrors production traffic to a candidate model/prompt in parallel (no user-facing impact), captures per-request diff vs baseline, blocks promotion until joint quality + latency + cost gates stay within named thresholds across a representative window.

**One-paragraph:** Mirrors production traffic to a candidate model/prompt in parallel (no user-facing impact), captures per-request diff vs baseline, blocks promotion until joint quality + latency + cost gates stay within named thresholds across a representative window. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Model swap (e.g. Sonnet → Opus) — потрібно перевірити divergence перед промо.
- Prompt-template зміна на критичному шляху (refunds, KYC, support).
- Latency-sensitive flows: candidate може повільніший — shadow вимірює перед rollout.
- Cost-sensitive flows: candidate може дорожчий — shadow рахує реальний bill.

## Applies If (ALL must hold)

- Production-mirror infra exists (request fan-out, no user impact).
- Judge model calibrated against ≥50 expert-labelled samples within 30 days.
- Baseline + candidate are independently identified (model id, prompt version).
- Traffic volume supports ≥500 scored requests in 48h.

## Skip If (ANY kills it)

- No production-mirror infra available — methodology can't execute.
- Candidate is config-only (region, retry policy) with no behavior delta.
- No judge calibration exists and cannot be produced.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baseline model id + prompt version | string / semver | Repo / config |
| Candidate model id + prompt version | string / semver | Repo / config |
| Judge config (model + prompt + calibration date) | YAML | ML eng team |
| Mirror infra config | Kubernetes manifest / fan-out config | Infra team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-shadow-traffic-rollout-pattern` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadow-traffic-rollout-pattern.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[model-upgrade-migration-playbook]]
- [[golden-set-curation-and-maintenance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
