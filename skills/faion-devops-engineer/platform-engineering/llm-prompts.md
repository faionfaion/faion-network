# Platform Engineering LLM Prompts

AI prompts for platform engineering tasks.

## Platform Assessment

### Analyze Developer Experience

```
Analyze the developer experience for this organization.

Context:
- Current tools: [list current tools]
- Team size: [number] developers
- Services count: [number] services
- Deployment frequency: [frequency]
- Average onboarding time: [days]

Evaluate:
1. Cognitive load on developers (infrastructure vs features)
2. Self-service capabilities (what can devs do without ops?)
3. Golden paths (standardized approaches vs ad-hoc)
4. Documentation quality and discoverability
5. Deployment friction points

Output:
- Current state assessment (score 1-10)
- Top 5 pain points with impact
- Quick wins (can implement in 1-2 weeks)
- Strategic improvements (1-3 months)
- Recommended platform tools
```

### Design IDP Architecture

```
Design an Internal Developer Platform architecture.

Requirements:
- Cloud provider: [AWS/GCP/Azure]
- Kubernetes: [yes/no]
- Team structure: [centralized/distributed]
- Existing CI/CD: [tool]
- Security requirements: [list]
- Budget constraints: [if any]

Deliverables:
1. Architecture diagram (describe layers)
2. Tool selection with rationale
3. Integration points
4. Data flow for common operations
5. Security and access control model
6. Migration path from current state
```

## Golden Path Design

### Create Service Golden Path

```
Design a golden path for creating new [service type] services.

Service type: [microservice/API/worker/frontend]
Language: [Python/Go/Node.js/Java]
Infrastructure: [Kubernetes/serverless]

Golden path should include:
1. Repository structure template
2. CI/CD pipeline configuration
3. Infrastructure provisioning
4. Observability setup (metrics, logs, traces)
5. Security baseline (authentication, secrets)
6. Documentation template
7. Local development setup

Constraints:
- [list any organizational constraints]

Output format:
- Template files with comments
- Setup instructions
- What it provides vs what developer configures
- Escape hatches for non-standard cases
```

### Define Database Golden Path

```
Design a golden path for database provisioning.

Database types to support: [PostgreSQL/MySQL/MongoDB/Redis]
Environment: [AWS/GCP/on-prem Kubernetes]

Golden path should provide:
1. Self-service request interface (form fields)
2. Sizing options (small/medium/large with specs)
3. Security defaults (encryption, network isolation)
4. Backup configuration
5. Monitoring alerts
6. Connection string delivery (secrets management)
7. Cost estimation

Output:
- Crossplane/Terraform composition
- Backstage template (if applicable)
- Documentation for developers
```

## Platform Operations

### Generate Runbook

```
Create a runbook for [operation].

Operation: [database failover/service rollback/incident response]
Platform: [describe platform components]
SLA requirements: [recovery time objectives]

Runbook should include:
1. Trigger conditions (when to use this runbook)
2. Prerequisites (access, tools)
3. Step-by-step procedure
4. Verification steps after each action
5. Rollback procedure
6. Escalation path
7. Post-incident checklist

Format: Numbered steps with commands and expected outputs.
```

### Design Self-Service Workflow

```
Design a self-service workflow for [request type].

Request type: [environment clone/database creation/API key rotation]
Current process: [describe manual process if exists]
Approvals needed: [automatic/manager/security team]

Workflow should define:
1. Request interface (form fields, validation)
2. Approval gates (if any)
3. Automation steps
4. Notification points
5. Audit logging
6. Error handling and retry logic
7. Time to completion target

Output: Workflow diagram and implementation spec.
```

## Backstage Configuration

### Generate catalog-info.yaml

```
Generate a Backstage catalog-info.yaml for this service.

Service details:
- Name: [service name]
- Description: [what it does]
- Repository: [GitHub URL]
- Language: [language]
- Dependencies: [list of dependent services]
- APIs provided: [list of APIs]
- Owner team: [team name]
- Lifecycle: [experimental/production/deprecated]

Include annotations for:
- GitHub integration
- TechDocs
- PagerDuty (if applicable)
- SonarQube (if applicable)

Output valid YAML with comments explaining each section.
```

