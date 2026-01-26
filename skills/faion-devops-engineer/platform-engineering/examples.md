# Platform Engineering Examples

Real-world case studies and implementation patterns from industry leaders.

## Case Study: Spotify Backstage

### Context

Spotify had 280 engineering teams managing 2,000+ backend services, 300 websites, 4,000 data pipelines, and 200 mobile features. Engineers struggled to find information and manage services across this complexity.

### Solution

Developed Backstage as a unified developer portal combining:
- Software catalog
- Tech documentation
- Golden paths (templates)
- Plugin ecosystem

### Implementation

**Service Catalog:**
- Every service registered with ownership
- Dependencies mapped automatically
- Health and quality scorecards

**Golden Paths:**
- Opinionated but optional templates
- Pre-configured CI/CD, monitoring, security
- One-click service creation

**Key Decision:** Golden paths "nudge" teams toward best practices without forcing compliance. This preserved Spotify's autonomous engineering culture.

### Results

| Metric | Before | After |
|--------|--------|-------|
| Onboarding time | 60+ days | 20 days |
| Documentation discovery | Hours | Minutes |
| Service creation | Days | Hours |

**Productivity Impact (frequent Backstage users):**
- 2.3x more active in GitHub
- 2x more code changes
- 17% less cycle time
- 2x deployment frequency
- 3x longer deployment stability

### Open Source

Spotify open-sourced Backstage in 2020, donated to CNCF. Now a foundation for many enterprise IDPs.

---

## Case Study: Netflix Wall-E

### Context

Netflix needed to ensure security best practices across thousands of microservices without slowing down development velocity.

### Solution

Built Wall-E, an internal platform that:
- Bootstraps new services with security best practices pre-integrated
- Provides self-service security compliance
- Eliminates manual security checkbox reviews

### Implementation

**Security Golden Path:**
- Authentication/authorization pre-configured
- Secrets management integrated
- Vulnerability scanning automated
- Compliance templates embedded

**Developer Experience:**
- One command to create secure service
- Security invisible to developers (built-in, not bolt-on)
- Escape hatches for edge cases

### Results

- Security compliance: Near 100% for new services
- Developer friction: Minimal (security is default)
- Time to secure service: Days to minutes

---

## Case Study: Google "Shift Down"

### Context

DevOps "shift left" pushed more responsibilities to developers, increasing cognitive load. Google developed "shift down" as an alternative approach.

### Philosophy

**Shift Left:** Push responsibilities earlier in dev cycle (to developers)
**Shift Down:** Push responsibilities into the platform (away from developers)

### Implementation

**Platform Absorbs Complexity:**
- Security scanning: Platform responsibility
- Cost management: Platform controls
- Compliance: Policy as code
- Observability: Pre-configured

**Developers Focus On:**
- Application logic
- Feature development
- Business value

### Key Principles

1. Platform makes 80% of decisions for developers
2. Remaining 20% = intentional, high-value choices
3. Defaults are best practices
4. Deviation possible but explicit

---

## Implementation Pattern: Backstage-Based IDP

### Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Developer Portal            │
                    │  (Backstage + Custom Plugins)       │
                    └─────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ Service       │         │ Tech Docs     │         │ Golden Paths  │
│ Catalog       │         │               │         │ (Templates)   │
└───────────────┘         └───────────────┘         └───────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ GitHub/GitLab │         │ MkDocs/       │         │ Cookiecutter/ │
│ Integration   │         │ Docusaurus    │         │ Yeoman        │
└───────────────┘         └───────────────┘         └───────────────┘
```

### Components

**Service Catalog Plugin:**
```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  description: User authentication service
  annotations:
    github.com/project-slug: myorg/my-service
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: platform-team
  dependsOn:
    - component:user-database
    - component:auth-provider
```

**Golden Path Template:**
```yaml
# template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: microservice-template
  title: Create Microservice
  description: Standard microservice with CI/CD, monitoring
spec:
  owner: platform-team
  type: service
  parameters:
    - title: Service Details
      properties:
        name:
          title: Service Name
          type: string
        language:
          title: Language
          type: string
          enum: [python, go, node]
  steps:
    - id: fetch
      name: Fetch Template
      action: fetch:template
    - id: publish
      name: Create Repository
      action: publish:github
    - id: register
      name: Register in Catalog
      action: catalog:register
```

---

## Implementation Pattern: Crossplane-Based IDP

### Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Platform API (K8s CRDs)     │
                    └─────────────────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────┐
                    │         Crossplane Controller       │
                    └─────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ AWS Provider  │         │ GCP Provider  │         │ Azure Provider│
└───────────────┘         └───────────────┘         └───────────────┘
```

### Composition Example

```yaml
# composition.yaml - Database Golden Path
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: database-postgres
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: Database
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBInstance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "15"
            instanceClass: db.t3.medium
            storageEncrypted: true
            # Security best practices built-in
    - name: security-group
      base:
        apiVersion: ec2.aws.crossplane.io/v1beta1
        kind: SecurityGroup
        # Locked down by default
```

### Developer Request

```yaml
# my-database.yaml - What developer writes
apiVersion: platform.example.com/v1alpha1
kind: Database
metadata:
  name: user-db
spec:
  size: small
  environment: production
```

---

## Golden Path Examples

### New Service Golden Path

**What it provides:**
- Repository with standardized structure
- CI/CD pipeline (build, test, deploy)
- Observability (metrics, logs, traces)
- Security scanning
- Documentation template
- Environment configurations

**Developer effort:** Fill form, click create

### Database Golden Path

**What it provides:**
- Managed database (RDS, Cloud SQL)
- Connection credentials in secrets manager
- Backup configuration
- Monitoring alerts
- Encryption at rest

**Developer effort:** Specify size and environment

### API Golden Path

**What it provides:**
- API gateway configuration
- Authentication/authorization
- Rate limiting
- Documentation (OpenAPI)
- Client SDK generation

**Developer effort:** Define API specification

---

## Metrics Dashboard Example

### Platform Adoption

```
Golden Path Usage (Last 30 Days)
================================
New Service Template    ████████████████████ 89%
Database Golden Path    ████████████████     72%
API Gateway Golden Path ████████████         58%
Custom Setup            ██                   11%

Self-Service Requests
=====================
Infrastructure       ████████████████████ 156 (↑23%)
Environment Clone    ████████████         89 (↑12%)
Database Creation    ████████             64 (↑8%)
Manual Ticket        ██                   18 (↓45%)
```

### Developer Productivity

```
Time to First Deployment
========================
Week 1:  ████████████████████ 4.2 days
Week 4:  ████████████         2.8 days
Week 8:  ████████             1.9 days
Week 12: ████                 0.8 days

Deployment Frequency
====================
Before Platform: 2x/week
After Platform:  8x/week (4x improvement)
```
