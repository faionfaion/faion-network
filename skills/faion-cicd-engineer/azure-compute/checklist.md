# Azure Compute Checklists

Pre-deployment and operational checklists for Azure compute services.

---

## Virtual Machines (VMs)

### Pre-Deployment Checklist

- [ ] **Sizing**
  - [ ] Analyzed workload requirements (CPU, memory, storage, network)
  - [ ] Selected appropriate VM series (B/D/E/F/N/L)
  - [ ] Considered burstable (B-series) for variable workloads
  - [ ] Reviewed Azure Advisor sizing recommendations

- [ ] **Availability**
  - [ ] Configured Availability Zones for production (99.99% SLA)
  - [ ] Or configured Availability Set (99.95% SLA)
  - [ ] Defined fault domain and update domain strategy

- [ ] **Networking**
  - [ ] Created VNet with proper address space
  - [ ] Configured NSG rules (deny all inbound by default)
  - [ ] Planned for public IP (if needed) or Bastion
  - [ ] Configured DNS settings

- [ ] **Storage**
  - [ ] Selected disk type (Premium SSD for production)
  - [ ] Configured disk encryption (platform or customer-managed keys)
  - [ ] Planned data disk layout
  - [ ] Configured disk caching appropriately

- [ ] **Security**
  - [ ] Enabled Azure Defender for VMs
  - [ ] Configured Managed Identity (avoid credentials)
  - [ ] Set up Just-in-Time VM access
  - [ ] Disabled password auth (use SSH keys)
  - [ ] Configured Azure AD authentication (if applicable)

- [ ] **Operations**
  - [ ] Configured Azure Update Manager
  - [ ] Set up Azure Backup with retention policy
  - [ ] Enabled boot diagnostics
  - [ ] Configured monitoring and alerts
  - [ ] Added proper tags for cost allocation

### Post-Deployment Checklist

- [ ] Verified VM is running and healthy
- [ ] Tested connectivity (SSH/RDP)
- [ ] Verified backup job runs successfully
- [ ] Confirmed monitoring data in Log Analytics
- [ ] Validated application deployment
- [ ] Documented VM configuration

---

## Virtual Machine Scale Sets (VMSS)

### Pre-Deployment Checklist

- [ ] **Orchestration Mode**
  - [ ] Using Flexible orchestration mode (recommended)
  - [ ] Documented reason if using Uniform mode

- [ ] **Scaling Configuration**
  - [ ] Configured autoscale rules (CPU, memory, custom metrics)
  - [ ] Set appropriate min/max instance counts
  - [ ] Configured scale-in policy
  - [ ] Set cooldown periods to prevent thrashing

- [ ] **Spot Configuration** (if using)
  - [ ] Configured Spot Priority Mix ratios
  - [ ] Set eviction policy (Deallocate or Delete)
  - [ ] Set max price (-1 for on-demand cap)
  - [ ] Enabled Spot restore (if needed)
  - [ ] Application handles graceful termination

- [ ] **Health & Upgrades**
  - [ ] Configured Application Health Extension
  - [ ] Set up rolling upgrade policy
  - [ ] Configured health probe endpoint
  - [ ] Set max unhealthy percentage threshold

- [ ] **Networking**
  - [ ] Configured load balancer or Application Gateway
  - [ ] Set up backend pools
  - [ ] Configured health probes
  - [ ] Enabled zone redundancy

- [ ] **Availability**
  - [ ] Enabled zone spreading (platformFaultDomainCount)
  - [ ] Configured max spreading for fault domains
  - [ ] Tested failover scenarios

### Operational Checklist

- [ ] Monitored scale events in Activity Log
- [ ] Validated autoscale triggers work correctly
- [ ] Tested Spot eviction handling
- [ ] Verified rolling upgrade behavior
- [ ] Confirmed health probes detect failures
- [ ] Set up alerts for scaling events

---

## Azure Kubernetes Service (AKS)

### Pre-Deployment Checklist

