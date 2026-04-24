# Cloud Run Checklists

## Pre-Deployment Checklist

### Container Preparation

- [ ] Container image built and tested locally
- [ ] Image pushed to Artifact Registry (not Container Registry)
- [ ] Base image is actively maintained and secure
- [ ] Only necessary packages included
- [ ] No secrets baked into image
- [ ] Container listens on PORT environment variable
- [ ] Container starts in < 10 seconds (ideally < 4s)
- [ ] Container handles SIGTERM gracefully

### Configuration

- [ ] Region selected (consider latency, compliance)
- [ ] Memory limit set appropriately
- [ ] CPU limit set (1-8 vCPU)
- [ ] Request timeout configured
- [ ] Concurrency limit set (default 80)
- [ ] Min instances configured (0 for dev, 1+ for prod)
- [ ] Max instances set (cost control)

### Environment & Secrets

- [ ] Environment variables defined
- [ ] Secrets stored in Secret Manager
- [ ] Secrets mounted as env vars or volumes
- [ ] No sensitive data in environment variables

### Networking

- [ ] Ingress setting configured (internal/all)
- [ ] VPC egress configured if needed (Direct VPC egress)
- [ ] Subnet selected for Direct VPC egress (/26 minimum)
- [ ] Firewall rules created for VPC access
- [ ] Cloud NAT configured if external egress needed

### Health Checks

- [ ] Startup probe configured
- [ ] Liveness probe configured (if needed)
- [ ] Health check endpoints implemented
- [ ] Probe timeouts appropriate for startup time

---

## Security Checklist

### Identity & Access

- [ ] Dedicated service account created
- [ ] Minimal IAM roles assigned (least privilege)
- [ ] run.invoker role granted only to authorized principals
- [ ] Service account has only required permissions
- [ ] No allUsers/allAuthenticatedUsers unless intentional

### Image Security

- [ ] Binary Authorization enabled
- [ ] Attestor configured for image signing
- [ ] Vulnerability scanning enabled in Artifact Registry
- [ ] Images signed before deployment
- [ ] Only approved registries allowed

### Encryption

- [ ] CMEK configured (if required)
- [ ] Cloud KMS key created with appropriate permissions
- [ ] Key rotation policy configured
- [ ] Audit logging enabled for key usage

### Network Security

- [ ] Ingress restricted appropriately
- [ ] VPC Service Controls configured (if required)
- [ ] Cloud Armor policy attached (public services)
- [ ] WAF rules configured
- [ ] DDoS protection enabled

### Secret Management

- [ ] All secrets in Secret Manager
- [ ] Secret versions managed
- [ ] Secret access logged
- [ ] No secrets in environment variables or code

---

## Jobs Checklist

### Job Configuration

- [ ] Task count defined
- [ ] Parallelism configured appropriately
- [ ] Task timeout set (default 10min, max 168h)
- [ ] Retry count configured (default 3)
- [ ] Memory and CPU allocated

### Task Design

- [ ] Tasks are idempotent
- [ ] Checkpointing implemented for long tasks
- [ ] CLOUD_RUN_TASK_INDEX used for work distribution
- [ ] CLOUD_RUN_TASK_COUNT used for work calculation
- [ ] Error handling and logging implemented

### Scheduling (if applicable)

- [ ] Cloud Scheduler job created
- [ ] Service account with run.jobs.run permission
- [ ] Schedule expression correct (cron format)
- [ ] Timezone configured
- [ ] Retry policy configured

---

## Scaling Checklist

### Autoscaling Configuration

- [ ] Min instances set for critical services
- [ ] Max instances set for cost control
- [ ] Concurrency tuned for workload
- [ ] Startup CPU boost enabled (if needed)
- [ ] Instance-based billing (if background work needed)

### Performance

- [ ] Container startup optimized (< 10s)
- [ ] Application warm-up handled
- [ ] Connection pooling implemented
- [ ] Graceful shutdown handles in-flight requests
- [ ] CPU allocation matches workload type

---

## Multi-Container (Sidecars) Checklist

### Container Configuration

- [ ] Ingress container port explicitly set
- [ ] Only ingress container has port exposed
- [ ] Container dependencies defined
- [ ] Startup probes configured for dependencies
- [ ] Shared volumes configured if needed

### Sidecar Patterns

- [ ] Database proxy sidecar (Cloud SQL, AlloyDB)
- [ ] Observability sidecar (OpenTelemetry, Prometheus)
- [ ] Security sidecar (Envoy, WAF)
- [ ] All sidecars have appropriate resources

### Billing Considerations

- [ ] Instance-based billing enabled (if sidecars need CPU outside requests)
- [ ] Sidecar resource limits set appropriately

---

## Traffic Management Checklist

### Deployment Strategy

- [ ] Tag assigned to new revision
- [ ] No-traffic deployment for testing
- [ ] Traffic split configured
- [ ] Rollback plan documented

### Blue-Green Deployment

- [ ] Green revision deployed with tag
- [ ] Green revision tested via tagged URL
- [ ] Traffic shift to green verified
- [ ] Old revision cleanup scheduled

### Canary Deployment

- [ ] Canary traffic percentage set (e.g., 5%)
- [ ] Metrics and alerts configured
- [ ] Rollback threshold defined
- [ ] Gradual traffic increase plan

---

## Observability Checklist

### Logging

- [ ] Structured logging implemented (JSON)
- [ ] Log levels appropriate
- [ ] Request IDs propagated
- [ ] Sensitive data excluded from logs
- [ ] Log-based metrics created

### Monitoring

- [ ] Cloud Monitoring dashboards created
- [ ] Key metrics identified (latency, errors, throughput)
- [ ] Alerting policies configured
- [ ] SLOs defined and monitored
- [ ] Uptime checks configured

### Tracing

- [ ] Cloud Trace enabled
- [ ] Trace propagation implemented
- [ ] Custom spans added for key operations
- [ ] Trace sampling configured

---

## Cost Optimization Checklist

- [ ] Min instances = 0 for non-critical services
- [ ] Max instances limited
- [ ] Request-based billing used (when possible)
- [ ] CPU allocation matches workload
- [ ] Memory allocation right-sized
- [ ] Committed use discounts evaluated
- [ ] Regional vs multi-regional decision made
- [ ] Idle instance timeout configured
