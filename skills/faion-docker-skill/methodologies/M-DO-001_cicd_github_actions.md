# M-DO-001: CI/CD with GitHub Actions

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #cicd, #github, #actions, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Manual deployment is error-prone and time-consuming. Without CI/CD, developers fear pushing code because deployments are unpredictable and risky.

## Promise

After this methodology, you will automate testing, building, and deployment with GitHub Actions. Every push will trigger reliable pipelines.

## Overview

GitHub Actions provides CI/CD built into GitHub. Workflows are defined in YAML files and triggered by events (push, PR, schedule).

---

## Framework

### Step 1: Workflow Structure

```
.github/
└── workflows/
    ├── ci.yml           # Tests on every push/PR
    ├── deploy.yml       # Deploy on main branch
    ├── release.yml      # Create releases
    └── scheduled.yml    # Cron jobs
```

### Step 2: Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

### Step 3: Multi-Platform Matrix

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
      fail-fast: false

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

### Step 4: Caching

```yaml
# npm caching (built-in)
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

# Custom caching
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Docker layer caching
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: user/app:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Step 5: Secrets Management

```yaml
# Using secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# Environment-specific secrets
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.PROD_API_KEY }}
        run: ./deploy.sh
```

### Step 6: Deployment Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

      # Alternative: Deploy to AWS S3
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: aws s3 sync ./dist s3://my-bucket --delete
```

---

## Templates

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: |
          npm ci
          npm run build

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/*
          generate_release_notes: true
```

### Docker Build and Push

```yaml
name: Docker

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            user/app:latest
            user/app:${{ github.sha }}
```

### Scheduled Workflow

```yaml
name: Scheduled Tasks

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Allow manual trigger

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Clean old artifacts
        run: echo "Running cleanup..."

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

---

## Examples

### Reusable Workflows

```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm run build

# Calling reusable workflow
# .github/workflows/main.yml
jobs:
  call-build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Conditional Jobs

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
      frontend: ${{ steps.filter.outputs.frontend }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            backend:
              - 'backend/**'
            frontend:
              - 'frontend/**'

  backend:
    needs: changes
    if: ${{ needs.changes.outputs.backend == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Backend changed"

  frontend:
    needs: changes
    if: ${{ needs.changes.outputs.frontend == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Frontend changed"
```

---

## Common Mistakes

1. **Not using caching** - Slow builds from reinstalling dependencies
2. **Secrets in code** - Use GitHub secrets, never commit credentials
3. **Missing fail-fast** - Matrix builds continue after first failure
4. **No timeout** - Jobs run indefinitely without timeout-minutes
5. **Ignoring permissions** - Use least privilege for GITHUB_TOKEN

---

## Checklist

- [ ] CI workflow on push and PR
- [ ] Caching for dependencies
- [ ] Matrix testing for multiple versions
- [ ] Secrets stored in GitHub Secrets
- [ ] Deployment workflow with environment
- [ ] Release workflow with tags
- [ ] Scheduled security scans
- [ ] Reusable workflows for DRY

---

## Next Steps

- M-DO-002: GitLab CI
- M-DO-003: Docker Basics
- M-DO-009: Terraform Basics

---

*Methodology M-DO-001 v1.0*
