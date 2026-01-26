# Azure Compute LLM Prompts

Prompts for AI assistance with Azure compute infrastructure.

---

## Service Selection

### Prompt: Choose Compute Service

```
I need to deploy an application on Azure. Help me choose the right compute service.

**Application Details:**
- Type: [web app / API / background worker / batch job / microservices]
- Language/Framework: [e.g., .NET, Node.js, Python, Go]
- Container: [yes / no]
- Traffic pattern: [steady / variable / event-driven / scheduled]
- Scale requirements: [min instances, max instances]
- State: [stateless / stateful]
- Special requirements: [GPU, Windows, custom OS, compliance, etc.]

**Constraints:**
- Team expertise: [VMs / Kubernetes / Serverless]
- Budget: [development / production, cost-sensitive / performance-first]
- Management overhead tolerance: [minimal / some / full control needed]

Based on these requirements, recommend the best Azure compute service and explain why.
```

### Prompt: Migration Assessment

```
I need to migrate an application to Azure. Assess the compute options.

**Current State:**
- Running on: [on-premises VMs / AWS EC2 / Heroku / etc.]
- Application type: [monolith / microservices]
- OS: [Linux / Windows]
- Dependencies: [database, cache, message queue, etc.]
- Current scale: [instances, CPU, memory]

**Migration Goals:**
- Priority: [minimize changes / modernize / cost optimization]
- Timeline: [urgent / planned]
- Downtime tolerance: [zero / minimal / scheduled window]

Recommend a migration path with Azure compute services.
```

---

## Virtual Machines

### Prompt: VM Sizing

```
Help me size an Azure VM for the following workload:

**Workload:**
- Type: [web server / database / application server / batch processing]
- CPU requirements: [cores needed, utilization pattern]
- Memory requirements: [GB needed]
- Storage: [type: OS + data, IOPS requirements]
- Network: [bandwidth requirements]

**Constraints:**
- Budget: [monthly budget or cost-sensitive flag]
- Availability: [development / production, SLA requirements]
- Region: [Azure region]

Recommend:
1. VM series and size
2. Disk configuration
3. Availability options (zones, sets)
4. Cost estimate
```

### Prompt: VM Security Hardening

```
Generate a security hardening checklist for Azure Linux VMs.

**Requirements:**
- OS: [Ubuntu 22.04 / RHEL 9 / etc.]
- Exposure: [internet-facing / internal only]
- Compliance: [none / PCI-DSS / HIPAA / SOC2]
- Access method: [Bastion / VPN / public SSH]

Include:
1. NSG rules
2. OS-level hardening
3. Monitoring and logging
4. Backup and recovery
5. Update management
```

---

## Virtual Machine Scale Sets

### Prompt: VMSS Design

```
Design a VMSS configuration for the following scenario:

**Workload:**
- Type: [stateless web tier / batch processing / etc.]
- Instance requirements: [min, typical, max]
- Scale triggers: [CPU %, memory %, custom metric, schedule]
- Spot tolerance: [yes / no, percentage acceptable]

**Requirements:**
- Orchestration: [Flexible / Uniform]
- Health monitoring: [HTTP endpoint, TCP port]
- Update strategy: [rolling / manual]
- Zone redundancy: [required / optional]

Generate:
1. VMSS configuration
2. Autoscale rules
3. Health probe settings
4. Spot Priority Mix (if applicable)
```

### Prompt: Spot Instance Strategy

```
Design a Spot VM strategy for cost optimization.

**Workload:**
- Type: [batch processing / CI/CD agents / dev/test / fault-tolerant service]
- Interruption tolerance: [high / medium / graceful shutdown needed]
- Minimum guaranteed capacity: [number of instances]

**Questions:**
- What percentage of workload can run on Spot?
- How to handle evictions gracefully?
- What's the expected cost savings?

Generate:
1. Spot Priority Mix configuration
2. Eviction handling strategy
3. Application-level considerations
4. Cost comparison
```

---

## AKS

### Prompt: AKS Cluster Design

```
Design an AKS cluster for production workloads.

**Workloads:**
- Number of applications: [count]
- Types: [web APIs, background workers, scheduled jobs]
- Total pods expected: [min, typical, max]
- Resource requirements: [typical pod CPU/memory]

**Requirements:**
- Multi-tenancy: [single team / multiple teams / multiple customers]
- Networking: [CNI type, network policy needed]
- Identity: [Workload Identity, Pod Identity (legacy)]
- Compliance: [none / specific requirements]
- GitOps: [yes / no]

Generate:
1. Cluster configuration
2. Node pool strategy (system, user, spot, GPU)
3. Networking design
4. Security configuration
5. Monitoring setup
```

### Prompt: AKS Node Pool Strategy

