# Vector Database Templates

Configuration templates, Docker/Kubernetes deployments, and Python client code templates.

---

## Table of Contents

- [Docker Compose Templates](#docker-compose-templates)
- [Kubernetes Templates](#kubernetes-templates)
- [Configuration Templates](#configuration-templates)
- [Python Client Templates](#python-client-templates)
- [Integration Templates](#integration-templates)

---

## Docker Compose Templates

### Qdrant

```yaml
# docker-compose.qdrant.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"  # HTTP API
      - "6334:6334"  # gRPC
    volumes:
      - qdrant_storage:/qdrant/storage
      - ./qdrant_config.yaml:/qdrant/config/production.yaml:ro
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__TELEMETRY_DISABLED=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G

volumes:
  qdrant_storage:
```

### Weaviate

```yaml
# docker-compose.weaviate.yml
version: '3.8'

services:
  weaviate:
    image: semitechnologies/weaviate:latest
    container_name: weaviate
    restart: unless-stopped
    ports:
      - "8080:8080"   # HTTP API
      - "50051:50051" # gRPC
    volumes:
      - weaviate_data:/var/lib/weaviate
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
      AUTHENTICATION_APIKEY_ENABLED: 'true'
      AUTHENTICATION_APIKEY_ALLOWED_KEYS: '${WEAVIATE_API_KEY}'
      AUTHENTICATION_APIKEY_USERS: 'admin'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: ''
      CLUSTER_HOSTNAME: 'node1'
      LOG_LEVEL: 'info'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/v1/.well-known/ready"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G

volumes:
  weaviate_data:
```

### Milvus Standalone

```yaml
# docker-compose.milvus.yml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.5
    container_name: milvus-etcd
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - etcd_data:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd

  minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    container_name: milvus-minio
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - minio_data:/data
    command: minio server /data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  milvus:
    image: milvusdb/milvus:v2.3.4
    container_name: milvus
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - milvus_data:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - etcd
      - minio
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  etcd_data:
  minio_data:
  milvus_data:
```

### pgvector (PostgreSQL)

```yaml
# docker-compose.pgvector.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: pgvector
    restart: unless-stopped
    ports:
      - "5432:5432"
    volumes:
      - pgvector_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-vectordb}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-vectordb}
      POSTGRES_DB: ${POSTGRES_DB:-vectors}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vectordb -d vectors"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 2G

volumes:
  pgvector_data:
```

```sql
-- init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255),
    category VARCHAR(100),
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS documents_category_idx ON documents(category);
```

### Chroma

```yaml
# docker-compose.chroma.yml
version: '3.8'

services:
  chroma:
    image: chromadb/chroma:latest
    container_name: chroma
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
      - PERSIST_DIRECTORY=/chroma/chroma
      - ANONYMIZED_TELEMETRY=FALSE
      - CHROMA_SERVER_AUTH_CREDENTIALS=${CHROMA_API_KEY}
      - CHROMA_SERVER_AUTH_PROVIDER=chromadb.auth.token.TokenAuthServerProvider
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  chroma_data:
```

---

## Kubernetes Templates

### Qdrant Deployment

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
          image: qdrant/qdrant:latest
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
            - name: config
              mountPath: /qdrant/config
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
        - name: config
          configMap:
            name: qdrant-config

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

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: qdrant-config
data:
  production.yaml: |
    storage:
      storage_path: /qdrant/storage
      snapshots_path: /qdrant/snapshots
    service:
      http_port: 6333
      grpc_port: 6334
    hnsw_index:
      m: 16
      ef_construct: 100
      on_disk: false
```

### Weaviate StatefulSet

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
          image: semitechnologies/weaviate:latest
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 50051
              name: grpc
          env:
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
      targetPort: 8080
    - name: grpc
      port: 50051
      targetPort: 50051

---
apiVersion: v1
kind: Secret
metadata:
  name: weaviate-secrets
type: Opaque
stringData:
  api-key: "your-secure-api-key"
```

### Helm Values (Qdrant)

```yaml
# values.qdrant.yaml
replicaCount: 3

image:
  repository: qdrant/qdrant
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  httpPort: 6333
  grpcPort: 6334

persistence:
  enabled: true
  size: 100Gi
  storageClass: "fast-ssd"

resources:
  requests:
    memory: "4Gi"
    cpu: "1000m"
  limits:
    memory: "8Gi"
    cpu: "4000m"

config:
  storage:
    storage_path: /qdrant/storage
  service:
    enable_tls: false
  hnsw_index:
    m: 16
    ef_construct: 100
  quantization:
    scalar:
      type: int8
      quantile: 0.99
      always_ram: true

metrics:
  enabled: true
  serviceMonitor:
    enabled: true

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: qdrant.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: qdrant-tls
      hosts:
        - qdrant.example.com
```

---

## Configuration Templates

### Qdrant Configuration

```yaml
# qdrant_config.yaml
storage:
  storage_path: /qdrant/storage
  snapshots_path: /qdrant/snapshots
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

cluster:
  enabled: false

hnsw_index:
  m: 16
  ef_construct: 100
  full_scan_threshold: 10000
  max_indexing_threads: 0  # Auto
  on_disk: false

quantization:
  scalar:
    type: int8
    quantile: 0.99
    always_ram: true

telemetry_disabled: true
```

### Weaviate Schema

```json
{
  "classes": [
    {
      "class": "Document",
      "description": "A document with embeddings",
      "vectorizer": "none",
      "vectorIndexType": "hnsw",
      "vectorIndexConfig": {
        "ef": 100,
        "efConstruction": 128,
        "maxConnections": 16,
        "distance": "cosine"
      },
      "properties": [
        {
          "name": "text",
          "dataType": ["text"],
          "description": "Document content"
        },
        {
          "name": "source",
          "dataType": ["text"],
          "description": "Source file path"
        },
        {
          "name": "page",
          "dataType": ["int"],
          "description": "Page number"
        },
        {
          "name": "category",
          "dataType": ["text"],
          "description": "Document category",
          "indexFilterable": true,
          "indexSearchable": false
        },
        {
          "name": "createdAt",
          "dataType": ["date"],
          "description": "Creation timestamp"
        }
      ],
      "invertedIndexConfig": {
        "bm25": {
          "b": 0.75,
          "k1": 1.2
        },
        "indexTimestamps": true
      }
    }
  ]
}
```

### Milvus Configuration

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
```

---

## Python Client Templates

### Base Client Interface

```python
# vector_store.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os


@dataclass
class SearchResult:
    id: str
    score: float
    metadata: Dict[str, Any]
    vector: Optional[List[float]] = None


@dataclass
class VectorRecord:
    id: str
    vector: List[float]
    metadata: Dict[str, Any]


class VectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    def create_collection(
        self,
        name: str,
        dimension: int,
        distance: str = "cosine",
        **kwargs,
    ) -> None:
        """Create a new collection."""
        pass

    @abstractmethod
    def upsert(
        self,
        collection: str,
        records: List[VectorRecord],
        batch_size: int = 100,
    ) -> int:
        """Upsert records into collection. Returns count of upserted records."""
        pass

    @abstractmethod
    def search(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        include_vectors: bool = False,
    ) -> List[SearchResult]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    def delete(
        self,
        collection: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Delete records by ID or filter. Returns count of deleted records."""
        pass

    @abstractmethod
    def count(self, collection: str) -> int:
        """Count records in collection."""
        pass
```

### Qdrant Client Template

```python
# qdrant_store.py
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue, Range,
    PayloadSchemaType,
)
import os

from vector_store import VectorStore, VectorRecord, SearchResult


class QdrantStore(VectorStore):
    """Qdrant vector store implementation."""

    DISTANCE_MAP = {
        "cosine": Distance.COSINE,
        "euclidean": Distance.EUCLID,
        "dot": Distance.DOT,
    }

    def __init__(
        self,
        host: str = None,
        port: int = None,
        url: str = None,
        api_key: str = None,
        prefer_grpc: bool = True,
    ):
        host = host or os.getenv("QDRANT_HOST", "localhost")
        port = port or int(os.getenv("QDRANT_PORT", "6333"))
        url = url or os.getenv("QDRANT_URL")
        api_key = api_key or os.getenv("QDRANT_API_KEY")

        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            grpc_port = 6334 if prefer_grpc else None
            self.client = QdrantClient(
                host=host,
                port=port,
                grpc_port=grpc_port,
                prefer_grpc=prefer_grpc,
            )

    def create_collection(
        self,
        name: str,
        dimension: int,
        distance: str = "cosine",
        on_disk_payload: bool = True,
        hnsw_m: int = 16,
        hnsw_ef_construct: int = 100,
        **kwargs,
    ) -> None:
        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=dimension,
                distance=self.DISTANCE_MAP[distance],
            ),
            hnsw_config={
                "m": hnsw_m,
                "ef_construct": hnsw_ef_construct,
            },
            on_disk_payload=on_disk_payload,
        )

    def create_payload_index(
        self,
        collection: str,
        field: str,
        field_type: str = "keyword",
    ) -> None:
        """Create index on payload field for faster filtering."""
        type_map = {
            "keyword": PayloadSchemaType.KEYWORD,
            "integer": PayloadSchemaType.INTEGER,
            "float": PayloadSchemaType.FLOAT,
            "datetime": PayloadSchemaType.DATETIME,
            "text": PayloadSchemaType.TEXT,
        }
        self.client.create_payload_index(
            collection_name=collection,
            field_name=field,
            field_schema=type_map[field_type],
        )

    def upsert(
        self,
        collection: str,
        records: List[VectorRecord],
        batch_size: int = 100,
    ) -> int:
        count = 0
        batch = []

        for record in records:
            batch.append(PointStruct(
                id=record.id,
                vector=record.vector,
                payload=record.metadata,
            ))

            if len(batch) >= batch_size:
                self.client.upsert(
                    collection_name=collection,
                    points=batch,
                    wait=False,
                )
                count += len(batch)
                batch = []

        if batch:
            self.client.upsert(
                collection_name=collection,
                points=batch,
                wait=True,
            )
            count += len(batch)

        return count

    def search(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        include_vectors: bool = False,
        score_threshold: float = None,
    ) -> List[SearchResult]:
        query_filter = self._build_filter(filters) if filters else None

        results = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold,
            with_vectors=include_vectors,
        )

        return [
            SearchResult(
                id=str(r.id),
                score=r.score,
                metadata=r.payload or {},
                vector=r.vector if include_vectors else None,
            )
            for r in results
        ]

    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """Build Qdrant filter from dict."""
        conditions = []

        for key, value in filters.items():
            if isinstance(value, dict):
                # Range filter: {"field": {"gte": 1, "lte": 10}}
                conditions.append(FieldCondition(
                    key=key,
                    range=Range(**value),
                ))
            elif isinstance(value, list):
                # IN filter: {"field": ["a", "b", "c"]}
                from qdrant_client.models import MatchAny
                conditions.append(FieldCondition(
                    key=key,
                    match=MatchAny(any=value),
                ))
            else:
                # Exact match: {"field": "value"}
                conditions.append(FieldCondition(
                    key=key,
                    match=MatchValue(value=value),
                ))

        return Filter(must=conditions)

    def delete(
        self,
        collection: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        if ids:
            self.client.delete(
                collection_name=collection,
                points_selector=ids,
            )
            return len(ids)
        elif filters:
            query_filter = self._build_filter(filters)
            self.client.delete(
                collection_name=collection,
                points_selector=query_filter,
            )
            return -1  # Unknown count
        return 0

    def count(self, collection: str) -> int:
        info = self.client.get_collection(collection)
        return info.points_count
```

### Pinecone Client Template

```python
# pinecone_store.py
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
import os

from vector_store import VectorStore, VectorRecord, SearchResult


class PineconeStore(VectorStore):
    """Pinecone vector store implementation."""

    def __init__(
        self,
        api_key: str = None,
        environment: str = None,
    ):
        api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=api_key)
        self._indexes: Dict[str, Any] = {}

    def create_collection(
        self,
        name: str,
        dimension: int,
        distance: str = "cosine",
        cloud: str = "aws",
        region: str = "us-east-1",
        **kwargs,
    ) -> None:
        self.pc.create_index(
            name=name,
            dimension=dimension,
            metric=distance,
            spec=ServerlessSpec(cloud=cloud, region=region),
        )

    def _get_index(self, name: str):
        if name not in self._indexes:
            self._indexes[name] = self.pc.Index(name)
        return self._indexes[name]

    def upsert(
        self,
        collection: str,
        records: List[VectorRecord],
        batch_size: int = 100,
        namespace: str = "",
    ) -> int:
        index = self._get_index(collection)
        count = 0

        vectors = [
            {
                "id": r.id,
                "values": r.vector,
                "metadata": r.metadata,
            }
            for r in records
        ]

        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            index.upsert(vectors=batch, namespace=namespace)
            count += len(batch)

        return count

    def search(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        include_vectors: bool = False,
        namespace: str = "",
    ) -> List[SearchResult]:
        index = self._get_index(collection)

        # Convert filters to Pinecone format
        filter_dict = None
        if filters:
            filter_dict = {k: {"$eq": v} for k, v in filters.items()}

        results = index.query(
            vector=query_vector,
            top_k=limit,
            filter=filter_dict,
            include_metadata=True,
            include_values=include_vectors,
            namespace=namespace,
        )

        return [
            SearchResult(
                id=m["id"],
                score=m["score"],
                metadata=m.get("metadata", {}),
                vector=m.get("values") if include_vectors else None,
            )
            for m in results["matches"]
        ]

    def delete(
        self,
        collection: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        namespace: str = "",
    ) -> int:
        index = self._get_index(collection)

        if ids:
            index.delete(ids=ids, namespace=namespace)
            return len(ids)
        elif filters:
            filter_dict = {k: {"$eq": v} for k, v in filters.items()}
            index.delete(filter=filter_dict, namespace=namespace)
            return -1
        return 0

    def count(self, collection: str) -> int:
        index = self._get_index(collection)
        stats = index.describe_index_stats()
        return stats["total_vector_count"]
```

### pgvector Client Template

```python
# pgvector_store.py
from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
import os

from vector_store import VectorStore, VectorRecord, SearchResult


class PgVectorStore(VectorStore):
    """pgvector (PostgreSQL) vector store implementation."""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        database: str = None,
        user: str = None,
        password: str = None,
        dsn: str = None,
    ):
        dsn = dsn or os.getenv("DATABASE_URL")

        if dsn:
            self.conn = psycopg2.connect(dsn)
        else:
            self.conn = psycopg2.connect(
                host=host or os.getenv("PGVECTOR_HOST", "localhost"),
                port=port or int(os.getenv("PGVECTOR_PORT", "5432")),
                database=database or os.getenv("PGVECTOR_DATABASE", "vectors"),
                user=user or os.getenv("PGVECTOR_USER", "vectordb"),
                password=password or os.getenv("PGVECTOR_PASSWORD"),
            )

        register_vector(self.conn)

    def create_collection(
        self,
        name: str,
        dimension: int,
        distance: str = "cosine",
        hnsw_m: int = 16,
        hnsw_ef_construct: int = 64,
        **kwargs,
    ) -> None:
        ops_map = {
            "cosine": "vector_cosine_ops",
            "euclidean": "vector_l2_ops",
            "dot": "vector_ip_ops",
        }

        with self.conn.cursor() as cur:
            # Create table
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id TEXT PRIMARY KEY,
                    embedding vector({dimension}),
                    metadata JSONB DEFAULT '{{}}'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create HNSW index
            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS {name}_embedding_idx
                ON {name} USING hnsw (embedding {ops_map[distance]})
                WITH (m = {hnsw_m}, ef_construction = {hnsw_ef_construct})
            """)

            # Create metadata GIN index
            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS {name}_metadata_idx
                ON {name} USING gin (metadata)
            """)

        self.conn.commit()

    def upsert(
        self,
        collection: str,
        records: List[VectorRecord],
        batch_size: int = 100,
    ) -> int:
        data = [
            (r.id, r.vector, psycopg2.extras.Json(r.metadata))
            for r in records
        ]

        with self.conn.cursor() as cur:
            execute_values(cur, f"""
                INSERT INTO {collection} (id, embedding, metadata)
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                    embedding = EXCLUDED.embedding,
                    metadata = EXCLUDED.metadata
            """, data)

        self.conn.commit()
        return len(records)

    def search(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        include_vectors: bool = False,
        distance: str = "cosine",
    ) -> List[SearchResult]:
        ops_map = {
            "cosine": "<=>",
            "euclidean": "<->",
            "dot": "<#>",
        }
        op = ops_map[distance]

        # Build WHERE clause
        where_parts = []
        params = [query_vector]

        if filters:
            for key, value in filters.items():
                where_parts.append(f"metadata->>%s = %s")
                params.extend([key, str(value)])

        where_clause = ""
        if where_parts:
            where_clause = "WHERE " + " AND ".join(where_parts)

        vector_select = ", embedding" if include_vectors else ""

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, metadata,
                       1 - (embedding {op} %s) AS score
                       {vector_select}
                FROM {collection}
                {where_clause}
                ORDER BY embedding {op} %s
                LIMIT %s
            """, params + [query_vector, limit])

            results = []
            for row in cur.fetchall():
                results.append(SearchResult(
                    id=row[0],
                    metadata=row[1] or {},
                    score=float(row[2]),
                    vector=list(row[3]) if include_vectors and len(row) > 3 else None,
                ))

        return results

    def delete(
        self,
        collection: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        with self.conn.cursor() as cur:
            if ids:
                cur.execute(f"""
                    DELETE FROM {collection}
                    WHERE id = ANY(%s)
                """, (ids,))
            elif filters:
                where_parts = []
                params = []
                for key, value in filters.items():
                    where_parts.append(f"metadata->>%s = %s")
                    params.extend([key, str(value)])

                cur.execute(f"""
                    DELETE FROM {collection}
                    WHERE {' AND '.join(where_parts)}
                """, params)

            count = cur.rowcount

        self.conn.commit()
        return count

    def count(self, collection: str) -> int:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {collection}")
            return cur.fetchone()[0]

    def close(self):
        self.conn.close()
```

---

## Integration Templates

### FastAPI Integration

```python
# api.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from qdrant_store import QdrantStore
from vector_store import VectorRecord

app = FastAPI(title="Vector Search API")

# Dependency
def get_store():
    store = QdrantStore()
    try:
        yield store
    finally:
        pass  # Cleanup if needed


class UpsertRequest(BaseModel):
    collection: str
    records: List[Dict[str, Any]]


class SearchRequest(BaseModel):
    collection: str
    query_vector: List[float]
    limit: int = 10
    filters: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


@app.post("/upsert")
async def upsert(
    request: UpsertRequest,
    store: QdrantStore = Depends(get_store),
):
    records = [
        VectorRecord(
            id=r["id"],
            vector=r["vector"],
            metadata=r.get("metadata", {}),
        )
        for r in request.records
    ]

    count = store.upsert(request.collection, records)
    return {"upserted": count}


@app.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    store: QdrantStore = Depends(get_store),
):
    results = store.search(
        collection=request.collection,
        query_vector=request.query_vector,
        limit=request.limit,
        filters=request.filters,
    )

    return SearchResponse(
        results=[
            {
                "id": r.id,
                "score": r.score,
                "metadata": r.metadata,
            }
            for r in results
        ]
    )


@app.delete("/delete/{collection}")
async def delete(
    collection: str,
    ids: Optional[List[str]] = None,
    store: QdrantStore = Depends(get_store),
):
    count = store.delete(collection, ids=ids)
    return {"deleted": count}
```

### LangChain Integration

```python
# langchain_integration.py
from langchain_core.vectorstores import VectorStore as LCVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from typing import List, Optional, Any

from qdrant_store import QdrantStore
from vector_store import VectorRecord


class CustomVectorStore(LCVectorStore):
    """Custom LangChain vector store using our unified interface."""

    def __init__(
        self,
        store: QdrantStore,
        collection: str,
        embedding: Embeddings,
    ):
        self.store = store
        self.collection = collection
        self.embedding = embedding

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        embedding: Embeddings,
        collection: str = "documents",
        **kwargs,
    ) -> "CustomVectorStore":
        store = QdrantStore(**kwargs)

        # Create collection
        sample_embedding = embedding.embed_query("sample")
        store.create_collection(
            name=collection,
            dimension=len(sample_embedding),
        )

        # Index documents
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        embeddings = embedding.embed_documents(texts)

        records = [
            VectorRecord(
                id=str(i),
                vector=emb,
                metadata={**meta, "text": text},
            )
            for i, (emb, meta, text) in enumerate(zip(embeddings, metadatas, texts))
        ]

        store.upsert(collection, records)

        return cls(store, collection, embedding)

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs,
    ) -> List[str]:
        metadatas = metadatas or [{} for _ in texts]
        embeddings = self.embedding.embed_documents(texts)

        ids = [str(i) for i in range(len(texts))]
        records = [
            VectorRecord(
                id=id_,
                vector=emb,
                metadata={**meta, "text": text},
            )
            for id_, emb, meta, text in zip(ids, embeddings, metadatas, texts)
        ]

        self.store.upsert(self.collection, records)
        return ids

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        **kwargs,
    ) -> List[Document]:
        query_embedding = self.embedding.embed_query(query)

        results = self.store.search(
            collection=self.collection,
            query_vector=query_embedding,
            limit=k,
            filters=kwargs.get("filter"),
        )

        return [
            Document(
                page_content=r.metadata.get("text", ""),
                metadata={k: v for k, v in r.metadata.items() if k != "text"},
            )
            for r in results
        ]

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        **kwargs,
    ) -> List[tuple[Document, float]]:
        query_embedding = self.embedding.embed_query(query)

        results = self.store.search(
            collection=self.collection,
            query_vector=query_embedding,
            limit=k,
            filters=kwargs.get("filter"),
        )

        return [
            (
                Document(
                    page_content=r.metadata.get("text", ""),
                    metadata={k: v for k, v in r.metadata.items() if k != "text"},
                ),
                r.score,
            )
            for r in results
        ]
