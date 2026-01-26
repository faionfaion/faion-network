# Platform Engineering LLM Prompts

## IDP Strategy & Planning

### Assess Current State

```
Analyze our current developer experience and identify platform engineering opportunities:

Context:
- Organization size: {{TEAM_COUNT}} teams, {{DEVELOPER_COUNT}} developers
- Current tools: {{TOOL_LIST}}
- Pain points reported: {{PAIN_POINTS}}
- Average onboarding time: {{ONBOARDING_DAYS}} days
- DevOps ticket volume: {{TICKET_VOLUME}}/month

Please provide:
1. Gap analysis comparing current state to IDP best practices
2. Top 5 quick wins for immediate improvement
3. Long-term platform roadmap (3 phases)
4. ROI estimates based on industry benchmarks
5. Recommended tooling stack with justification
```

### Define Platform Vision

```
Create a platform engineering vision document for our organization:

Context:
- Company: {{COMPANY_NAME}}
- Industry: {{INDUSTRY}}
- Current challenges: {{CHALLENGES}}
- Strategic goals: {{GOALS}}
- Budget constraints: {{BUDGET}}

Generate:
1. Platform mission statement
2. Target developer experience (north star)
3. Success metrics and KPIs
4. Stakeholder communication plan
5. Risk assessment and mitigation strategies
```

## Golden Path Design

### Design Golden Path

```
Design a golden path for: {{USE_CASE}}

Requirements:
- Target developers: {{DEVELOPER_PERSONA}}
- Technology stack: {{TECH_STACK}}
- Compliance requirements: {{COMPLIANCE}}
- Must integrate with: {{EXISTING_TOOLS}}

Provide:
1. User journey map (before and after)
2. Required components and their interactions
3. Automation workflow
4. Self-service interface design
5. Guardrails and defaults
6. Documentation outline
7. Adoption strategy
```

### Create Service Template

```
Create a service template specification for: {{SERVICE_TYPE}}

Technical context:
- Language: {{LANGUAGE}}
- Framework: {{FRAMEWORK}}
- Infrastructure: {{INFRA}} (e.g., Kubernetes, serverless)
- CI/CD: {{CICD_TOOL}}

Template should include:
1. Project structure with all boilerplate
2. Dockerfile and container configuration
3. CI/CD pipeline configuration
4. Kubernetes manifests or infrastructure code
5. Observability setup (logging, metrics, tracing)
6. Security defaults (RBAC, secrets, policies)
7. Documentation templates
8. Test scaffolding
```

## Self-Service Actions

### Design Self-Service Action

```
Design a self-service action for: {{ACTION_NAME}}

Current process:
- Steps: {{MANUAL_STEPS}}
- Time required: {{CURRENT_TIME}}
- Teams involved: {{TEAMS}}
- Frequency: {{FREQUENCY}}/month

Design requirements:
1. User input form with validation
2. Approval workflow (if needed)
3. Backend automation steps
4. Error handling and rollback
5. Notification and audit logging
6. Cost estimation (if applicable)
7. Port/Backstage action definition
```

### Implement Provisioning Workflow

```
Create an automated provisioning workflow for: {{RESOURCE_TYPE}}

Specifications:
- Cloud provider: {{CLOUD}}
- IaC tool: {{IAC_TOOL}} (Terraform/Crossplane/Pulumi)
- GitOps: {{GITOPS_ENABLED}}
- Cost threshold: {{COST_LIMIT}}/month

Generate:
1. Resource definition/module
2. Input validation schema
3. Cost estimation logic
4. GitHub Actions/GitLab CI workflow
5. Crossplane composition (if applicable)
6. Rollback procedure
7. Documentation for users
```

## Architecture & Integration

### Design IDP Architecture

```
Design an Internal Developer Platform architecture:

Constraints:
- Cloud: {{CLOUD_PROVIDER}}
- Kubernetes: {{K8S_VERSION}}
- Existing tools to keep: {{KEEP_TOOLS}}
- Budget: {{BUDGET}}
- Timeline: {{TIMELINE}}

Architecture should cover:
1. Component diagram with all integrations
2. Data flow between components
3. Authentication/authorization model
4. API contracts between layers
5. High availability considerations
6. Migration path from current state
7. Build vs buy recommendations
```

### Integrate Tool with IDP

```
Create an integration plan for: {{TOOL_NAME}} with our IDP

Current IDP components:
- Portal: {{PORTAL}} (Backstage/Port/custom)
- GitOps: {{GITOPS_TOOL}}
- Secrets: {{SECRETS_TOOL}}
- Monitoring: {{MONITORING_TOOL}}

Integration requirements:
1. Authentication flow (SSO/OAuth)
2. API integration points
3. Data synchronization strategy
4. Entity relationships in catalog
5. Self-service actions to expose
6. Dashboard/metrics to surface
7. Implementation steps
```

