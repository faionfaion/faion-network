# LLM Prompts for Cloud Architecture

Effective prompts for LLM-assisted cloud architecture design, review, and optimization.

## Architecture Design Prompts

### Initial Architecture Design

```
Design a cloud architecture for [WORKLOAD_TYPE] with the following requirements:

**Business Context:**
- Industry: [industry]
- Users: [number] DAU, [number] peak concurrent
- Data: [volume] storage, [rate] ingestion
- Growth: [percentage] YoY for [years]

**Technical Requirements:**
- Availability: [percentage] SLA
- Latency: p99 < [ms]
- Compliance: [GDPR/HIPAA/PCI-DSS/SOC2]
- Data residency: [regions/countries]

**Constraints:**
- Budget: $[amount]/month
- Team size: [number] engineers
- Cloud experience: [beginner/intermediate/advanced]
- Preferred provider: [AWS/Azure/GCP/multi-cloud/no preference]

**Deliverables:**
1. High-level architecture diagram (describe components and connections)
2. Key design decisions with rationale
3. Technology stack recommendations
4. Cost estimate breakdown
5. Risks and mitigation strategies
```

### Multi-Cloud Strategy

```
Help me design a multi-cloud strategy for [COMPANY_TYPE]:

**Current State:**
- Primary cloud: [provider]
- Monthly spend: $[amount]
- Critical workloads: [list]
- Pain points: [vendor lock-in/costs/availability/compliance]

**Goals:**
- [List 3-5 specific goals]

**Questions to address:**
1. Which workloads should move to which cloud and why?
2. How to handle identity and access management across clouds?
3. What abstraction layers are needed (Kubernetes, Terraform, etc.)?
4. How to achieve unified monitoring and alerting?
5. What are the networking requirements between clouds?
6. How to manage costs and prevent bill shock?
7. What's the migration approach and timeline?

Provide specific service recommendations for each cloud provider.
```

### Landing Zone Design

```
Design a landing zone for [ORGANIZATION_TYPE] on [CLOUD_PROVIDER]:

**Organization Details:**
- Size: [number] employees, [number] engineering teams
- Regulatory requirements: [list]
- Existing infrastructure: [on-prem/cloud/hybrid]
- Security posture: [startup/enterprise/regulated]

**Requirements:**
- Account/project structure strategy
- Identity federation approach
- Network topology design
- Security controls and guardrails
- Logging and monitoring setup
- Cost management structure
- Automation and IaC standards

**Deliverables:**
1. Organization hierarchy diagram
2. Network topology diagram
3. IAM strategy document
4. Security control matrix
5. Tagging taxonomy
6. IaC module structure
```

## Architecture Review Prompts

### Well-Architected Review

```
Review the following architecture against the Well-Architected Framework:

**Architecture Description:**
[Paste architecture description or diagram]

**Current Implementation:**
- Compute: [services]
- Database: [services]
- Network: [configuration]
- Security: [controls]

**Review Focus:**
For each pillar, identify:
1. Current state assessment (1-5 rating)
2. Gaps and risks
3. Specific recommendations with priority
4. Implementation effort (Low/Medium/High)

**Pillars to Review:**
- [ ] Operational Excellence
- [ ] Security
- [ ] Reliability
- [ ] Performance Efficiency
- [ ] Cost Optimization
- [ ] Sustainability

Format as a structured report with actionable items.
```

### Security Architecture Review

```
Perform a security architecture review:

**Architecture:**
[Paste architecture description]

**Security Controls in Place:**
- Network: [firewalls, WAF, etc.]
- Identity: [IAM, SSO, MFA, etc.]
- Data: [encryption, DLP, etc.]
- Application: [SAST, DAST, etc.]

**Review Against:**
1. Zero Trust principles (verify every access, least privilege, assume breach)
2. Defense in depth (multiple security layers)
3. OWASP Top 10 for cloud
4. CIS Benchmarks for [provider]
5. [SPECIFIC_COMPLIANCE] requirements

**Deliverables:**
1. Security gaps matrix (finding, severity, recommendation)
2. Threat model for critical paths
3. Prioritized remediation roadmap
4. Quick wins (implement this week)
```

### Cost Optimization Review

```
Review this architecture for cost optimization:

**Current Architecture:**
[Paste architecture description]

**Current Costs:**
- Compute: $[amount]/month
- Database: $[amount]/month
- Storage: $[amount]/month
- Network: $[amount]/month
- Other: $[amount]/month

**Analysis Required:**
1. Right-sizing opportunities (over-provisioned resources)
2. Reserved instance / savings plan recommendations
3. Spot/preemptible instance candidates
4. Unused resource identification
5. Architecture changes for cost reduction
6. Storage tier optimization
7. Network optimization (data transfer costs)

**Constraints:**
- Cannot reduce availability below [percentage]
- Cannot increase latency above [ms]
- [Other constraints]

Provide specific savings estimates for each recommendation.
```

