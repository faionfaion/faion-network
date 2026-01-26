# Cloud Run Templates

## Terraform Templates

### Basic Service

```hcl
# variables.tf
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
}

variable "image" {
  description = "Container image URL"
  type        = string
}

# main.tf
resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.image

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      ports {
        container_port = 8080
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Allow unauthenticated access
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_v2_service.default.uri
}
```

### Production Service with VPC and Secrets

```hcl
# variables.tf
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "service_name" {
  type = string
}

variable "image" {
  type = string
}

variable "vpc_network" {
  type = string
}

variable "vpc_subnet" {
  type = string
}

variable "service_account_email" {
  type = string
}

# main.tf
resource "google_cloud_run_v2_service" "production" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    service_account = var.service_account_email

    vpc_access {
      network_interfaces {
        network    = var.vpc_network
        subnetwork = var.vpc_subnet
      }
      egress = "ALL_TRAFFIC"
    }

    containers {
      image = var.image

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
        cpu_idle          = false
        startup_cpu_boost = true
      }

      ports {
        container_port = 8080
      }

      env {
        name  = "ENV"
        value = "production"
      }

      env {
        name  = "LOG_LEVEL"
        value = "info"
      }

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = "database-url"
            version = "latest"
          }
        }
      }

      env {
        name = "API_KEY"
        value_source {
          secret_key_ref {
            secret  = "api-key"
            version = "latest"
          }
        }
      }

      startup_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        timeout_seconds       = 3
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        period_seconds    = 30
        timeout_seconds   = 5
        failure_threshold = 3
      }
    }

    scaling {
      min_instance_count = 1
      max_instance_count = 100
    }

    max_instance_request_concurrency = 80
    timeout                          = "300s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# IAM for specific invokers
resource "google_cloud_run_v2_service_iam_member" "invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.production.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${var.service_account_email}"
}
```

### Cloud Run Job

```hcl
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "job_name" {
  type = string
}

variable "image" {
  type = string
}

variable "task_count" {
  type    = number
  default = 1
}

variable "parallelism" {
  type    = number
  default = 1
}

resource "google_cloud_run_v2_job" "batch" {
  name     = var.job_name
  location = var.region

  template {
    task_count  = var.task_count
    parallelism = var.parallelism

    template {
      containers {
        image = var.image

        resources {
          limits = {
            cpu    = "2"
            memory = "4Gi"
          }
        }

        env {
          name  = "BUCKET"
          value = "my-data-bucket"
        }
      }

      max_retries = 3
      timeout     = "3600s"
    }
  }
}

# Cloud Scheduler for scheduled execution
resource "google_cloud_scheduler_job" "trigger" {
  name             = "${var.job_name}-trigger"
  region           = var.region
  schedule         = "0 6 * * *"
  time_zone        = "Europe/Kyiv"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.job_name}:run"

    oauth_token {
      service_account_email = "scheduler-sa@${var.project_id}.iam.gserviceaccount.com"
    }
  }
}
```

### Service with Cloud SQL Sidecar

```hcl
resource "google_cloud_run_v2_service" "with_cloudsql" {
  name     = "my-app"
  location = var.region

  template {
    service_account = var.service_account_email

    containers {
      name  = "my-app"
      image = var.image

      ports {
        container_port = 8080
      }

      env {
        name  = "DB_HOST"
        value = "localhost"
      }

      env {
        name  = "DB_PORT"
        value = "5432"
      }

      depends_on = ["cloud-sql-proxy"]

      startup_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }
    }

    containers {
      name  = "cloud-sql-proxy"
      image = "gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.8.0"

      args = [
        "--structured-logs",
        "${var.project_id}:${var.region}:${var.database_instance}"
      ]

      startup_probe {
        tcp_socket {
          port = 5432
        }
        initial_delay_seconds = 0
        period_seconds        = 1
        failure_threshold     = 30
      }
    }
  }
}
```

---

## YAML Templates

### Basic Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
  labels:
    app: my-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
        - image: us-central1-docker.pkg.dev/my-project/my-repo/my-service:v1
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "1"
              memory: 512Mi
