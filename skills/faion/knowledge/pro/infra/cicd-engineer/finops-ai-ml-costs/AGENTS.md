---
slug: finops-ai-ml-costs
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI/ML workloads present unique FinOps challenges: GPU costs run 5-10x higher than standard compute, token economics are invisible to instance-hour dashboards, and standard rightsizing heuristics (CPU utilization) are misleading for GPU workloads.
content_id: "2feab88045f36f0a"
tags: [finops, ai-costs, gpu-optimization, inference-caching, ml-cost-tracking]
---
# FinOps for AI/ML Workloads: GPU, Training, and Inference Costs

## Summary

**One-sentence:** AI/ML workloads present unique FinOps challenges: GPU costs run 5-10x higher than standard compute, token economics are invisible to instance-hour dashboards, and standard rightsizing heuristics (CPU utilization) are misleading for GPU workloads.

**One-paragraph:** AI/ML workloads present unique FinOps challenges: GPU costs run 5-10x higher than standard compute, token economics are invisible to instance-hour dashboards, and standard rightsizing heuristics (CPU utilization) are misleading for GPU workloads. This methodology covers training cost optimization via spot instances with checkpointing, inference cost reduction via caching and quantization, and cost tracking at the request and experiment level.

## Applies If (ALL must hold)

- Any AI/ML workload with GPU instances — standard rightsizing is not applicable.
- Training costs exceeding $10k/month — spot + checkpointing pays back immediately.
- Inference serving with repetitive queries — response caching provides 20-60% cost reduction.
- Monthly AI spend opaque (reported as instance-hours, not per-request costs).
- LLM API spend growing with no per-model or per-experiment tracking.

## Skip If (ANY kills it)

- Standard CPU-only workloads — apply general rightsizing and commitment discount methodology instead.
- Real-time inference with strict SLA (sub-100ms) where caching adds latency complexity.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