## Infrastructure as Code Prompts

### Terraform Module Design

```
Help me design a Terraform module for [RESOURCE_TYPE]:

**Requirements:**
- Support for [environments: dev, staging, prod]
- [HIGH_AVAILABILITY/SINGLE_REGION] deployment
- [Security requirements]
- [Compliance requirements]

**Features Needed:**
- [List specific features]

**Deliverables:**
1. Module structure (files and directories)
2. Input variables with descriptions and validation
3. Resource configurations with best practices
4. Output values for integration
5. Example usage in different environments
6. Documentation (README.md)

Follow Terraform best practices:
- Use data sources appropriately
- Implement proper tagging
- Use locals for complex expressions
- Add lifecycle rules where needed
- Include sensible defaults
```

### CDK Stack Design

```
Design an AWS CDK stack for [APPLICATION_TYPE]:

**Application Details:**
- Type: [web app/API/data pipeline/etc.]
- Language: [TypeScript/Python/Java]
- Traffic: [patterns and volume]
- Data: [storage needs]

**Architecture Requirements:**
- [List components needed]

**Best Practices to Follow:**
1. Use constructs appropriately (L1, L2, L3)
2. Implement proper resource naming
3. Use environment-aware configurations
4. Add appropriate tags
5. Include security best practices
6. Add outputs for cross-stack references

**Deliverables:**
1. Stack structure and constructs
2. Props interface definitions
3. Complete stack implementation
4. Unit test examples
5. Deployment commands
```

### IaC Code Review

```
Review this [Terraform/CDK/Pulumi] code:

```[language]
[Paste code here]
```

**Review Criteria:**
1. Security issues
   - Hardcoded credentials
   - Overly permissive policies
   - Missing encryption
   - Public exposure risks

2. Best practices
   - Module structure
   - Variable usage
   - Resource naming
   - Tagging implementation
   - State management

3. Reliability
   - Error handling
   - Dependency management
   - Lifecycle policies
   - Backup configurations

4. Cost implications
   - Resource sizing
   - Reserved capacity opportunities
   - Unused resources

5. Maintainability
   - Code organization
   - Documentation
   - Reusability

Provide specific line-by-line feedback where applicable.
```

## Migration Prompts

### Migration Assessment

```
Assess the migration of [APPLICATION_NAME] to [TARGET_CLOUD]:

**Current State:**
- Hosting: [on-prem/other cloud/colocation]
- Architecture: [monolith/microservices/legacy]
- Technologies: [list]
- Dependencies: [internal/external]
- Data: [volume, sensitivity, location]

**Application Characteristics:**
- Users: [number and distribution]
- Traffic patterns: [steady/bursty/seasonal]
- SLA requirements: [availability, latency]
- Compliance: [requirements]

**Analysis Required:**
1. Migration strategy recommendation (rehost/replatform/refactor/rebuild)
2. Target architecture on [cloud]
3. Migration phases and timeline
4. Risk assessment and mitigation
5. Cost comparison (current vs target)
6. Team skills gap analysis
7. Dependencies and integration points

**Constraints:**
- Migration window: [timeframe]
- Budget: $[amount]
- Acceptable downtime: [duration]
```

### Database Migration

```
Plan a database migration:

**Source:**
- Database: [type and version]
- Size: [GB/TB]
- Tables: [number]
- Transactions: [TPS]
- Current location: [on-prem/cloud]

**Target:**
- Database: [type and version]
- Location: [cloud provider/region]

**Requirements:**
- Maximum acceptable downtime: [duration]
- Data validation approach
- Rollback strategy
- Performance requirements post-migration

**Deliverables:**
1. Migration approach (big bang/phased/CDC)
2. Pre-migration checklist
3. Migration steps with timeline
4. Data validation strategy
5. Performance testing plan
6. Rollback procedure
7. Post-migration verification
```

## Troubleshooting Prompts

### Performance Debugging

```
Help debug this cloud performance issue:

**Symptoms:**
- [Describe the issue]
- Started: [when]
- Frequency: [constant/intermittent]
- Impact: [latency increase/errors/timeouts]

**Architecture Context:**
[Paste relevant architecture]

**Metrics Observed:**
- CPU: [percentage]
- Memory: [percentage]
- Network: [bandwidth/latency]
- Database: [query times/connections]
- Error rate: [percentage]

**Recent Changes:**
- [List any recent deployments or changes]

**Analysis Required:**
1. Potential root causes (ranked by likelihood)
2. Diagnostic steps to confirm each cause
3. Immediate mitigation actions
4. Long-term fixes
5. Monitoring improvements to catch earlier
```

### Cost Spike Investigation

