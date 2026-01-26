# Backup Basics LLM Prompts

## Prompt 1: Backup Strategy Assessment

```
You are a backup and disaster recovery specialist. Analyze the following system and recommend a comprehensive backup strategy.

**System Information:**
- Environment: [production/staging/development]
- Data types: [databases, files, configurations, SaaS data]
- Total data volume: [X GB/TB]
- Data growth rate: [X% monthly]
- Current backup solution: [describe or "none"]
- Compliance requirements: [GDPR/HIPAA/SOC2/PCI-DSS/none]
- Budget constraints: [if any]

**Business Requirements:**
- Maximum acceptable downtime (RTO): [X hours]
- Maximum acceptable data loss (RPO): [X hours]
- Critical systems: [list]
- Existing infrastructure: [AWS/GCP/Azure/on-prem/hybrid]

**Deliverables:**
1. Recommended backup strategy (3-2-1 or enhanced variant)
2. Backup schedule for each system tier
3. Storage location recommendations
4. Retention policy recommendations
5. Testing schedule
6. Tool recommendations
7. Estimated storage costs

Provide specific, actionable recommendations with example configurations.
```

## Prompt 2: RTO/RPO Calculator

```
You are a backup planning specialist. Help me calculate appropriate RTO and RPO targets for my systems.

**Business Context:**
- Industry: [e.g., e-commerce, healthcare, SaaS]
- Revenue per hour of downtime: [estimate if known]
- Customer SLA commitments: [describe]
- Peak usage times: [describe]
- Number of users: [X]

**Systems to Analyze:**
1. [System 1]: [description, data sensitivity]
2. [System 2]: [description, data sensitivity]
3. [System 3]: [description, data sensitivity]

**For each system, provide:**
1. Recommended RTO with justification
2. Recommended RPO with justification
3. Backup strategy to achieve these objectives
4. Cost implications of different RTO/RPO levels
5. Risk assessment if objectives are not met

Format as a table with detailed explanations.
```

## Prompt 3: Backup Configuration Generator

```
You are a DevOps engineer specializing in backup automation. Generate backup configurations for the following setup.

**Infrastructure:**
- Cloud provider: [AWS/GCP/Azure]
- Databases: [PostgreSQL/MySQL/MongoDB/Redis]
- Application framework: [describe]
- Container orchestration: [Kubernetes/Docker Compose/ECS]
- CI/CD platform: [GitHub Actions/GitLab CI/Jenkins]

**Requirements:**
- Follow 3-2-1-1-0 backup strategy
- RTO: [X hours]
- RPO: [X hours]
- Retention: [X days hot, X days warm, X days cold]
- Encryption: Required
- Immutable backups: Required

**Generate:**
1. Complete backup configuration YAML
2. Backup script for databases
3. CI/CD workflow for automated backups
4. Monitoring and alerting configuration
5. Restore runbook outline

Use production-ready code with comments explaining each section.
```

## Prompt 4: Disaster Recovery Plan Generator

```
You are a disaster recovery planning specialist. Create a comprehensive DR plan for the following scenario.

**Organization:**
- Type: [startup/enterprise/non-profit]
- Industry: [describe]
- Size: [employees, data centers]

**Current Infrastructure:**
- Primary region: [describe]
- DR region: [describe or "none"]
- Existing backup solution: [describe]
- Current RTO capability: [X hours]
- Current RPO capability: [X hours]

**Scenarios to Cover:**
1. Database corruption/data loss
2. Regional cloud outage
3. Ransomware attack
4. Accidental deletion by administrator
5. Hardware failure

**For each scenario, provide:**
1. Detection mechanism
2. Step-by-step recovery procedure
3. Communication plan
4. Verification checklist
5. Post-incident actions
6. Estimated recovery time

Include specific commands and configurations where applicable.
```

## Prompt 5: Backup Audit Review

```
You are a backup compliance auditor. Review the following backup setup and identify gaps, risks, and improvements.

**Current Setup:**
- Backup schedule: [describe]
- Backup locations: [describe]
- Encryption: [yes/no, method]
- Immutability: [yes/no, method]
- Testing frequency: [describe]
- Retention policy: [describe]
- Monitoring: [describe]
- Documentation: [describe]

**Compliance Requirements:**
- [List applicable: GDPR, HIPAA, SOC2, PCI-DSS, ISO 27001]

**Audit against:**
1. 3-2-1-1-0 backup rule compliance
2. Industry best practices (2025)
3. Compliance requirements
4. Security standards

**Provide:**
1. Compliance scorecard (0-100%)
2. Critical gaps (must fix)
3. High-priority improvements
4. Medium-priority improvements
5. Recommendations with priority ranking
6. Remediation timeline suggestion
```

