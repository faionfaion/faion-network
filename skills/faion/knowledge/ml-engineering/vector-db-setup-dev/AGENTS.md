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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-setup-dev.py` | Lint dev-setup.yaml | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-prod]]
- external: [Qdrant Docker](https://qdrant.tech/documentation/quick-start/)

## Decision tree

See `content/06-decision-tree.xml`. Routes by chosen DB to the matching docker-run / pip-install one-liner.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/docker-compose.qdrant.yml`

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.10.0   # pinned per r1
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage   # persistent per r2
    environment:
      QDRANT__LOG_LEVEL: INFO
    healthcheck:
      test: ["CMD-SHELL", "curl -fs http://localhost:6333/healthz || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### `templates/verify-dev.py`

```python
"""Smoke test for dev vector DB setup."""
from __future__ import annotations

import sys
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


def smoke(host: str = "localhost", port: int = 6333) -> int:
    client = QdrantClient(host=host, port=port)
    coll = f"smoke_{uuid.uuid4().hex[:8]}"
    client.create_collection(collection_name=coll,
                             vectors_config=VectorParams(size=4, distance=Distance.COSINE))
    client.upsert(
        collection_name=coll,
        points=[PointStruct(id=i, vector=[float(i), 0.0, 0.0, 0.0]) for i in range(10)],
    )
    hits = client.search(collection_name=coll, query_vector=[1.0, 0.0, 0.0, 0.0], limit=5)
    client.delete_collection(coll)
    if not hits:
        sys.stderr.write("FAIL: search returned no results\n")
        return 1
    sys.stdout.write(f"OK: smoke returned {len(hits)} hits\n")
    return 0


if __name__ == "__main__":
    sys.exit(smoke())
```

### `templates/dev-setup.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [db_kind, image_tag, data_volume, client_version, smoke_passed, gitignore_entries]
properties:
  db_kind: {type: string, enum: [qdrant, weaviate, milvus, pgvector, chroma]}
  image_tag: {type: string, minLength: 5}
  data_volume: {type: string, minLength: 1}
  client_version: {type: string, minLength: 3}
  smoke_passed: {type: boolean}
  gitignore_entries: {type: array, items: {type: string}}
```

### `templates/_smoke-test.yaml`

```yaml
db_kind: qdrant
image_tag: "qdrant/qdrant:v1.10.0"
data_volume: "./qdrant_storage"
client_version: "qdrant-client==1.10.0"
smoke_passed: true
gitignore_entries: ["qdrant_storage/"]
```
