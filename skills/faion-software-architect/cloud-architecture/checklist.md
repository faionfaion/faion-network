# Cloud Architecture Checklist

Step-by-step checklist for designing, implementing, and operating cloud architectures.

## Phase 1: Requirements & Discovery

### Business Requirements
- [ ] Document business objectives and success metrics
- [ ] Identify stakeholders (app owners, security, operations, finance)
- [ ] Define SLAs (availability, latency, throughput)
- [ ] Document compliance requirements (GDPR, HIPAA, SOC2, PCI-DSS)
- [ ] Estimate budget constraints and TCO targets
- [ ] Identify data residency requirements
- [ ] Document growth projections (1 year, 3 year, 5 year)

### Technical Requirements
- [ ] Document current architecture (if migration)
- [ ] Identify workload types (web, batch, streaming, ML)
- [ ] Estimate peak and average load (RPS, concurrent users)
- [ ] Calculate data volume (storage, ingestion rate, retention)
- [ ] Identify integration points (internal, external APIs)
- [ ] Document latency requirements (p50, p95, p99)
- [ ] Identify RPO/RTO requirements

### Constraints
- [ ] Identify team skills and training needs
- [ ] Document existing vendor relationships/contracts
- [ ] Note timeline and migration constraints
- [ ] List technology mandates or restrictions
- [ ] Identify organizational standards and patterns

## Phase 2: Cloud Provider Selection

### Provider Evaluation
- [ ] Map requirements to provider capabilities
- [ ] Evaluate service availability in required regions
- [ ] Compare pricing models and estimate costs
- [ ] Assess support offerings and SLAs
- [ ] Review compliance certifications
- [ ] Evaluate existing skills and training investment
- [ ] Consider multi-cloud strategy needs

### Multi-Cloud Considerations
- [ ] Define which workloads go to which provider
- [ ] Plan for data synchronization between clouds
- [ ] Design unified identity and access management
- [ ] Plan network connectivity between providers
- [ ] Establish cross-cloud monitoring strategy
- [ ] Define vendor lock-in mitigation strategies

## Phase 3: Landing Zone Design

### Account/Project Structure
- [ ] Design organizational hierarchy (OUs, folders)
- [ ] Define account/subscription/project strategy
- [ ] Create naming conventions
- [ ] Establish tagging strategy and enforcement
- [ ] Define resource quotas and limits
- [ ] Design cost allocation model

### Identity & Access Management
- [ ] Design identity federation (SAML, OIDC)
- [ ] Plan SSO integration
- [ ] Define RBAC roles and policies
- [ ] Implement MFA requirements
- [ ] Design service account strategy
- [ ] Plan privileged access management (PAM)
- [ ] Configure JIT access for sensitive resources
- [ ] Document break-glass procedures

### Governance & Compliance
- [ ] Define organizational policies
- [ ] Create service control policies (SCPs)
- [ ] Implement guardrails for compliance
- [ ] Set up policy enforcement (Config, Policy, Organization Policy)
- [ ] Design approval workflows for exceptions
- [ ] Create compliance dashboards

## Phase 4: Network Architecture

### VPC/VNet Design
- [ ] Design IP addressing scheme (avoid overlaps)
- [ ] Plan CIDR ranges for growth
- [ ] Choose VPC mode (custom vs auto)
- [ ] Design subnet strategy (public, private, database)
- [ ] Plan for multiple availability zones
- [ ] Design for IPv6 support (dual-stack)

### Connectivity
- [ ] Design hub-and-spoke or mesh topology
- [ ] Plan VPC peering or Transit Gateway
- [ ] Configure VPN for hybrid connectivity
- [ ] Evaluate Direct Connect/ExpressRoute/Interconnect
- [ ] Design cross-region connectivity
- [ ] Plan DNS strategy (private zones, resolution)

### Network Security
- [ ] Design security group strategy
- [ ] Configure NACLs (if needed)
- [ ] Plan WAF deployment
- [ ] Configure DDoS protection
- [ ] Design network firewall rules
- [ ] Implement private endpoints for services
- [ ] Enable VPC flow logs
- [ ] Plan network segmentation

