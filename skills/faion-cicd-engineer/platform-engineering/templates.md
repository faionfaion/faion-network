# Platform Engineering Templates

## Backstage catalog-info.yaml

```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: {{SERVICE_NAME}}
  description: {{SERVICE_DESCRIPTION}}
  annotations:
    github.com/project-slug: {{ORG}}/{{REPO}}
    backstage.io/techdocs-ref: dir:.
    prometheus.io/scrape: "true"
    grafana/dashboard-selector: "service={{SERVICE_NAME}}"
  tags:
    - {{LANGUAGE}}
    - {{TIER}}
  links:
    - url: https://{{SERVICE_NAME}}.{{DOMAIN}}
      title: Production
      icon: web
spec:
  type: service
  lifecycle: production
  owner: {{TEAM}}
  system: {{SYSTEM}}
  providesApis:
    - {{SERVICE_NAME}}-api
  dependsOn:
    - resource:{{DATABASE}}
    - component:{{DEPENDENCY}}
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: {{SERVICE_NAME}}-api
  description: {{SERVICE_NAME}} REST API
spec:
  type: openapi
  lifecycle: production
  owner: {{TEAM}}
  definition:
    $text: ./openapi.yaml
```

## Backstage Template Skeleton

```yaml
# templates/service-template/template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: {{TEMPLATE_NAME}}
  title: {{TEMPLATE_TITLE}}
  description: {{TEMPLATE_DESCRIPTION}}
  tags:
    - recommended
    - {{LANGUAGE}}
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      required:
        - name
        - owner
        - description
      properties:
        name:
          title: Name
          type: string
          description: Unique service name (lowercase, hyphens allowed)
          pattern: '^[a-z][a-z0-9-]{2,30}$'
          ui:autofocus: true

        description:
          title: Description
          type: string
          description: Brief description of the service

        owner:
          title: Owner
          type: string
          description: Team that owns this service
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: Group

    - title: Technical Options
      properties:
        tier:
          title: Service Tier
          type: string
          description: Determines SLA and resources
          enum:
            - tier-1-critical
            - tier-2-standard
            - tier-3-experimental
          default: tier-2-standard

        database:
          title: Database
          type: string
          enum:
            - none
            - postgres
            - mysql
            - mongodb
          default: none

        cache:
          title: Cache
          type: string
          enum:
            - none
            - redis
            - memcached
          default: none

  steps:
    - id: fetch-base
      name: Fetch Base
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          description: ${{ parameters.description }}
          tier: ${{ parameters.tier }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: ${{ parameters.description }}
        repoUrl: github.com?owner={{ORG}}&repo=${{ parameters.name }}
        defaultBranch: main
        protectDefaultBranch: true

    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Repository
        url: ${{ steps['publish'].output.remoteUrl }}
      - title: Open in Catalog
        icon: catalog
        entityRef: ${{ steps['register'].output.entityRef }}
```

## Port Blueprint

```json
{
  "identifier": "service",
  "title": "Service",
  "icon": "Microservice",
  "schema": {
    "properties": {
      "name": {
        "type": "string",
        "title": "Service Name"
      },
      "description": {
        "type": "string",
        "title": "Description"
      },
      "owner": {
        "type": "string",
        "title": "Owner Team"
      },
      "tier": {
        "type": "string",
        "title": "Service Tier",
        "enum": ["critical", "standard", "experimental"]
      },
      "language": {
        "type": "string",
        "title": "Language",
        "enum": ["go", "python", "typescript", "java", "rust"]
      },
      "repository": {
        "type": "string",
        "format": "url",
        "title": "Repository URL"
      },
      "deploymentFrequency": {
        "type": "number",
        "title": "Deployments per Week"
      },
      "leadTime": {
        "type": "number",
        "title": "Lead Time (hours)"
      },
      "healthScore": {
        "type": "number",
        "title": "Health Score",
        "minimum": 0,
        "maximum": 100
      }
    },
    "required": ["name", "owner", "tier"]
  },
  "relations": {
    "system": {
      "title": "System",
      "target": "system",
      "required": false
    },
    "dependencies": {
      "title": "Dependencies",
      "target": "service",
      "many": true
    },
    "database": {
      "title": "Database",
      "target": "database",
      "required": false
    }
  },
  "scorecards": [
    {
      "identifier": "production-readiness",
      "title": "Production Readiness",
      "rules": [
        {
          "identifier": "has-docs",
          "title": "Has Documentation",
          "query": ".properties.documentation != null"
        },
        {
          "identifier": "has-owner",
          "title": "Has Owner",
          "query": ".properties.owner != null"
        },
        {
          "identifier": "has-monitoring",
          "title": "Has Monitoring",
          "query": ".properties.grafanaDashboard != null"
        }
      ]
    }
  ]
}
```

