# Platform Engineering Checklist

## Pre-Implementation Assessment

- [ ] Identify developer pain points (surveys, interviews)
- [ ] Map current tooling landscape
- [ ] Measure baseline metrics (deployment frequency, lead time)
- [ ] Document existing golden paths (formal or informal)
- [ ] Assess cognitive load on developers
- [ ] Calculate DevOps ticket volume

## Executive Buy-In

- [ ] Prepare ROI case with industry benchmarks
- [ ] Document inefficiencies from siloed teams
- [ ] Present DORA metrics correlation to business outcomes
- [ ] Define success criteria and timeline
- [ ] Secure budget and headcount

## Platform Team Setup

- [ ] Define team structure (product owner, engineers, SRE)
- [ ] Establish platform-as-product mindset
- [ ] Create feedback loops with developer customers
- [ ] Set up internal communication channels
- [ ] Define SLAs for platform services

## IDP Architecture

### Backend Layer
- [ ] Choose platform orchestrator (Humanitec, Crossplane, custom)
- [ ] Define resource abstractions
- [ ] Implement GitOps workflow
- [ ] Set up secrets management
- [ ] Configure RBAC model

### Service Catalog
- [ ] Select portal tool (Backstage, Port, Cortex)
- [ ] Define service metadata schema
- [ ] Create initial service entries
- [ ] Set up documentation standards
- [ ] Configure search and discovery

### Self-Service Actions
- [ ] Identify top 10 developer requests
- [ ] Create automation for each
- [ ] Implement approval workflows where needed
- [ ] Add cost estimation to provisioning
- [ ] Set up audit logging

## Golden Paths

### Path Design
- [ ] Identify common development patterns
- [ ] Document opinionated decisions
- [ ] Create scaffolding templates
- [ ] Add compliance/security by default
- [ ] Include observability setup

### Path Implementation
- [ ] Build path for new service creation
- [ ] Build path for database provisioning
- [ ] Build path for CI/CD pipeline setup
- [ ] Build path for environment creation
- [ ] Build path for secret management

### Path Adoption
- [ ] Make paths discoverable (no tickets)
- [ ] Create documentation and tutorials
- [ ] Run onboarding sessions
- [ ] Collect feedback iteratively
- [ ] Measure adoption rates

## Security & Compliance

- [ ] Implement policy-as-code (OPA, Kyverno)
- [ ] Set up automated security scanning
- [ ] Configure least-privilege access
- [ ] Implement audit trails
- [ ] Create compliance dashboards

## FinOps Integration

- [ ] Add cost visibility to developer portal
- [ ] Implement budget alerts
- [ ] Create cost allocation tags
- [ ] Set up pre-deployment cost gates
- [ ] Build showback/chargeback reports

## AI Agent Integration (2026)

- [ ] Define AI agent personas and permissions
- [ ] Set resource quotas for AI workloads
- [ ] Implement governance policies
- [ ] Add AI actions to service catalog
- [ ] Monitor AI agent usage and costs

## Measurement & Improvement

### DORA Metrics
- [ ] Set up deployment frequency tracking
- [ ] Measure lead time for changes
- [ ] Track mean time to recovery
- [ ] Monitor change failure rate

### Platform Metrics
- [ ] Track self-service adoption rate
- [ ] Measure time-to-first-deployment (new devs)
- [ ] Survey developer satisfaction quarterly
- [ ] Monitor ticket volume trends
- [ ] Calculate platform ROI

## Ongoing Operations

- [ ] Establish deprecation policies
- [ ] Create runbooks for platform incidents
- [ ] Set up on-call rotation
- [ ] Schedule regular platform reviews
- [ ] Plan capacity for growth

---

*Platform Engineering Checklist | faion-cicd-engineer*
