---
name: docker-for-prod
description: Harden a Node.js or Python app into a production-ready Docker image with multi-stage build, non-root user, healthcheck, and trivy scanning in CI.
tier: pro
group: devops-cicd
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a production-hardened Docker image: multi-stage build with a distroless or Alpine final layer, non-root user, proper `.dockerignore`, a healthcheck, and a trivy vulnerability scan wired into your CI pipeline — plus a docker-compose file for local development parity.

## Prerequisites

- Docker Engine 24+ installed locally (`docker --version`).
- A Node.js 20+ or Python 3.11+ application in a Git repo.
- GitHub Actions (or GitLab CI) already running basic tests.
- `trivy` CLI available in CI — either installed in the runner image or via the `aquasecurity/trivy-action` GitHub Action.
- Basic familiarity with layered Docker builds (knows what `COPY`, `RUN`, `CMD` do).

## Steps

### Node.js app

1. Create `.dockerignore` at the repo root to exclude everything not needed in the image:

   ```
   node_modules
   .git
   .env*
   *.log
   coverage
   dist
   .husky
   ```

2. Write a multi-stage `Dockerfile` that compiles in a full `node:20-alpine` builder stage and runs in a distroless final stage:

   ```dockerfile
   # Stage 1: install + build
   FROM node:20-alpine AS builder
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN npm ci --omit=dev
   COPY . .
   RUN npm run build

   # Stage 2: runtime — distroless nodejs
   FROM gcr.io/distroless/nodejs20-debian12 AS runtime
   WORKDIR /app
   # Copy only the compiled output and production deps
   COPY --from=builder /app/dist ./dist
   COPY --from=builder /app/node_modules ./node_modules
   COPY --from=builder /app/package.json ./
   # Non-root user is the default in distroless (uid 65532 "nonroot")
   EXPOSE 3000
   HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
     CMD ["/nodejs/bin/node", "-e", "require('http').get('http://localhost:3000/healthz', r => process.exit(r.statusCode === 200 ? 0 : 1))"]
   CMD ["dist/server.js"]
   ```

3. Verify image size before moving on:

   ```bash
   docker build -t myapp:dev .
   docker images myapp:dev --format "{{.Size}}"
   ```

   A typical Express app should be under 120 MB with distroless.

### Python app

1. Create `.dockerignore`:

   ```
   __pycache__
   *.pyc
   .git
   .env*
   .venv
   *.log
   tests
   ```

2. Write the multi-stage `Dockerfile`:

   ```dockerfile
   # Stage 1: install deps
   FROM python:3.11-slim AS builder
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

   # Stage 2: runtime — slim + non-root user
   FROM python:3.11-slim AS runtime
   WORKDIR /app
   # Copy installed packages from builder
   COPY --from=builder /install /usr/local
   COPY . .
   # Create and switch to non-root user
   RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
   USER appuser
   EXPOSE 8000
   HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
     CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1
   CMD ["python", "-m", "gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
   ```

   Use `python:3.11-slim` (not `python:3.11`) — saves ~700 MB. For stricter isolation, `gcr.io/distroless/python3-debian12` works for single-binary apps.

### docker-compose for local dev

3. Add `docker-compose.yml` at the repo root for local parity with production dependencies:

   ```yaml
   services:
     app:
       build:
         context: .
         target: builder        # use builder stage with dev tools
       ports:
         - "3000:3000"          # or 8000:8000 for Python
       volumes:
         - .:/app
         - /app/node_modules    # anonymous volume prevents host override
       environment:
         - NODE_ENV=development
         - DATABASE_URL=postgres://appuser:secret@db:5432/appdb
       depends_on:
         db:
           condition: service_healthy

     db:
       image: postgres:16-alpine
       environment:
         POSTGRES_USER: appuser
         POSTGRES_PASSWORD: secret
         POSTGRES_DB: appdb
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U appuser"]
         interval: 5s
         timeout: 3s
         retries: 5
   ```

   Start: `docker compose up --build`. Stop: `docker compose down -v` (removes volumes).

### Trivy scan in CI

