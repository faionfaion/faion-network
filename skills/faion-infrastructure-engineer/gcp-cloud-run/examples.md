# Cloud Run Examples

## Services

### Basic Service Deployment

```bash
# Deploy from source (Buildpacks)
gcloud run deploy my-service \
    --source=. \
    --region=us-central1 \
    --allow-unauthenticated

# Deploy from container image
gcloud run deploy my-service \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1 \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated
```

### Production Service Deployment

```bash
gcloud run deploy my-api \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-api:v1.2.3 \
    --region=us-central1 \
    --service-account=my-api-sa@my-project.iam.gserviceaccount.com \
    --memory=2Gi \
    --cpu=2 \
    --concurrency=80 \
    --min-instances=1 \
    --max-instances=100 \
    --timeout=300 \
    --set-env-vars=ENV=production,LOG_LEVEL=info \
    --set-secrets=DATABASE_URL=db-connection-string:latest,API_KEY=api-key:latest \
    --cpu-boost \
    --ingress=internal-and-cloud-load-balancing \
    --no-allow-unauthenticated
```

### Service with Direct VPC Egress

```bash
gcloud run deploy my-service \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-service:v1 \
    --region=us-central1 \
    --network=my-vpc \
    --subnet=my-subnet \
    --vpc-egress=all-traffic \
    --no-allow-unauthenticated
```

### Service with Health Checks

```bash
gcloud run deploy my-service \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-service:v1 \
    --region=us-central1 \
    --startup-probe-http-get-path=/health \
    --startup-probe-initial-delay-seconds=5 \
    --startup-probe-timeout-seconds=3 \
    --startup-probe-period-seconds=10 \
    --startup-probe-failure-threshold=3 \
    --liveness-probe-http-get-path=/health \
    --liveness-probe-period-seconds=30 \
    --liveness-probe-timeout-seconds=5 \
    --liveness-probe-failure-threshold=3
```

---

## Jobs

### Basic Job Creation

```bash
# Create job
gcloud run jobs create my-job \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-job:v1 \
    --region=us-central1 \
    --task-timeout=600 \
    --max-retries=3

# Execute job
gcloud run jobs execute my-job --region=us-central1

# Execute with overrides
gcloud run jobs execute my-job \
    --region=us-central1 \
    --update-env-vars=BATCH_SIZE=1000
```

### Parallel Job

```bash
gcloud run jobs create batch-processor \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/processor:v1 \
    --region=us-central1 \
    --tasks=100 \
    --parallelism=10 \
    --task-timeout=3600 \
    --max-retries=3 \
    --memory=4Gi \
    --cpu=2 \
    --set-env-vars=BUCKET=my-data-bucket
```

### Job Task Index Usage (Python)

```python
import os

def process_batch():
    task_index = int(os.environ.get('CLOUD_RUN_TASK_INDEX', 0))
    task_count = int(os.environ.get('CLOUD_RUN_TASK_COUNT', 1))

    # Calculate work slice
    total_items = 10000
    items_per_task = total_items // task_count
    start = task_index * items_per_task
    end = start + items_per_task

    if task_index == task_count - 1:
        end = total_items  # Last task handles remainder

    print(f"Task {task_index}: Processing items {start} to {end}")

    # Process items
    for i in range(start, end):
        process_item(i)
```

### Scheduled Job with Cloud Scheduler

```bash
# Create job
gcloud run jobs create daily-report \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/report:v1 \
    --region=us-central1 \
    --task-timeout=1800

# Create scheduler
gcloud scheduler jobs create http daily-report-trigger \
    --location=us-central1 \
    --schedule="0 6 * * *" \
    --time-zone="Europe/Kyiv" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/my-project/jobs/daily-report:run" \
    --oauth-service-account-email=scheduler-sa@my-project.iam.gserviceaccount.com
```

---

## Traffic Management

### Blue-Green Deployment

```bash
# Deploy green revision with no traffic
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:v2 \
    --region=us-central1 \
    --no-traffic \
    --tag=green

# Test green revision
curl https://green---my-app-xxxxx-uc.a.run.app

# Shift 100% traffic to green
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=green=100
```

### Canary Deployment

```bash
# Deploy canary with 5% traffic
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:v2 \
    --region=us-central1 \
    --tag=canary

gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=canary=5

# Gradually increase (10%, 25%, 50%, 100%)
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=canary=25

# Full rollout
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-latest
```

### Rollback

