---
id: github-actions-workflows
name: "GitHub Actions Advanced Workflows"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# GitHub Actions Advanced Workflows

## CD Pipeline

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
  staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.28.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster --region eu-central-1

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
            -n staging

          kubectl rollout status deployment/app -n staging --timeout=5m

      - name: Run smoke tests
        run: |
          npm ci
          npm run test:smoke -- --url=https://staging.example.com

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Staging deployment failed for ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": ":x: *Staging deployment failed*\nRepo: ${{ github.repository }}\nCommit: ${{ github.sha }}"
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
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_ROLE_ARN }}
          aws-region: eu-central-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Setup Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'v1.28.0'

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name production-cluster --region eu-central-1

      - name: Deploy with canary
        run: |
          # Deploy canary (10% traffic)
          kubectl set image deployment/app-canary \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
            -n production

          kubectl rollout status deployment/app-canary -n production --timeout=5m

          # Wait and validate
          sleep 300

          # If canary healthy, deploy to main
          kubectl set image deployment/app \
            app=${{ steps.login-ecr.outputs.registry }}/app:${{ github.sha }} \
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
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Production deployment successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": ":white_check_mark: *Production deployment successful*\nRepo: ${{ github.repository }}\nCommit: ${{ github.sha }}"
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
      - name: Checkout
        uses: actions/checkout@v4
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
        uses: softprops/action-gh-release@v1
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
        uses: docker/build-push-action@v5
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
    secrets:
      AWS_ROLE_ARN:
        required: true
      SLACK_WEBHOOK:
        required: false

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment }}
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

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
        run: |
          kubectl set image deployment/app app=${{ inputs.image-tag }} -n ${{ inputs.namespace }}
          kubectl rollout status deployment/app -n ${{ inputs.namespace }} --timeout=10m

      - name: Notify
        if: always() && secrets.SLACK_WEBHOOK != ''
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "Deployment to ${{ inputs.environment }}: ${{ job.status }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Using Reusable Workflow

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

## Scheduled Workflow

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
      - name: Checkout
        uses: actions/checkout@v4

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

## References

- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Deployment Protection Rules](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-protection-rules)

## Sources

- [GitHub Actions Workflow Examples](https://docs.github.com/en/actions/examples)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Docker Build-Push Action](https://github.com/docker/build-push-action)
- [GitHub Actions for Cloud Deployments](https://github.com/marketplace?type=actions&query=deploy)
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides)
