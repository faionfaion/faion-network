# GraphRAG Configuration Templates

## 1. Microsoft GraphRAG Settings

### settings.yaml

```yaml
# Microsoft GraphRAG Configuration
# https://microsoft.github.io/graphrag/config/

encoding_model: cl100k_base
skip_workflows: []
llm:
  api_key: ${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-4o
  model_supports_json: true
  max_tokens: 4096
  temperature: 0
  top_p: 1
  request_timeout: 180.0
  api_base: null
  api_version: null
  concurrent_requests: 25
  tokens_per_minute: 150000
  requests_per_minute: 10000

parallelization:
  stagger: 0.3
  num_threads: 50

async_mode: threaded

embeddings:
  async_mode: threaded
  llm:
    api_key: ${OPENAI_API_KEY}
    type: openai_embedding
    model: text-embedding-3-small
    api_base: null
    api_version: null
    concurrent_requests: 25
    tokens_per_minute: 350000
    requests_per_minute: 10000

chunks:
  size: 1200
  overlap: 100
  group_by_columns: [id]

input:
  type: file
  file_type: text
  base_dir: input
  file_encoding: utf-8
  file_pattern: ".*\\.txt$"

cache:
  type: file
  base_dir: cache

storage:
  type: file
  base_dir: output

reporting:
  type: file
  base_dir: output

entity_extraction:
  prompt: prompts/entity_extraction.txt
  entity_types: [organization, person, geo, event, product, technology]
  max_gleanings: 1

summarize_descriptions:
  prompt: prompts/summarize_descriptions.txt
  max_length: 500

claim_extraction:
  enabled: false
  prompt: prompts/claim_extraction.txt
  description: "Any claims or facts that could be relevant."
  max_gleanings: 1

community_reports:
  prompt: prompts/community_report.txt
  max_length: 2000
  max_input_length: 8000

cluster_graph:
  max_cluster_size: 10

embed_graph:
  enabled: false
  num_walks: 10
  walk_length: 40
  window_size: 2
  iterations: 3
  random_seed: 597832

umap:
  enabled: false

snapshots:
  graphml: true
  raw_entities: true
  top_level_nodes: true

local_search:
  text_unit_prop: 0.5
  community_prop: 0.1
  conversation_history_max_turns: 5
  top_k_entities: 10
  top_k_relationships: 10
  max_tokens: 12000

global_search:
  max_tokens: 12000
  data_max_tokens: 12000
  map_max_tokens: 1000
  reduce_max_tokens: 2000
  concurrency: 32
```

### Environment-specific overrides

```yaml
# settings.development.yaml
llm:
  model: gpt-4o-mini  # Cheaper for dev
  concurrent_requests: 5
  tokens_per_minute: 50000

parallelization:
  num_threads: 10

---

# settings.production.yaml
llm:
  model: gpt-4o
  concurrent_requests: 50
  tokens_per_minute: 500000

parallelization:
  num_threads: 100

cache:
  type: blob
  connection_string: ${AZURE_STORAGE_CONNECTION_STRING}
  container_name: graphrag-cache

storage:
  type: blob
  connection_string: ${AZURE_STORAGE_CONNECTION_STRING}
  container_name: graphrag-output
```

## 2. Neo4j GraphRAG Python

### Configuration Class

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Neo4jGraphRAGConfig:
    """Configuration for Neo4j GraphRAG."""

    # Neo4j connection
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"

    # LLM settings
    llm_provider: str = "openai"  # openai, anthropic, azure
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # Embedding settings
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # Entity extraction
    entity_types: list[str] = None
    relation_types: list[str] = None
    extraction_prompt: Optional[str] = None

    # Retrieval settings
    vector_index_name: str = "entity_embeddings"
    fulltext_index_name: str = "entity_fulltext"
    top_k: int = 10
    traversal_depth: int = 2

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    def __post_init__(self):
        if self.entity_types is None:
            self.entity_types = [
                "Person", "Organization", "Location",
                "Product", "Technology", "Event"
            ]
        if self.relation_types is None:
            self.relation_types = [
                "WORKS_FOR", "LOCATED_IN", "PRODUCES",
                "USES", "KNOWS", "PART_OF"
            ]