```
Design node pools for an AKS cluster.

**Workloads:**
| Workload | CPU | Memory | GPU | Spot OK | Count |
|----------|-----|--------|-----|---------|-------|
| [name]   | [x] | [xGi]  | [y/n] | [y/n] | [n]  |

**Requirements:**
- Availability zones: [yes / no]
- Autoscaling: [yes / no, ranges]
- Cost optimization priority: [high / medium / low]

Generate:
1. System node pool configuration
2. User node pool(s) configuration
3. Spot node pool configuration (if applicable)
4. Taints and tolerations strategy
5. Pod affinity/anti-affinity recommendations
```

### Prompt: KEDA Scaling

```
Design KEDA scaling for an AKS workload.

**Scenario:**
- Trigger source: [Azure Service Bus / Azure Queue / HTTP / Prometheus / etc.]
- Current processing rate: [messages/second or requests/second]
- Processing time per item: [seconds]
- Acceptable latency: [seconds]

**Requirements:**
- Scale to zero: [yes / no]
- Max replicas: [number]
- Authentication: [Workload Identity / Connection String]

Generate:
1. KEDA ScaledObject YAML
2. TriggerAuthentication (if using Workload Identity)
3. Deployment adjustments
4. Scaling calculation explanation
```

### Prompt: AKS Cost Optimization

```
Review AKS cluster for cost optimization.

**Current Configuration:**
- Node pools: [describe each: VM size, count, autoscaling]
- Workloads: [number, resource requests/limits]
- Utilization: [CPU %, memory %]
- Current monthly cost: [amount]

**Goals:**
- Target savings: [percentage or amount]
- Acceptable trade-offs: [performance / availability]

Analyze and recommend:
1. Node pool right-sizing
2. Spot instance opportunities
3. Reserved Instance recommendations
4. Resource request optimization
5. Cluster autoscaler tuning
```

---

## Container Apps

### Prompt: Container Apps Design

```
Design an Azure Container Apps deployment.

**Application:**
- Type: [API / background worker / event processor]
- Container image: [registry/image:tag]
- Ports: [exposed ports]
- Environment variables: [list]
- Secrets needed: [list]

**Scaling:**
- Min replicas: [number, 0 for scale-to-zero]
- Max replicas: [number]
- Scale trigger: [HTTP requests / Queue depth / Custom]

**Integration:**
- Dapr needed: [yes / no]
- Dapr building blocks: [state, pubsub, bindings, etc.]
- Other services: [databases, queues, etc.]

Generate:
1. Container App configuration (Terraform/Bicep)
2. Dapr components (if applicable)
3. KEDA scale rules
4. Ingress configuration
```

### Prompt: Container Apps vs AKS

```
Compare Container Apps vs AKS for my scenario.

**Application:**
- Complexity: [single container / few microservices / many microservices]
- Team size: [small / medium / large]
- Kubernetes experience: [none / some / expert]
- Custom requirements: [list any: service mesh, custom CNI, etc.]

**Workload Characteristics:**
- Traffic pattern: [steady / variable / event-driven]
- Scale-to-zero important: [yes / no]
- Windows containers needed: [yes / no]
- GPU needed: [yes / no]

Generate:
1. Detailed comparison table
2. Recommendation with reasoning
3. Migration path (if switching)
4. Cost comparison estimate
```

### Prompt: Dapr Integration

```
Design Dapr integration for Azure Container Apps.

**Microservices:**
| Service | Needs State | Pub/Sub | Service Calls | Bindings |
|---------|-------------|---------|---------------|----------|
| [name]  | [y/n]       | [y/n]   | [y/n]         | [list]   |

**Azure Services:**
- State store: [Cosmos DB / Redis / Blob]
- Pub/Sub: [Service Bus / Event Hubs]
- Bindings: [list input/output bindings]

Generate:
1. Dapr component configurations
2. Application code examples (showing Dapr SDK usage)
3. Resiliency configuration
4. Observability setup
```

---

## App Service

### Prompt: App Service Plan Sizing

```
Recommend an App Service Plan for my application.

**Application:**
- Type: [web app / API / function app]
- Framework: [.NET / Node.js / Python / etc.]
- Traffic: [requests/day, peak RPS]
- CPU/Memory requirements: [estimates]

**Features Needed:**
- Deployment slots: [number needed]
- Custom domains: [number]
- VNet integration: [yes / no]
- Always On: [yes / no]
- Autoscaling: [yes / no]

**Environment:**
- [development / staging / production]
- Budget: [monthly limit if applicable]

Recommend:
1. Tier and SKU
2. Scaling configuration
3. Cost estimate
4. Upgrade path
```

### Prompt: Deployment Slot Strategy

```
Design a deployment slot strategy for App Service.

**Deployment Requirements:**
- Frequency: [daily / weekly / on-demand]
- Zero-downtime required: [yes / no]
- Testing stages: [list: staging, QA, UAT, etc.]
- Rollback needs: [quick rollback / can redeploy]

**Configuration:**
- Slot-specific settings: [list settings that differ per slot]
- Shared settings: [list settings shared across slots]

Generate:
1. Slot configuration
2. Deployment pipeline flow
3. Swap settings
4. Traffic routing strategy (if gradual rollout needed)
5. Rollback procedure
```

---

## Cross-Service