```

### RAG Pipeline Template

```python
# rag_pipeline.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import openai

from qdrant_store import QdrantStore
from vector_store import VectorRecord


@dataclass
class RAGConfig:
    collection: str = "documents"
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o"
    top_k: int = 5
    score_threshold: float = 0.7


class RAGPipeline:
    """Simple RAG pipeline with vector search."""

    def __init__(
        self,
        store: QdrantStore,
        config: RAGConfig = None,
    ):
        self.store = store
        self.config = config or RAGConfig()
        self.client = openai.OpenAI()

    def embed(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=texts,
        )
        return [d.embedding for d in response.data]

    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        batch_size: int = 100,
    ) -> int:
        """Index documents into vector store."""
        records = []

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            texts = [d["text"] for d in batch]
            embeddings = self.embed_batch(texts)

            for doc, emb in zip(batch, embeddings):
                records.append(VectorRecord(
                    id=doc.get("id", str(len(records))),
                    vector=emb,
                    metadata={
                        "text": doc["text"],
                        **{k: v for k, v in doc.items() if k not in ["id", "text"]},
                    },
                ))

        return self.store.upsert(self.config.collection, records)

    def retrieve(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents."""
        query_embedding = self.embed(query)

        results = self.store.search(
            collection=self.config.collection,
            query_vector=query_embedding,
            limit=self.config.top_k,
            filters=filters,
            score_threshold=self.config.score_threshold,
        )

        return [
            {
                "text": r.metadata.get("text", ""),
                "score": r.score,
                "metadata": {k: v for k, v in r.metadata.items() if k != "text"},
            }
            for r in results
        ]

    def generate(
        self,
        query: str,
        context: List[Dict[str, Any]],
        system_prompt: str = None,
    ) -> str:
        """Generate response using retrieved context."""
        system_prompt = system_prompt or """You are a helpful assistant.
Answer the question based on the provided context.
If the context doesn't contain relevant information, say so."""

        context_text = "\n\n".join([
            f"[Source {i+1}] {c['text']}"
            for i, c in enumerate(context)
        ])

        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    def query(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        include_sources: bool = True,
    ) -> Dict[str, Any]:
        """End-to-end RAG query."""
        # Retrieve
        context = self.retrieve(query, filters)

        # Generate
        answer = self.generate(query, context)

        result = {"answer": answer}
        if include_sources:
            result["sources"] = context

        return result


# Usage example
if __name__ == "__main__":
    store = QdrantStore()

    # Create collection
    store.create_collection(
        name="documents",
        dimension=1536,
    )

    # Initialize pipeline
    rag = RAGPipeline(store)

    # Index documents
    documents = [
        {"id": "1", "text": "Python is a programming language.", "category": "tech"},
        {"id": "2", "text": "Machine learning uses algorithms.", "category": "tech"},
    ]
    rag.index_documents(documents)

    # Query
    result = rag.query("What is Python?")
    print(result["answer"])
```

---

*Templates v2.0*
*Part of vector-databases skill*
