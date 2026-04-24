# GCP Compute Engine Checklist

Production readiness checklist for VMs, instance groups, autoscaling, and Spot VMs.

## VM Creation Checklist

### Basic Configuration

- [ ] Machine type selected based on workload requirements
- [ ] Appropriate boot disk type chosen (pd-balanced, pd-ssd, pd-standard)
- [ ] Boot disk size adequate for OS + application
- [ ] Region/zone selected based on latency and compliance requirements
- [ ] Network tags applied for firewall rules
- [ ] Labels applied for cost allocation and organization

### Security

- [ ] Service account with minimal required permissions
- [ ] OS Login enabled (replaces SSH key management)
- [ ] Shielded VM enabled for production workloads
- [ ] Sole-tenant nodes for compliance (if required)
- [ ] Confidential VMs for sensitive data (if required)
- [ ] No external IP if not needed (use Cloud NAT)

### Startup/Shutdown

- [ ] Startup script tested and idempotent
- [ ] Shutdown script saves state (especially for Spot VMs)
- [ ] Scripts complete within timeout (30s for preemption)
- [ ] Metadata-based configuration (not hardcoded)

---

## Instance Template Checklist

### Template Design

- [ ] Uses instance templates (not manual VM creation)
- [ ] Template versioned with date or semantic version
- [ ] Image family used (not specific image) for auto-updates
- [ ] Custom image with pre-installed software (faster startup)
- [ ] Startup script included in template

### Reusability

- [ ] Machine type parameterized where needed
- [ ] Network/subnet configurable
- [ ] Labels include template version
- [ ] Description documents purpose and version

---

## Managed Instance Group (MIG) Checklist

### Basic Setup

- [ ] Regional MIG for production (not zonal)
- [ ] Minimum 3 instances for regional MIGs
- [ ] Target distribution shape: EVEN (default) or BALANCED
- [ ] Instance template attached

### Health Checks

- [ ] HTTP(S) health check configured
- [ ] Health check path returns 200 for healthy
- [ ] Check interval appropriate (10-30s typical)
- [ ] Unhealthy threshold set (3 consecutive failures typical)
- [ ] Autohealing enabled with health check

### Updates

- [ ] Update policy: PROACTIVE or OPPORTUNISTIC
- [ ] maxUnavailable set (1 or 10-20%)
- [ ] maxSurge set for faster updates
- [ ] Minimal action: REPLACE or RESTART
- [ ] Instance redistribution: PROACTIVE for regional

---

## Autoscaling Checklist

### Autoscaling Configuration

- [ ] Autoscaling enabled on MIG
- [ ] Min replicas set (never 0 for production)
- [ ] Max replicas set with cost considerations
- [ ] Cooldown period configured (60s default)
- [ ] Scale-in controls configured to prevent flapping

### Signals

- [ ] Primary signal selected (CPU, custom metric, LB capacity)
- [ ] CPU target utilization set (60-80% typical)
- [ ] Multiple signals configured for complex workloads
- [ ] Custom Cloud Monitoring metrics if needed

### Initialization Period

- [ ] Initialization period > VM startup time
- [ ] Accounts for application warmup
- [ ] Tested under load to verify timing

### Predictive Autoscaling (if applicable)

- [ ] Enabled for apps with >2 min initialization
- [ ] Traffic pattern is predictable and cyclical
- [ ] Historical data available (1-2 weeks minimum)
- [ ] Mode: FORECAST_AND_SCALE or FORECAST_ONLY

### Scale-in Controls

- [ ] Max scale-in rate configured
- [ ] Time window appropriate for workload
- [ ] Prevents rapid downscaling during traffic spikes

---

## Spot VM Checklist

### Spot VM Configuration

- [ ] Provisioning model: SPOT (not STANDARD)
- [ ] Termination action: STOP or DELETE
- [ ] Shutdown script saves state within 30 seconds
- [ ] Workload is fault-tolerant and resumable

### High Availability

- [ ] Uses MIG for automatic recreation
- [ ] Regional MIG for zone distribution
- [ ] Mixed Spot + standard VMs for critical workloads
- [ ] Autohealing enabled

### GKE Spot Node Pools

- [ ] Node pool with --spot flag
- [ ] Mixed node pools (Spot + standard)
- [ ] Node taints applied to Spot nodes
- [ ] Tolerations on Pods that can run on Spot
- [ ] PodDisruptionBudgets configured

### Cost Optimization

- [ ] Spot VMs used for batch processing
- [ ] Spot VMs used for dev/test environments
- [ ] Committed use discounts for baseline
- [ ] Spot for burst capacity

---

## Disk Checklist

### Boot Disk

- [ ] Appropriate disk type for IOPS requirements
- [ ] Size adequate for OS + logs + temp files
- [ ] Snapshot schedule configured

### Additional Disks

- [ ] Regional persistent disks for HA (if needed)
- [ ] Local SSDs for ephemeral high-IOPS (data loss on preemption)
- [ ] Hyperdisk for extreme performance requirements
- [ ] Disk encryption (default or CMEK)

---

## Networking Checklist

- [ ] VPC and subnet selected
- [ ] Internal IP sufficient (no external IP if possible)
- [ ] Cloud NAT for outbound internet access
- [ ] Firewall rules via network tags
- [ ] Private Google Access enabled on subnet
- [ ] Load balancer configured (if applicable)

---

## Monitoring & Logging

- [ ] Ops Agent installed (Cloud Logging + Monitoring)
- [ ] Custom metrics exported (if needed)
- [ ] Alerting policies configured
- [ ] Uptime checks for external endpoints
- [ ] Log-based metrics for error tracking

---

## Cost Optimization Checklist

- [ ] Right-sized machine types (not over-provisioned)
- [ ] Spot VMs for fault-tolerant workloads
- [ ] Committed use discounts for stable workloads
- [ ] Sustained use discounts (automatic)
- [ ] Preemptible/Spot for batch jobs
- [ ] Instance scheduler for dev/test (stop nights/weekends)
- [ ] Idle VM recommendations reviewed

---

## Disaster Recovery

- [ ] Snapshots scheduled for critical disks
- [ ] Machine images for full VM backup
- [ ] Cross-region snapshots for DR
- [ ] Recovery procedures documented and tested
- [ ] RTO/RPO requirements met

---

*Checklist v2.0 | GCP Compute Engine*