### Prompt: Multi-Service Architecture

```
Design a multi-service architecture on Azure.

**Services:**
| Service | Type | Scale | Notes |
|---------|------|-------|-------|
| [name]  | [API/worker/etc.] | [min-max] | [requirements] |

**Communication:**
- Synchronous: [HTTP / gRPC]
- Asynchronous: [queues / events]
- Service discovery: [DNS / service mesh / Dapr]

**Shared Resources:**
- Database: [type]
- Cache: [type]
- Storage: [type]
- Secrets: [Key Vault]

Generate:
1. Architecture diagram description
2. Compute service recommendation per component
3. Networking design
4. Security design
5. Deployment strategy
```

### Prompt: Cost Optimization Review

```
Review my Azure compute costs for optimization opportunities.

**Current Setup:**
| Service | SKU/Size | Count | Monthly Cost |
|---------|----------|-------|--------------|
| [type]  | [sku]    | [n]   | [$xxx]       |

**Utilization:**
- Average CPU: [%]
- Average Memory: [%]
- Traffic patterns: [describe]

**Constraints:**
- Cannot change: [list any fixed requirements]
- Downtime windows: [available / not available]

Analyze and provide:
1. Right-sizing recommendations
2. Reserved capacity opportunities
3. Spot instance opportunities
4. Architecture optimizations
5. Estimated savings
```

### Prompt: Disaster Recovery Design

```
Design disaster recovery for Azure compute workloads.

**Requirements:**
- RPO: [recovery point objective, e.g., 1 hour]
- RTO: [recovery time objective, e.g., 4 hours]
- Regions: [primary, secondary]
- Budget for DR: [percentage of production cost]

**Workloads:**
| Component | Compute Service | Data | Criticality |
|-----------|-----------------|------|-------------|
| [name]    | [type]          | [DB/storage] | [high/medium/low] |

Generate:
1. DR architecture
2. Replication strategy
3. Failover procedure
4. Failback procedure
5. Testing plan
6. Cost estimate
```

---

## Troubleshooting

### Prompt: Performance Issues

```
Help troubleshoot performance issues on Azure compute.

**Environment:**
- Service: [VM / VMSS / AKS / Container Apps / App Service]
- Configuration: [describe]

**Symptoms:**
- Issue: [slow response / high latency / timeouts / etc.]
- When started: [date/time or event]
- Pattern: [constant / intermittent / time-based]
- Affected: [all requests / specific endpoints / specific users]

**Metrics:**
- CPU: [%]
- Memory: [%]
- Network: [Mbps]
- Disk: [IOPS, latency]

Provide:
1. Diagnostic steps
2. Common causes
3. Azure Monitor queries
4. Resolution recommendations
```

### Prompt: Scaling Issues

```
Help troubleshoot autoscaling issues.

**Environment:**
- Service: [VMSS / AKS / Container Apps / App Service]
- Current scaling config: [describe rules]

**Issue:**
- Scaling too slow / too fast / not scaling at all
- Current metric values: [describe]
- Expected behavior: [what should happen]
- Actual behavior: [what is happening]

Analyze and provide:
1. Diagnostic steps
2. Common misconfigurations
3. Recommended settings
4. Monitoring queries
```

---

## Implementation

### Prompt: Terraform Generation

```
Generate Terraform code for Azure compute infrastructure.

**Requirements:**
- Service: [VM / VMSS / AKS / Container Apps / App Service]
- Environment: [dev / staging / prod]
- [Include specific requirements from other prompts]

**Standards:**
- Use modules: [yes / no]
- State backend: [Azure Storage / Terraform Cloud]
- Provider version: [specify or latest]

Generate:
1. Complete Terraform configuration
2. Variables file
3. Outputs file
4. tfvars example
5. README with usage instructions
```

### Prompt: Bicep Generation

```
Generate Bicep templates for Azure compute infrastructure.

**Requirements:**
- Service: [VM / VMSS / AKS / Container Apps / App Service]
- Environment: [dev / staging / prod]
- [Include specific requirements]

**Standards:**
- Module structure: [single file / modules]
- Parameter files: [per environment]

Generate:
1. Main Bicep file
2. Modules (if applicable)
3. Parameter files
4. Deployment script
```

---

## Quick Reference Prompts

### VM Quick Size

```
Recommend Azure VM size for: [workload description]
Requirements: [CPU cores], [GB RAM], [storage needs]
Budget: [monthly limit]
```

### AKS Quick Config

```
Configure AKS for: [X] pods, [Y] services
Workloads: [stateless web / stateful / batch]
Features needed: [KEDA / Workload Identity / Spot pools]
```

### Container Apps Quick Deploy

```
Deploy Container App for: [image:tag]
Scale: [min]-[max] replicas
Trigger: [HTTP / Queue / Schedule]
Dapr: [yes/no, which building blocks]
```

### App Service Quick Plan

```
Recommend App Service plan for: [app type]
Traffic: [requests/day]
Features: [slots / VNet / always-on]
Budget: [monthly limit]
```