### Load Balancing & Traffic Management
- [ ] Select load balancer type (ALB, NLB, GLB)
- [ ] Design health check strategy
- [ ] Configure SSL/TLS termination
- [ ] Plan for global load balancing
- [ ] Design traffic routing policies (weighted, geo, latency)
- [ ] Configure CDN for static assets

## Phase 5: Compute Architecture

### Compute Selection
- [ ] Evaluate compute options (VMs, containers, serverless)
- [ ] Size instances appropriately (right-sizing)
- [ ] Select instance families for workload type
- [ ] Plan for GPU/accelerator needs (ML workloads)
- [ ] Design placement groups (if needed)
- [ ] Consider spot/preemptible for suitable workloads

### Container Orchestration
- [ ] Select Kubernetes distribution (EKS, AKS, GKE, self-managed)
- [ ] Design cluster topology (regional, multi-zone)
- [ ] Plan node pool strategy
- [ ] Configure cluster autoscaling
- [ ] Design namespace strategy
- [ ] Plan for service mesh (Istio, Linkerd)
- [ ] Configure pod security standards

### Serverless
- [ ] Evaluate serverless fit for workloads
- [ ] Design function architecture
- [ ] Plan cold start mitigation
- [ ] Configure memory and timeout settings
- [ ] Design event source integration
- [ ] Plan for concurrency limits

### Auto-Scaling
- [ ] Define scaling metrics (CPU, memory, custom)
- [ ] Configure scaling policies (target tracking, step)
- [ ] Set min/max instance counts
- [ ] Plan for scale-in protection
- [ ] Test scaling behavior under load
- [ ] Configure predictive scaling (if available)

## Phase 6: Data Architecture

### Database Selection
- [ ] Evaluate database requirements (ACID, scale, query patterns)
- [ ] Choose database type (relational, NoSQL, time-series, graph)
- [ ] Select managed service vs self-managed
- [ ] Plan for read replicas
- [ ] Design backup and recovery strategy
- [ ] Configure encryption at rest
- [ ] Plan for cross-region replication

### Storage Strategy
- [ ] Design object storage structure
- [ ] Configure storage classes and lifecycle policies
- [ ] Plan block storage for VMs
- [ ] Design shared file storage (if needed)
- [ ] Implement storage encryption
- [ ] Configure backup policies
- [ ] Plan for data archival

### Caching
- [ ] Identify caching opportunities
- [ ] Select caching solution (Redis, Memcached)
- [ ] Design cache invalidation strategy
- [ ] Plan for cache warming
- [ ] Configure cache sizing
- [ ] Design for cache failures

### Data Pipelines
- [ ] Design ETL/ELT pipelines
- [ ] Select streaming platform (Kafka, Kinesis, Pub/Sub)
- [ ] Plan data lake architecture
- [ ] Configure data catalog
- [ ] Implement data quality checks
- [ ] Design data lineage tracking

## Phase 7: Security Architecture

### Zero Trust Implementation
- [ ] Implement identity verification for all access
- [ ] Configure microsegmentation
- [ ] Enable continuous monitoring
- [ ] Implement device posture checks
- [ ] Configure context-aware access policies
- [ ] Plan for least privilege access

### Data Security
- [ ] Encrypt data at rest (KMS, customer-managed keys)
- [ ] Encrypt data in transit (TLS 1.3)
- [ ] Implement secrets management (Vault, Secrets Manager)
- [ ] Configure key rotation policies
- [ ] Plan for data classification
- [ ] Implement DLP controls

### Application Security
- [ ] Integrate SAST in CI/CD
- [ ] Configure DAST scanning
- [ ] Implement dependency scanning
- [ ] Configure container image scanning
- [ ] Plan for runtime protection
- [ ] Implement API security (rate limiting, auth)

### Compliance & Audit
- [ ] Enable audit logging (CloudTrail, Activity Log)
- [ ] Configure log retention
- [ ] Integrate with SIEM
- [ ] Set up compliance monitoring
- [ ] Plan for regular security assessments
- [ ] Document security controls

## Phase 8: Observability

### Logging
- [ ] Design centralized logging architecture
- [ ] Configure log aggregation
- [ ] Define log retention policies
- [ ] Implement structured logging
- [ ] Set up log-based alerting
- [ ] Plan for log analysis tools

