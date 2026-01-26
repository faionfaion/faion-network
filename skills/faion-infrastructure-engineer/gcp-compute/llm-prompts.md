# GCP Compute Engine LLM Prompts

Prompts for LLM-assisted infrastructure tasks related to VMs, instance groups, autoscaling, and Spot VMs.

## VM Creation Prompts

### Create VM Prompt

```
Create a GCP Compute Engine VM with the following requirements:

Requirements:
- Name: {name}
- Zone: {zone}
- Machine type: {machine_type}
- OS: {os_family} (e.g., Ubuntu 24.04 LTS)
- Disk size: {disk_size}GB
- Disk type: {disk_type} (pd-standard, pd-balanced, pd-ssd)
- Network tags: {tags}
- Service account: {service_account_email}
- Startup script: {startup_script_path or "none"}

Provide:
1. gcloud CLI command
2. Terraform resource definition
3. Explanation of configuration choices
```

### Create Spot VM Prompt

```
Create a GCP Spot VM for cost-optimized workloads:

Requirements:
- Name: {name}
- Zone: {zone}
- Machine type: {machine_type}
- Termination action: {STOP or DELETE}
- Workload type: {batch, dev/test, fault-tolerant processing}

Provide:
1. gcloud CLI command with --provisioning-model=SPOT
2. Terraform resource with scheduling block
3. Shutdown script template (30-second limit)
4. Cost savings estimate compared to standard VM
5. Best practices for handling preemption
```

### VM Sizing Prompt

```
Recommend GCP machine type for the following workload:

Workload characteristics:
- Type: {web app, API server, batch processing, ML training, database}
- Expected CPU utilization: {low, medium, high}
- Memory requirements: {approximate GB}
- IOPS requirements: {low, medium, high}
- Network throughput: {low, medium, high}
- Cost sensitivity: {low, medium, high}
- Availability requirement: {99%, 99.9%, 99.99%}

Consider:
1. E2 vs N2 vs C2 vs M2 machine families
2. Custom vs predefined machine types
3. Spot VM eligibility
4. Committed use discount eligibility
5. Total cost of ownership
```

---

## Instance Group Prompts

### Create MIG Prompt

```
Create a Managed Instance Group (MIG) for production:

Requirements:
- Name: {mig_name}
- Region: {region}
- Instance template: {template_name}
- Target size: {size}
- Health check: {health_check_type} on port {port}
- Named ports: {port_name}:{port_number}

Provide:
1. gcloud CLI commands for:
   - Instance template creation
   - Regional MIG creation
   - Health check configuration
   - Autohealing setup
2. Terraform resources
3. Rolling update configuration
4. Best practices for the deployment type
```

### MIG Migration Prompt

```
Migrate from zonal MIG to regional MIG:

Current setup:
- MIG name: {mig_name}
- Zone: {zone}
- Instance template: {template}
- Current size: {size}

Target:
- Region: {region}
- Zones: {zone1}, {zone2}, {zone3}
- Minimum instances per zone: {min_per_zone}

Provide:
1. Step-by-step migration plan
2. gcloud CLI commands
3. Terraform configuration changes
4. Zero-downtime migration strategy
5. Rollback plan
```

### Instance Template Update Prompt

```
Create a new instance template version for rolling update:

Current template: {current_template_name}

Changes:
- {change_1: e.g., "Update machine type from e2-medium to e2-standard-2"}
- {change_2: e.g., "Add new startup script"}
- {change_3: e.g., "Update image to latest version"}

Provide:
1. New instance template gcloud command
2. Rolling update command with:
   - maxUnavailable: {value}
   - maxSurge: {value}
3. Canary deployment option (10% then full)
4. Rollback command
5. Monitoring recommendations during update
```

---

## Autoscaling Prompts

### Configure Autoscaling Prompt