```

### Neo4j Schema Setup

```cypher
// Create constraints for entity uniqueness
CREATE CONSTRAINT entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;

CREATE CONSTRAINT person_name IF NOT EXISTS
FOR (p:Person) REQUIRE p.name IS UNIQUE;

CREATE CONSTRAINT organization_name IF NOT EXISTS
FOR (o:Organization) REQUIRE o.name IS UNIQUE;

// Create vector index for embeddings
CREATE VECTOR INDEX entity_embeddings IF NOT EXISTS
FOR (e:Entity)
ON e.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}};

// Create fulltext index for hybrid search
CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS
FOR (e:Entity)
ON EACH [e.name, e.description];

// Create index for efficient traversal
CREATE INDEX entity_type IF NOT EXISTS
FOR (e:Entity) ON (e.type);

CREATE INDEX relationship_type IF NOT EXISTS
FOR ()-[r:RELATED_TO]-() ON (r.type);
```

## 3. LlamaIndex Property Graph

### Configuration

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LlamaIndexGraphConfig:
    """Configuration for LlamaIndex Property Graph."""

    # Storage
    graph_store_type: str = "neo4j"  # neo4j, nebula, kuzu
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = ""

    # LLM
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0

    # Embeddings
    embedding_model: str = "text-embedding-3-small"

    # Extraction
    entity_types: list[str] = field(default_factory=lambda: [
        "Person", "Organization", "Location", "Product", "Technology"
    ])
    relation_types: list[str] = field(default_factory=lambda: [
        "WORKS_AT", "LOCATED_IN", "USES", "DEVELOPS", "ACQUIRED"
    ])
    strict_schema: bool = False

    # Retrieval
    include_text: bool = True
    similarity_top_k: int = 10
    path_depth: int = 2
```

### Index Configuration

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

def configure_llama_index(config: LlamaIndexGraphConfig):
    """Configure LlamaIndex global settings."""

    Settings.llm = OpenAI(
        model=config.llm_model,
        temperature=config.llm_temperature,
    )

    Settings.embed_model = OpenAIEmbedding(
        model=config.embedding_model,
    )

    Settings.chunk_size = 1024
    Settings.chunk_overlap = 128
```

## 4. LangChain Graph Configuration

### Configuration

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class LangChainGraphConfig:
    """Configuration for LangChain with Neo4j."""

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = ""

    # LLM
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.0

    # Graph QA
    verbose: bool = True
    return_intermediate_steps: bool = True
    validate_cypher: bool = True

    # Vector store
    embedding_model: str = "text-embedding-3-small"
    vector_index_name: str = "entity_index"
    node_label: str = "Entity"
    text_properties: list[str] = None
    embedding_property: str = "embedding"

    def __post_init__(self):
        if self.text_properties is None:
            self.text_properties = ["name", "description"]
```

## 5. Entity Schema Templates

### Generic Schema

