# GCP Checklists

Security, operational, and infrastructure checklists for GCP deployments (2025-2026).

## Security Checklist

### IAM Security

- [ ] Use Workload Identity Federation (no service account keys)
- [ ] Implement least privilege with predefined roles
- [ ] Enable MFA for all human users
- [ ] Use Cloud Identity for centralized identity management
- [ ] Review IAM policies with IAM Recommender
- [ ] Implement permission boundaries with deny policies
- [ ] Use organization-level constraints (Organization Policy)
- [ ] Separate service accounts per workload
- [ ] No primitive roles (Owner, Editor, Viewer) in production
- [ ] Audit IAM bindings quarterly
- [ ] Use groups for permission management (not individual users)
- [ ] Enable audit logging for IAM changes

### Network Security

- [ ] Run workloads in private subnets (no public IPs)
- [ ] Use VPC-native GKE clusters
- [ ] Configure firewall rules with least privilege
- [ ] Restrict SSH to IAP (Identity-Aware Proxy)
- [ ] Enable VPC Flow Logs for traffic monitoring
- [ ] Use Private Google Access for GCP APIs
- [ ] Implement VPC Service Controls for data exfiltration prevention
- [ ] Configure Cloud NAT for outbound traffic
- [ ] Use Cloud Armor for WAF protection
- [ ] Enable Cloud DNS Security (DNSSEC)
- [ ] Use internal load balancers for internal traffic
- [ ] Configure firewall insights for optimization

### Compute Engine Security

- [ ] Use Shielded VMs for sensitive workloads
- [ ] Enable OS Login (no SSH keys)
- [ ] Configure organization policies for public IP restrictions
- [ ] Use Confidential VMs for highly sensitive data
- [ ] Enable VM Manager for patch management
- [ ] Use encrypted boot disks (CMEK for sensitive)
- [ ] Configure organization policy constraints
- [ ] Disable serial port access
- [ ] Use sole-tenant nodes for compliance workloads
- [ ] Enable integrity monitoring

### Cloud Run Security

- [ ] Use dedicated service account (not default compute)
- [ ] Enable VPC connector for private resources
- [ ] Configure IAM for authentication (not --allow-unauthenticated in prod)
- [ ] Use Secret Manager for sensitive config
- [ ] Set concurrency and memory limits
- [ ] Enable Binary Authorization for trusted images
- [ ] Configure egress settings (all-traffic through VPC)
- [ ] Use custom service accounts with minimal permissions
- [ ] Enable Cloud Run audit logging
- [ ] Implement request timeout limits

### GKE Security

- [ ] Use Autopilot mode (or hardened Standard)
- [ ] Enable Workload Identity for pod authentication
- [ ] Configure private cluster (no public endpoint)
- [ ] Enable network policies
- [ ] Use Binary Authorization
- [ ] Enable GKE Sandbox for untrusted workloads
- [ ] Configure pod security standards
- [ ] Enable Container Threat Detection
- [ ] Use node auto-upgrade
- [ ] Configure authorized networks for master
- [ ] Enable Dataplane V2 (Cilium)
- [ ] Use Artifact Registry with vulnerability scanning

### Data Security

- [ ] Enable encryption at rest with CMEK
- [ ] Use Cloud KMS for key management
- [ ] Enable automatic key rotation
- [ ] Configure Object Lock for compliance
- [ ] Enable versioning on Cloud Storage buckets
- [ ] Block public access on storage buckets
- [ ] Use Secret Manager for credentials
- [ ] Enable Cloud SQL SSL connections
- [ ] Configure Cloud SQL private IP only
- [ ] Use AlloyDB for enterprise PostgreSQL
- [ ] Enable data loss prevention (DLP)

### Monitoring & Auditing

- [ ] Enable Cloud Audit Logs (Admin, Data Access)
- [ ] Configure log export to BigQuery/GCS
- [ ] Enable Security Command Center
- [ ] Configure alerting for security events
- [ ] Enable Cloud Asset Inventory
- [ ] Use Cloud Logging for centralized logs
- [ ] Enable Event Threat Detection
- [ ] Configure uptime checks
- [ ] Enable SLO monitoring
- [ ] Use Error Reporting for application errors

## Operational Checklist

### High Availability

- [ ] Deploy across minimum 3 zones (regional)
- [ ] Use regional managed instance groups
- [ ] Configure health checks for load balancers
- [ ] Enable multi-zone for Cloud SQL
- [ ] Use regional GKE clusters
- [ ] Configure Cloud CDN for global distribution
- [ ] Implement Cloud Load Balancing (global)
- [ ] Test failover procedures regularly
- [ ] Document disaster recovery procedures
- [ ] Use regional Cloud Storage (dual-region for critical)

### Backup & Recovery

- [ ] Enable automated Cloud SQL backups
- [ ] Configure cross-region backup for critical data
- [ ] Test restoration procedures regularly
- [ ] Enable persistent disk snapshots
- [ ] Schedule snapshot policies
- [ ] Use lifecycle policies for backup retention
- [ ] Document RPO and RTO requirements
- [ ] Configure backup export to Cloud Storage
- [ ] Enable point-in-time recovery for Cloud SQL
- [ ] Use Backup for GKE