```

### Production Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-api
  labels:
    app: my-api
    environment: production
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/startup-cpu-boost: "true"
        run.googleapis.com/vpc-access-egress: all-traffic
        run.googleapis.com/network-interfaces: '[{"network":"my-vpc","subnetwork":"my-subnet"}]'
    spec:
      serviceAccountName: my-api-sa@my-project.iam.gserviceaccount.com
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
        - name: my-api
          image: us-central1-docker.pkg.dev/my-project/my-repo/my-api:v1
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "2"
              memory: 2Gi
          env:
            - name: ENV
              value: production
            - name: LOG_LEVEL
              value: info
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-url
                  key: latest
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-key
                  key: latest
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            periodSeconds: 30
            timeoutSeconds: 5
            failureThreshold: 3
```

### Cloud Run Job

```yaml
apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: batch-processor
spec:
  template:
    spec:
      taskCount: 100
      parallelism: 10
      template:
        spec:
          maxRetries: 3
          timeoutSeconds: 3600
          containers:
            - image: us-central1-docker.pkg.dev/my-project/my-repo/processor:v1
              resources:
                limits:
                  cpu: "2"
                  memory: 4Gi
              env:
                - name: BUCKET
                  value: my-data-bucket
```

### Multi-Container Service

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/container-dependencies: '{"my-app":["cloud-sql-proxy","otel-collector"]}'
    spec:
      serviceAccountName: my-app-sa@my-project.iam.gserviceaccount.com
      containers:
        # Main application container
        - name: my-app
          image: us-central1-docker.pkg.dev/my-project/my-repo/my-app:v1
          ports:
            - containerPort: 8080
          env:
            - name: DB_HOST
              value: localhost
            - name: DB_PORT
              value: "5432"
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http://localhost:4317
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3

        # Cloud SQL Proxy sidecar
        - name: cloud-sql-proxy
          image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.8.0
          args:
            - "--structured-logs"
            - "my-project:us-central1:my-db"
          resources:
            limits:
              cpu: "0.5"
              memory: 256Mi
          startupProbe:
            tcpSocket:
              port: 5432
            initialDelaySeconds: 0
            periodSeconds: 1
            failureThreshold: 30

        # OpenTelemetry Collector sidecar
        - name: otel-collector
          image: otel/opentelemetry-collector:0.90.0
          args: ["--config=/etc/otel/config.yaml"]
          resources:
            limits:
              cpu: "0.5"
              memory: 256Mi
          volumeMounts:
            - name: otel-config
              mountPath: /etc/otel

      volumes:
        - name: otel-config
          secret:
            secretName: otel-collector-config
```

---

## Dockerfile Templates

### Python FastAPI

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Cloud Run uses PORT environment variable
ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Node.js

```dockerfile
FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Create non-root user
USER node

# Cloud Run uses PORT environment variable
ENV PORT=8080
EXPOSE 8080

CMD ["node", "server.js"]
```

### Go

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /server ./cmd/server

# Runtime stage
FROM gcr.io/distroless/static-debian12

COPY --from=builder /server /server

USER nonroot:nonroot

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Java Spring Boot

```dockerfile
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy JAR
COPY target/*.jar app.jar

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar", "--server.port=${PORT}"]
```

---

## cloudbuild.yaml Templates

### Build and Deploy

```yaml
steps:
  # Build container image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:latest'
      - '.'

  # Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '--all-tags'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}'

  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE}'
      - '--image=${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}'
      - '--region=${_REGION}'
      - '--platform=managed'

substitutions:
  _REGION: us-central1
  _REPO: my-repo
  _SERVICE: my-service

options:
  logging: CLOUD_LOGGING_ONLY
```

### Build, Test, and Deploy with Blue-Green

```yaml
steps:
  # Run tests
  - name: 'python:3.12'
    entrypoint: bash
    args:
      - '-c'
      - |
        pip install -r requirements.txt
        pytest tests/

  # Build container image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}'
      - '.'

  # Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}'

  # Deploy without traffic
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE}'
      - '--image=${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/${_SERVICE}:${SHORT_SHA}'
      - '--region=${_REGION}'
      - '--no-traffic'
      - '--tag=green'

  # Shift traffic to new revision
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'services'
      - 'update-traffic'
      - '${_SERVICE}'
      - '--region=${_REGION}'
      - '--to-tags=green=100'

substitutions:
  _REGION: us-central1
  _REPO: my-repo
  _SERVICE: my-service
```