### Create Scaffolder Template

```
Create a Backstage Scaffolder template for [use case].

Use case: [new microservice/new library/new infrastructure component]
Language/framework: [specify]

Template should:
1. Collect necessary parameters (with validation)
2. Fetch and render template files
3. Create repository with proper structure
4. Set up CI/CD pipeline
5. Register in Backstage catalog
6. Provide output links

Include template.yaml and skeleton directory structure.
```

## Crossplane/IaC

### Design Crossplane Composition

```
Design a Crossplane composition for [resource type].

Resource: [database/cache/storage/network]
Cloud provider: [AWS/GCP/Azure]
Variants needed: [development/staging/production]

Composition should:
1. Define CompositeResourceDefinition (XRD) with claim
2. Provide sensible defaults
3. Allow customization where needed
4. Include security best practices
5. Set up monitoring/alerting
6. Handle credentials securely

Output:
- XRD YAML
- Composition YAML
- Example claim YAML
- Documentation for developers
```

### Generate Terraform Module

```
Generate a Terraform module for [platform component].

Component: [EKS cluster/RDS database/VPC/S3 bucket]
Requirements: [list specific requirements]
Security: [encryption, network isolation, IAM]

Module should:
1. Follow Terraform best practices
2. Use variables for customization
3. Include sensible defaults
4. Output necessary values for consumers
5. Include examples in README

Output: Complete module with main.tf, variables.tf, outputs.tf, README.md
```

## Observability

### Design Metrics Strategy

```
Design an observability strategy for the platform.

Platform components: [list components]
SLO requirements: [availability, latency targets]
Current tools: [Prometheus/Grafana/Datadog/etc]

Strategy should cover:
1. Golden signals for each component
2. SLI definitions
3. Alert thresholds and escalation
4. Dashboard design (what to show)
5. Log aggregation approach
6. Distributed tracing setup
7. Cost-effective retention policies
```

### Create Platform Dashboard

```
Design a platform health dashboard.

Audience: [platform team/leadership/all developers]
Platform components: [list components]

Dashboard should show:
1. Platform availability and SLO status
2. Golden path adoption metrics
3. Self-service request volume
4. Developer satisfaction trends
5. Cost per team/service
6. Incident metrics

Output: Grafana JSON or dashboard specification.
```

## Migration and Adoption

### Create Adoption Strategy

```
Create an adoption strategy for the new platform.

Current state: [describe current tools/processes]
Target state: [describe IDP vision]
Team size: [number of teams/developers]

Strategy should include:
1. Phased rollout plan
2. Early adopter selection criteria
3. Training and documentation plan
4. Success metrics for each phase
5. Feedback collection mechanisms
6. Support model during transition
7. Rollback criteria

Timeline: [desired migration timeline]
```

### Generate Migration Checklist

```
Generate a migration checklist for moving [service/team] to the platform.

Service details: [describe service]
Current infrastructure: [describe current setup]
Target platform capabilities: [what platform provides]

Checklist should cover:
1. Pre-migration assessment
2. Dependencies to migrate first
3. CI/CD pipeline migration
4. Infrastructure migration
5. Observability setup
6. Security validation
7. Performance testing
8. Cutover procedure
9. Rollback plan
10. Post-migration validation
```

## Cost Optimization

### Analyze Platform Costs

```
Analyze platform costs and suggest optimizations.

Current costs:
- Compute: [amount]
- Storage: [amount]
- Network: [amount]
- Tools/licenses: [amount]

Usage patterns: [describe typical usage]

Analyze:
1. Cost breakdown by team/service
2. Unused or underutilized resources
3. Right-sizing opportunities
4. Reserved capacity potential
5. Architecture optimizations
6. Tool consolidation opportunities

Output: Prioritized recommendations with estimated savings.
```

### Design FinOps Integration

```
Design FinOps integration for the platform.

Requirements:
- Cost visibility per team/service
- Pre-deployment cost estimation
- Budget alerts and controls
- Chargeback/showback reporting

Current cloud: [AWS/GCP/Azure]
Tagging strategy: [describe or ask to design]

Output:
1. Tagging standards
2. Cost allocation approach
3. Alert configuration
4. Dashboard design
5. Integration with golden paths
```
