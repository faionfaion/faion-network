# GitHub Actions Workflow Examples

Complete, production-ready workflow examples for common CI/CD scenarios.

## CI Pipeline with Matrix Testing

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  checks: write

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier
        run: npm run format:check

  test:
    name: Test (${{ matrix.os }}, Node ${{ matrix.node }})
    runs-on: ${{ matrix.os }}
    needs: lint

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node == '20'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
          retention-days: 7
```

## CD Pipeline with Staged Deployments

```yaml
# .github/workflows/cd.yml
name: CD

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

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false

jobs:
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

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
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.29.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster --region eu-central-1

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/app -n staging --timeout=5m

      - name: Run smoke tests
        run: |
          npm ci
          npm run test:smoke -- --url=https://staging.example.com

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1.26.0
        with:
          payload: |
            {
              "text": ":x: Staging deployment failed for ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Staging deployment failed*\nRepo: `${{ github.repository }}`\nCommit: `${{ github.sha }}`"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: staging
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.29.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name production-cluster --region eu-central-1

      - name: Deploy with canary
        run: |
          # Deploy canary (10% traffic)
          kubectl set image deployment/app-canary \
            app=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/app-canary -n production --timeout=5m

          # Wait for validation
          sleep 300

          # Deploy to main
          kubectl set image deployment/app \
            app=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/app -n production --timeout=10m

      - name: Create Sentry release
        uses: getsentry/action-release@v1
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: ${{ vars.SENTRY_ORG }}
          SENTRY_PROJECT: ${{ vars.SENTRY_PROJECT }}
        with:
          environment: production
          version: ${{ github.sha }}

      - name: Notify on success
        uses: slackapi/slack-github-action@v1.26.0
        with:
          payload: |
            {
              "text": ":white_check_mark: Production deployment successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production deployment successful*\nRepo: `${{ github.repository }}`\nCommit: `${{ github.sha }}`"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

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

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          registry-url: 'https://npm.pkg.github.com'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Generate changelog
        id: changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --latest --strip header

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.content }}
          draft: false
          prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') || contains(github.ref, 'rc') }}
          files: |
            dist/*.tar.gz
            dist/*.zip

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ steps.version.outputs.version }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Reusable Workflow

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
      cluster-name:
        required: true
        type: string
      namespace:
        required: true
        type: string
      timeout:
        required: false
        type: string
        default: '10m'
    secrets:
      AWS_ROLE_ARN:
        required: true
      SLACK_WEBHOOK:
        required: false
    outputs:
      deployment-url:
        description: "URL of deployed environment"
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment }}
    runs-on: ubuntu-latest
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    environment:
      name: ${{ inputs.environment }}

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name ${{ inputs.cluster-name }} --region eu-central-1

      - name: Deploy
        id: deploy
        run: |
          kubectl set image deployment/app app=${{ inputs.image-tag }} -n ${{ inputs.namespace }}
          kubectl rollout status deployment/app -n ${{ inputs.namespace }} --timeout=${{ inputs.timeout }}
          echo "url=https://${{ inputs.environment }}.example.com" >> $GITHUB_OUTPUT

      - name: Notify
        if: always() && secrets.SLACK_WEBHOOK != ''
        uses: slackapi/slack-github-action@v1.26.0
        with:
          payload: |
            {
              "text": "Deployment to ${{ inputs.environment }}: ${{ job.status }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Calling Reusable Workflow

```yaml
# .github/workflows/deploy-all.yml
name: Deploy All Environments

on:
  push:
    branches: [main]

jobs:
  staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image-tag: ghcr.io/org/app:${{ github.sha }}
      cluster-name: staging-cluster
      namespace: staging
    secrets:
      AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}

  production:
    needs: staging
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      image-tag: ghcr.io/org/app:${{ github.sha }}
      cluster-name: production-cluster
      namespace: production
    secrets:
      AWS_ROLE_ARN: ${{ secrets.AWS_PROD_ROLE_ARN }}
      SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

## Scheduled Maintenance Workflow

```yaml
# .github/workflows/scheduled.yml
name: Scheduled Tasks

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 02:00 UTC
  workflow_dispatch:

jobs:
  cleanup:
    name: Cleanup Old Artifacts
    runs-on: ubuntu-latest

    steps:
      - name: Delete old artifacts
        uses: c-hive/gha-remove-artifacts@v1
        with:
          age: '30 days'
          skip-recent: 5

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  dependency-update:
    name: Check Dependency Updates
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Check outdated dependencies
        run: npm outdated || true

      - name: Run npm audit
        run: npm audit --audit-level=high

  backup:
    name: Database Backup
    runs-on: ubuntu-latest

    steps:
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Backup database
        run: |
          TIMESTAMP=$(date +%Y%m%d-%H%M%S)
          aws rds create-db-snapshot \
            --db-instance-identifier production-db \
            --db-snapshot-identifier backup-$TIMESTAMP
```

## Python CI with Matrix and Caching

```yaml
# .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-${{ matrix.python-version }}-
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linting
        run: |
          ruff check .
          ruff format --check .

      - name: Run type checking
        run: mypy src/

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: coverage.xml
```

## Monorepo CI with Path Filters

```yaml
# .github/workflows/monorepo-ci.yml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      frontend: ${{ steps.filter.outputs.frontend }}
      backend: ${{ steps.filter.outputs.backend }}
      shared: ${{ steps.filter.outputs.shared }}

    steps:
      - uses: actions/checkout@v4

      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            frontend:
              - 'packages/frontend/**'
              - 'packages/shared/**'
            backend:
              - 'packages/backend/**'
              - 'packages/shared/**'
            shared:
              - 'packages/shared/**'

  frontend:
    name: Frontend CI
    runs-on: ubuntu-latest
    needs: changes
    if: needs.changes.outputs.frontend == 'true'

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build frontend
        run: npm run build --workspace=packages/frontend

      - name: Test frontend
        run: npm test --workspace=packages/frontend

  backend:
    name: Backend CI
    runs-on: ubuntu-latest
    needs: changes
    if: needs.changes.outputs.backend == 'true'

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd packages/backend
          pip install -r requirements.txt

      - name: Test backend
        run: |
          cd packages/backend
          pytest
```
