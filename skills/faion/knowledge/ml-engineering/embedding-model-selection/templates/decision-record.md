<!-- purpose: Filled-in decision-record skeleton for an embedding model choice -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites table -->
<!-- produces: artefact conforming to content/02-output-contract.xml (embedding-model-selection) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150-400 tokens when loaded as context -->

# Embedding Model Decision Record

## Context

Corpus: <size, language mix, growth rate>.
SLA: <p50/p95 latency, $/1k queries>.
Compliance: <PII / air-gap / GDPR flags>.

## Decision

- **Model:** <text-embedding-3-large>
- **Provider:** <openai>
- **Dimensions:** <1024>
- **Max input tokens:** <8191>
- **Cost per 1M tokens:** <$0.13>

## Rationale (>= 40 chars)

<Why this model + dim count beats alternatives on quality / cost / latency for this workload.>

## Alternatives considered

1. <text-embedding-3-small @ 512 dims> — rejected because <reason>
2. <embed-english-v3.0> — rejected because <reason>

## Migration plan

Index versioned as `embeddings_v<N>_<model>_<dim>`. Switch model = new collection + dual-write window.