### Metrics
- [ ] Define key performance indicators
- [ ] Configure infrastructure metrics
- [ ] Implement application metrics
- [ ] Design custom metrics for business KPIs
- [ ] Set up metric-based alerting
- [ ] Create dashboards for operations

### Tracing
- [ ] Implement distributed tracing
- [ ] Configure trace sampling
- [ ] Integrate with APM tools
- [ ] Design correlation IDs
- [ ] Plan for trace storage and analysis

### Alerting
- [ ] Define SLOs and error budgets
- [ ] Configure alert thresholds
- [ ] Design escalation policies
- [ ] Set up on-call rotations
- [ ] Implement alert suppression and grouping
- [ ] Create runbooks for common alerts

## Phase 9: Cost Optimization

### Cost Visibility
- [ ] Implement comprehensive tagging
- [ ] Configure cost allocation
- [ ] Set up budgets and alerts
- [ ] Create cost dashboards
- [ ] Implement showback/chargeback
- [ ] Enable cost anomaly detection

### Resource Optimization
- [ ] Identify unused resources
- [ ] Right-size over-provisioned resources
- [ ] Configure auto-scaling policies
- [ ] Implement scheduling for non-prod
- [ ] Evaluate spot/preemptible instances
- [ ] Review storage tier usage

### Commitment-Based Savings
- [ ] Analyze steady-state usage
- [ ] Evaluate Reserved Instances
- [ ] Consider Savings Plans
- [ ] Plan commitment coverage
- [ ] Schedule commitment reviews
- [ ] Monitor utilization rates

### FinOps Practices
- [ ] Establish FinOps team/practice
- [ ] Define cost ownership
- [ ] Create optimization workflows
- [ ] Schedule regular cost reviews
- [ ] Implement continuous optimization
- [ ] Track unit economics

## Phase 10: Disaster Recovery

### DR Planning
- [ ] Define RPO/RTO for each workload
- [ ] Select DR strategy (backup, pilot light, warm, active-active)
- [ ] Design data replication strategy
- [ ] Plan for cross-region failover
- [ ] Document recovery procedures
- [ ] Create DR runbooks

### Backup Strategy
- [ ] Configure automated backups
- [ ] Implement cross-region backup copies
- [ ] Test backup restoration regularly
- [ ] Document backup schedules
- [ ] Verify backup encryption
- [ ] Plan for backup retention

### Testing
- [ ] Schedule regular DR tests
- [ ] Conduct tabletop exercises
- [ ] Perform failover drills
- [ ] Test backup restoration
- [ ] Document test results
- [ ] Update procedures based on findings

## Phase 11: Operations

### Deployment
- [ ] Implement IaC for all infrastructure
- [ ] Configure CI/CD pipelines
- [ ] Design deployment strategies (blue-green, canary)
- [ ] Implement automated testing
- [ ] Configure rollback procedures
- [ ] Document deployment processes

### Change Management
- [ ] Implement change tracking
- [ ] Configure automated approvals
- [ ] Plan maintenance windows
- [ ] Design emergency change procedures
- [ ] Document change procedures

### Incident Response
- [ ] Define incident severity levels
- [ ] Create incident response procedures
- [ ] Configure alerting and escalation
- [ ] Implement communication templates
- [ ] Plan post-incident reviews
- [ ] Document lessons learned

## Phase 12: Documentation & Training

### Documentation
- [ ] Create architecture diagrams (C4 model)
- [ ] Document design decisions (ADRs)
- [ ] Write operational runbooks
- [ ] Create onboarding guides
- [ ] Maintain configuration documentation
- [ ] Update documentation regularly

### Training
- [ ] Identify skill gaps
- [ ] Plan training programs
- [ ] Schedule certification paths
- [ ] Conduct knowledge sharing sessions
- [ ] Create hands-on labs
- [ ] Document institutional knowledge

## Continuous Improvement

### Regular Reviews
- [ ] Schedule quarterly architecture reviews
- [ ] Conduct Well-Architected reviews
- [ ] Review cost optimization opportunities
- [ ] Assess security posture
- [ ] Evaluate new services and features
- [ ] Update documentation and training

### Metrics Tracking
- [ ] Track SLO compliance
- [ ] Monitor cost trends
- [ ] Review incident frequency
- [ ] Measure deployment frequency
- [ ] Track mean time to recovery
- [ ] Report on security metrics
