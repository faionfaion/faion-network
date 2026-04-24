# Vector Database Setup Examples

Practical examples for setting up and configuring vector databases.

---

## Table of Contents

- [Docker Setup Examples](#docker-setup-examples)
- [Kubernetes Setup Examples](#kubernetes-setup-examples)
- [Configuration Examples](#configuration-examples)
- [Client Connection Examples](#client-connection-examples)
- [Collection Setup Examples](#collection-setup-examples)
- [Index Configuration Examples](#index-configuration-examples)
- [Security Configuration Examples](#security-configuration-examples)

---

## Docker Setup Examples

### Qdrant Development Setup

```bash
# Simple development setup
docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant:latest

# With persistent storage
docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant:latest

# With custom configuration
docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  -v $(pwd)/qdrant_config.yaml:/qdrant/config/production.yaml:ro \
  -e QDRANT__SERVICE__GRPC_PORT=6334 \
  -e QDRANT__TELEMETRY_DISABLED=true \
  qdrant/qdrant:latest

# Verify health
curl http://localhost:6333/readyz
```

### Weaviate Development Setup

```bash
# Simple development setup
docker run -d --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  semitechnologies/weaviate:latest

# With persistent storage
docker run -d --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -v weaviate_data:/var/lib/weaviate \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e DEFAULT_VECTORIZER_MODULE=none \
  semitechnologies/weaviate:latest

# Verify health
curl http://localhost:8080/v1/.well-known/ready
```

### Milvus Standalone Setup

```bash
# Download standalone script
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

# Start Milvus
bash standalone_embed.sh start

# Stop Milvus
bash standalone_embed.sh stop

# Verify health
curl http://localhost:9091/healthz
```

### pgvector Setup

```bash
# Run PostgreSQL with pgvector
docker run -d --name pgvector \
  -p 5432:5432 \
  -e POSTGRES_USER=vectordb \
  -e POSTGRES_PASSWORD=vectordb \
  -e POSTGRES_DB=vectors \
  -v pgvector_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16

# Connect and enable extension
docker exec -it pgvector psql -U vectordb -d vectors -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Verify
docker exec -it pgvector psql -U vectordb -d vectors -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';"
```

### Chroma Setup

```bash
# Run Chroma server (optional - usually used as library)
docker run -d --name chroma \
  -p 8000:8000 \
  -v chroma_data:/chroma/chroma \
  -e IS_PERSISTENT=TRUE \
  -e ANONYMIZED_TELEMETRY=FALSE \
  chromadb/chroma:latest

# Verify health
curl http://localhost:8000/api/v1/heartbeat
```

---

## Kubernetes Setup Examples

### Qdrant Kubernetes Deployment

```yaml
# qdrant-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qdrant
  labels:
    app: qdrant
spec:
  replicas: 1
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
        - name: qdrant
          image: qdrant/qdrant:v1.7.4
          ports:
            - containerPort: 6333
              name: http
            - containerPort: 6334
              name: grpc
          env:
            - name: QDRANT__TELEMETRY_DISABLED
              value: "true"
          volumeMounts:
            - name: storage
              mountPath: /qdrant/storage
          resources:
            requests:
              memory: "2Gi"
              cpu: "500m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          livenessProbe:
            httpGet:
              path: /readyz
              port: 6333
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /readyz
              port: 6333
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: storage
          persistentVolumeClaim:
            claimName: qdrant-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: qdrant
spec:
  selector:
    app: qdrant
  ports:
    - name: http
      port: 6333
      targetPort: 6333
    - name: grpc
      port: 6334
      targetPort: 6334
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: qdrant-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: standard
```

Apply with:
```bash
kubectl apply -f qdrant-deployment.yaml
kubectl get pods -l app=qdrant
kubectl port-forward svc/qdrant 6333:6333
```

### Weaviate Kubernetes StatefulSet

```yaml
# weaviate-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: weaviate
spec:
  serviceName: weaviate
  replicas: 1
  selector:
    matchLabels:
      app: weaviate
  template:
    metadata:
      labels:
        app: weaviate
    spec:
      containers:
        - name: weaviate
          image: semitechnologies/weaviate:1.24.1
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 50051
              name: grpc
          env:
            - name: AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED
              value: "false"
            - name: AUTHENTICATION_APIKEY_ENABLED
              value: "true"
            - name: AUTHENTICATION_APIKEY_ALLOWED_KEYS
              valueFrom:
                secretKeyRef:
                  name: weaviate-secrets
                  key: api-key
            - name: PERSISTENCE_DATA_PATH
              value: "/var/lib/weaviate"
            - name: DEFAULT_VECTORIZER_MODULE
              value: "none"
          volumeMounts:
            - name: data
              mountPath: /var/lib/weaviate
          resources:
            requests:
              memory: "2Gi"
              cpu: "500m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          livenessProbe:
            httpGet:
              path: /v1/.well-known/ready
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /v1/.well-known/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: weaviate
spec:
  selector:
    app: weaviate
  ports:
    - name: http
      port: 8080
    - name: grpc
      port: 50051
---
apiVersion: v1
kind: Secret
metadata:
  name: weaviate-secrets
type: Opaque
stringData:
  api-key: "your-secure-api-key-here"
```

---

## Configuration Examples

### Qdrant Configuration File

```yaml
# qdrant_config.yaml
storage:
  storage_path: /qdrant/storage
  snapshots_path: /qdrant/snapshots

  # Optimizer settings
  optimizers:
    default_segment_number: 5
    indexing_threshold: 20000
    flush_interval_sec: 5
    max_optimization_threads: 2

service:
  http_port: 6333
  grpc_port: 6334
  max_request_size_mb: 32
  enable_tls: false

# Cluster mode (for distributed setup)
cluster:
  enabled: false

# HNSW index defaults
hnsw_index:
  m: 16                      # Connections per node
  ef_construct: 100          # Build quality
  full_scan_threshold: 10000 # Switch to brute force below this
  max_indexing_threads: 0    # 0 = auto-detect
  on_disk: false             # Keep index in RAM

# Quantization for memory efficiency
quantization:
  scalar:
    type: int8
    quantile: 0.99
    always_ram: true

# Disable telemetry
telemetry_disabled: true
```

### Milvus Configuration File

```yaml
# milvus.yaml
etcd:
  endpoints:
    - etcd:2379
  rootPath: by-dev

minio:
  address: minio
  port: 9000
  accessKeyID: minioadmin
  secretAccessKey: minioadmin
  useSSL: false
  bucketName: milvus-bucket

common:
  gracefulTime: 5000
  chanNamePrefix:
    cluster: by-dev

proxy:
  port: 19530
  http:
    enabled: true
    debug_mode: false

queryNode:
  gracefulTime: 5000
  enableDisk: true

indexNode:
  scheduler:
    buildParallel: 1

dataNode:
  flush:
    insertBufSize: 16777216

log:
  level: info
  format: text
  file:
    maxSize: 300
    maxAge: 10
    maxBackups: 20
```

### PostgreSQL Configuration for pgvector

```sql
-- postgresql.conf optimizations
-- shared_buffers = 4GB              -- 25% of RAM
-- effective_cache_size = 12GB        -- 75% of RAM
-- maintenance_work_mem = 2GB         -- For index builds
-- work_mem = 256MB                   -- For queries

-- Session-level settings
SET hnsw.ef_search = 100;             -- Search quality (higher = better recall)
SET maintenance_work_mem = '2GB';     -- For index builds

-- Check current settings
SHOW hnsw.ef_search;
SHOW maintenance_work_mem;
```

---

## Client Connection Examples

### Qdrant Client Connection

```python
from qdrant_client import QdrantClient

# Local development
client = QdrantClient(host="localhost", port=6333)

# With gRPC (recommended for production)
client = QdrantClient(
    host="localhost",
    port=6334,
    prefer_grpc=True,
)

# Cloud/remote with API key
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key",
)

# Verify connection
print(client.get_collections())
```

### Weaviate Client Connection

```python
import weaviate
from weaviate.classes.init import Auth

# Local development
client = weaviate.connect_to_local()

# Cloud connection
client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://your-cluster.weaviate.cloud",
    auth_credentials=Auth.api_key("your-api-key"),
)

# Custom connection
client = weaviate.connect_to_custom(
    http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False,
)

# Verify connection
print(client.is_ready())
```

### Milvus Client Connection

```python
from pymilvus import MilvusClient, connections

# Simple client (local file)
client = MilvusClient("milvus_demo.db")

# Connect to server
client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus",
)

# Legacy connection API
connections.connect(
    alias="default",
    host="localhost",
    port="19530",
)

# Verify connection
print(client.list_collections())
```

### pgvector Connection

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Direct connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="vectors",
    user="vectordb",
    password="vectordb",
)
register_vector(conn)

# Using connection string
conn = psycopg2.connect("postgresql://vectordb:vectordb@localhost:5432/vectors")
register_vector(conn)

# Verify connection
cur = conn.cursor()
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
print(cur.fetchone())
```

### Chroma Client

```python
import chromadb

# In-memory (ephemeral)
client = chromadb.Client()

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Remote server (if using Chroma server)
client = chromadb.HttpClient(host="localhost", port=8000)

# Verify connection
print(client.list_collections())
```

### Pinecone Client

```python
from pinecone import Pinecone

# Initialize client
pc = Pinecone(api_key="your-api-key")

# List indexes
for idx in pc.list_indexes():
    print(idx.name)

# Connect to specific index
index = pc.Index("my-index")

# Verify connection
print(index.describe_index_stats())
```

---

## Collection Setup Examples

### Qdrant Collection Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance,
    HnswConfigDiff, OptimizersConfigDiff,
    ScalarQuantization, ScalarQuantizationConfig,
    PayloadSchemaType,
)

client = QdrantClient(host="localhost", port=6333)

# Create collection with HNSW config
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE,
    ),
    hnsw_config=HnswConfigDiff(
        m=16,
        ef_construct=100,
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20000,
    ),
    on_disk_payload=True,  # Store large payloads on disk
)

# Create payload indexes for faster filtering
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD,
)

client.create_payload_index(
    collection_name="documents",
    field_name="page",
    field_schema=PayloadSchemaType.INTEGER,
)

client.create_payload_index(
    collection_name="documents",
    field_name="created_at",
    field_schema=PayloadSchemaType.DATETIME,
)

# Verify collection
info = client.get_collection("documents")
print(f"Created collection with {info.vectors_count} vectors")
```

### Weaviate Collection Setup

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType, VectorDistances

client = weaviate.connect_to_local()

# Create collection
documents = client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # Bring your own vectors
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="page", data_type=DataType.INT),
        Property(name="category", data_type=DataType.TEXT, skip_vectorization=True),
        Property(name="created_at", data_type=DataType.DATE),
    ],
    vector_index_config=Configure.VectorIndex.hnsw(
        ef=100,
        max_connections=16,
        distance_metric=VectorDistances.COSINE,
    ),
)

# Verify collection
print(f"Created collection: {documents.name}")
```

### Milvus Collection Setup

```python
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType

client = MilvusClient(uri="http://localhost:19530")

# Simple creation
client.create_collection(
    collection_name="documents",
    dimension=1536,
    metric_type="COSINE",
)

# Or with detailed schema
from pymilvus import Collection

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="page", dtype=DataType.INT64),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
]

schema = CollectionSchema(fields=fields, description="Document collection")
collection = Collection(name="documents_detailed", schema=schema)

# Create HNSW index
index_params = {
    "metric_type": "COSINE",
    "index_type": "HNSW",
    "params": {"M": 16, "efConstruction": 200},
}
collection.create_index(field_name="embedding", index_params=index_params)

# Load to memory
collection.load()

print(f"Created collection with schema: {collection.schema}")
```

### pgvector Table Setup

```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect("postgresql://vectordb:vectordb@localhost:5432/vectors")
register_vector(conn)
cur = conn.cursor()

# Enable extension
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id BIGSERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        source VARCHAR(255),
        page INTEGER,
        category VARCHAR(100),
        embedding vector(1536),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Create HNSW index
cur.execute("""
    CREATE INDEX IF NOT EXISTS documents_embedding_idx
    ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
""")

# Create metadata indexes
cur.execute("CREATE INDEX IF NOT EXISTS documents_category_idx ON documents(category);")
cur.execute("CREATE INDEX IF NOT EXISTS documents_source_idx ON documents(source);")

conn.commit()
print("Table and indexes created successfully")
```

### Pinecone Index Setup

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

# Create serverless index
pc.create_index(
    name="documents",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    ),
)

# Wait for index to be ready
import time
while not pc.describe_index("documents").status["ready"]:
    time.sleep(1)

# Connect to index
index = pc.Index("documents")
print(f"Index ready: {index.describe_index_stats()}")
```

---

## Index Configuration Examples

### HNSW Parameter Tuning

```python
# Qdrant HNSW configuration
from qdrant_client.models import HnswConfigDiff

# High recall configuration
high_recall_config = HnswConfigDiff(
    m=32,              # More connections = better recall
    ef_construct=200,  # Higher quality index
)

# Balanced configuration (default)
balanced_config = HnswConfigDiff(
    m=16,
    ef_construct=100,
)

# Memory-efficient configuration
memory_efficient_config = HnswConfigDiff(
    m=8,               # Fewer connections = less memory
    ef_construct=50,
    on_disk=True,      # Store index on disk
)
```

### Quantization Configuration

```python
# Qdrant quantization
from qdrant_client.models import (
    ScalarQuantization, ScalarQuantizationConfig,
    BinaryQuantization, BinaryQuantizationConfig,
)

# Scalar quantization (4x memory reduction, ~2% recall loss)
scalar_config = ScalarQuantization(
    scalar=ScalarQuantizationConfig(
        type="int8",
        quantile=0.99,
        always_ram=True,  # Keep quantized vectors in RAM
    )
)

# Binary quantization (32x memory reduction, ~5-10% recall loss)
binary_config = BinaryQuantization(
    binary=BinaryQuantizationConfig(
        always_ram=True,
    )
)

# Apply to collection
client.update_collection(
    collection_name="documents",
    quantization_config=scalar_config,
)
```

### Search Parameter Tuning

```python
# Qdrant search with tuned parameters
from qdrant_client.models import SearchParams, QuantizationSearchParams

# High accuracy search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(
        hnsw_ef=200,  # Higher = better recall, slower
        quantization=QuantizationSearchParams(
            rescore=True,       # Rescore with original vectors
            oversampling=2.0,   # Retrieve 2x candidates for rescoring
        )
    ),
)

# Fast search (lower accuracy)
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=10,
    search_params=SearchParams(
        hnsw_ef=50,  # Lower = faster, less accurate
    ),
)
```

---

## Security Configuration Examples

### Qdrant with API Key

```yaml
# docker-compose.yml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
      - QDRANT__TELEMETRY_DISABLED=true
```

```python
# Connect with API key
client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="your-api-key",
)
```

### Weaviate with Authentication

```yaml
# docker-compose.yml
version: '3.8'
services:
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
      AUTHENTICATION_APIKEY_ENABLED: 'true'
      AUTHENTICATION_APIKEY_ALLOWED_KEYS: '${WEAVIATE_API_KEY}'
      AUTHENTICATION_APIKEY_USERS: 'admin'
```

```python
# Connect with API key
from weaviate.classes.init import Auth

client = weaviate.connect_to_local(
    auth_credentials=Auth.api_key("your-api-key"),
)
```

### pgvector with TLS

```python
import psycopg2
import ssl

# Create SSL context
ssl_context = ssl.create_default_context(
    ssl.Purpose.SERVER_AUTH,
    cafile="/path/to/ca-certificate.crt"
)
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Connect with SSL
conn = psycopg2.connect(
    host="your-host",
    port=5432,
    database="vectors",
    user="vectordb",
    password="secure-password",
    sslmode="verify-full",
    sslrootcert="/path/to/ca-certificate.crt",
)
```

---

*Examples v1.0*
*Part of vector-database-setup skill*
