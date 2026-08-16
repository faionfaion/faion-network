<!--

purpose: Filled-in decision-record skeleton for an embedding model choice
consumes: inputs declared in AGENTS.md Prerequisites table
produces: artefact conforming to content/02-output-contract.xml (embedding-model-selection)
depends-on: content/01-core-rules.xml
token-budget-impact: ~150-400 tokens when loaded as context
-->



# Embedding Model Decision Record

## Context

Corpus: <corpus_profile>

SLA: <latency_sla>

Compliance: <compliance_flags>

## Decision

- **Model:** <chosen_model>
- **Provider:** <provider>
- **Dimensions:** <dimensions>
- **Max input tokens:** <limit>
- **Cost per 1M tokens:** <price>

## Rationale (>= 40 chars)

[Why this model and dimension count beat the alternatives on quality, cost and latency for this workload.]

## Alternatives considered

1. <model_dimensions> — rejected because <reason>
2. <model_dimensions> — rejected because <reason>

## Migration plan

Index versioned as `embeddings_v[N]_<chosen_model>_<dimensions>`. Switching model = new collection + dual-write window.
