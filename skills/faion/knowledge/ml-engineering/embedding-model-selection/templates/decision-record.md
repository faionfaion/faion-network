<!--
purpose: Filled-in decision-record skeleton for an embedding model choice
consumes: inputs declared in AGENTS.md Prerequisites table
produces: artefact conforming to content/02-output-contract.xml (embedding-model-selection)
depends-on: content/01-core-rules.xml
token-budget-impact: ~150-400 tokens when loaded as context
variables:
  - name: corpus_profile
    type: text
    required: true
    description: Size, language mix and growth rate of what you will embed. Name the languages - multilingual content against an English-tuned model is the exact failure this record exists to prevent.
  - name: latency_sla
    type: text
    required: true
    description: The p50 and p95 query latency you must stay inside, and the cost per thousand queries you can afford. Both, with numbers - a choice made on quality alone gets reversed by the invoice.
  - name: compliance_flags
    type: text
    required: true
    description: PII, air-gap or data-residency constraints that rule providers out. If there are none, write none - an unexamined "none" is how customer records end up in a hosted embedding API.
  - name: chosen_model
    type: string
    required: true
    description: Model and version you are committing to. The version matters - providers reissue a name and the vectors from the two are not comparable, let alone interchangeable.
  - name: provider
    type: string
    required: true
    description: Who serves it - openai, cohere, self-hosted. Self-hosting moves the cost from invoice to ops time; say which side you have chosen to pay on, because both are real.
  - name: dimensions
    type: integer
    required: true
    description: Vector dimensions you will store. It sets index size and memory cost directly, and reducing it later means re-embedding the whole corpus behind a dual-write window.
-->

# Embedding Model Decision Record

## Context

Corpus: {{corpus_profile}}

SLA: {{latency_sla}}

Compliance: {{compliance_flags}}

## Decision

- **Model:** {{chosen_model}}
- **Provider:** {{provider}}
- **Dimensions:** {{dimensions}}
- **Max input tokens:** [limit]
- **Cost per 1M tokens:** [price]

## Rationale (>= 40 chars)

[Why this model and dimension count beat the alternatives on quality, cost and latency for this workload.]

## Alternatives considered

1. [model @ dimensions] — rejected because [reason]
2. [model @ dimensions] — rejected because [reason]

## Migration plan

Index versioned as `embeddings_v[N]_{{chosen_model}}_{{dimensions}}`. Switching model = new collection + dual-write window.
