# Microservices Templates

Production-ready templates for microservices development.

## Service Directory Structure

### Standard Service Layout

```
service-name/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   └── health.ts
│   │   └── middleware/
│   │       ├── auth.ts
│   │       ├── error-handler.ts
│   │       └── request-logger.ts
│   ├── domain/
│   │   ├── entities/
│   │   ├── repositories/
│   │   └── services/
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── messaging/
│   │   └── external/
│   ├── config/
│   │   └── index.ts
│   └── index.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── kustomization.yaml
│   ├── overlays/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── README.md
├── Dockerfile
├── docker-compose.yaml
├── openapi.yaml
├── .env.example
├── package.json
└── README.md
```

## Dockerfile Templates

### Node.js Service

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

# Set environment
ENV NODE_ENV=production
USER nodejs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Python Service (FastAPI)

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Install dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY src ./src

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go Service

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Production stage
FROM alpine:3.19 AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Copy binary
COPY --from=builder /app/server .

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./server"]
```

## Docker Compose Templates

### Development Environment

```yaml
# docker-compose.yaml
version: '3.8'

services:
  # Application service
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder  # Use builder stage for hot reload
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:password@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    volumes:
      - ./src:/app/src  # Hot reload
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  # PostgreSQL
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Kafka (with KRaft mode - no Zookeeper)
  kafka:
    image: bitnami/kafka:3.6
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    volumes:
      - kafka_data:/bitnami/kafka
    networks:
      - app-network

  # Kafka UI (optional)
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    ports:
      - "8080:8080"
    environment:
      - KAFKA_CLUSTERS_0_NAME=local
      - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092
    depends_on:
      - kafka
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:
  kafka_data:

networks:
  app-network:
    driver: bridge
```

### Multi-Service Development

```yaml
# docker-compose.services.yaml
version: '3.8'

services:
  # API Gateway
  gateway:
    build: ./services/gateway
    ports:
      - "8000:8000"
    environment:
      - USER_SERVICE_URL=http://user-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
      - PRODUCT_SERVICE_URL=http://product-service:3003
    depends_on:
      - user-service
      - order-service
      - product-service
    networks:
      - microservices

  # User Service
  user-service:
    build: ./services/user
    ports:
      - "3001:3001"
    environment:
      - DATABASE_URL=postgres://user:password@user-db:5432/users
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      user-db:
        condition: service_healthy
    networks:
      - microservices

  user-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: users
    volumes:
      - user_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d users"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - microservices

  # Order Service
  order-service:
    build: ./services/order
    ports:
      - "3002:3002"
    environment:
      - DATABASE_URL=postgres://user:password@order-db:5432/orders
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      order-db:
        condition: service_healthy
    networks:
      - microservices

  order-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: orders
    volumes:
      - order_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d orders"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - microservices

  # Product Service
  product-service:
    build: ./services/product
    ports:
      - "3003:3003"
    environment:
      - DATABASE_URL=postgres://user:password@product-db:5432/products
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      product-db:
        condition: service_healthy
    networks:
      - microservices

  product-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: products
    volumes:
      - product_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d products"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - microservices

  # Shared Kafka
  kafka:
    image: bitnami/kafka:3.6
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    networks:
      - microservices

volumes:
  user_db_data:
  order_db_data:
  product_db_data:

networks:
  microservices:
    driver: bridge
```

## Kubernetes Manifests

### Deployment Template

```yaml
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-name
  labels:
    app: service-name
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: service-name
  template:
    metadata:
      labels:
        app: service-name
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: service-name
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
        - name: service-name
          image: registry/service-name:latest
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: service-name-secrets
                  key: database-url
          envFrom:
            - configMapRef:
                name: service-name-config
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
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
                        - service-name
                topologyKey: kubernetes.io/hostname
```

### Service Template

```yaml
# k8s/base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: service-name
  labels:
    app: service-name
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
  selector:
    app: service-name
```

### ConfigMap Template

```yaml
# k8s/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-name-config
data:
  LOG_LEVEL: "info"
  METRICS_ENABLED: "true"
  TRACING_ENABLED: "true"
  TRACING_ENDPOINT: "http://jaeger-collector:14268/api/traces"
```

### HorizontalPodAutoscaler

```yaml
# k8s/base/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-name
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-name
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### PodDisruptionBudget

```yaml
# k8s/base/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: service-name
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: service-name
```

### NetworkPolicy

```yaml
# k8s/base/networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: service-name
spec:
  podSelector:
    matchLabels:
      app: service-name
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: kafka
      ports:
        - protocol: TCP
          port: 9092
```

