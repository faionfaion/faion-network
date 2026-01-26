# GCP Checklists

Pre-deployment, security, and operational checklists for Google Cloud Platform.

---

## Project Setup Checklist

### Initial Configuration

- [ ] Create project with meaningful ID (cannot be changed)
- [ ] Link billing account
- [ ] Enable required APIs
- [ ] Set up organization hierarchy (folders)
- [ ] Configure labels for cost allocation
- [ ] Set up budget alerts

### IAM Setup

- [ ] Create service accounts with descriptive names
- [ ] Apply least privilege principle
- [ ] Avoid primitive roles (Owner/Editor/Viewer)
- [ ] Configure Workload Identity Federation for external access
- [ ] Enable audit logging
- [ ] Set up IAM Recommender

### Networking

- [ ] Plan IP address ranges (avoid overlaps)
- [ ] Create custom VPC (not default)
- [ ] Configure subnets per region
- [ ] Set up Cloud NAT for private instances
- [ ] Configure firewall rules (deny by default)
- [ ] Enable VPC Flow Logs

---

## GKE Deployment Checklist

### Cluster Creation

- [ ] Choose mode: Autopilot (recommended) or Standard
- [ ] Select appropriate region/zone
- [ ] Plan node pool strategy
- [ ] Configure private cluster (recommended)
- [ ] Enable Workload Identity
- [ ] Enable Binary Authorization (if required)
- [ ] Configure maintenance windows

### Autopilot-Specific

- [ ] Review Autopilot constraints for workload compatibility
- [ ] Configure compute classes if needed
- [ ] Set up HPA for autoscaling
- [ ] Review pod resource requests

### Standard-Specific

- [ ] Configure node pools by workload type
- [ ] Enable cluster autoscaler
- [ ] Set appropriate min/max nodes
- [ ] Configure node auto-provisioning
- [ ] Consider Spot VMs for non-critical workloads
- [ ] Set up node taints for workload isolation

### Security

- [ ] Enable Workload Identity
- [ ] Configure Pod Security Standards
- [ ] Enable network policies
- [ ] Set up namespace isolation
- [ ] Configure RBAC
- [ ] Enable GKE Security Posture

### Networking

- [ ] Plan pod and service CIDR ranges
- [ ] Configure authorized networks for control plane
- [ ] Set up ingress (GKE Ingress or Istio)
- [ ] Configure Cloud Armor if public-facing
- [ ] Enable Container-native load balancing

### Monitoring

- [ ] Enable GKE metrics in Cloud Monitoring
- [ ] Configure Cloud Logging
- [ ] Set up alerting policies
- [ ] Enable cost allocation (namespace labels)

---

## Cloud Run Deployment Checklist

### Service Configuration

- [ ] Choose appropriate region (latency, compliance)
- [ ] Set CPU allocation strategy (request-based vs always-on)
- [ ] Configure memory and CPU limits
- [ ] Set concurrency (requests per instance)
- [ ] Configure min/max instances
- [ ] Set request timeout

### Container

- [ ] Use minimal base image
- [ ] Set proper health check endpoint
- [ ] Configure graceful shutdown
- [ ] Avoid large container images
- [ ] Use Artifact Registry (not Docker Hub)

### Security

- [ ] Configure IAM for invocation (authenticated vs unauthenticated)
- [ ] Use Secret Manager for secrets
- [ ] Enable VPC connector for private resources
- [ ] Configure Cloud Armor if needed
- [ ] Enable Binary Authorization (if required)

### Networking

- [ ] Configure custom domain (if needed)
- [ ] Set up VPC connector for private access
- [ ] Configure egress settings
- [ ] Enable Cloud CDN for static content

### Monitoring

- [ ] Set up custom metrics
- [ ] Configure alerting for error rates
- [ ] Monitor cold start latency
- [ ] Set up billing alerts

---

## IAM Security Checklist

### Service Accounts

- [ ] Avoid service account keys (use Workload Identity Federation)
- [ ] If keys required: rotate regularly, store securely
- [ ] Use descriptive names
- [ ] Document purpose and owner
- [ ] Disable unused service accounts
- [ ] Review permissions quarterly

### Workload Identity Federation