```python
ENTITY_SCHEMA = {
    "entities": [
        {
            "name": "Person",
            "description": "A human individual",
            "properties": ["name", "title", "affiliation", "expertise"]
        },
        {
            "name": "Organization",
            "description": "A company, institution, or group",
            "properties": ["name", "type", "industry", "location", "founded"]
        },
        {
            "name": "Location",
            "description": "A geographic place",
            "properties": ["name", "type", "country", "coordinates"]
        },
        {
            "name": "Product",
            "description": "A product or service",
            "properties": ["name", "type", "manufacturer", "release_date"]
        },
        {
            "name": "Technology",
            "description": "A technology, framework, or tool",
            "properties": ["name", "type", "version", "license"]
        },
        {
            "name": "Event",
            "description": "A notable occurrence or happening",
            "properties": ["name", "date", "location", "participants"]
        },
        {
            "name": "Concept",
            "description": "An abstract idea or topic",
            "properties": ["name", "domain", "related_concepts"]
        }
    ],
    "relationships": [
        {
            "name": "WORKS_FOR",
            "source": "Person",
            "target": "Organization",
            "properties": ["role", "start_date", "end_date"]
        },
        {
            "name": "LOCATED_IN",
            "source": ["Person", "Organization"],
            "target": "Location",
            "properties": []
        },
        {
            "name": "PRODUCES",
            "source": "Organization",
            "target": "Product",
            "properties": ["since"]
        },
        {
            "name": "USES",
            "source": ["Person", "Organization", "Product"],
            "target": "Technology",
            "properties": []
        },
        {
            "name": "ACQUIRED",
            "source": "Organization",
            "target": "Organization",
            "properties": ["date", "amount"]
        },
        {
            "name": "RELATED_TO",
            "source": "*",
            "target": "*",
            "properties": ["type", "strength"]
        },
        {
            "name": "PARTICIPATED_IN",
            "source": ["Person", "Organization"],
            "target": "Event",
            "properties": ["role"]
        }
    ]
}
```

### Domain-Specific: Technical Documentation

```python
TECH_DOCS_SCHEMA = {
    "entities": [
        {"name": "API", "properties": ["name", "version", "type"]},
        {"name": "Function", "properties": ["name", "signature", "module"]},
        {"name": "Class", "properties": ["name", "module", "parent_class"]},
        {"name": "Parameter", "properties": ["name", "type", "default"]},
        {"name": "Module", "properties": ["name", "package", "version"]},
        {"name": "ErrorType", "properties": ["name", "code", "severity"]},
    ],
    "relationships": [
        {"name": "CONTAINS", "source": "Module", "target": ["Function", "Class"]},
        {"name": "CALLS", "source": "Function", "target": "Function"},
        {"name": "INHERITS", "source": "Class", "target": "Class"},
        {"name": "ACCEPTS", "source": ["Function", "API"], "target": "Parameter"},
        {"name": "RETURNS", "source": "Function", "target": "Class"},
        {"name": "RAISES", "source": "Function", "target": "ErrorType"},
        {"name": "DEPENDS_ON", "source": "Module", "target": "Module"},
    ]
}
```

### Domain-Specific: Healthcare

```python
HEALTHCARE_SCHEMA = {
    "entities": [
        {"name": "Disease", "properties": ["name", "icd_code", "category"]},
        {"name": "Symptom", "properties": ["name", "severity", "duration"]},
        {"name": "Treatment", "properties": ["name", "type", "efficacy"]},
        {"name": "Medication", "properties": ["name", "dosage", "frequency"]},
        {"name": "Procedure", "properties": ["name", "cpt_code", "duration"]},
        {"name": "Anatomy", "properties": ["name", "system", "location"]},
    ],
    "relationships": [
        {"name": "CAUSES", "source": "Disease", "target": "Symptom"},
        {"name": "TREATS", "source": ["Treatment", "Medication"], "target": "Disease"},
        {"name": "CONTRAINDICATES", "source": "Medication", "target": "Medication"},
        {"name": "AFFECTS", "source": "Disease", "target": "Anatomy"},
        {"name": "INVOLVES", "source": "Procedure", "target": "Anatomy"},
    ]
}
```

### Domain-Specific: Legal

