# LLM Guardrails — Concepts, Types, and Architecture

## Summary

**One-sentence:** Maps the five guardrail rail types to pipeline stages, picks block/filter/transform/warn/log per stage, and sets a tiered-latency budget (regex → classifier → LLM-judge).

**One-paragraph:** Guardrails are runtime mechanisms that constrain LLM behaviour without retraining. This methodology turns a vague "we need safety" requirement into a concrete report: which rail type fires at which pipeline stage (input / output / dialog / retrieval / execution), which action it takes on a violation (block / filter / transform / warn / log), what the latency budget per tier is, and which framework owns each layer (NeMo for dialog, Guardrails AI for output, Llama Guard for safety class, custom for the rest). Output is a `guardrail-plan.json` consumed by downstream methodologies (`guardrails-nemo`, `guardrails-custom-pipeline`, `guardrails-testing`).

**Ефективно для:**

- Customer-facing LLM апки в регульованих доменах (health/fin/legal) — комплаєнс без retraining.
- Agent pipelines з tool-use — execution rails — єдиний кордон між LLM-рішенням і побічним ефектом.
- RAG-системи — retrieval rails чистять контекст від injection і PII у chunks.
- Будь-який pipeline з multi-turn dialog — dialog rails ловлять topic drift і persona-break.

## Applies If (ALL must hold)

- Customer-facing LLM application where uncontrolled output exposes business to liability or harm.
- Regulated domain (healthcare, finance, legal) or PII-handling — compliance dictates input/output rails.
- Agent or RAG pipeline with tool-use, retrieval, or multi-turn state where one rail type is insufficient.

## Skip If (ANY kills it)

- Internal developer tooling with high-trust users — false positives waste time, ROI negative.
- Latency budget < 50 ms — LLM-as-judge alone adds 500 ms+, breaks SLO.
- Base model already refuses the content class (Claude refusing CSAM) — extra rail adds no value.
- Prototyping / local experimentation — premature guardrails slow iteration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pipeline diagram | Mermaid / Markdown | `architecture-doc` |
| Threat model | Markdown bullet list | `security-review` or `stride` methodology |
| Latency SLO | float (ms p99) | `slo-doc` |
| Compliance scope | enum (HIPAA / SOC2 / GDPR / none) | `compliance-register` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `prompt-injection-defense` | Input-rail rule set assumes injection patterns already enumerated. |
| `llm-decision-framework` | Model + provider choice informs which embedded guardrails are already present. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: rail-types, embedded-vs-programmable, action-strategy, tiered-latency, defense-in-depth, log-sanitized | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for `guardrail-plan.json` + valid + invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: agent-relay, llm-judge-injectable, no-isolation, coupled-to-prompt | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: classify pipeline → map rails → pick actions → set tiers → pick frameworks → emit plan | 800 |
| `content/05-examples.xml` | essential | One end-to-end example: RAG support-bot guardrail plan | 600 |
| `content/06-decision-tree.xml` | essential | Pipeline shape → rail set → framework selector | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_pipeline_shape` | haiku | Pattern-match against 3 canonical shapes (basic/RAG/multi-agent). |
| `draft_guardrail_plan` | sonnet | Synthesis across rails + frameworks; needs reasoning, not raw recall. |
| `review_threat_coverage` | opus | High-stakes — missed rail = compliance gap; deep coverage check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/guardrail-plan.json` | JSON skeleton of the output artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in plan for a basic pipeline |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-guardrails-concepts.py` | Validate `guardrail-plan.json` against the schema | Before handing off to `guardrails-nemo` / `guardrails-custom-pipeline` |

## Related

- [[guardrails-nemo]] — Colang dialog rails referenced from the plan
- [[guardrails-custom-pipeline]] — input/output rail implementation
- [[guardrails-testing]] — adversarial harness that the plan must pass

## Decision tree

See `content/06-decision-tree.xml`. Branches on pipeline shape (basic / RAG / multi-agent), then on compliance scope and latency budget. Leaves reference the rule that picks the rail set, action policy, and framework slot.