## Port Self-Service Action

```json
{
  "identifier": "create-service",
  "title": "Create New Service",
  "icon": "Plus",
  "description": "Provision a new microservice with all dependencies",
  "trigger": {
    "type": "self-service",
    "operation": "CREATE",
    "blueprintIdentifier": "service",
    "userInputs": {
      "properties": {
        "name": {
          "type": "string",
          "title": "Service Name",
          "pattern": "^[a-z][a-z0-9-]*$"
        },
        "template": {
          "type": "string",
          "title": "Template",
          "enum": ["go-microservice", "python-fastapi", "node-express"],
          "default": "go-microservice"
        },
        "database": {
          "type": "string",
          "title": "Database",
          "enum": ["none", "postgres", "mysql", "mongodb"],
          "default": "none"
        },
        "environment": {
          "type": "string",
          "title": "Initial Environment",
          "enum": ["dev", "staging"],
          "default": "dev"
        }
      },
      "required": ["name", "template"]
    }
  },
  "invocationMethod": {
    "type": "GITHUB",
    "org": "{{ORG}}",
    "repo": "platform-actions",
    "workflow": "create-service.yaml",
    "reportWorkflowStatus": true
  }
}
```

## Score Workload

```yaml
# score.yaml
apiVersion: score.dev/v1b1
metadata:
  name: {{SERVICE_NAME}}
  labels:
    team: {{TEAM}}
    tier: {{TIER}}

containers:
  main:
    image: .
    command: ["/app/{{SERVICE_NAME}}"]
    variables:
      LOG_LEVEL: ${resources.env.LOG_LEVEL}
      DB_HOST: ${resources.db.host}
      DB_PORT: ${resources.db.port}
      DB_NAME: ${resources.db.name}
      DB_USER: ${resources.db.username}
      DB_PASSWORD: ${resources.db.password}
      REDIS_URL: ${resources.cache.url}
    resources:
      limits:
        cpu: ${resources.env.CPU_LIMIT}
        memory: ${resources.env.MEMORY_LIMIT}
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
    readinessProbe:
      httpGet:
        path: /readyz
        port: 8080

service:
  ports:
    www:
      port: 8080
      protocol: TCP
      targetPort: 8080

resources:
  env:
    type: environment

  db:
    type: postgres
    properties:
      version: 15

  cache:
    type: redis

  dns:
    type: dns
    properties:
      subdomain: {{SERVICE_NAME}}
```

## Crossplane Composite Resource

```yaml
# crossplane/composite/service-infrastructure.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xserviceinfras.platform.example.org
spec:
  group: platform.example.org
  names:
    kind: XServiceInfra
    plural: xserviceinfras
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                serviceName:
                  type: string
                tier:
                  type: string
                  enum: [critical, standard, experimental]
                database:
                  type: object
                  properties:
                    engine:
                      type: string
                      enum: [postgres, mysql]
                    size:
                      type: string
                      enum: [small, medium, large]
                cache:
                  type: object
                  properties:
                    enabled:
                      type: boolean
                    size:
                      type: string
                      enum: [small, medium, large]
              required:
                - serviceName
                - tier
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: aws-service-infra
spec:
  compositeTypeRef:
    apiVersion: platform.example.org/v1alpha1
    kind: XServiceInfra
  resources:
    - name: namespace
      base:
        apiVersion: kubernetes.crossplane.io/v1alpha1
        kind: Object
        spec:
          forProvider:
            manifest:
              apiVersion: v1
              kind: Namespace
      patches:
        - fromFieldPath: spec.serviceName
          toFieldPath: spec.forProvider.manifest.metadata.name

    - name: database
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "15"
            instanceClass: db.t3.micro
            allocatedStorage: 20
      patches:
        - fromFieldPath: spec.serviceName
          toFieldPath: metadata.name
          transforms:
            - type: string
              string:
                fmt: "%s-db"
        - fromFieldPath: spec.database.size
          toFieldPath: spec.forProvider.instanceClass
          transforms:
            - type: map
              map:
                small: db.t3.micro
                medium: db.t3.small
                large: db.t3.medium
```

## GitHub Actions: Create Service Workflow