### Monitoring & Observability

- [ ] Configure Cloud Monitoring dashboards
- [ ] Enable uptime checks for services
- [ ] Configure alerting policies
- [ ] Enable Cloud Trace for distributed tracing
- [ ] Use Cloud Profiler for performance
- [ ] Configure log-based metrics
- [ ] Enable Container Insights for GKE
- [ ] Set up SLO monitoring
- [ ] Configure notification channels
- [ ] Use Ops Agent for enhanced metrics

### Cost Management

- [ ] Enable billing export to BigQuery
- [ ] Configure budget alerts
- [ ] Review committed use discounts
- [ ] Use Recommender for right-sizing
- [ ] Configure lifecycle policies for storage
- [ ] Delete unused persistent disks
- [ ] Use preemptible/spot VMs where appropriate
- [ ] Review network egress costs
- [ ] Enable cost allocation labels
- [ ] Use Cloud Scheduler to stop dev environments

## Infrastructure Setup Checklist

### Organization Setup

- [ ] Configure organization hierarchy (folders)
- [ ] Enable organization policies
- [ ] Set up resource hierarchy (org/folders/projects)
- [ ] Configure billing accounts per business unit
- [ ] Enable Cloud Identity for user management
- [ ] Set up centralized logging project
- [ ] Configure Security Command Center
- [ ] Enable Access Transparency Logs
- [ ] Set up shared VPC host project
- [ ] Configure organization-level IAM

### VPC Setup

- [ ] Plan IP address ranges (avoid overlaps)
- [ ] Create custom VPC (not default)
- [ ] Configure subnets per region/tier
- [ ] Enable Private Google Access
- [ ] Configure Cloud NAT for outbound
- [ ] Set up Cloud Router for BGP
- [ ] Enable VPC Flow Logs
- [ ] Configure firewall rules (deny by default)
- [ ] Set up Shared VPC for multi-project
- [ ] Document network architecture

### Compute Engine Setup

- [ ] Create instance templates with best practices
- [ ] Configure managed instance groups
- [ ] Set up health checks
- [ ] Configure autoscaling policies
- [ ] Enable OS patch management
- [ ] Use startup scripts or Ops Agent
- [ ] Configure metadata and labels
- [ ] Set up scheduled snapshots
- [ ] Enable Shielded VM features
- [ ] Configure organization constraints

### Cloud Run Setup

- [ ] Create dedicated service accounts
- [ ] Configure VPC connector
- [ ] Set up Artifact Registry
- [ ] Configure build triggers (Cloud Build)
- [ ] Set resource limits (CPU, memory)
- [ ] Configure traffic splitting
- [ ] Enable Cloud Run audit logs
- [ ] Set up custom domains
- [ ] Configure Secret Manager integration
- [ ] Enable Binary Authorization

### GKE Setup

- [ ] Choose Autopilot or Standard mode
- [ ] Configure private cluster
- [ ] Enable Workload Identity
- [ ] Set up node pools per workload type
- [ ] Configure cluster autoscaler
- [ ] Enable network policies
- [ ] Set up Artifact Registry
- [ ] Configure pod security standards
- [ ] Enable GKE audit logging
- [ ] Set up maintenance windows

## Pre-Production Checklist

- [ ] Security review completed
- [ ] Load testing performed
- [ ] Disaster recovery tested
- [ ] Monitoring and alerting configured
- [ ] Runbooks documented
- [ ] Cost estimates reviewed
- [ ] Compliance requirements verified
- [ ] Change management process defined
- [ ] Rollback procedure documented
- [ ] On-call rotation established
- [ ] Penetration testing (if required)
- [ ] VPC-SC perimeter tested (dry-run mode)

## Cloud Run Deployment Checklist

- [ ] Container image scanned for vulnerabilities
- [ ] Health check endpoint implemented
- [ ] Graceful shutdown configured
- [ ] Resource limits set (CPU, memory)
- [ ] Concurrency configured appropriately
- [ ] Service account created (not default)
- [ ] Secrets from Secret Manager
- [ ] VPC connector for private resources
- [ ] Traffic management configured
- [ ] Logging configured (structured)
- [ ] Min instances set for production
- [ ] Custom domain configured with SSL

## Sources

- [GCP Security Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
- [GCP IAM Best Practices](https://cloud.google.com/iam/docs/using-iam-securely)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
- [GKE Security Best Practices](https://cloud.google.com/kubernetes-engine/docs/concepts/security-best-practices)
- [VPC Best Practices](https://cloud.google.com/vpc/docs/best-practices)
- [GCP Security Checklist 2026](https://www.sentinelone.com/cybersecurity-101/cloud-security/gcp-security-checklist/)
- [GCP Security Best Practices 2026](https://fidelissecurity.com/cybersecurity-101/best-practices/google-cloud-platform-gcp-security/)

---

*GCP Checklists | faion-infrastructure-engineer*