- [ ] **Cluster Configuration**
  - [ ] Selected Kubernetes version (latest stable)
  - [ ] Configured automatic patch upgrades
  - [ ] Set maintenance window for off-peak hours
  - [ ] Enabled Azure RBAC for Kubernetes

- [ ] **Identity & Security**
  - [ ] Configured User Assigned Managed Identity
  - [ ] Enabled Workload Identity (not Pod Identity)
  - [ ] Enabled OIDC issuer
  - [ ] Configured Azure AD integration
  - [ ] Enabled Azure Policy add-on
  - [ ] Enabled Microsoft Defender for Containers

- [ ] **Networking**
  - [ ] Selected CNI (Azure CNI Overlay for scale)
  - [ ] Configured network policy (Calico/Azure)
  - [ ] Set up authorized IP ranges for API server
  - [ ] Configured private cluster (if required)
  - [ ] Planned ingress strategy (AGIC, nginx, etc.)

- [ ] **Node Pools**
  - [ ] Created system node pool (small VMs, 2-3 nodes)
  - [ ] Configured system pool taints
  - [ ] Created user node pool(s) with autoscaling
  - [ ] Configured zone redundancy (zones 1,2,3)
  - [ ] Set max surge for upgrades (33% recommended)

- [ ] **Spot Node Pool** (if using)
  - [ ] Configured priority as Spot
  - [ ] Set eviction policy
  - [ ] Added tolerations to workloads
  - [ ] Set min_count to 0 for cost savings
  - [ ] Application handles preemption gracefully

- [ ] **Monitoring & Logging**
  - [ ] Enabled Container Insights
  - [ ] Connected to Log Analytics workspace
  - [ ] Enabled Prometheus metrics (Monitor Metrics)
  - [ ] Configured diagnostic settings

- [ ] **Add-ons**
  - [ ] Enabled Key Vault secrets provider
  - [ ] Enabled secret rotation
  - [ ] Enabled KEDA (if event-driven scaling needed)
  - [ ] Enabled Workload Identity BEFORE KEDA

### Post-Deployment Checklist

- [ ] Verified cluster health with `kubectl get nodes`
- [ ] Tested Workload Identity authentication
- [ ] Deployed sample workload successfully
- [ ] Verified HPA scales pods correctly
- [ ] Verified cluster autoscaler scales nodes
- [ ] Tested KEDA scaling (if enabled)
- [ ] Validated network policies work
- [ ] Confirmed logs appear in Log Analytics
- [ ] Set up Grafana dashboards

---

## Azure Container Apps (ACA)

### Pre-Deployment Checklist

- [ ] **Environment Setup**
  - [ ] Created Container Apps environment
  - [ ] Connected to Log Analytics workspace
  - [ ] Configured VNet integration (if needed)
  - [ ] Set up workload profiles (if dedicated plan)

- [ ] **Application Configuration**
  - [ ] Configured container image and registry
  - [ ] Set resource limits (CPU, memory)
  - [ ] Configured environment variables
  - [ ] Set up secrets (Key Vault references)
  - [ ] Configured min/max replicas

- [ ] **Scaling**
  - [ ] Configured HTTP scaling rules
  - [ ] Set up KEDA scale rules (if event-driven)
  - [ ] Tested scale-to-zero behavior
  - [ ] Set min replicas > 0 for latency-sensitive apps

- [ ] **Networking & Ingress**
  - [ ] Configured ingress (external/internal)
  - [ ] Set up custom domain (if needed)
  - [ ] Configured TLS certificates
  - [ ] Set up traffic splitting (if needed)

- [ ] **Dapr** (if using)
  - [ ] Enabled Dapr sidecar
  - [ ] Configured Dapr components (state, pubsub)
  - [ ] Set up component scopes
  - [ ] Configured resiliency policies

- [ ] **Revisions**
  - [ ] Configured revision mode (single/multiple)
  - [ ] Set up revision labels for traffic splitting
  - [ ] Planned blue-green deployment strategy

### Operational Checklist

