# Azure Architecture Checklists

Implementation checklists for Azure Well-Architected Framework, Landing Zones, and Governance.

## Well-Architected Framework Checklists

### Reliability Checklist

#### Design

- [ ] Define reliability targets (SLA, SLO, SLI)
- [ ] Identify critical flows and dependencies
- [ ] Map failure modes and recovery strategies
- [ ] Design for availability zones (minimum 2)
- [ ] Plan for regional failover (critical workloads)

#### Implementation

- [ ] Implement health probes for all services
- [ ] Configure auto-scaling based on metrics
- [ ] Set up circuit breakers for external dependencies
- [ ] Implement retry policies with exponential backoff
- [ ] Enable zone-redundant storage (ZRS/GZRS)

#### Data Protection

- [ ] Configure automated backups
- [ ] Test backup restoration (quarterly)
- [ ] Implement geo-redundant backups for production
- [ ] Document RTO/RPO requirements
- [ ] Enable soft delete for storage and Key Vault

#### Monitoring

- [ ] Set up availability alerts (<99.9%)
- [ ] Configure dependency monitoring
- [ ] Implement synthetic monitoring
- [ ] Create runbooks for common failures
- [ ] Document escalation procedures

### Security Checklist

#### Identity & Access

- [ ] Implement Microsoft Entra ID for all identities
- [ ] Enable MFA for all users (no exceptions)
- [ ] Configure Privileged Identity Management (PIM)
- [ ] Implement just-in-time (JIT) access
- [ ] Review access permissions quarterly

#### Network Security

- [ ] Deploy Azure Firewall or NVA
- [ ] Implement Network Security Groups (NSGs)
- [ ] Enable DDoS Protection Standard
- [ ] Use Private Endpoints for PaaS services
- [ ] Disable public endpoints where possible

#### Data Protection

- [ ] Encrypt data at rest (Azure-managed or CMK)
- [ ] Encrypt data in transit (TLS 1.2+)
- [ ] Classify data and apply sensitivity labels
- [ ] Implement Key Vault for secrets management
- [ ] Enable Key Vault soft delete and purge protection

#### Threat Protection

- [ ] Enable Microsoft Defender for Cloud
- [ ] Configure Microsoft Sentinel for SIEM
- [ ] Enable diagnostic logging for all resources
- [ ] Implement Azure WAF for web applications
- [ ] Review security recommendations weekly

#### Compliance

- [ ] Enable Azure Policy for compliance
- [ ] Document compliance requirements (SOC2, ISO, GDPR)
- [ ] Configure compliance dashboards
- [ ] Schedule regular compliance audits
- [ ] Maintain evidence for audit trails

### Cost Optimization Checklist

#### Planning

- [ ] Define cost ownership model
- [ ] Set up cost allocation tags
- [ ] Configure budgets and alerts
- [ ] Review Azure Advisor cost recommendations
- [ ] Identify workloads for reservations

#### Right-Sizing

- [ ] Review VM utilization (monthly)
- [ ] Identify idle resources
- [ ] Resize underutilized resources
- [ ] Consider B-series for variable workloads
- [ ] Use spot instances for interruptible workloads

#### Purchasing

- [ ] Purchase Azure Reservations (1-3 year)
- [ ] Evaluate Savings Plans for compute
- [ ] Use Azure Hybrid Benefit for Windows/SQL
- [ ] Consolidate dev/test workloads (dev/test pricing)
- [ ] Review unused reservations

#### Monitoring

- [ ] Set up Cost Management alerts
- [ ] Review anomaly detection alerts
- [ ] Generate monthly cost reports
- [ ] Track cost per environment/team
- [ ] Review storage lifecycle policies

### Operational Excellence Checklist

#### Infrastructure as Code

- [ ] All infrastructure defined in code
- [ ] IaC stored in version control
- [ ] Code review required for changes
- [ ] Automated testing for IaC
- [ ] Documentation generated from code

#### CI/CD Pipelines

- [ ] Automated builds on commit
- [ ] Automated testing in pipelines
- [ ] Staged deployments (dev/staging/prod)
- [ ] Automated rollback capability
- [ ] Deployment approvals for production

#### Monitoring & Observability

- [ ] Centralized logging (Log Analytics)
- [ ] Application Performance Monitoring (APM)
- [ ] Custom dashboards for key metrics
- [ ] Alerting for critical metrics
- [ ] Log retention policies defined

#### Documentation

- [ ] Architecture diagrams up to date
- [ ] Runbooks for common operations
- [ ] Incident response procedures documented
- [ ] Change management process defined
- [ ] Post-incident reviews conducted

### Performance Efficiency Checklist

#### Capacity Planning

- [ ] Define performance baselines
- [ ] Document expected growth patterns
- [ ] Plan for peak load scenarios
- [ ] Configure auto-scaling rules
- [ ] Test scaling behavior under load

#### Optimization

- [ ] Implement caching (Redis, CDN)
- [ ] Optimize database queries
- [ ] Use connection pooling
- [ ] Enable compression for web traffic
- [ ] Review and optimize cold start times

#### Monitoring

- [ ] Set up performance alerts
- [ ] Monitor response times (P95, P99)
- [ ] Track resource utilization
- [ ] Implement distributed tracing
- [ ] Conduct regular load testing

---

## Landing Zone Checklists

### Design Area 1: Billing & Tenant

