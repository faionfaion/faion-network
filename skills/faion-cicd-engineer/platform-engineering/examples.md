# Platform Engineering Examples

## Case Study: Spotify (Backstage)

### Before
- 60+ days onboarding time for new developers
- Fragmented tooling across 280 engineering teams
- Tribal knowledge for infrastructure provisioning

### After (with Backstage)
- 20 days onboarding time (-67%)
- 2,000+ backend services managed centrally
- 300 websites, 4,000 data pipelines, 200 mobile features
- Frequent Backstage users: 2.3x more active in GitHub
- 2x code changes in 17% less cycle time
- 2x deployment frequency
- 3x longer deployment uptime

## Golden Path: New Microservice

### Developer Experience

```
Developer: "Create new payment service"
           |
           v
   Service Catalog Portal
           |
           v
   Select: "Microservice (Go)" template
           |
           v
   Fill: service name, team, tier
           |
           v
   [Create] button
           |
           v
   Automated:
   - Git repo created
   - CI/CD pipeline configured
   - Kubernetes namespace provisioned
   - Secrets vault configured
   - Monitoring dashboards created
   - Service registered in catalog
           |
           v
   Developer gets: ready-to-code repo
   Time: 5 minutes (was: 2-3 days)
```

### Technical Implementation

```yaml
# backstage/templates/microservice-go/template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: microservice-go
  title: Go Microservice
  description: Creates a production-ready Go microservice
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Details
      required:
        - name
        - owner
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]*$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
        tier:
          title: Service Tier
          type: string
          enum: [critical, standard, experimental]
          default: standard

  steps:
    - id: fetch
      name: Fetch Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}

    - id: createRepo
      name: Create Repository
      action: github:repo:create
      input:
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}

    - id: createK8sResources
      name: Create Kubernetes Resources
      action: kubernetes:apply
      input:
        manifest: |
          apiVersion: v1
          kind: Namespace
          metadata:
            name: ${{ parameters.name }}
            labels:
              team: ${{ parameters.owner }}
              tier: ${{ parameters.tier }}

    - id: registerCatalog
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.createRepo.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml
```

## Self-Service: Database Provisioning

### Port Action Definition

```yaml
# port/actions/provision-database.yaml
identifier: provision-database
title: Provision Database
description: Self-service database provisioning
trigger:
  type: self-service
  userInputs:
    properties:
      name:
        type: string
        title: Database Name
      engine:
        type: string
        title: Engine
        enum:
          - postgres-15
          - mysql-8
          - mongodb-7
      size:
        type: string
        title: Size
        enum:
          - small    # 1 vCPU, 2GB RAM
          - medium   # 2 vCPU, 4GB RAM
          - large    # 4 vCPU, 8GB RAM
      environment:
        type: string
        enum: [dev, staging, prod]

invocationMethod:
  type: GITHUB
  org: myorg
  repo: infrastructure
  workflow: provision-database.yaml

backend:
  type: CROSSPLANE
```

### Crossplane Resource

```yaml
# crossplane/database-claim.yaml
apiVersion: database.example.org/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: payment-db
  namespace: payment-service
spec:
  parameters:
    version: "15"
    size: medium
    backup:
      enabled: true
      retentionDays: 30
  compositionRef:
    name: aws-rds-postgres
  writeConnectionSecretToRef:
    name: payment-db-credentials
```

## IDP Architecture: Score + Humanitec

### Score Workload Definition

```yaml
# score.yaml
apiVersion: score.dev/v1b1
metadata:
  name: payment-service

containers:
  main:
    image: .
    variables:
      DB_HOST: ${resources.db.host}
      DB_PORT: ${resources.db.port}
      DB_NAME: ${resources.db.name}

resources:
  db:
    type: postgres
    properties:
      version: 15

  dns:
    type: dns
    properties:
      subdomain: payment

  cache:
    type: redis
```

### Environment Resolution (Humanitec)

```yaml
# Development: Local PostgreSQL
db:
  host: postgres.dev.svc.cluster.local
  port: 5432

# Production: AWS RDS with replicas
db:
  host: payment-db.xxx.us-east-1.rds.amazonaws.com
  port: 5432
  replicas: 2
```

## Monitoring Dashboard Setup

### Grafana Dashboard as Code

```json
{
  "dashboard": {
    "title": "Platform Health",
    "panels": [
      {
        "title": "Self-Service Adoption",
        "type": "stat",
        "targets": [{
          "expr": "sum(platform_self_service_requests_total) / sum(platform_ticket_requests_total) * 100"
        }]
      },
      {
        "title": "Deployment Frequency",
        "type": "timeseries",
        "targets": [{
          "expr": "sum(rate(deployments_total[1d])) by (team)"
        }]
      },
      {
        "title": "Lead Time for Changes",
        "type": "gauge",
        "targets": [{
          "expr": "histogram_quantile(0.50, sum(rate(lead_time_seconds_bucket[7d])) by (le))"
        }]
      },
      {
        "title": "Platform Cost by Team",
        "type": "piechart",
        "targets": [{
          "expr": "sum(cloud_cost_daily) by (team)"
        }]
      }
    ]
  }
}
```

## Cost Gate Implementation

### Pre-Deployment Cost Check

```yaml
# .github/workflows/deploy.yaml
jobs:
  cost-check:
    runs-on: ubuntu-latest
    steps:
      - name: Estimate Infrastructure Cost
        uses: infracost/actions/setup@v2

      - name: Generate Cost Diff
        run: |
          infracost diff \
            --path=terraform/ \
            --format=json \
            --out-file=/tmp/infracost.json

      - name: Check Cost Threshold
        run: |
          MONTHLY_DIFF=$(jq '.totalMonthlyCost' /tmp/infracost.json)
          if (( $(echo "$MONTHLY_DIFF > 500" | bc -l) )); then
            echo "Cost increase exceeds $500/month threshold"
            exit 1
          fi

      - name: Comment on PR
        uses: infracost/actions/comment@v1
        with:
          path: /tmp/infracost.json
```

## AI Agent Integration (2026)

### Agent Definition

```yaml
# platform/agents/infra-assistant.yaml
apiVersion: platform.io/v1
kind: AIAgent
metadata:
  name: infra-assistant
spec:
  model: claude-3-opus
  permissions:
    - resource: namespace
      verbs: [create, list]
    - resource: deployment
      verbs: [create, update, list]
    - resource: service
      verbs: [create, list]
  quotas:
    maxRequestsPerHour: 100
    maxCostPerDay: $50
  governance:
    requireApproval:
      - production deployments
      - resources > $100/month
```

### Natural Language Provisioning

```
Developer: "Create a new staging environment for the checkout service
            with a small postgres database and redis cache"

AI Agent:
1. Validates permissions
2. Checks cost estimate ($45/month)
3. Creates namespace: checkout-staging
4. Provisions PostgreSQL (small)
5. Provisions Redis (small)
6. Deploys checkout service
7. Returns access credentials and URLs
```

---

*Platform Engineering Examples | faion-cicd-engineer*