- [ ] Verified application is running
- [ ] Tested ingress endpoint
- [ ] Validated scaling behavior
- [ ] Confirmed Dapr communication (if enabled)
- [ ] Tested traffic splitting between revisions
- [ ] Monitored logs and metrics
- [ ] Set up alerts for failures and scaling

---

## Azure App Service

### Pre-Deployment Checklist

- [ ] **Plan Selection**
  - [ ] Selected appropriate tier (Standard+ for production)
  - [ ] Sized instance based on workload
  - [ ] Considered Premium for high traffic
  - [ ] Planned for Reserved Instances (cost savings)

- [ ] **Deployment Slots**
  - [ ] Created staging slot
  - [ ] Configured slot settings (connection strings, app settings)
  - [ ] Marked environment-specific settings as "slot setting"
  - [ ] Set up auto-swap (if CD pipeline)

- [ ] **Scaling**
  - [ ] Configured autoscale rules
  - [ ] Set min/max instance counts
  - [ ] Configured scale-in cooldown
  - [ ] Tested scaling behavior

- [ ] **Networking**
  - [ ] Configured VNet integration (if needed)
  - [ ] Set up private endpoints (if needed)
  - [ ] Configured access restrictions (IP whitelist)
  - [ ] Set up custom domain

- [ ] **Security**
  - [ ] Configured Managed Identity
  - [ ] Enabled HTTPS only
  - [ ] Set minimum TLS version (1.2+)
  - [ ] Configured authentication (if needed)
  - [ ] Enabled Azure Defender

- [ ] **Application Settings**
  - [ ] Configured all app settings
  - [ ] Set up connection strings
  - [ ] Configured Key Vault references for secrets
  - [ ] Set runtime version

### Deployment Checklist

- [ ] Deploy to staging slot first
- [ ] Run smoke tests on staging
- [ ] Verify application health
- [ ] Check logs for errors
- [ ] Swap staging to production
- [ ] Monitor production after swap
- [ ] Roll back if issues detected

### Post-Deployment Checklist

- [ ] Verified application is healthy
- [ ] Tested all endpoints
- [ ] Confirmed diagnostics logging works
- [ ] Validated backup configuration
- [ ] Set up availability alerts
- [ ] Documented deployment process

---

## Cross-Service Security Checklist

- [ ] **Identity**
  - [ ] Using Managed Identity (no credentials in code)
  - [ ] Configured least-privilege RBAC
  - [ ] Set up conditional access (if using Azure AD)

- [ ] **Network**
  - [ ] Private endpoints for PaaS services
  - [ ] NSG rules are restrictive
  - [ ] No public IPs unless required
  - [ ] DDoS protection enabled (if public)

- [ ] **Data Protection**
  - [ ] Encryption at rest (Azure managed or CMK)
  - [ ] Encryption in transit (TLS 1.2+)
  - [ ] Secrets in Key Vault

- [ ] **Compliance**
  - [ ] Azure Policy assignments active
  - [ ] Defender for Cloud enabled
  - [ ] Audit logging enabled
  - [ ] Compliance reports generated

---

## Cost Optimization Checklist

- [ ] **Right-Sizing**
  - [ ] Reviewed Azure Advisor recommendations
  - [ ] Identified oversized resources
  - [ ] Configured autoscaling to scale down

- [ ] **Commitments**
  - [ ] Evaluated Reserved Instances for stable workloads
  - [ ] Considered Savings Plans for flexibility
  - [ ] Purchased reservations for predictable usage

- [ ] **Spot/Preemptible**
  - [ ] Identified interruptible workloads
  - [ ] Configured Spot VMs/node pools
  - [ ] Tested graceful termination handling

- [ ] **Dev/Test**
  - [ ] Using Dev/Test pricing for non-production
  - [ ] Scale down/stop non-prod during off-hours
  - [ ] Using lower tiers for development

- [ ] **Monitoring**
  - [ ] Set up cost alerts
  - [ ] Configured budgets
  - [ ] Regular cost reviews scheduled
  - [ ] Tags applied for cost allocation