```
Configure autoscaling for a Managed Instance Group:

MIG details:
- Name: {mig_name}
- Region/Zone: {location}
- Current size: {size}

Scaling requirements:
- Minimum instances: {min}
- Maximum instances: {max}
- Target CPU utilization: {cpu_target}% (e.g., 60%)
- Cooldown period: {seconds}s

Additional signals (optional):
- Load balancer utilization target: {lb_target}
- Custom metric: {metric_name} with target {target_value}

Provide:
1. gcloud CLI command
2. Terraform google_compute_region_autoscaler resource
3. Scale-in control recommendations
4. Predictive autoscaling recommendation
5. Cost implications of configuration
```

### Predictive Autoscaling Prompt

```
Enable predictive autoscaling for a workload:

Workload characteristics:
- Traffic pattern: {predictable daily, weekly cycles, unpredictable}
- Initialization time: {seconds} seconds
- Historical data available: {weeks} weeks

Current autoscaling:
- MIG: {mig_name}
- Current scaling signal: CPU at {target}%

Provide:
1. Recommendation: OPTIMIZE_AVAILABILITY vs FORECAST_ONLY
2. gcloud command to enable predictive autoscaling
3. Terraform configuration
4. Prerequisites checklist
5. How to monitor prediction accuracy
```

### Schedule-Based Autoscaling Prompt

```
Configure schedule-based autoscaling:

Traffic patterns:
- Business hours peak: {weekdays} {start_time} to {end_time} {timezone}
- Expected peak traffic multiplier: {multiplier}x normal
- Special events: {event_schedule}

Current configuration:
- MIG: {mig_name}
- Normal min replicas: {min}
- Normal max replicas: {max}

Provide:
1. gcloud commands for scaling schedules
2. Terraform configuration with scaling_schedules
3. Cron expressions for each schedule
4. Overlap handling strategy
5. Cost projection with schedules
```

### Troubleshoot Autoscaling Prompt

```
Troubleshoot autoscaling issues:

Symptoms:
- {symptom: e.g., "Autoscaler not scaling up during traffic spikes"}
- {symptom: e.g., "Scaling too aggressively, causing flapping"}
- {symptom: e.g., "VMs added but not receiving traffic"}

Current configuration:
- MIG: {mig_name}
- Autoscaling signal: {signal}
- Min/Max: {min}/{max}
- Cooldown: {cooldown}s
- Initialization period: {init_period}s

Provide:
1. Diagnostic gcloud commands
2. Key metrics to check in Cloud Monitoring
3. Common issues and solutions
4. Configuration adjustments to try
5. Scale-in control recommendations
```

---

## Spot VM Prompts

### Spot VM Strategy Prompt

```
Design Spot VM strategy for cost optimization:

Workload details:
- Type: {batch, web app, data processing, ML training}
- Fault tolerance: {high, medium, low}
- Data persistence: {stateless, checkpointing, external storage}
- SLA requirement: {uptime percentage}

Current infrastructure:
- Standard VMs: {count} x {machine_type}
- Monthly cost: ${cost}

Provide:
1. Recommended Spot vs Standard VM mix
2. MIG configuration for automatic recreation
3. Shutdown script template for state saving
4. Fallback strategy for preemption
5. Estimated cost savings
6. Monitoring and alerting setup
```

### GKE Spot Node Pool Prompt

```
Configure GKE cluster with Spot node pools:

Cluster details:
- Cluster name: {cluster_name}
- Region: {region}
- Current node pools: {node_pool_details}

Requirements:
- Standard nodes for: {critical workloads}
- Spot nodes for: {batch, dev, non-critical workloads}
- Cost reduction target: {percentage}%

Provide:
1. gcloud commands to:
   - Create Spot node pool
   - Add taints to Spot nodes
2. Kubernetes manifests for:
   - Toleration for Spot nodes
   - Node affinity rules
   - PodDisruptionBudget
3. Workload placement strategy
4. Cost monitoring setup
```

### Spot VM Shutdown Script Prompt