## Measurement & Optimization

### Design Platform Metrics Dashboard

```
Design a platform metrics dashboard for: {{AUDIENCE}} (leadership/platform team/developers)

Available data sources:
- Git: {{GIT_PROVIDER}}
- CI/CD: {{CICD_TOOL}}
- Kubernetes: {{K8S_METRICS}}
- Cloud: {{CLOUD_METRICS}}
- Service catalog: {{CATALOG_TOOL}}

Dashboard should include:
1. DORA metrics with benchmarks
2. Self-service adoption metrics
3. Platform health indicators
4. Cost allocation by team/service
5. Developer satisfaction trends
6. Recommended Grafana/Datadog queries
7. Alert thresholds and escalation
```

### Analyze Platform Adoption

```
Analyze platform adoption and recommend improvements:

Current metrics:
- Self-service vs ticket ratio: {{RATIO}}
- Golden path adoption: {{ADOPTION_RATE}}%
- Average onboarding time: {{ONBOARDING_TIME}}
- Developer satisfaction score: {{SATISFACTION}}
- Most common support requests: {{TOP_REQUESTS}}

Provide:
1. Adoption analysis by team/service type
2. Friction points preventing adoption
3. Quick wins for improvement
4. Long-term optimization roadmap
5. Communication strategy for low adopters
6. Success stories to highlight
```

## Security & Governance

### Design Platform Security Model

```
Design security and governance model for our IDP:

Compliance requirements:
- Frameworks: {{COMPLIANCE_FRAMEWORKS}} (SOC2, HIPAA, PCI-DSS)
- Data classification: {{DATA_CLASSES}}
- Audit requirements: {{AUDIT_REQS}}

Current security tools:
- Identity: {{IDP_PROVIDER}}
- Secrets: {{SECRETS_MANAGEMENT}}
- Policy: {{POLICY_ENGINE}}

Design should include:
1. RBAC model with role definitions
2. Policy-as-code implementation (OPA/Kyverno)
3. Secrets management workflow
4. Audit logging requirements
5. Compliance automation
6. Security scanning integration
7. Incident response procedures
```

### Create Policy-as-Code

```
Create policy-as-code rules for: {{POLICY_AREA}}

Policy requirements:
{{POLICY_REQUIREMENTS}}

Technology:
- Policy engine: {{ENGINE}} (OPA/Kyverno/custom)
- Enforcement point: {{ENFORCEMENT}} (admission/CI/audit)

Generate:
1. Policy definitions with explanations
2. Test cases for each policy
3. Exemption handling
4. Error messages for developers
5. Documentation for policy library
6. CI integration for policy testing
```

## FinOps Integration

### Implement Platform FinOps

```
Design FinOps integration for our IDP:

Cloud spend:
- Monthly budget: {{BUDGET}}
- Current spend: {{CURRENT_SPEND}}
- Top cost drivers: {{COST_DRIVERS}}

Requirements:
1. Cost visibility in developer portal
2. Pre-deployment cost estimation
3. Budget alerts and thresholds
4. Team-level showback reports
5. Optimization recommendations
6. Integration with {{FINOPS_TOOL}}

Provide implementation plan including:
- Data pipeline architecture
- Dashboard design
- Alert configuration
- Automation for cost gates
- Developer communication strategy
```

## AI Agent Integration

### Design AI Platform Agent

```
Design an AI agent for platform operations:

Use cases:
{{AI_USE_CASES}}

Constraints:
- Model: {{MODEL}} (Claude/GPT-4/custom)
- Max cost per request: {{MAX_COST}}
- Approval required for: {{APPROVAL_AREAS}}
- Audit requirements: {{AUDIT_REQS}}

Design should include:
1. Agent persona and capabilities
2. Permission model (what it can/cannot do)
3. Resource quotas and limits
4. Governance policies
5. Interaction patterns (chat/actions/automation)
6. Feedback and learning mechanisms
7. Monitoring and observability
8. Safety guardrails
```

---

## Usage Tips

1. **Be specific**: Replace all {{PLACEHOLDERS}} with actual values
2. **Provide context**: More context leads to better recommendations
3. **Iterate**: Use follow-up prompts to refine outputs
4. **Validate**: Always review generated configurations before applying
5. **Document**: Save successful prompts for team knowledge base

---

*Platform Engineering LLM Prompts | faion-cicd-engineer*
