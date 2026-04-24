# GCP Architecture Checklists

Landing zone, architecture design, and implementation checklists for Google Cloud Platform.

---

## Landing Zone Setup Checklist

### Phase 1: Planning

#### Team and Governance

- [ ] Assemble cross-functional team (security, identity, network, ops)
- [ ] Define project governance model
- [ ] Establish naming conventions
- [ ] Define tagging/labeling strategy
- [ ] Set up communication channels
- [ ] Create project timeline with milestones

#### Requirements Gathering

- [ ] Document compliance requirements (SOC2, HIPAA, PCI, etc.)
- [ ] Define data residency requirements
- [ ] Identify integration points (on-premises, other clouds)
- [ ] List initial workloads to migrate
- [ ] Define SLA requirements per environment

---

### Phase 2: Identity and Access

#### Organization Setup

- [ ] Create Google Cloud organization
- [ ] Connect Cloud Identity or Google Workspace
- [ ] Configure organization admin
- [ ] Set up super admin recovery
- [ ] Enable audit logging at org level

#### Identity Federation

- [ ] Choose identity provider (Google, external IdP)
- [ ] Configure SSO with corporate IdP
- [ ] Set up identity groups mapping
- [ ] Define group naming conventions
- [ ] Configure MFA requirements

#### IAM Foundation

- [ ] Define IAM policy for organization
- [ ] Create standard IAM roles per function
- [ ] Implement least privilege principle
- [ ] Avoid primitive roles (Owner/Editor/Viewer)
- [ ] Set up service accounts naming convention
- [ ] Configure Workload Identity Federation for CI/CD

---

### Phase 3: Resource Hierarchy

#### Organization Structure

- [ ] Design folder hierarchy (by dept, env, or both)
- [ ] Create environment folders (prod, staging, dev)
- [ ] Set up shared infrastructure folder
- [ ] Document hierarchy in architecture diagram

#### Project Strategy

- [ ] Define project creation process
- [ ] Set up project naming convention
- [ ] Configure default project settings
- [ ] Create shared services projects:
  - [ ] Shared VPC host project
  - [ ] Shared monitoring project
  - [ ] Security/audit project
  - [ ] CI/CD project

#### Organization Policies

- [ ] Restrict resource locations
- [ ] Disable service account key creation
- [ ] Require OS Login for VMs
- [ ] Restrict VM external IPs
- [ ] Disable default network creation
- [ ] Enforce uniform bucket-level access

---

### Phase 4: Network Architecture

#### VPC Design

- [ ] Choose VPC pattern (single, shared, hub-spoke)
- [ ] Design IP address plan (non-overlapping)
- [ ] Plan for future growth (sufficient CIDR space)
- [ ] Document network topology

#### Shared VPC (if applicable)

- [ ] Create host project
- [ ] Configure shared VPC
- [ ] Define service project attachment process
- [ ] Set up network IAM delegation

#### Subnets

- [ ] Create subnets per region
- [ ] Configure secondary ranges for GKE
- [ ] Enable Private Google Access
- [ ] Configure VPC Flow Logs

#### Connectivity

- [ ] Set up Cloud NAT for private instances
- [ ] Configure Private Service Connect for Google APIs
- [ ] Plan hybrid connectivity (VPN/Interconnect)
- [ ] Set up DNS configuration (Cloud DNS)

#### Firewall

- [ ] Define firewall policy hierarchy
- [ ] Create base deny-all rules
- [ ] Set up allow rules by service tag
- [ ] Document all firewall rules

---

### Phase 5: Security Controls

#### Encryption

- [ ] Verify default encryption at rest
- [ ] Set up CMEK for sensitive data (if required)
- [ ] Configure encryption in transit (TLS)
- [ ] Document key management process

#### Logging and Monitoring

- [ ] Enable Cloud Audit Logs
- [ ] Configure log sinks to central location
- [ ] Set up Security Command Center
- [ ] Enable data access logging for sensitive APIs
- [ ] Configure log retention policies

#### Security Services

- [ ] Enable Security Command Center
- [ ] Configure Cloud Armor (if public workloads)
- [ ] Set up VPC Service Controls (if sensitive data)
- [ ] Enable Binary Authorization (if containers)

---

### Phase 6: Operations

#### Monitoring Setup

- [ ] Configure Cloud Monitoring workspace
- [ ] Set up alerting policies
- [ ] Create operations dashboards
- [ ] Configure notification channels

#### Cost Management

- [ ] Link billing account
- [ ] Set up billing export to BigQuery
- [ ] Create budgets and alerts
- [ ] Configure cost allocation labels
- [ ] Review Recommender insights

#### Automation

- [ ] Set up IaC repository (Terraform)
- [ ] Configure CI/CD for infrastructure
- [ ] Document deployment procedures
- [ ] Create runbooks for common operations

---

## Architecture Framework Checklist

### Operational Excellence

- [ ] Infrastructure defined as code
- [ ] CI/CD pipelines for all deployments
- [ ] Automated testing in pipelines
- [ ] Incident management process defined
- [ ] Runbooks documented
- [ ] Post-incident reviews conducted
- [ ] Change management process in place

### Security, Privacy, Compliance