## Prompt 6: Backup Cost Optimizer

```
You are a FinOps specialist focusing on backup cost optimization. Analyze the following backup infrastructure and recommend optimizations.

**Current Backup Costs:**
- Monthly storage: $[X]
- Data transfer: $[X]
- Backup software/licensing: $[X]
- Total monthly: $[X]

**Current Configuration:**
- Total backup data: [X TB]
- Retention period: [X days]
- Backup frequency: [describe]
- Storage tiers used: [describe]
- Deduplication: [yes/no]
- Compression: [yes/no]

**Requirements:**
- Cannot reduce RTO below: [X hours]
- Cannot reduce RPO below: [X hours]
- Compliance retention minimum: [X days]

**Provide:**
1. Current cost breakdown analysis
2. Optimization opportunities with estimated savings
3. Storage tier recommendations
4. Retention policy optimization
5. Deduplication/compression recommendations
6. Alternative tools/providers comparison
7. Implementation priority based on ROI
```

## Prompt 7: Backup Testing Strategy

```
You are a backup reliability engineer. Design a comprehensive backup testing strategy for our environment.

**Environment:**
- Production systems: [list]
- Data sensitivity: [PII, financial, healthcare, general]
- Current testing: [describe current testing, if any]
- Available testing environment: [yes/no, describe]

**Constraints:**
- Maintenance windows: [describe]
- Testing budget: [describe]
- Team capacity: [describe]

**Design a testing strategy that includes:**
1. Automated daily verification tests
2. Weekly integrity checks
3. Monthly restore tests
4. Quarterly DR drills
5. Annual comprehensive review

**For each test type, specify:**
- What to test
- How to test (automation vs manual)
- Success criteria
- Failure handling
- Documentation requirements
- Reporting format
```

## Prompt 8: SaaS Backup Strategy

```
You are a SaaS data protection specialist. Design a backup strategy for our SaaS application portfolio.

**SaaS Applications:**
1. [App 1]: [data types, criticality, native backup capabilities]
2. [App 2]: [data types, criticality, native backup capabilities]
3. [App 3]: [data types, criticality, native backup capabilities]

**Requirements:**
- Centralized backup management preferred
- Data residency requirements: [describe]
- Compliance: [GDPR/HIPAA/etc.]
- Budget: [if known]

**Provide:**
1. Analysis of native backup limitations for each SaaS
2. Third-party backup tool recommendations
3. Backup schedule for each application
4. Retention policy by data type
5. Cross-SaaS search and restore capabilities
6. Cost comparison of solutions
7. Implementation roadmap
```

## Prompt 9: Ransomware-Resilient Backup Design

```
You are a cybersecurity specialist focusing on ransomware recovery. Design a ransomware-resilient backup architecture.

**Current Environment:**
- Infrastructure: [describe]
- Current backup solution: [describe]
- Network segmentation: [yes/no]
- Immutable backups: [yes/no]

**Security Posture:**
- Security monitoring: [describe]
- Incident response plan: [exists/not exists]
- Previous incidents: [if any]

**Design requirements:**
1. Immutable backup strategy
2. Air-gapped backup option
3. Rapid detection of ransomware encryption
4. Clean recovery procedure
5. Prevention of backup compromise

**Provide:**
1. Architecture diagram (describe in detail)
2. Immutability implementation (Object Lock, WORM tape, etc.)
3. Air-gap strategy (physical or logical)
4. Detection mechanisms for backup tampering
5. Recovery procedure from immutable backups
6. Testing methodology for ransomware scenarios
7. Timeline for implementation
```

## Prompt 10: Migration Backup Strategy

```
You are a cloud migration specialist. Design a backup strategy for a major infrastructure migration.

**Migration Details:**
- Source: [on-prem/Cloud A]
- Target: [Cloud B]
- Data volume: [X TB]
- Migration timeline: [X weeks/months]
- Downtime tolerance: [X hours]

**Systems to Migrate:**
1. [System 1]: [type, size, criticality]
2. [System 2]: [type, size, criticality]
3. [System 3]: [type, size, criticality]

**Design:**
1. Pre-migration backup strategy
2. During-migration backup approach
3. Post-migration backup validation
4. Rollback procedure if migration fails
5. Parallel backup systems during transition
6. Cutover backup verification
7. Decommissioning old backup infrastructure

Include specific timing, checkpoints, and go/no-go criteria.
```

---

*Backup Basics LLM Prompts | faion-cicd-engineer*
