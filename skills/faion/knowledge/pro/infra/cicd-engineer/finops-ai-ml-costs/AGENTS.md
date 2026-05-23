---
slug: finops-ai-ml-costs
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an AI/ML cost-control config (GPU spot strategy with checkpointing + inference caching + quantization + batch policy + per-run/per-request attribution) for training and inference.
content_id: "29089542f8586f2a"
complexity: deep
produces: config
est_tokens: 4300
tags: [finops, ai-costs, gpu-optimization, inference-caching, ml-cost-tracking]
---
# FinOps for AI / ML Workloads

## Summary

**One-sentence:** Generates an AI/ML cost-control config (GPU spot strategy with checkpointing + inference caching + quantization + batch policy + per-run/per-request attribution) for training and inference.

**One-paragraph:** Generates an AI/ML cost-control config (GPU spot strategy with checkpointing + inference caching + quantization + batch policy + per-run/per-request attribution) for training and inference. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- GPU training pipelines з runtime ≥1h і checkpointable jobs.
- Inference fleet з cacheable prompts (RAG, classification, embeddings).
- Multi-tenant ML platforms де per-team chargeback потрібен.
- Pre-deployment review нового model: cost-per-prediction must clear ROI gate.

## Applies If (ALL must hold)

- GPU spend ≥$5k/month OR cloud LLM inference spend ≥$2k/month.
- Training jobs support checkpoint/resume.
- Per-team or per-product attribution required by finance.
- Inference traffic has measurable repeat-input rate (≥10%) to justify caching.

## Skip If (ANY kills it)

- GPU spend <$2k/month — vendor pricing optimization gives bigger ROI than spot.
- Training jobs cannot checkpoint (research scripts in flux) — spot is unsafe.
- Latency-critical inference (<100ms P99) — caching may add coherence drift unacceptably.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Training-run telemetry | JSON Lines (job_id, gpu_hours, cost) | ML Platform |
| Inference traffic profile | histogram of input hashes | ML Platform |
| Spot interruption history | CSV from CSP | Cloud Platform |
| Model registry | JSON (model → variant → cost-per-token) | ML Eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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
| `draft-finops-ai-ml-costs` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-ai-ml-costs.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