```yaml
# .github/workflows/create-service.yaml
name: Create Service

on:
  workflow_dispatch:
    inputs:
      name:
        description: 'Service name'
        required: true
      template:
        description: 'Template'
        required: true
        default: 'go-microservice'
      database:
        description: 'Database type'
        required: false
        default: 'none'
      environment:
        description: 'Environment'
        required: true
        default: 'dev'

env:
  SERVICE_NAME: ${{ github.event.inputs.name }}
  TEMPLATE: ${{ github.event.inputs.template }}

jobs:
  create-repo:
    runs-on: ubuntu-latest
    outputs:
      repo-url: ${{ steps.create.outputs.url }}
    steps:
      - name: Create Repository from Template
        id: create
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.ORG_ADMIN_TOKEN }}
          script: |
            const repo = await github.rest.repos.createUsingTemplate({
              template_owner: context.repo.owner,
              template_repo: '${{ env.TEMPLATE }}',
              owner: context.repo.owner,
              name: '${{ env.SERVICE_NAME }}',
              private: true,
              include_all_branches: false
            });
            core.setOutput('url', repo.data.html_url);

  provision-infra:
    runs-on: ubuntu-latest
    needs: create-repo
    steps:
      - name: Checkout Infrastructure Repo
        uses: actions/checkout@v4
        with:
          repository: ${{ github.repository_owner }}/infrastructure
          token: ${{ secrets.ORG_ADMIN_TOKEN }}

      - name: Generate Crossplane Claim
        run: |
          cat > claims/${{ env.SERVICE_NAME }}.yaml << EOF
          apiVersion: platform.example.org/v1alpha1
          kind: ServiceInfra
          metadata:
            name: ${{ env.SERVICE_NAME }}
            namespace: crossplane-system
          spec:
            serviceName: ${{ env.SERVICE_NAME }}
            tier: standard
            database:
              engine: ${{ github.event.inputs.database }}
              size: small
          EOF

      - name: Commit and Push
        run: |
          git config user.name "platform-bot"
          git config user.email "platform@example.com"
          git add claims/
          git commit -m "Add infrastructure for ${{ env.SERVICE_NAME }}"
          git push

  register-catalog:
    runs-on: ubuntu-latest
    needs: [create-repo, provision-infra]
    steps:
      - name: Register in Backstage
        run: |
          curl -X POST "${{ secrets.BACKSTAGE_URL }}/api/catalog/locations" \
            -H "Authorization: Bearer ${{ secrets.BACKSTAGE_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "type": "url",
              "target": "${{ needs.create-repo.outputs.repo-url }}/blob/main/catalog-info.yaml"
            }'

  notify:
    runs-on: ubuntu-latest
    needs: [create-repo, provision-infra, register-catalog]
    steps:
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: platform-notifications
          slack-message: |
            New service created: ${{ env.SERVICE_NAME }}
            Repository: ${{ needs.create-repo.outputs.repo-url }}
            Template: ${{ env.TEMPLATE }}
            Environment: ${{ github.event.inputs.environment }}
```

## Terraform Module: Platform Base

```hcl
# modules/platform-base/main.tf

variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"
}

variable "cluster_name" {
  type        = string
  description = "Kubernetes cluster name"
}

# Backstage namespace and resources
resource "kubernetes_namespace" "backstage" {
  metadata {
    name = "backstage"
    labels = {
      "app.kubernetes.io/name"      = "backstage"
      "app.kubernetes.io/component" = "platform"
    }
  }
}

# ArgoCD for GitOps
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = "argocd"
  version    = "5.51.0"

  create_namespace = true

  values = [
    yamlencode({
      server = {
        extraArgs = ["--insecure"]
        ingress = {
          enabled = true
          hosts   = ["argocd.${var.environment}.example.com"]
        }
      }
    })
  ]
}

# Crossplane for infrastructure provisioning
resource "helm_release" "crossplane" {
  name       = "crossplane"
  repository = "https://charts.crossplane.io/stable"
  chart      = "crossplane"
  namespace  = "crossplane-system"
  version    = "1.14.0"

  create_namespace = true
}

# External Secrets for secrets management
resource "helm_release" "external_secrets" {
  name       = "external-secrets"
  repository = "https://charts.external-secrets.io"
  chart      = "external-secrets"
  namespace  = "external-secrets"
  version    = "0.9.0"

  create_namespace = true
}

output "argocd_url" {
  value = "https://argocd.${var.environment}.example.com"
}
```

---

*Platform Engineering Templates | faion-cicd-engineer*
