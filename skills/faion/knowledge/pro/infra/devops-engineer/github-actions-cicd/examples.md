# GitHub Actions Examples

## Complete CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.12'

permissions:
  contents: read

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier
        run: npm run format:check

  test:
    name: Test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: lint

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  build:
    name: Build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [lint, test]

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
          retention-days: 7

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: lint
    permissions:
      contents: read
      security-events: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript

      - name: Perform CodeQL analysis
        uses: github/codeql-action/analyze@v3
```

---

## Docker Build and Push

```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:

permissions:
  contents: read
  packages: write
  id-token: write

jobs:
  docker:
    name: Build and Push
    runs-on: ubuntu-latest
    timeout-minutes: 30

    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build-push.outputs.digest }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        id: build-push
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true
```

---

## Matrix Build

```yaml
# .github/workflows/matrix.yml
name: Matrix Build

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 20
            coverage: true

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- ${{ matrix.coverage && '--coverage' || '' }}

      - name: Upload coverage
        if: matrix.coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

---

## Reusable Workflow (Caller)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  deploy-staging:
    if: github.event_name == 'push' || inputs.environment == 'staging'
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: staging
      url: https://staging.example.com
    secrets: inherit

  deploy-production:
    if: inputs.environment == 'production'
    needs: deploy-staging
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: production
      url: https://example.com
    secrets: inherit
```

---

## Reusable Workflow (Called)

```yaml
# .github/workflows/deploy-reusable.yml
name: Deploy Reusable

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
        description: 'Environment name'
      url:
        required: true
        type: string
        description: 'Deployment URL'
    secrets:
      DEPLOY_KEY:
        required: true

permissions:
  contents: read
  deployments: write

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment }}
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment:
      name: ${{ inputs.environment }}
      url: ${{ inputs.url }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/

      - name: Deploy
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          # Add deployment commands here
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

---

## Custom Composite Action

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Node.js environment with caching'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
  install-deps:
    description: 'Install dependencies'
    required: false
    default: 'true'

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - name: Get npm cache directory
      id: npm-cache-dir
      shell: bash
      run: echo "dir=$(npm config get cache)" >> $GITHUB_OUTPUT

    - name: Cache npm dependencies
      id: cache
      uses: actions/cache@v4
      with:
        path: |
          ${{ steps.npm-cache-dir.outputs.dir }}
          node_modules
        key: ${{ runner.os }}-node-${{ inputs.node-version }}-${{ hashFiles('**/package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-node-${{ inputs.node-version }}-

    - name: Install dependencies
      if: inputs.install-deps == 'true' && steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

---

## OIDC Authentication (AWS)

```yaml
# .github/workflows/aws-deploy.yml
name: AWS Deploy

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

---

## Scheduled Workflow

```yaml
# .github/workflows/scheduled.yml
name: Scheduled Tasks

on:
  schedule:
    # Every day at 2:00 UTC
    - cron: '0 2 * * *'
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  stale:
    name: Close stale issues
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Stale issues
        uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue has been inactive for 30 days.'
          stale-pr-message: 'This PR has been inactive for 30 days.'
          days-before-stale: 30
          days-before-close: 7

  dependency-update:
    name: Check for updates
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Check outdated packages
        run: npm outdated || true
```

---

## Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Generate changelog
        id: changelog
        run: |
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          git log --pretty=format:"- %s" $(git describe --tags --abbrev=0 HEAD^)..HEAD >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.changelog }}
          files: |
            dist/*
          generate_release_notes: true
```

## Sources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
