---
name: production-cicd-pipeline
description: Build a GitHub Actions multi-stage CI/CD pipeline from scratch: lint → test → security scan → container build → registry push → staging deploy → smoke tests → manual gate → production deploy.
tier: pro
group: devops-cicd
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a fully wired GitHub Actions pipeline that automatically lints, tests, scans for vulnerabilities, builds and pushes a container image to a registry, deploys to staging, runs smoke tests, waits for a manual approval, then deploys to production — with every stage gated on the previous one passing.

## Prerequisites

- A GitHub repository with your application source and a `Dockerfile` at the root.
- GitHub Actions enabled on the repo (default for public and private repos).
- A container registry: AWS ECR (`<account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>`) or GitHub Container Registry (`ghcr.io/<owner>/<image-name>`).
- A staging and a production deployment target (VPS with SSH access, ECS service, or Kubernetes cluster). This playbook uses a VPS with `docker compose` as the concrete example.
- GitHub repository secrets configured (see Step 1).
- Two GitHub Environments created: `staging` and `production` (Settings → Environments).
- `trivy` and `semgrep` available as GitHub Actions — no local install needed.

## Steps

### 1. Configure repository secrets and environments

1. Open your repository → Settings → Secrets and variables → Actions. Add these secrets:

   | Secret name | Value |
   |-------------|-------|
   | `AWS_ACCESS_KEY_ID` | IAM key with `ecr:GetAuthorizationToken`, `ecr:PutImage` | 
   | `AWS_SECRET_ACCESS_KEY` | Paired secret key |
   | `AWS_REGION` | `eu-central-1` (or your region) |
   | `ECR_REPOSITORY` | `myapp` (the ECR repo name, not the full URI) |
   | `AWS_ACCOUNT_ID` | 12-digit account ID |
   | `STAGING_SSH_HOST` | `staging.myapp.io` |
   | `STAGING_SSH_USER` | `deploy` |
   | `STAGING_SSH_KEY` | Private SSH key (no passphrase) |
   | `PROD_SSH_HOST` | `prod.myapp.io` |
   | `PROD_SSH_USER` | `deploy` |
   | `PROD_SSH_KEY` | Private SSH key for production |

   If you use GHCR instead of ECR, replace the AWS secrets with a single `GHCR_TOKEN` (a GitHub personal access token with `write:packages` scope).

2. Open Settings → Environments. Create `staging` with no protection rules. Create `production` with **Required reviewers** — add yourself (or your lead developer) as a required approver. This is the manual gate.

### 2. Create the workflow file

Create `.github/workflows/cicd.yml` in your repository:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

env:
  IMAGE_NAME: ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com/${{ secrets.ECR_REPOSITORY }}

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install ruff
        run: pip install ruff==0.4.4
      - name: Run ruff lint
        run: ruff check . --output-format=github
      - name: Run ruff format check
        run: ruff format --check .

  unit-test:
    name: Unit Tests
    runs-on: ubuntu-24.04
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run pytest
        run: pytest tests/unit/ --tb=short --cov=myapp --cov-report=xml
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  integration-test:
    name: Integration Tests
    runs-on: ubuntu-24.04
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: myapp
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: myapp_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://myapp:testpass@localhost:5432/myapp_test
        run: pytest tests/integration/ --tb=short

  security-scan:
    name: Security Scan
    runs-on: ubuntu-24.04
    needs: lint
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run semgrep SAST
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/python
            p/secrets
            p/owasp-top-ten
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}

      - name: Build image for Trivy scan
        run: docker build -t myapp:scan-${{ github.sha }} .

      - name: Run Trivy container scan
        uses: aquasecurity/trivy-action@0.24.0
        with:
          image-ref: myapp:scan-${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          exit-code: "1"
          severity: CRITICAL,HIGH
          ignore-unfixed: true

      - name: Upload Trivy SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-results.sarif

  build-push:
    name: Build & Push Image
    runs-on: ubuntu-24.04
    needs: [unit-test, integration-test, security-scan]
    if: github.ref == 'refs/heads/main'
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to Amazon ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v2

      - name: Extract image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=,format=short
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        id: build
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-24.04
    needs: build-push
    environment: staging
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.STAGING_SSH_HOST }}
          username: ${{ secrets.STAGING_SSH_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /srv/myapp
            export IMAGE_TAG=${{ env.IMAGE_NAME }}:${{ github.sha }}
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f

  smoke-test:
    name: Smoke Tests
    runs-on: ubuntu-24.04
    needs: deploy-staging
    steps:
      - uses: actions/checkout@v4
      - name: Wait for staging to be ready
        run: |
          for i in $(seq 1 12); do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://staging.myapp.io/health)
            if [ "$STATUS" = "200" ]; then
              echo "Staging healthy (HTTP $STATUS)"
              exit 0
            fi
            echo "Attempt $i: HTTP $STATUS — retrying in 10s"
            sleep 10
          done
          echo "Staging not healthy after 2 minutes"
          exit 1
      - name: Run smoke tests
        run: |
          curl -sf https://staging.myapp.io/health | grep '"status":"ok"'
          curl -sf -o /dev/null -w "%{http_code}" https://staging.myapp.io/ | grep 200
          curl -sf -o /dev/null -w "%{http_code}" https://staging.myapp.io/api/v1/ping | grep 200

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-24.04
    needs: smoke-test
    environment: production
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.PROD_SSH_HOST }}
          username: ${{ secrets.PROD_SSH_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /srv/myapp
            export IMAGE_TAG=${{ env.IMAGE_NAME }}:${{ github.sha }}
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f
      - name: Verify production health
        run: |
          sleep 15
          curl -sf https://myapp.io/health | grep '"status":"ok"'
```

### 3. Add a health endpoint to your application

The smoke tests and final verify step hit `/health`. Add a minimal handler if your app lacks one. For a Django app:

```python
# myapp/views.py
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "version": "1.0.0"})
```

```python
# myapp/urls.py  (add to urlpatterns)
path("health", views.health),
```

### 4. Add a docker-compose.yml on each server

On both `staging.myapp.io` and `myapp.io`, create `/srv/myapp/docker-compose.yml`:

```yaml
services:
  web:
    image: ${IMAGE_TAG:-latest}
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    env_file: .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