4. Add a trivy scan step to your GitHub Actions workflow (`.github/workflows/ci.yml`) after the build step:

   ```yaml
   - name: Build image
     run: docker build -t myapp:${{ github.sha }} .

   - name: Scan image for vulnerabilities
     uses: aquasecurity/trivy-action@0.20.0
     with:
       image-ref: myapp:${{ github.sha }}
       format: table
       exit-code: "1"
       ignore-unfixed: true
       severity: CRITICAL,HIGH
   ```

   Setting `exit-code: "1"` fails the pipeline on unpatched CRITICAL/HIGH CVEs. `ignore-unfixed: true` suppresses false positives where no fix exists yet.

5. Pin the base image digest in production (`FROM node:20-alpine@sha256:<digest>`) once the scan passes to prevent upstream tag drift:

   ```bash
   docker inspect --format='{{index .RepoDigests 0}}' node:20-alpine
   # → node:20-alpine@sha256:abc123...
   ```

   Replace the tag reference with the pinned digest in the production Dockerfile.

## Verify

Build and run the production image locally, then check the healthcheck status:

```bash
docker build -t myapp:prod --target runtime .
docker run -d --name myapp-test -p 3000:3000 myapp:prod
sleep 15
docker inspect --format='{{.State.Health.Status}}' myapp-test
```

Expected output: `healthy`. If it shows `unhealthy`, run `docker logs myapp-test` to inspect startup errors.

Confirm the process runs as non-root:

```bash
docker exec myapp-test whoami
# → nonroot  (distroless)  or  appuser  (slim)
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `COPY --from=builder` fails with "layer not found" | Target stage name typo or missing `AS builder` | Verify stage names match exactly; `docker build --progress=plain` shows which stage fails |
| Distroless image has no shell — can't debug | Distroless by design strips shell | Use `gcr.io/distroless/nodejs20-debian12:debug` temporarily for `docker exec` access; revert before push |
| `npm ci` installs devDependencies in final image | Missing `--omit=dev` flag | Add `--omit=dev` to `npm ci` in builder stage; or copy only `dist/` and `node_modules` selectively |
| Trivy exits 1 on unfixed CVEs | `ignore-unfixed: false` (default) | Set `ignore-unfixed: true` in the action; upgrade base image to a newer patch tag |
| Healthcheck always `starting` | Start period too short for slow boot | Increase `--start-period` to 30s or more; check if the `/healthz` route is defined before the server is fully listening |
| Python app fails: `ModuleNotFoundError` | `COPY --from=builder /install` mismatches Python path | Confirm that `/install` was passed with `--prefix=/install` and that `/usr/local` is on `PYTHONPATH`; alternatively `pip install` directly to the runtime layer |
| docker compose volumes mount node_modules from host | Missing anonymous volume override | Add `- /app/node_modules` entry under volumes for the app service |

## Next

- `production-cicd-pipeline` — wire the Docker build + trivy scan into a full multi-stage GitHub Actions pipeline with staging gate and production deploy.
- Add container signing with `cosign` (Sigstore) after the trivy scan to produce a verifiable provenance chain for production images.
- Consider `docker scout cves myapp:prod` as a complementary scan — it integrates with Docker Hub and provides remediation advice alongside trivy.

## References

- [knowledge/pro/infra/devops-engineer/docker](../../../../../knowledge/pro/infra/devops-engineer/docker) — core Docker architecture and layer caching model; informs the stage split and `COPY` ordering in Steps 2–3 to maximize cache reuse.
- [knowledge/pro/infra/devops-engineer/docker-image-optimization](../../../../../knowledge/pro/infra/devops-engineer/docker-image-optimization) — distroless vs. Alpine size trade-offs and `--omit=dev` pattern used in the Node.js Dockerfile.
- [knowledge/pro/infra/devops-engineer/docker-security-hardening](../../../../../knowledge/pro/infra/devops-engineer/docker-security-hardening) — non-root user creation, read-only filesystem flags, and CVE triage logic applied in Steps 2, 3, and 4 (trivy exit-code policy).
- [knowledge/pro/infra/devops-engineer/github-actions-cicd](../../../../../knowledge/pro/infra/devops-engineer/github-actions-cicd) — job sequencing and `uses:` action pinning conventions applied when wiring the trivy scan step in Step 4.
