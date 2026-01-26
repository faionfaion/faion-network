# GitHub Actions Workflow Templates

Copy-paste templates for quick workflow setup. Customize variables marked with `{PLACEHOLDER}`.

## Quick Start Templates

### Minimal CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### Minimal CD

```yaml
# .github/workflows/cd.yml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - name: Deploy
        run: |
          # Add deployment command here
          echo "Deploying to production..."
```

## Matrix Templates

### Node.js Multi-Version

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Multi-OS Testing

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Full Matrix with Exclusions

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18
          - os: macos-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 22
            coverage: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test ${{ matrix.coverage && '-- --coverage' || '' }}
```

## Caching Templates

### npm Cache

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Built-in caching
```

### Manual npm Cache

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### pip Cache

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Go Cache

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/go/pkg/mod
      ~/.cache/go-build
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
    restore-keys: |
      ${{ runner.os }}-go-
```

### Rust Cache

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      ~/.cargo/git/db/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
```

### Docker Layer Cache (Buildx)

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Artifact Templates

### Upload Artifact

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/
    retention-days: 7
```

### Download Artifact

```yaml
- uses: actions/download-artifact@v4
  with:
    name: build
    path: dist/
```

### Upload Test Results

```yaml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results-${{ matrix.node }}
    path: |
      coverage/
      junit.xml
    retention-days: 30
```

### Matrix Artifact Pattern

```yaml
jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.os }}
          path: dist/

  combine:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          pattern: build-*
          merge-multiple: true
          path: all-builds/
```

## Docker Templates

### Build and Push

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha
            type=ref,event=branch
            type=semver,pattern={{version}}

      - uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Deployment Templates

### AWS EKS

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: {REGION}

- uses: azure/setup-kubectl@v4
  with:
    version: 'v1.29.0'

- run: aws eks update-kubeconfig --name {CLUSTER_NAME} --region {REGION}

- run: |
    kubectl set image deployment/{DEPLOYMENT} \
      {CONTAINER}={IMAGE}:${{ github.sha }} \
      -n {NAMESPACE}
    kubectl rollout status deployment/{DEPLOYMENT} -n {NAMESPACE} --timeout=5m
```

### Vercel

```yaml
- uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
    vercel-args: '--prod'
```

### Netlify

```yaml
- uses: netlify/actions/cli@master
  with:
    args: deploy --prod --dir=dist
  env:
    NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
    NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

### SSH Deploy

```yaml
- uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.SSH_HOST }}
    username: ${{ secrets.SSH_USER }}
    key: ${{ secrets.SSH_KEY }}
    port: ${{ secrets.SSH_PORT }}
    script: |
      cd /var/www/{APP_NAME}
      git pull origin main
      npm ci
      npm run build
      pm2 restart {APP_NAME}
```

## Notification Templates

### Slack

```yaml
- uses: slackapi/slack-github-action@v1.26.0
  if: failure()
  with:
    payload: |
      {
        "text": "Build failed: ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": ":x: *Build failed*\nRepo: `${{ github.repository }}`\nBranch: `${{ github.ref_name }}`\nCommit: `${{ github.sha }}`"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Discord

```yaml
- uses: sarisia/actions-status-discord@v1
  if: always()
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}
    title: "Build"
    description: "Build completed for ${{ github.repository }}"
```

## Reusable Workflow Template

```yaml
# .github/workflows/_reusable-{NAME}.yml
name: Reusable {NAME}

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: false
        type: string
        default: 'latest'
    secrets:
      API_TOKEN:
        required: true
    outputs:
      result:
        description: "Result of the workflow"
        value: ${{ jobs.main.outputs.result }}

jobs:
  main:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.action.outputs.result }}
    environment: ${{ inputs.environment }}

    steps:
      - uses: actions/checkout@v4

      - name: Main action
        id: action
        run: |
          echo "Running for ${{ inputs.environment }} with version ${{ inputs.version }}"
          echo "result=success" >> $GITHUB_OUTPUT
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
```

## Composite Action Template

```yaml
# .github/actions/{NAME}/action.yml
name: '{NAME}'
description: '{DESCRIPTION}'

inputs:
  version:
    description: 'Version to use'
    required: false
    default: 'latest'

outputs:
  result:
    description: 'Result of the action'
    value: ${{ steps.main.outputs.result }}

runs:
  using: 'composite'
  steps:
    - name: Main step
      id: main
      shell: bash
      run: |
        echo "Running with version ${{ inputs.version }}"
        echo "result=success" >> $GITHUB_OUTPUT
```

## Scheduled Workflow Template

```yaml
# .github/workflows/scheduled-{NAME}.yml
name: Scheduled {NAME}

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger

jobs:
  {NAME}:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run scheduled task
        run: |
          echo "Running scheduled task at $(date)"
          # Add task commands here
```

## Concurrency Template

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Deployment Concurrency (No Cancel)

```yaml
concurrency:
  group: deploy-${{ inputs.environment }}
  cancel-in-progress: false
```

## Permission Templates

### Minimal Permissions

```yaml
permissions:
  contents: read
```

### CI Permissions

```yaml
permissions:
  contents: read
  checks: write
  pull-requests: write
```

### Release Permissions

```yaml
permissions:
  contents: write
  packages: write
```

### OIDC Permissions

```yaml
permissions:
  id-token: write
  contents: read
```
