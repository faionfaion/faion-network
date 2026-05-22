---
slug: guardrails-basics
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a 4-layer defense-in-depth guardrails spec — regex pre-filter, length cap, output schema, LLM classifier last — with per-layer latency budget and order constraint.
content_id: "f22c1a9df438682d"
complexity: light
produces: spec
est_tokens: 2700
tags: [guardrails, safety, defense-in-depth, pii, prompt-injection]
---
# Guardrails Basics

## Summary

**One-sentence:** Produces a 4-layer defense-in-depth guardrails spec — regex pre-filter, length cap, output schema, LLM classifier last — with per-layer latency budget and order constraint.

**One-paragraph:** No single guardrail check holds against adversarial inputs. The minimum-viable shape is layered: (1) regex pre-filter for known PII / token patterns, microsecond cost; (2) length cap on inputs and outputs, microsecond cost; (3) output schema validation, sub-millisecond; (4) LLM classifier (last) for semantic checks, 300-800ms. Order matters — cheap deterministic checks reject 80% of bad inputs without paying the classifier cost. Track per-layer block rates in a dashboard; one layer accounting for 100% of blocks is a sign the others are misconfigured.

**Ефективно для:** customer-facing chat, regulated content pipelines, multi-tenant agents, output-validation gates.

## Applies If (ALL must hold)

- Application accepts untrusted user input OR produces public-facing output.
- Latency budget allows up to 1s of guardrail overhead.
- A named owner can maintain regex patterns + classifier prompt + threshold.
- A telemetry sink records per-layer block events.

## Skip If (ANY kills it)

- Internal-only tool with no external input.
- Prototype / demo — guardrails added before production, not before pitch.
- Output format only — use structured output (response_schema / tool_choice) instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of policy categories | doc | safety policy |
| Sample bad-input fixtures | JSONL | red team / eval |
| Classifier model + prompt | string | prompt repo |
| Telemetry sink | URL | observability |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[guardrails-implementation]]` | Sibling for advanced patterns (NeMo Guardrails, semantic router). |
| `[[ai-failure-mode-taxonomy]]` | Naming categories the guardrails defend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: layered, cheap-first order, per-layer block-rate dashboard, classifier last, fail-closed default | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for guardrails-spec.json: layers, thresholds, latency budget | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: single-layer, classifier-first, no telemetry, no fail-closed, classifier-as-detector-only | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "untrusted input or public output?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Author regex patterns | sonnet | Pattern matching. |
| Author classifier prompt | opus | Adversarial wording. |
| Tune thresholds | sonnet | A/B from telemetry. |

## Templates

| File | Purpose |
|---|---|
| `templates/input-guardrails.py` | Layer-1 regex/PII/length pre-filter + prompt-injection detector. |
| `templates/layered-check.py` | Ordered 4-layer runner returning a structured dict. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-guardrails-basics.py` | Validates guardrails-spec.json: ≥4 layers, classifier is last, fail_closed default true. | Pre-commit on spec. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[guardrails-implementation]]`
- `[[indirect-prompt-injection-defense]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks whether layered guardrails apply: internal-only or prototype → skip; production + untrusted input → run the spec.
