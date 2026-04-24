# Vector Database Setup Templates

Docker Compose, Kubernetes, Terraform, and configuration templates for vector database deployments.

---

## Table of Contents

- [Docker Compose Templates](#docker-compose-templates)
- [Kubernetes Templates](#kubernetes-templates)
- [Helm Values Templates](#helm-values-templates)
- [Terraform Templates](#terraform-templates)
- [Configuration File Templates](#configuration-file-templates)
- [Environment Templates](#environment-templates)

---

## Docker Compose Templates

### Qdrant Production

```yaml
# docker-compose.qdrant.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:v1.7.4
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
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
      - QDRANT__TELEMETRY_DISABLED=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

volumes:
  qdrant_storage:
    driver: local
```

### Weaviate Production

```yaml
# docker-compose.weaviate.yml
version: '3.8'

services:
  weaviate:
    image: semitechnologies/weaviate:1.24.1
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
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

volumes:
  weaviate_data:
    driver: local
```

### Milvus Standalone

```yaml
# docker-compose.milvus.yml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.5
    container_name: milvus-etcd
    restart: unless-stopped
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - etcd_data:/etcd
    command: >
      etcd
      -advertise-client-urls=http://127.0.0.1:2379
      -listen-client-urls=http://0.0.0.0:2379
      --data-dir=/etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    container_name: milvus-minio
    restart: unless-stopped
    environment:
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY:-minioadmin}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY:-minioadmin}
    volumes:
      - minio_data:/data
    command: minio server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  milvus:
    image: milvusdb/milvus:v2.3.4
    container_name: milvus
    restart: unless-stopped
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY:-minioadmin}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY:-minioadmin}
    volumes:
      - milvus_data:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      etcd:
        condition: service_healthy
      minio:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      timeout: 20s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 8G

volumes:
  etcd_data:
  minio_data:
  milvus_data:
```

### pgvector Production

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
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-vectordb} -d ${POSTGRES_DB:-vectors}"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    command: >
      postgres
      -c shared_buffers=1GB
      -c effective_cache_size=3GB
      -c maintenance_work_mem=512MB
      -c work_mem=64MB

volumes:
  pgvector_data:
    driver: local
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

### Chroma Server

```yaml
# docker-compose.chroma.yml
version: '3.8'

services:
  chroma:
    image: chromadb/chroma:0.4.22
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
    driver: local
```

---

## Kubernetes Templates

### Qdrant StatefulSet

```yaml
# qdrant-k8s.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vector-db
---
apiVersion: v1
kind: Secret
metadata:
  name: qdrant-secrets
  namespace: vector-db
type: Opaque
stringData:
  api-key: "your-secure-api-key"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: qdrant-config
  namespace: vector-db
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
    telemetry_disabled: true
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant
  namespace: vector-db
spec:
  serviceName: qdrant
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
            - name: QDRANT__SERVICE__API_KEY
              valueFrom:
                secretKeyRef:
                  name: qdrant-secrets
                  key: api-key
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
        - name: config
          configMap:
            name: qdrant-config
  volumeClaimTemplates:
    - metadata:
        name: storage
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        resources:
          requests:
            storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: qdrant
  namespace: vector-db
spec:
  type: ClusterIP
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
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: qdrant-ingress
  namespace: vector-db
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - qdrant.example.com
      secretName: qdrant-tls
  rules:
    - host: qdrant.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: qdrant
                port:
                  number: 6333
```

### Weaviate StatefulSet

```yaml
# weaviate-k8s.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vector-db
---
apiVersion: v1
kind: Secret
metadata:
  name: weaviate-secrets
  namespace: vector-db
type: Opaque
stringData:
  api-key: "your-secure-api-key"
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: weaviate
  namespace: vector-db
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
            - name: QUERY_DEFAULTS_LIMIT
              value: "25"
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
        storageClassName: standard
        resources:
          requests:
            storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: weaviate
  namespace: vector-db
spec:
  type: ClusterIP
  selector:
    app: weaviate
  ports:
    - name: http
      port: 8080
      targetPort: 8080
    - name: grpc
      port: 50051
      targetPort: 50051
```

### pgvector Deployment

```yaml
# pgvector-k8s.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vector-db
---
apiVersion: v1
kind: Secret
metadata:
  name: pgvector-secrets
  namespace: vector-db
type: Opaque
stringData:
  postgres-password: "your-secure-password"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: pgvector-init
  namespace: vector-db
data:
  init.sql: |
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
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: pgvector
  namespace: vector-db
spec:
  serviceName: pgvector
  replicas: 1
  selector:
    matchLabels:
      app: pgvector
  template:
    metadata:
      labels:
        app: pgvector
    spec:
      containers:
        - name: postgres
          image: pgvector/pgvector:pg16
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_USER
              value: "vectordb"
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: pgvector-secrets
                  key: postgres-password
            - name: POSTGRES_DB
              value: "vectors"
          args:
            - "-c"
            - "shared_buffers=1GB"
            - "-c"
            - "effective_cache_size=3GB"
            - "-c"
            - "maintenance_work_mem=512MB"
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
            - name: init-scripts
              mountPath: /docker-entrypoint-initdb.d
          resources:
            requests:
              memory: "2Gi"
              cpu: "500m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - vectordb
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - vectordb
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: init-scripts
          configMap:
            name: pgvector-init
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        resources:
          requests:
            storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: pgvector
  namespace: vector-db
spec:
  type: ClusterIP
  selector:
    app: pgvector
  ports:
    - port: 5432
      targetPort: 5432
```

---

## Helm Values Templates

### Qdrant Helm Values

```yaml
# values.qdrant.yaml
replicaCount: 3

image:
  repository: qdrant/qdrant
  tag: v1.7.4
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

apiKey:
  existingSecret: qdrant-secrets
  secretKey: api-key

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

nodeSelector: {}

tolerations: []

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - qdrant
          topologyKey: kubernetes.io/hostname
```

### Weaviate Helm Values

```yaml
# values.weaviate.yaml
replicas: 3

image:
  registry: docker.io
  repo: semitechnologies/weaviate
  tag: 1.24.1

service:
  type: ClusterIP
  port: 80
  grpcPort: 50051

persistence:
  enabled: true
  size: 100Gi
  storageClassName: fast-ssd

resources:
  requests:
    cpu: '1000m'
    memory: '4Gi'
  limits:
    cpu: '4000m'
    memory: '8Gi'

env:
  AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
  AUTHENTICATION_APIKEY_ENABLED: 'true'
  PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
  DEFAULT_VECTORIZER_MODULE: 'none'
  QUERY_DEFAULTS_LIMIT: '25'

extraSecretEnv:
  - name: AUTHENTICATION_APIKEY_ALLOWED_KEYS
    secretKeyRef:
      name: weaviate-secrets
      key: api-key

modules:
  text2vec-openai:
    enabled: false
  generative-openai:
    enabled: false

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: weaviate.example.com
  tls:
    - secretName: weaviate-tls
      hosts:
        - weaviate.example.com

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - weaviate
          topologyKey: kubernetes.io/hostname
```

---

## Terraform Templates

### AWS RDS pgvector

```hcl
# pgvector-aws.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID for the database"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for the database"
  type        = list(string)
}

resource "aws_db_subnet_group" "pgvector" {
  name       = "pgvector-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "pgvector-subnet-group"
  }
}

resource "aws_security_group" "pgvector" {
  name        = "pgvector-sg"
  description = "Security group for pgvector RDS"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Adjust as needed
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "pgvector-sg"
  }
}

resource "aws_db_instance" "pgvector" {
  identifier             = "pgvector"
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = "db.r6g.large"
  allocated_storage      = 100
  max_allocated_storage  = 500
  storage_type           = "gp3"
  storage_encrypted      = true

  db_name  = "vectors"
  username = "vectordb"
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.pgvector.name
  vpc_security_group_ids = [aws_security_group.pgvector.id]

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  multi_az               = true
  deletion_protection    = true
  skip_final_snapshot    = false
  final_snapshot_identifier = "pgvector-final-snapshot"

  performance_insights_enabled = true
  monitoring_interval          = 60

  parameter_group_name = aws_db_parameter_group.pgvector.name

  tags = {
    Name        = "pgvector"
    Environment = "production"
  }
}

resource "aws_db_parameter_group" "pgvector" {
  family = "postgres16"
  name   = "pgvector-params"

  parameter {
    name  = "shared_buffers"
    value = "{DBInstanceClassMemory/4}"
  }

  parameter {
    name  = "maintenance_work_mem"
    value = "524288"  # 512MB in KB
  }

  parameter {
    name  = "work_mem"
    value = "65536"  # 64MB in KB
  }

  parameter {
    name  = "shared_preload_libraries"
    value = "vector"
  }

  tags = {
    Name = "pgvector-params"
  }
}

output "endpoint" {
  value = aws_db_instance.pgvector.endpoint
}

output "port" {
  value = aws_db_instance.pgvector.port
}
```

### GCP Cloud SQL pgvector

```hcl
# pgvector-gcp.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "network_id" {
  description = "VPC Network ID"
  type        = string
}

resource "google_sql_database_instance" "pgvector" {
  name             = "pgvector"
  project          = var.project_id
  region           = var.region
  database_version = "POSTGRES_16"

  settings {
    tier              = "db-custom-4-16384"  # 4 vCPU, 16GB RAM
    availability_type = "REGIONAL"

    disk_size       = 100
    disk_type       = "PD_SSD"
    disk_autoresize = true

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
    }

    database_flags {
      name  = "cloudsql.enable_pgvector"
      value = "on"
    }

    database_flags {
      name  = "maintenance_work_mem"
      value = "524288"  # 512MB
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "vectors" {
  name     = "vectors"
  instance = google_sql_database_instance.pgvector.name
  project  = var.project_id
}

resource "google_sql_user" "vectordb" {
  name     = "vectordb"
  instance = google_sql_database_instance.pgvector.name
  password = var.db_password
  project  = var.project_id
}

output "connection_name" {
  value = google_sql_database_instance.pgvector.connection_name
}

output "private_ip" {
  value = google_sql_database_instance.pgvector.private_ip_address
}
```

---

## Configuration File Templates

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
    memmap_threshold_kb: 1000000  # 1GB

service:
  http_port: 6333
  grpc_port: 6334
  max_request_size_mb: 32
  enable_tls: false
  # api_key: set via environment variable

cluster:
  enabled: false
  # consensus:
  #   tick_period_ms: 100

hnsw_index:
  m: 16
  ef_construct: 100
  full_scan_threshold: 10000
  max_indexing_threads: 0  # Auto-detect
  on_disk: false

quantization:
  scalar:
    type: int8
    quantile: 0.99
    always_ram: true

telemetry_disabled: true
```

### Weaviate Schema Template

```json
{
  "classes": [
    {
      "class": "Document",
      "description": "A document with vector embeddings",
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
          "description": "Document content",
          "moduleConfig": {
            "text2vec-openai": {
              "skip": true
            }
          }
        },
        {
          "name": "source",
          "dataType": ["text"],
          "description": "Source file path",
          "indexFilterable": true,
          "indexSearchable": false
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
        "indexTimestamps": true,
        "indexNullState": true,
        "indexPropertyLength": true
      }
    }
  ]
}
```

---

## Environment Templates

### Development Environment

```bash
# .env.development
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=dev-api-key

# Weaviate
WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080
WEAVIATE_API_KEY=dev-api-key

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# pgvector
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=vectordb
POSTGRES_PASSWORD=vectordb
POSTGRES_DB=vectors

# Pinecone
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=us-east-1

# Chroma
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### Production Environment

```bash
# .env.production
# Qdrant
QDRANT_URL=https://qdrant.example.com
QDRANT_API_KEY=${QDRANT_API_KEY}  # From secrets manager

# Weaviate
WEAVIATE_URL=https://weaviate.example.com
WEAVIATE_API_KEY=${WEAVIATE_API_KEY}

# Milvus
MILVUS_HOST=milvus.vector-db.svc.cluster.local
MILVUS_PORT=19530
MILVUS_TOKEN=${MILVUS_TOKEN}

# pgvector
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}?sslmode=require

# Pinecone
PINECONE_API_KEY=${PINECONE_API_KEY}
PINECONE_INDEX=production

# General
VECTOR_DB_PROVIDER=qdrant
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
```

---

*Templates v1.0*
*Part of vector-database-setup skill*
