---
slug: vision-agentic-pipeline
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Wires a three-subagent vision pipeline: image-router (classifies + selects VLM), vision-extractor (calls VLM, returns Pydantic), validation-agent (cross-checks against business rules).
content_id: "31c29b608bbf4231"
complexity: deep
produces: spec
est_tokens: 5200
tags: [vision, agentic, pipeline, vlm, production]
---
# Vision Agentic Pipeline — Production Architecture

## Summary

**One-sentence:** Wires a three-subagent vision pipeline: image-router (classifies + selects VLM), vision-extractor (calls VLM, returns Pydantic), validation-agent (cross-checks against business rules).

**One-paragraph:** Production vision pipelines that pile every concern into a single mega-prompt regress on accuracy as the prompt grows. This methodology splits the work into three subagents, each with a single responsibility and a structured-output contract. Router decides which VLM + prompt to use. Extractor runs the VLM call with retries + Pydantic enforcement. Validator cross-checks extracted fields against business rules and triggers human review on failure.

**Ефективно для:**

- Document-extraction pipelines that must scale past 1k docs/day.
- Multi-doc-type intake (invoices + receipts + IDs) where a router beats one-prompt-to-rule-them-all.
- Compliance scenarios where a validation agent must veto extractor output before downstream use.
- Production stacks where you must swap VLMs (provider outage, price war) without breaking the extractor contract.

## Applies If (ALL must hold)

- Building a vision pipeline that must run at >100 docs/day in production.
- Multiple image / document types flow into the same pipeline.
- Business rules exist that must veto extracted output (totals must add up, dates must be in range, IDs must match a checksum).

## Skip If (ANY kills it)

- Single-image-type pipeline with <100/day volume — one prompt is fine.
- Free-form caption generation (no structured output) — no router or validator needed.
- Real-time latency budget <500ms — three sequential VLM calls cannot fit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Image queue | JSONL of {image_url, doc_type_hint} | Intake bus |
| Doc-type taxonomy | YAML | Business analyst output |
| Business rules | YAML / Python | Domain SME |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `router` | haiku | Classify doc_type; cheap + fast. |
| `extractor` | sonnet | VLM call with structured-output enforcement. |
| `validator` | haiku | Apply deterministic business rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pipeline-config.yaml` | Three-subagent pipeline config skeleton |
| `templates/router-prompt.txt` | Router classification prompt |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-agentic-pipeline.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-document-extraction]]
- [[vision-classification-moderation]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Has the pipeline received a new image event? Branches route to a rule id from `content/01-core-rules.xml` (idempotent-by-hash, router-cheap-model, retry-on-schema-fail, ...) so every leaf is traceable to a testable statement.