The `deploy` user needs `docker` group membership (`usermod -aG docker deploy`).

### 5. Wire branch protection

In GitHub → Settings → Branches → Add rule for `main`:

- Require a pull request before merging
- Require status checks to pass: select `Lint`, `Unit Tests`, `Integration Tests`, `Security Scan`
- Require branches to be up to date before merging
- Do not allow bypassing the above settings

This ensures the pipeline cannot be skipped by direct pushes from anyone — including repository owners.

## Verify

Push a commit to `main` and watch the pipeline in the Actions tab. The expected job sequence is:

```
lint ─┬─ unit-test ─────────────┐
      ├─ integration-test ──────┤
      └─ security-scan ─────────┴─ build-push → deploy-staging → smoke-test → [approval gate] → deploy-production
```

Confirm each stage:

1. **Lint + tests + scan** run in parallel after lint passes — check the job graph in the Actions UI.
2. **build-push** only triggers on `main` (not on PRs).
3. **deploy-staging** shows `environment: staging` in the job summary.
4. **smoke-test** returns a non-zero exit code if `/health` is down — verify by temporarily breaking the health endpoint.
5. **deploy-production** shows a pending approval banner in the Actions UI — click "Review deployments", approve, and confirm the production deploy completes.
6. Confirm production:

```bash
curl -sf https://myapp.io/health
# → {"status":"ok","version":"1.0.0"}
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECR: no basic auth credentials` | `amazon-ecr-login` step skipped or AWS credentials wrong | Verify `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` secrets; ensure the IAM user has `ecr:GetAuthorizationToken` and `ecr:PutImage` |
| Trivy scan exits 1 on a base image you cannot change | Known unfixed CVE in `python:3.12-slim` base | Add a `.trivyignore` file listing the CVE IDs you accept; document rationale in a comment |
| `smoke-test` fails: `curl: (6) Could not resolve host` | Staging deploy completed but DNS not propagated | Use the server IP directly in smoke tests; set `STAGING_SSH_HOST` to an IP, not a hostname |
| `semgrep-action` fails with `SEMGREP_APP_TOKEN` missing | Token not added to secrets | Either add the token from semgrep.dev, or run `semgrep/semgrep-action` with `publishToken: ""` and `--config auto` to skip the dashboard upload |
| `deploy-production` approval email not received | GitHub notification for environment approvals defaults to off | Go to github.com → Settings → Notifications → Actions → enable "Workflows, deployment review requests" |
| `cancel-in-progress` cancels a production deploy | Concurrency group is too broad | Set a separate group per environment: `group: deploy-prod-${{ github.sha }}` for the production job |
| Docker cache miss on every run | `cache-to: type=gha` hit the 10 GB GHA cache limit | Scope cache keys by branch: `cache-from: type=gha,scope=main` |

## Next

- [gitops-flux](../../../knowledge/pro/infra/cicd-engineer/gitops-flux) — replace the SSH deploy step with a Flux GitOps controller so production state is always reconciled from Git rather than pushed imperatively.
- Add a rollback job: on health check failure after production deploy, re-run `deploy-production` with the previous image tag (stored as an artifact).
- Move to OIDC-based AWS authentication (replace long-lived `AWS_ACCESS_KEY_ID` with `aws-actions/configure-aws-credentials` OIDC role assumption) — eliminates the rotating-secret problem entirely.

## References

- [knowledge/pro/infra/cicd-engineer/gha-workflow-structure](../../../knowledge/pro/infra/cicd-engineer/gha-workflow-structure) — the job DAG design rules and concurrency group patterns applied directly in the `needs:` chain and the `cancel-in-progress` conditional in this pipeline.
- [knowledge/pro/infra/cicd-engineer/gha-security-hardening](../../../knowledge/pro/infra/cicd-engineer/gha-security-hardening) — drives the `permissions: security-events: write` scope, pinned action versions (`@v4`, `@0.24.0`), and the SARIF upload pattern for Trivy results.
- [knowledge/pro/infra/cicd-engineer/security-container-scanning](../../../knowledge/pro/infra/cicd-engineer/security-container-scanning) — informs the Trivy `severity: CRITICAL,HIGH` threshold, `ignore-unfixed: true` flag, and the `.trivyignore` escape hatch in Troubleshooting.
- [knowledge/pro/infra/cicd-engineer/gha-deployment-patterns](../../../knowledge/pro/infra/cicd-engineer/gha-deployment-patterns) — the `environment:` protection rule pattern and manual approval gate configuration used in `deploy-production`.