```python
LEGAL_SCHEMA = {
    "entities": [
        {"name": "Case", "properties": ["name", "citation", "year", "jurisdiction"]},
        {"name": "Statute", "properties": ["name", "code", "section", "jurisdiction"]},
        {"name": "Party", "properties": ["name", "type", "role"]},
        {"name": "Judge", "properties": ["name", "court", "appointed_by"]},
        {"name": "Court", "properties": ["name", "level", "jurisdiction"]},
        {"name": "LegalConcept", "properties": ["name", "area_of_law"]},
    ],
    "relationships": [
        {"name": "CITES", "source": "Case", "target": ["Case", "Statute"]},
        {"name": "OVERRULES", "source": "Case", "target": "Case"},
        {"name": "INTERPRETS", "source": "Case", "target": "Statute"},
        {"name": "INVOLVES", "source": "Case", "target": "Party"},
        {"name": "DECIDED_BY", "source": "Case", "target": "Judge"},
        {"name": "HEARD_IN", "source": "Case", "target": "Court"},
        {"name": "ESTABLISHES", "source": "Case", "target": "LegalConcept"},
    ]
}
```

## 6. Cypher Query Templates

### Traversal Patterns

```cypher
// 1-hop neighborhood
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
RETURN n, r, neighbor
LIMIT 50;

// 2-hop with relationship types
MATCH path = (n:Entity {name: $entity_name})-[r*1..2]-(related)
WHERE ALL(rel IN relationships(path) WHERE type(rel) IN $relationship_types)
RETURN path
LIMIT 100;

// Weighted traversal
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
WHERE r.weight > 0.5
RETURN n, r, neighbor
ORDER BY r.weight DESC
LIMIT 20;

// Path finding between entities
MATCH path = shortestPath(
  (a:Entity {name: $source})-[*1..5]-(b:Entity {name: $target})
)
RETURN path;

// Community-based retrieval
MATCH (n:Entity)-[:BELONGS_TO]->(c:Community {id: $community_id})
MATCH (n)-[r]-(related)
WHERE (related)-[:BELONGS_TO]->(c)
RETURN n, r, related;
```

### Hybrid Vector + Graph

```cypher
// Vector search with graph expansion
CALL db.index.vector.queryNodes('entity_embeddings', 10, $query_embedding)
YIELD node, score
WHERE score > 0.7
MATCH (node)-[r*1..2]-(related)
RETURN node, score,
       collect(DISTINCT {
         entity: related.name,
         relationship: type(r),
         properties: properties(r)
       }) AS context
ORDER BY score DESC;

// Hybrid (vector + fulltext) with traversal
CALL {
  CALL db.index.vector.queryNodes('entity_embeddings', 5, $embedding)
  YIELD node, score
  RETURN node, score, 'vector' AS source
  UNION
  CALL db.index.fulltext.queryNodes('entity_fulltext', $query)
  YIELD node, score
  RETURN node, score, 'fulltext' AS source
}
WITH node, max(score) AS score
MATCH (node)-[r*1..2]-(related)
RETURN node.name AS entity,
       node.description AS description,
       score,
       collect(DISTINCT related.name) AS related_entities
ORDER BY score DESC
LIMIT 10;
```

## 7. Docker Compose Template

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.15.0
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD:-password}
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
      NEO4J_dbms_memory_heap_max__size: 2G
      NEO4J_dbms_memory_pagecache_size: 1G
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"  # REST API
      - "6334:6334"  # gRPC
    volumes:
      - qdrant_data:/qdrant/storage

  graphrag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USERNAME: neo4j
      NEO4J_PASSWORD: ${NEO4J_PASSWORD:-password}
      QDRANT_URL: http://qdrant:6333
    depends_on:
      - neo4j
      - qdrant

volumes:
  neo4j_data:
  neo4j_logs:
  qdrant_data:
```

## 8. Environment Variables

```bash
# .env.template

# LLM Provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=...

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=...
WEAVIATE_URL=http://localhost:8080

# GraphRAG Settings
GRAPHRAG_MAX_CLUSTER_SIZE=10
GRAPHRAG_CHUNK_SIZE=1200
GRAPHRAG_CHUNK_OVERLAP=100

# Logging
LOG_LEVEL=INFO
```