```
Investigate this cost spike:

**Cost Information:**
- Normal monthly spend: $[amount]
- Current/projected spend: $[amount]
- Spike percentage: [percentage]
- Started: [date]

**Cost Breakdown (if known):**
- [Service 1]: $[amount] (change from normal)
- [Service 2]: $[amount]
- [etc.]

**Recent Changes:**
- [List deployments, configuration changes, traffic changes]

**Investigation Required:**
1. Most likely causes based on cost breakdown
2. Commands/queries to identify the source
3. Immediate actions to reduce costs
4. Prevention measures for future
5. Monitoring/alerting improvements
```

## Comparison Prompts

### Service Comparison

```
Compare [SERVICE_A] vs [SERVICE_B] for [USE_CASE]:

**Requirements:**
- [List specific requirements]

**Evaluation Criteria:**
1. Features and capabilities
2. Performance characteristics
3. Pricing model and estimated costs
4. Operational complexity
5. Integration options
6. Vendor lock-in considerations
7. Community and support

**Context:**
- Scale: [expected usage]
- Team expertise: [relevant experience]
- Existing stack: [current technologies]

**Deliverables:**
1. Feature comparison matrix
2. Cost comparison for our usage
3. Pros/cons summary
4. Recommendation with reasoning
5. Migration considerations (if switching)
```

### Cloud Provider Comparison

```
Compare AWS, Azure, and GCP for [WORKLOAD_TYPE]:

**Workload Details:**
- Type: [web app/data analytics/ML/etc.]
- Scale: [users, data volume, compute needs]
- Requirements: [list specific needs]

**Evaluation Dimensions:**
1. Service availability and maturity
2. Pricing (compute, storage, network)
3. Global presence and regions needed
4. Compliance certifications
5. Integration with existing tools
6. Team expertise and learning curve
7. Support options and costs
8. Vendor ecosystem

**Current Situation:**
- Existing investments: [licenses, training, etc.]
- Team skills: [cloud experience]
- Preferred languages: [Python/Go/Java/etc.]

Provide specific service recommendations for each provider.
```

## FinOps Prompts

### FinOps Strategy

```
Develop a FinOps strategy for [ORGANIZATION]:

**Current State:**
- Cloud spend: $[amount]/month
- Growth rate: [percentage]/year
- Number of teams: [number]
- Cost visibility: [none/basic/advanced]
- Optimization maturity: [crawl/walk/run]

**Goals:**
- [List specific goals]

**Deliverables:**
1. FinOps team structure and RACI
2. Cost allocation and tagging strategy
3. Showback/chargeback model
4. Optimization workflow
5. Tooling recommendations
6. KPIs and reporting cadence
7. Governance policies
8. Training and enablement plan
```

### Commitment Planning

```
Help plan Reserved Instances / Savings Plans:

**Current Usage:**
- On-demand compute spend: $[amount]/month
- Instance types used: [list]
- Usage patterns: [steady/variable]
- Flexibility needs: [instance type/region/OS]

**Historical Data:**
- [Provide usage trends if available]

**Constraints:**
- Maximum upfront payment: $[amount]
- Commitment term preference: [1 year/3 year]
- Risk tolerance: [conservative/moderate/aggressive]

**Analysis Required:**
1. Coverage recommendation (percentage)
2. Commitment type recommendation (RI vs SP)
3. Expected savings
4. Break-even analysis
5. Risks and mitigation
6. Monitoring strategy
```

## Prompt Engineering Tips

### Context Setting

Always provide:
- Business context (industry, scale, constraints)
- Technical context (existing stack, team skills)
- Specific requirements (compliance, SLAs)
- Constraints (budget, timeline, resources)

### Effective Patterns

**For design prompts:**
```
Start with: "Design a [type] architecture for [context]..."
Include: Requirements, constraints, deliverables
End with: "Explain your reasoning for key decisions."
```

**For review prompts:**
```
Start with: "Review this [artifact] for [specific aspects]..."
Include: Current state, criteria, context
End with: "Prioritize findings by severity and impact."
```

**For troubleshooting:**
```
Start with: "Help debug/investigate [issue]..."
Include: Symptoms, metrics, recent changes
End with: "Provide diagnostic steps and potential fixes."
```

### Follow-up Prompts

```
# Drill down on a recommendation
"Explain more about [specific recommendation].
What are the implementation steps and potential issues?"

# Challenge the design
"What are the weaknesses of this architecture?
How would it fail under [specific scenario]?"

# Cost focus
"How can we reduce costs by 30% while maintaining
[specific requirements]?"

# Security focus
"What additional security controls would you recommend
if this system handled [sensitive data type]?"
```

### Iterative Refinement

```
# After initial response
"Good start. Now let's refine:
1. [Specific area to expand]
2. [Additional constraint to consider]
3. [Alternative approach to explore]"

# For trade-off analysis
"Compare the recommended approach with [alternative].
What are the trade-offs in terms of:
- Cost
- Complexity
- Performance
- Time to implement"
```

## Related

- [README.md](README.md) - Cloud architecture overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - IaC templates