- [ ] Zero trust architecture implemented
- [ ] All data encrypted at rest and in transit
- [ ] IAM follows least privilege
- [ ] Workload Identity used (no SA keys)
- [ ] Audit logging enabled
- [ ] Security scanning in CI/CD
- [ ] Compliance requirements documented and verified

### Reliability

- [ ] Multi-zone deployment for production
- [ ] Auto-scaling configured
- [ ] Health checks implemented
- [ ] Graceful degradation designed
- [ ] Backup strategy documented
- [ ] DR plan tested
- [ ] SLOs defined and monitored

### Cost Optimization

- [ ] Right-sizing analysis performed
- [ ] Committed use discounts evaluated
- [ ] Spot VMs used for fault-tolerant workloads
- [ ] Storage lifecycle policies configured
- [ ] Idle resources identified and removed
- [ ] Cost allocation by team/project
- [ ] Regular cost reviews scheduled

### Performance Optimization

- [ ] Resource requests/limits defined
- [ ] Auto-scaling policies tuned
- [ ] CDN configured for static content
- [ ] Database connection pooling
- [ ] Caching strategy implemented
- [ ] Performance testing in CI/CD
- [ ] Monitoring for latency and throughput

---

## GKE Architecture Checklist

### Cluster Design

- [ ] Choose mode: Autopilot (recommended) vs Standard
- [ ] Select regional vs zonal deployment
- [ ] Plan node pool strategy
- [ ] Define resource quotas

### Security

- [ ] Enable private cluster
- [ ] Configure Workload Identity
- [ ] Enable Binary Authorization
- [ ] Set up Pod Security Standards
- [ ] Configure network policies
- [ ] Enable GKE Security Posture

### Networking

- [ ] Plan pod and service CIDR ranges
- [ ] Configure authorized networks for control plane
- [ ] Set up ingress controller
- [ ] Configure Cloud Armor (if public)
- [ ] Enable container-native load balancing

### Operations

- [ ] Configure maintenance windows
- [ ] Set up release channel (REGULAR recommended)
- [ ] Enable cluster autoscaler
- [ ] Configure HPA/VPA
- [ ] Set up monitoring and logging
- [ ] Configure cost allocation labels

### Node Pools (Standard mode)

- [ ] Create general-purpose pool
- [ ] Configure spot pool for batch workloads
- [ ] Set appropriate min/max nodes
- [ ] Enable auto-repair and auto-upgrade
- [ ] Configure taints for workload isolation

---

## Cloud SQL Architecture Checklist

### Instance Configuration

- [ ] Choose database version
- [ ] Select appropriate tier
- [ ] Configure storage (type, size, auto-increase)
- [ ] Set up maintenance window
- [ ] Configure deletion protection (production)

### High Availability

- [ ] Enable Regional HA (production)
- [ ] Configure read replicas (if needed)
- [ ] Test failover procedure

### Security

- [ ] Enable private IP only
- [ ] Require SSL connections
- [ ] Configure authorized networks
- [ ] Set up IAM database authentication
- [ ] Enable audit logging

### Backup

- [ ] Enable automated backups
- [ ] Configure PITR (production)
- [ ] Set retention period
- [ ] Test restore procedure
- [ ] Consider cross-region backups

### Monitoring

- [ ] Enable Query Insights
- [ ] Set up alerting for connections/CPU/memory
- [ ] Monitor replication lag (if replicas)
- [ ] Configure slow query logging

---

## Cloud Storage + CDN Checklist

### Bucket Configuration

- [ ] Enable uniform bucket-level access
- [ ] Configure versioning
- [ ] Set up lifecycle policies
- [ ] Configure CORS (if web access)
- [ ] Enable access logging

### Security

- [ ] Configure IAM permissions (no public unless required)
- [ ] Enable CMEK (if required)
- [ ] Set up VPC Service Controls (if sensitive)
- [ ] Configure signed URLs for temporary access

### CDN Configuration

- [ ] Create backend bucket
- [ ] Enable Cloud CDN
- [ ] Configure cache policy
- [ ] Set up SSL certificate
- [ ] Configure URL map
- [ ] Set up Cloud Armor (if needed)

### Operations

- [ ] Set up monitoring for cache hit ratio
- [ ] Configure alerting for errors
- [ ] Document cache invalidation procedure
- [ ] Test CDN performance

---

## Pre-Production Architecture Review

### Security Review

- [ ] IAM audit completed
- [ ] Network security review passed
- [ ] Encryption verified
- [ ] Vulnerability scan clean
- [ ] Penetration test (if required)
- [ ] Compliance checklist verified

### Performance Review

- [ ] Load testing completed
- [ ] Auto-scaling validated
- [ ] Cold start latency acceptable
- [ ] Database performance verified
- [ ] CDN configured and tested

### Operational Review

- [ ] Monitoring configured
- [ ] Alerting tested
- [ ] Runbooks documented
- [ ] On-call procedures defined
- [ ] Incident response plan ready

### Cost Review

- [ ] Resource sizing optimized
- [ ] CUDs evaluated
- [ ] Budget alerts configured
- [ ] Cost allocation labels applied
- [ ] FinOps review completed

### Documentation Review

- [ ] Architecture diagram current
- [ ] Network diagram updated
- [ ] Security documentation complete
- [ ] Operational procedures documented
- [ ] DR plan documented and tested

---

*GCP Architecture Checklists v2.0 | Updated: 2026-01*