```bash
# List revisions
gcloud run revisions list --service=my-app --region=us-central1

# Rollback to specific revision
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-revisions=my-app-00005-abc=100
```

---

## Multi-Container (Sidecars)

### Service with Cloud SQL Proxy Sidecar

```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/container-dependencies: '{"my-app":["cloud-sql-proxy"]}'
    spec:
      serviceAccountName: my-app-sa@my-project.iam.gserviceaccount.com
      containers:
        - name: my-app
          image: us-central1-docker.pkg.dev/my-project/my-repo/my-app:v1
          ports:
            - containerPort: 8080
          env:
            - name: DB_HOST
              value: localhost
            - name: DB_PORT
              value: "5432"
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
        - name: cloud-sql-proxy
          image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.8.0
          args:
            - "--structured-logs"
            - "my-project:us-central1:my-db"
          startupProbe:
            tcpSocket:
              port: 5432
            initialDelaySeconds: 0
            periodSeconds: 1
            failureThreshold: 30
```

```bash
gcloud run services replace service.yaml --region=us-central1
```

### Service with Prometheus Sidecar

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/container-dependencies: '{"my-app":["collector"]}'
    spec:
      containers:
        - name: my-app
          image: us-central1-docker.pkg.dev/my-project/my-repo/my-app:v1
          ports:
            - containerPort: 8080
        - name: collector
          image: us-docker.pkg.dev/cloud-ops-agents-artifacts/cloud-run-gmp-sidecar/cloud-run-gmp-sidecar:1
          env:
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: http://localhost:4317
```

---

## Security

### Enable Binary Authorization

```bash
# Enable Binary Authorization on service
gcloud run services update my-service \
    --region=us-central1 \
    --binary-authorization=default

# Create attestor
gcloud container binauthz attestors create my-attestor \
    --attestation-authority-note=my-attestor-note \
    --attestation-authority-note-project=my-project

# Create attestation
gcloud container binauthz attestations create \
    --attestor=my-attestor \
    --artifact-url=us-central1-docker.pkg.dev/my-project/my-repo/my-image@sha256:abc123 \
    --signature-file=signature.pgp \
    --pgp-key-fingerprint=ABC123
```

### Enable CMEK

```bash
# Create KMS key
gcloud kms keyrings create my-keyring --location=us-central1
gcloud kms keys create my-key \
    --keyring=my-keyring \
    --location=us-central1 \
    --purpose=encryption

# Grant Cloud Run access to key
gcloud kms keys add-iam-policy-binding my-key \
    --keyring=my-keyring \
    --location=us-central1 \
    --member="serviceAccount:service-PROJECT_NUMBER@serverless-robot-prod.iam.gserviceaccount.com" \
    --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"

# Deploy with CMEK
gcloud run deploy my-service \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-service:v1 \
    --region=us-central1 \
    --key=projects/my-project/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-key
```

### IAM Configuration

```bash
# Create dedicated service account
gcloud iam service-accounts create my-service-sa \
    --display-name="My Service Account"

# Grant minimal permissions
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:my-service-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Allow specific users to invoke
gcloud run services add-iam-policy-binding my-service \
    --region=us-central1 \
    --member="user:developer@example.com" \
    --role="roles/run.invoker"

# Allow service account to invoke
gcloud run services add-iam-policy-binding my-service \
    --region=us-central1 \
    --member="serviceAccount:caller-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/run.invoker"
```

---

## Management Commands

### List and Describe

```bash
# List services
gcloud run services list --region=us-central1

# Describe service
gcloud run services describe my-service --region=us-central1

# Get service URL
gcloud run services describe my-service \
    --region=us-central1 \
    --format='value(status.url)'

# List jobs
gcloud run jobs list --region=us-central1

# Describe job
gcloud run jobs describe my-job --region=us-central1

# List job executions
gcloud run jobs executions list --job=my-job --region=us-central1
```

### Logs

```bash
# Service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=my-service" \
    --limit=100 \
    --format="table(timestamp, textPayload)"

# Job logs
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=my-job" \
    --limit=100

# Stream logs
gcloud beta run services logs tail my-service --region=us-central1
```

### Delete

```bash
# Delete service
gcloud run services delete my-service --region=us-central1

# Delete job
gcloud run jobs delete my-job --region=us-central1

# Delete all revisions except latest
gcloud run revisions list --service=my-service --region=us-central1 \
    --format="value(name)" | tail -n +2 | \
    xargs -I {} gcloud run revisions delete {} --region=us-central1 --quiet
```