- [ ] Create separate pools per environment
- [ ] Configure attribute mappings carefully
- [ ] Avoid user-modifiable attributes in mappings
- [ ] Test with minimal permissions first
- [ ] Enable audit logging
- [ ] Document provider configurations

### IAM Policies

- [ ] Use predefined roles when possible
- [ ] Create custom roles for specific needs
- [ ] Avoid primitive roles
- [ ] Apply conditions (time, resource attributes)
- [ ] Review IAM Recommender suggestions
- [ ] Remove unused bindings

### Audit

- [ ] Enable data access logs for sensitive APIs
- [ ] Configure log sinks for long-term storage
- [ ] Set up alerts for sensitive operations
- [ ] Regular access reviews
- [ ] Monitor for anomalous behavior

---

## Networking Security Checklist

### VPC

- [ ] Delete default VPC
- [ ] Use custom VPCs with explicit subnets
- [ ] Enable Private Google Access
- [ ] Configure VPC Flow Logs
- [ ] Plan for Shared VPC (if multi-project)

### Firewall

- [ ] Default deny all ingress
- [ ] Use network tags for targeted rules
- [ ] Document all firewall rules
- [ ] Review rules quarterly
- [ ] Use hierarchical firewall policies (org-level)

### Private Connectivity

- [ ] Use Private Service Connect for Google APIs
- [ ] Configure VPC Service Controls for sensitive data
- [ ] Use Cloud NAT for outbound (not public IPs)
- [ ] Configure private endpoints for Cloud SQL, etc.

### Load Balancing

- [ ] Enable HTTPS (managed certificates)
- [ ] Configure Cloud Armor policies
- [ ] Enable logging
- [ ] Set up health checks
- [ ] Configure appropriate timeouts

---

## Cost Optimization Checklist

### Compute

- [ ] Right-size VM instances
- [ ] Use Spot VMs for fault-tolerant workloads
- [ ] Schedule development resources (stop nights/weekends)
- [ ] Review and implement Recommender suggestions
- [ ] Consider Committed Use Discounts

### GKE

- [ ] Enable cluster autoscaler
- [ ] Use Autopilot mode where possible
- [ ] Configure HPA and VPA
- [ ] Use Spot nodes for batch workloads
- [ ] Review namespace-level costs

### Cloud Run

- [ ] Set min instances = 0 for non-critical services
- [ ] Right-size memory allocation
- [ ] Optimize container startup time
- [ ] Consider CUDs for steady-state usage

### Storage

- [ ] Implement lifecycle policies
- [ ] Use appropriate storage classes
- [ ] Delete unused snapshots
- [ ] Archive cold data
- [ ] Enable autoclass for variable access patterns

### Monitoring

- [ ] Set up budget alerts
- [ ] Enable billing export to BigQuery
- [ ] Review Recommender weekly
- [ ] Track cost by label/namespace
- [ ] Implement FinOps practices

---

## Disaster Recovery Checklist

### Data

- [ ] Configure automated backups
- [ ] Test restore procedures
- [ ] Store backups in different region
- [ ] Document RPO/RTO requirements
- [ ] Encrypt backups

### Infrastructure

- [ ] Document IaC (Terraform/Pulumi)
- [ ] Test infrastructure recreation
- [ ] Configure cross-region replicas (if needed)
- [ ] Document manual procedures
- [ ] Maintain runbooks

### Application

- [ ] Test failover procedures
- [ ] Document dependencies
- [ ] Configure health checks
- [ ] Test recovery time
- [ ] Regular DR drills

---

## Pre-Production Checklist

### Security

- [ ] Complete IAM security checklist
- [ ] Complete networking security checklist
- [ ] Run Security Command Center scan
- [ ] Review vulnerability reports
- [ ] Penetration testing (if required)

### Performance

- [ ] Load testing completed
- [ ] Auto-scaling tested
- [ ] Cold start latency acceptable
- [ ] Database performance validated
- [ ] CDN configured and tested

### Operations

- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Runbooks documented
- [ ] On-call procedures defined
- [ ] Incident response plan ready

### Compliance

- [ ] Data residency requirements met
- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Audit logging enabled
- [ ] Compliance documentation ready

---

*GCP Checklists v2.0 | Updated: 2026-01*
