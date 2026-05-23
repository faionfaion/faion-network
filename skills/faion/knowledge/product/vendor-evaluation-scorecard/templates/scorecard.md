<!-- purpose: Human-readable scorecard with five-axis table -->
<!-- consumes: inputs declared in AGENTS.md Prerequisites table -->
<!-- produces: artefact conforming to content/02-output-contract.xml (vendor-evaluation-scorecard) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150-400 tokens when loaded as context -->

# Vendor Scorecard — <vector-db>

## Weights (sum = 1.0)

| Dimension | Weight | Why |
|---|---|---|
| quality | 0.25 | Recall@10 directly drives user task success |
| cost | 0.20 | Budget cap $3k/mo |
| lock_in | 0.20 | 18-month commitment risk |
| security | 0.20 | PII workload requires SOC2 |
| sla | 0.15 | 99.9% uptime contract |

## Scores (each cell cites >= 2 evidence items)

| Vendor | Quality | Cost | Lock-in | Security | SLA |
|---|---|---|---|---|---|
| qdrant-cloud | 0.90 | 0.80 | 0.90 | 0.85 | 0.80 |
| pinecone | 0.92 | 0.60 | 0.50 | 0.90 | 0.90 |
| weaviate-cloud | 0.85 | 0.70 | 0.80 | 0.80 | 0.80 |

## Exit-cost (engineer-days)

- qdrant-cloud: 5
- pinecone: 25
- weaviate-cloud: 12

## Decision

Winner: **qdrant-cloud** (weighted 0.853). Lock-in score and exit-cost decisive.
