---
slug: vector-db-setup-dev
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "03cb64d3f85bd005"
summary: Spin up a vector DB locally for development (Qdrant / Weaviate / Milvus / pgvector / Chroma) via Docker one-liner or pip install, connect a Python client, create a collection, verify the stack — before writing pipeline code.
complexity: light
produces: code
est_tokens: 2400
tags: [vector-database, docker, development, qdrant, weaviate]
---

# Vector Database Development Setup

## Summary

**One-sentence:** Pre-flight dev setup that spins a vector DB locally (single docker-compose or pip install), exercises ingest + search, and ships a `dev-setup.yaml` recording chosen image + version + smoke test result.

**One-paragraph:** Skipping the dev-setup smoke test wastes hours debugging client-server protocol mismatches mid-pipeline. The pattern: pick DB consistent with `vector-databases` decision, docker-run with persistent volume, install matching Python client version, create a collection, insert 10 sample vectors, run a query, verify result. Output: a `dev-setup.yaml` recording the matrix that worked + a `verify-dev.py` script for new devs to re-run.

**Ефективно для:**

- Перший день на проєкті — нова людина за 5 хв має робочий vector DB на лептопі.
- Test fixtures — pytest setUp може швидко спінити Qdrant контейнер на random port.
- Multi-developer teams — стандартизована dev setup уникає "у мене працює" debug.
- CI smoke — той самий setup-скрипт у workflow.

## Applies If (ALL must hold)

- Choosing or onboarding to a vector DB project
- Docker available locally (or pip-installable DB like Chroma / pgvector)
- Need to verify client-server compatibility before pipeline code

## Skip If (ANY kills it)

- Pipeline already production-tested — re-do prod methodology instead
- Local resource constrained (no RAM) — use cloud dev instance

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `dev-machine-specs.yaml` | YAML | local laptop specs |
| `chosen-db.yaml` | YAML | output of `vector-databases` decision |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB picked |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pin image version, persistent volume, matching client version, smoke test, .gitignore data dir | 1000 |
| `content/02-output-contract.xml` | essential | dev-setup.yaml schema | 600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: latest tag, ephemeral volume, client version mismatch, no smoke, leak data dir | 700 |
| `content/04-procedure.xml` | essential | 4 steps: docker-run → install client → smoke → record | 500 |
| `content/05-examples.xml` | essential | Worked example: docker-compose for Qdrant + pip + smoke | 400 |
| `content/06-decision-tree.xml` | essential | Routes by DB choice → install path | 300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `setup_drafting` | haiku | Templated commands |
| `dev_setup_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/docker-compose.qdrant.yml` | Qdrant dev compose |
| `templates/verify-dev.py` | Smoke script |
| `templates/dev-setup.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable dev-setup record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-setup-dev.py` | Lint dev-setup.yaml | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-prod]]
- external: [Qdrant Docker](https://qdrant.tech/documentation/quick-start/)

## Decision tree

See `content/06-decision-tree.xml`. Routes by chosen DB to the matching docker-run / pip-install one-liner.