- [ ] Microsoft Entra tenant created
- [ ] Enterprise Agreement or MCA configured
- [ ] Billing account structure defined
- [ ] Cost management configured
- [ ] Invoice sections/departments set up

### Design Area 2: Identity & Access Management

#### Microsoft Entra ID

- [ ] Microsoft Entra ID configured
- [ ] Custom domains added and verified
- [ ] Emergency access accounts created
- [ ] Conditional Access policies enabled
- [ ] B2B/B2C configured (if needed)

#### RBAC Strategy

- [ ] Custom roles defined (if needed)
- [ ] PIM enabled for privileged roles
- [ ] Groups used instead of individual assignments
- [ ] Service principals documented
- [ ] Workload identities configured

### Design Area 3: Management Groups & Subscriptions

#### Hierarchy

- [ ] Management group hierarchy designed
- [ ] Root management group secured
- [ ] Default management group for new subscriptions set
- [ ] Subscription naming convention defined
- [ ] Subscription vending process documented

#### Organization

- [ ] Platform management group created
- [ ] Landing zones management group created
- [ ] Sandbox management group created (optional)
- [ ] Decommissioned management group created
- [ ] Corp/Online separation (if needed)

### Design Area 4: Network Topology & Connectivity

#### Hub Network

- [ ] Hub VNet deployed
- [ ] Azure Firewall or NVA deployed
- [ ] VPN Gateway configured (if needed)
- [ ] ExpressRoute configured (if needed)
- [ ] Azure Bastion deployed

#### Spoke Networks

- [ ] Spoke VNet template created
- [ ] VNet peering configured
- [ ] Route tables configured
- [ ] Network Security Groups applied
- [ ] Private DNS zones configured

#### Connectivity

- [ ] DNS resolution strategy defined
- [ ] Private endpoints strategy defined
- [ ] Internet egress path defined
- [ ] DDoS Protection enabled
- [ ] Network monitoring configured

### Design Area 5: Security

- [ ] Microsoft Defender for Cloud enabled
- [ ] Security benchmarks applied
- [ ] Vulnerability assessment configured
- [ ] Security contacts configured
- [ ] Regulatory compliance dashboards enabled

### Design Area 6: Management

#### Monitoring

- [ ] Log Analytics workspace deployed
- [ ] Diagnostic settings policy deployed
- [ ] Azure Monitor Insights enabled
- [ ] Alert rules configured
- [ ] Action groups configured

#### Business Continuity

- [ ] Backup policy defined
- [ ] Recovery Services Vault deployed
- [ ] Azure Site Recovery configured (if needed)
- [ ] Backup monitoring enabled
- [ ] Disaster recovery tested

#### Patching & Updates

- [ ] Update Management enabled
- [ ] Maintenance windows defined
- [ ] Patch compliance monitored
- [ ] Image update process defined
- [ ] Container image scanning enabled

### Design Area 7: Governance

#### Azure Policy

- [ ] Policy initiative deployed
- [ ] Tagging policies enforced
- [ ] Allowed locations policy deployed
- [ ] Allowed resource types policy (if needed)
- [ ] Diagnostic settings policy deployed

#### Compliance

- [ ] Compliance dashboards configured
- [ ] Exemption process documented
- [ ] Policy remediation tasks monitored
- [ ] Compliance reports automated
- [ ] Audit logging enabled

### Design Area 8: Platform Automation & DevOps

#### IaC Foundation

- [ ] IaC repository created
- [ ] Module library established
- [ ] CI/CD pipelines configured
- [ ] Testing framework implemented
- [ ] Documentation automation enabled

#### Deployment Automation

- [ ] Landing zone deployment automated
- [ ] Subscription vending automated
- [ ] Policy deployment automated
- [ ] Monitoring deployment automated
- [ ] Network deployment automated

---

## Governance Maturity Checklist

### Level 1: Basic

- [ ] Management group hierarchy exists
- [ ] Tagging policy in place
- [ ] Basic RBAC configured
- [ ] Azure Monitor enabled
- [ ] Manual policy deployment

### Level 2: Standardized

- [ ] Comprehensive policy initiatives
- [ ] PIM configured for all privileged roles
- [ ] Automated policy deployment
- [ ] Cost Management configured
- [ ] Security baseline applied

### Level 3: Advanced

- [ ] Governance as Code (fully automated)
- [ ] Custom policies for organizational needs
- [ ] Automated compliance reporting
- [ ] Self-service subscription vending
- [ ] Integration with ITSM tools

### Level 4: Optimized

- [ ] Continuous compliance monitoring
- [ ] Predictive cost management
- [ ] Automated remediation
- [ ] Advanced threat protection
- [ ] FinOps practices implemented

---

## Pre-Deployment Checklist

### Before Landing Zone Deployment

- [ ] Requirements documented
- [ ] Network IP addressing planned
- [ ] Naming conventions defined
- [ ] Tagging strategy defined
- [ ] RBAC model designed
- [ ] Security requirements documented
- [ ] Compliance requirements identified
- [ ] Monitoring strategy defined
- [ ] IaC templates tested in sandbox
- [ ] Stakeholder approval obtained

### Before Workload Deployment

- [ ] Landing zone prerequisites met
- [ ] Network connectivity verified
- [ ] DNS resolution tested
- [ ] Identity integration verified
- [ ] Security policies compliant
- [ ] Monitoring configured
- [ ] Backup policy applied
- [ ] Cost tags applied
- [ ] Documentation complete
- [ ] Runbooks created