```
Create a shutdown script for Spot VM preemption handling:

Application details:
- Application type: {type}
- State location: {file paths}
- State size: {approximate size}
- GCS bucket for checkpoints: {bucket_name}
- Maximum acceptable data loss: {seconds} seconds

Requirements:
- Must complete within 30 seconds
- Save application state
- Gracefully stop services
- Log shutdown events

Provide:
1. Complete shutdown script
2. GCS checkpoint naming strategy
3. Restart/resume script
4. Testing procedure for shutdown script
5. Monitoring for preemption events
```

---

## Cost Optimization Prompts

### Cost Analysis Prompt

```
Analyze and optimize GCP Compute costs:

Current infrastructure:
- VMs: {list of VMs with types and usage}
- MIGs: {list with sizes}
- Monthly spend: ${amount}

Usage patterns:
- Peak hours: {hours}
- Off-peak utilization: {percentage}%
- Batch processing: {schedule}

Provide:
1. Right-sizing recommendations
2. Spot VM candidates
3. Committed use discount analysis
4. Schedule-based scaling opportunities
5. Estimated savings per optimization
6. Implementation priority order
```

### Committed Use Discount Prompt

```
Evaluate Committed Use Discounts (CUDs):

Current usage:
- Machine types in use: {list}
- Stable baseline: {vCPUs} vCPUs, {memory} GB memory
- Expected growth: {percentage}% over {months} months

Consider:
- 1-year vs 3-year commitment
- Resource-based vs spend-based CUD
- Flexibility requirements

Provide:
1. CUD recommendation (type and term)
2. Committed resources calculation
3. Expected discount percentage
4. Monthly/annual savings
5. Risk analysis
6. Mixing CUD with Spot VMs strategy
```

---

## Disaster Recovery Prompts

### DR Setup Prompt

```
Design disaster recovery for Compute Engine workloads:

Requirements:
- RTO: {hours} hours
- RPO: {hours} hours
- Primary region: {region}
- DR region: {dr_region}

Current infrastructure:
- VMs: {list}
- MIGs: {list}
- Data: {storage details}

Provide:
1. DR architecture design
2. Snapshot schedule configuration
3. Cross-region replication setup
4. Failover procedure
5. Failback procedure
6. Testing schedule and procedure
7. Cost of DR infrastructure
```

### Backup Strategy Prompt

```
Configure backup strategy for Compute Engine:

Resources:
- VMs: {list with disk sizes}
- Data criticality: {high, medium, low}
- Retention requirement: {days} days

Provide:
1. Snapshot schedule policy (gcloud and Terraform)
2. Machine image backup for full VM recovery
3. Cross-region snapshot copy
4. Backup verification procedure
5. Recovery procedure documentation
6. Cost estimate for backup storage
```

---

## Monitoring Prompts

### Monitoring Setup Prompt

```
Configure monitoring for Compute Engine infrastructure:

Resources to monitor:
- VMs: {list}
- MIGs: {list}
- Health checks: {list}

Key metrics to track:
- CPU utilization
- Memory usage
- Disk I/O
- Network throughput
- Autoscaler decisions
- Preemption events (for Spot VMs)

Provide:
1. Cloud Monitoring dashboard JSON
2. Alerting policies for critical metrics
3. Uptime checks for endpoints
4. Log-based metrics for errors
5. SLO configuration
6. Ops Agent installation commands
```

---

## Usage Guidelines

### When to Use Each Prompt

| Task | Prompt Category |
|------|-----------------|
| New VM deployment | VM Creation Prompts |
| Cost reduction | Spot VM / Cost Optimization Prompts |
| High availability setup | Instance Group Prompts |
| Traffic-based scaling | Autoscaling Prompts |
| Backup and recovery | DR Prompts |
| Performance issues | Monitoring Prompts |

### Prompt Customization Tips

1. Replace `{placeholders}` with actual values
2. Add project-specific constraints
3. Include existing infrastructure context
4. Specify compliance requirements
5. Mention budget constraints

---

*LLM Prompts v2.0 | GCP Compute Engine*
