# GCP Architecture Patterns Checklist

## Pre-Deployment Checklist

### Project Setup

- [ ] Project ID follows naming convention (`{org}-{env}-{app}`)
- [ ] Billing account linked
- [ ] Required APIs enabled
- [ ] Service accounts created with least privilege
- [ ] VPC network designed (shared VPC if multi-project)

### GKE Cluster

- [ ] **Cluster Type:** Regional (not zonal) for production
- [ ] **Node Locations:** Minimum 3 zones for HA
- [ ] **Private Cluster:** Enabled for security
- [ ] **Workload Identity:** Enabled (no service account keys)
- [ ] **Binary Authorization:** Enabled for container security
- [ ] **Release Channel:** REGULAR or STABLE (not RAPID for prod)
- [ ] **Dataplane V2:** Enabled for eBPF networking
- [ ] **Network Policy:** Enabled with Calico/Cilium
- [ ] **Managed Prometheus:** Enabled for monitoring
- [ ] **Maintenance Window:** Scheduled during low-traffic hours
- [ ] **Shielded Nodes:** Enabled
- [ ] **Secure Boot:** Enabled on node pools

### Node Pools

- [ ] Default node pool removed (use dedicated pools)
- [ ] Autoscaling configured with min/max limits
- [ ] Appropriate machine types selected
- [ ] SSD disks for performance-sensitive workloads
- [ ] Spot pool configured with taints for batch workloads
- [ ] Resource quotas defined per namespace

### Cloud SQL

- [ ] **Availability:** REGIONAL for production
- [ ] **Private IP:** Enabled (no public IP)
- [ ] **SSL Required:** Enabled
- [ ] **Backups:** Enabled with PITR for production
- [ ] **Retention:** 30+ days for production
- [ ] **Maintenance Window:** Scheduled during low-traffic
- [ ] **Query Insights:** Enabled
- [ ] **Logging Flags:** checkpoints, connections, lock_waits
- [ ] **Read Replicas:** Configured for read-heavy workloads
- [ ] **Deletion Protection:** Enabled for production

### Cloud Storage

- [ ] Uniform bucket-level access enabled
- [ ] Versioning enabled
- [ ] Lifecycle rules configured (NEARLINE at 90d, COLDLINE at 365d)
- [ ] CORS configured for web access
- [ ] Retention policy set if compliance required
- [ ] Soft delete enabled

### CDN Configuration

- [ ] Backend bucket with CDN enabled
- [ ] Cache mode appropriate (CACHE_ALL_STATIC or USE_ORIGIN_HEADERS)
- [ ] TTLs configured (default, max, client)
- [ ] Negative caching enabled
- [ ] Cache key policy defined
- [ ] Managed SSL certificate provisioned
- [ ] HTTPS redirect configured

### Networking

- [ ] VPC with custom subnets (not default)
- [ ] Private Google Access enabled
- [ ] Cloud NAT for private node egress
- [ ] Firewall rules follow least privilege
- [ ] Private Service Connect for managed services
- [ ] Load balancer health checks configured

### Security

- [ ] IAM follows least privilege principle
- [ ] Service accounts are purpose-specific
- [ ] Secrets stored in Secret Manager
- [ ] VPC Service Controls (if sensitive data)
- [ ] Cloud Armor for DDoS protection
- [ ] Audit logging enabled

### Monitoring & Observability

- [ ] Cloud Monitoring dashboards created
- [ ] Alerting policies configured
- [ ] Log sinks for long-term retention
- [ ] Uptime checks for critical endpoints
- [ ] SLOs defined and tracked
- [ ] Error Reporting enabled

---

## Microservices Checklist

### Service Design

- [ ] Services bounded by business capability
- [ ] API contracts defined (OpenAPI/gRPC)
- [ ] Idempotency keys for mutations
- [ ] Retry policies with exponential backoff
- [ ] Circuit breakers configured
- [ ] Timeout budgets defined

### Communication

- [ ] Sync: gRPC preferred over REST for internal
- [ ] Async: Pub/Sub for event-driven
- [ ] Dead letter queues configured
- [ ] Message ordering where required
- [ ] Schema validation (Pub/Sub schemas)

### Observability

- [ ] Distributed tracing (Cloud Trace / OpenTelemetry)
- [ ] Structured logging with correlation IDs
- [ ] Metrics exported (Prometheus format)
- [ ] Health check endpoints (`/health`, `/ready`)

### Deployment

- [ ] Canary or blue-green deployments
- [ ] Rollback procedures documented
- [ ] Feature flags for risky changes
- [ ] Database migrations backward compatible

---

## Data Pipeline Checklist

### Batch Pipelines

- [ ] Idempotent processing (re-runnable)
- [ ] Watermarks for late data handling
- [ ] Checkpointing for recovery
- [ ] Partitioned outputs (date-based)
- [ ] Schema evolution strategy defined

### Streaming Pipelines

- [ ] At-least-once delivery with dedup
- [ ] Windowing strategy defined
- [ ] Triggers configured (event time/processing time)
- [ ] Side inputs refreshed appropriately
- [ ] Autoscaling configured

### Data Quality

- [ ] Schema validation at ingestion
- [ ] Data quality checks (Great Expectations / dbt tests)
- [ ] Anomaly detection alerts
- [ ] Data lineage tracked (Data Catalog)
- [ ] SLAs defined for freshness

### BigQuery

- [ ] Tables partitioned (ingestion or field)
- [ ] Clustering on filter columns
- [ ] Slots reserved for critical queries
- [ ] Materialized views for common aggregations
- [ ] Row-level security if multi-tenant

---

## Cost Optimization Checklist

- [ ] Rightsizing recommendations reviewed
- [ ] Committed Use Discounts evaluated
- [ ] Spot VMs for fault-tolerant workloads
- [ ] Autoscaling tuned (not over-provisioned)
- [ ] Idle resources identified and removed
- [ ] Storage lifecycle policies active
- [ ] BigQuery on-demand vs. slots analyzed
- [ ] Budget alerts configured

---

*GCP Architecture Patterns Checklist | faion-infrastructure-engineer*
