---
id: cd-pipelines
name: "CD Pipelines & Deployment"
domain: DEV
skill: faion-software-developer
category: "development-practices"
parent: continuous-delivery
---

# CD Pipelines & Deployment Strategies

## CD Pipeline Implementation

### GitHub Actions Example

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Build and Unit Test
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest tests/unit --cov=src --cov-fail-under=80

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  # Stage 2: Integration Tests
  integration:
    needs: build
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4

      - name: Run integration tests
        run: pytest tests/integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  # Stage 3: Deploy to Staging
  staging:
    needs: integration
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: kubectl rollout status deployment/app -n staging --timeout=300s

      - name: Run smoke tests
        run: ./scripts/smoke-tests.sh https://staging.example.com

  # Stage 4: E2E Tests on Staging
  e2e:
    needs: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run E2E tests
        uses: cypress-io/github-action@v6
        with:
          config: baseUrl=https://staging.example.com

  # Stage 5: Deploy to Production (Manual Approval)
  production:
    needs: e2e
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

      - name: Wait for rollout
        run: kubectl rollout status deployment/app -n production --timeout=300s

      - name: Run production smoke tests
        run: ./scripts/smoke-tests.sh https://example.com

      - name: Notify deployment
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "Deployed ${{ github.sha }} to production"}'
```

## Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue-Green: Two identical environments
# Switch traffic instantly

# Kubernetes example
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
    version: green  # Switch to blue for rollback
  ports:
    - port: 80

---
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: blue
  template:
    metadata:
      labels:
        app: app
        version: blue
    spec:
      containers:
        - name: app
          image: app:v1.0.0

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: green
  template:
    metadata:
      labels:
        app: app
        version: green
    spec:
      containers:
        - name: app
          image: app:v1.1.0
```

### Canary Deployment

```yaml
# Canary: Gradual traffic shift
# Catch issues before full rollout

# Using Istio for traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app
spec:
  hosts:
    - app
  http:
    - route:
        # 90% to stable
        - destination:
            host: app
            subset: stable
          weight: 90
        # 10% to canary
        - destination:
            host: app
            subset: canary
          weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: app
spec:
  host: app
  subsets:
    - name: stable
      labels:
        version: v1.0.0
    - name: canary
      labels:
        version: v1.1.0
```

### Rolling Deployment

```yaml
# Rolling: Gradual pod replacement
# Default Kubernetes strategy

apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max pods over desired
      maxUnavailable: 1  # Max pods unavailable
  template:
    spec:
      containers:
        - name: app
          image: app:v1.1.0
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
```

## Monitoring and Rollback

### Health Checks

```python
# app/health.py
from fastapi import APIRouter, Response
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health():
    """
    Kubernetes readiness/liveness probe.
    CD pipeline checks this after deployment.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/ready")
async def readiness():
    """
    Readiness probe: Can accept traffic?
    Checks all dependencies.
    """
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "external_api": await check_external_api(),
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return Response(
        content=json.dumps({"checks": checks, "ready": all_healthy}),
        status_code=status_code,
        media_type="application/json"
    )
```

### Automatic Rollback

```yaml
# Rollback on deployment failure
# .github/workflows/cd.yml (addition)

production:
  steps:
    - name: Deploy
      id: deploy
      run: kubectl set image ...

    - name: Wait for rollout
      id: rollout
      run: kubectl rollout status ...
      continue-on-error: true

    - name: Smoke tests
      id: smoke
      run: ./scripts/smoke-tests.sh
      continue-on-error: true

    - name: Rollback on failure
      if: steps.rollout.outcome == 'failure' || steps.smoke.outcome == 'failure'
      run: |
        echo "Deployment failed, rolling back..."
        kubectl rollout undo deployment/app -n production
        exit 1
```

### Deployment Metrics

```python
# Track deployment metrics
# Send to monitoring (Datadog, Prometheus, etc.)

from datadog import statsd

def track_deployment(version: str, success: bool, duration: float):
    """Track deployment metrics for DORA."""

    # Deployment frequency
    statsd.increment(
        "deployment.count",
        tags=[f"version:{version}", f"success:{success}"]
    )

    # Lead time (separate tracking from commit time)
    statsd.histogram(
        "deployment.duration_seconds",
        duration,
        tags=[f"version:{version}"]
    )

    if not success:
        # Change failure rate
        statsd.increment(
            "deployment.failure",
            tags=[f"version:{version}"]
        )
```

## Related

- [cd-basics.md](cd-basics.md) - CD principles and practices
- [feature-flags.md](feature-flags.md) - Feature flag patterns
- [monitoring-patterns.md](monitoring-patterns.md) - Monitoring and observability