### Kustomization Base

```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - hpa.yaml
  - pdb.yaml
  - networkpolicy.yaml

commonLabels:
  app.kubernetes.io/name: service-name
  app.kubernetes.io/component: backend
  app.kubernetes.io/part-of: platform
```

### Production Overlay

```yaml
# k8s/overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: production

patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
    target:
      kind: Deployment
      name: service-name

images:
  - name: registry/service-name
    newTag: v1.2.3

configMapGenerator:
  - name: service-name-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
```

## Health Check Templates

### Node.js/Express

```typescript
// src/api/routes/health.ts
import { Router, Request, Response } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';

const router = Router();

// Dependencies
let dbPool: Pool;
let redisClient: Redis;

export const initHealthChecks = (pool: Pool, redis: Redis) => {
  dbPool = pool;
  redisClient = redis;
};

// Liveness probe - is the process running?
router.get('/health/live', (req: Request, res: Response) => {
  res.status(200).json({ status: 'ok' });
});

// Readiness probe - can the service handle requests?
router.get('/health/ready', async (req: Request, res: Response) => {
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
  ]);

  const results = {
    database: checks[0].status === 'fulfilled' ? 'ok' : 'fail',
    redis: checks[1].status === 'fulfilled' ? 'ok' : 'fail',
  };

  const allHealthy = Object.values(results).every(v => v === 'ok');

  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'ok' : 'degraded',
    checks: results,
  });
});

async function checkDatabase(): Promise<void> {
  const client = await dbPool.connect();
  try {
    await client.query('SELECT 1');
  } finally {
    client.release();
  }
}

async function checkRedis(): Promise<void> {
  await redisClient.ping();
}

export default router;
```

### Go

```go
// internal/health/handler.go
package health

import (
    "context"
    "database/sql"
    "encoding/json"
    "net/http"
    "time"

    "github.com/redis/go-redis/v9"
)

type Handler struct {
    db    *sql.DB
    redis *redis.Client
}

func NewHandler(db *sql.DB, redis *redis.Client) *Handler {
    return &Handler{db: db, redis: redis}
}

type HealthResponse struct {
    Status string            `json:"status"`
    Checks map[string]string `json:"checks,omitempty"`
}

// Liveness - is the process running?
func (h *Handler) Liveness(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(HealthResponse{Status: "ok"})
}

// Readiness - can the service handle requests?
func (h *Handler) Readiness(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    checks := make(map[string]string)
    allHealthy := true

    // Check database
    if err := h.db.PingContext(ctx); err != nil {
        checks["database"] = "fail"
        allHealthy = false
    } else {
        checks["database"] = "ok"
    }

    // Check Redis
    if err := h.redis.Ping(ctx).Err(); err != nil {
        checks["redis"] = "fail"
        allHealthy = false
    } else {
        checks["redis"] = "ok"
    }

    status := "ok"
    statusCode := http.StatusOK
    if !allHealthy {
        status = "degraded"
        statusCode = http.StatusServiceUnavailable
    }

    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(HealthResponse{
        Status: status,
        Checks: checks,
    })
}
```

## OpenAPI Template

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: Service Name API
  version: 1.0.0
  description: Description of service functionality
  contact:
    name: Team Name
    email: team@company.com

servers:
  - url: http://localhost:3000
    description: Development
  - url: https://api.company.com/service
    description: Production

tags:
  - name: Health
    description: Health check endpoints
  - name: Resources
    description: Main resource operations

paths:
  /health/live:
    get:
      summary: Liveness probe
      tags: [Health]
      responses:
        '200':
          description: Service is running
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'

  /health/ready:
    get:
      summary: Readiness probe
      tags: [Health]
      responses:
        '200':
          description: Service is ready
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'
        '503':
          description: Service is not ready
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'

  /api/v1/resources:
    get:
      summary: List resources
      tags: [Resources]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: List of resources
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'

    post:
      summary: Create resource
      tags: [Resources]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceRequest'
      responses:
        '201':
          description: Resource created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'

  /api/v1/resources/{id}:
    get:
      summary: Get resource by ID
      tags: [Resources]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Resource details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    HealthResponse:
      type: object
      properties:
        status:
          type: string
          enum: [ok, degraded]
        checks:
          type: object
          additionalProperties:
            type: string
            enum: [ok, fail]

    Resource:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
      required:
        - id
        - name
        - createdAt
        - updatedAt

    CreateResourceRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
      required:
        - name

    ResourceList:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## Related Files

- [README.md](README.md) - Architecture overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [llm-prompts.md](llm-prompts.md) - AI-assisted design prompts
