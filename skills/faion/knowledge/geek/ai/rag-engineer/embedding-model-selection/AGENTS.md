---
slug: embedding-model-selection
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Selects an embedding model + dimension count for a RAG workload by matching quality, cost, token limits, language coverage, and latency to the corpus and SLA.
content_id: "ec6a0e52845bd0dd"
complexity: medium
produces: decision-record
est_tokens: 4300
tags: [embeddings, rag, model-selection, vector-search, openai]
---
# Embedding Model Selection for RAG

## Summary

**One-sentence:** Selects an embedding model + dimension count for a RAG workload by matching quality, cost, token limits, language coverage, and latency to the corpus and SLA.

**One-paragraph:** Selects an embedding model + dimension count for a RAG workload by matching quality, cost, token limits, language coverage, and latency to the corpus and SLA. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Стартуєш новий RAG-індекс і треба зафіксувати модель ДО першої ingestion.
- Балансуєш якість vs $ між OpenAI text-embedding-3-large / -small / Cohere / BGE.
- Багатомовний пошук де query і doc — різні мови; треба multilingual модель.
- Air-gapped/PII обмеження → локальна модель замість API.

## Applies If (ALL must hold)

- Будуєш RAG-pipeline і обираєш модель ДО першої ingestion.
- Корпус ≥ 500 текстів та індекс буде оновлюватися інкрементально.
- Доступний бюджет на API-токени АБО GPU для локальної моделі.

## Skip If (ANY kills it)

- Достатньо exact-keyword пошуку (BM25/TF-IDF) — embeddings зайві.
- Real-time SLA < 10ms на запит без локального GPU.
- Доменна специфіка без жодної придатної моделі (chemistry, genomics).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| corpus stats | JSON {avg_tokens, languages[], size} | ingestion telemetry |
| SLA targets | YAML latency_ms, $/1k queries | product owner |
| compliance flags | list (PII, air-gapped, GDPR) | security review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[chunking-basics]] | chunk size + overlap chosen before embedding |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Filled-in decision-record skeleton for an embedding model choice |
| `templates/decision-record.json` | Machine-readable decision-record matching 02-output-contract schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-model-selection.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[chunking-basics]]
- [[vector-database-setup]]
- [[rag-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does the corpus need semantic similarity beyond keyword matching?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
