# Vector Database Setup Checklists

Comprehensive checklists for database setup, deployment, and production readiness.

---

## Table of Contents

- [Pre-Setup Checklist](#pre-setup-checklist)
- [Development Setup Checklist](#development-setup-checklist)
- [Production Deployment Checklist](#production-deployment-checklist)
- [Security Hardening Checklist](#security-hardening-checklist)
- [High Availability Checklist](#high-availability-checklist)
- [Monitoring Setup Checklist](#monitoring-setup-checklist)
- [Database-Specific Checklists](#database-specific-checklists)

---

## Pre-Setup Checklist

### Requirements Analysis

- [ ] **Data requirements defined**
  - [ ] Expected vector count (initial and 12-month projection)
  - [ ] Vector dimensions determined (768, 1024, 1536, 3072)
  - [ ] Metadata schema designed
  - [ ] Update frequency estimated (real-time, batch, rarely)

- [ ] **Performance requirements defined**
  - [ ] Latency SLA (p50, p95, p99)
  - [ ] Throughput requirements (QPS)
  - [ ] Recall requirements (90%, 95%, 99%)
  - [ ] Availability SLA (99.9%, 99.99%)

- [ ] **Infrastructure decisions made**
  - [ ] Cloud provider selected (AWS, GCP, Azure, on-prem)
  - [ ] Managed vs self-hosted decision
  - [ ] Region/zone selection
  - [ ] Network architecture planned

- [ ] **Budget allocated**
  - [ ] Monthly infrastructure budget
  - [ ] Managed service costs estimated
  - [ ] Embedding API costs estimated
  - [ ] Operational overhead considered

### Database Selection

- [ ] Database selected based on requirements
- [ ] Proof of concept completed
- [ ] Benchmark results validated
- [ ] Migration path identified (if needs change)
- [ ] Vendor/community support evaluated

---

## Development Setup Checklist

### Local Environment

- [ ] **Docker setup**
  - [ ] Docker installed and running
  - [ ] Docker Compose available (if multi-container)
  - [ ] Sufficient disk space allocated
  - [ ] Port conflicts resolved

- [ ] **Database container running**
  - [ ] Image pulled (latest or pinned version)
  - [ ] Ports exposed correctly
  - [ ] Health check passing
  - [ ] Logs accessible

- [ ] **Client SDK installed**
  - [ ] Python SDK: `pip install {client-package}`
  - [ ] Version compatible with server
  - [ ] Connection tested successfully

- [ ] **Initial configuration**
  - [ ] Collection/index created
  - [ ] Vector dimensions configured
  - [ ] Distance metric selected (cosine, euclidean, dot)
  - [ ] Sample data inserted and queried

### Development Best Practices

- [ ] **Environment variables configured**
  - [ ] API keys in `.env` file (not committed)
  - [ ] Connection strings parameterized
  - [ ] Different configs for dev/test/prod

- [ ] **Data persistence configured**
  - [ ] Volume mounted for data persistence
  - [ ] Backup location identified
  - [ ] Data can survive container restart

- [ ] **Testing setup**
  - [ ] Unit tests for vector operations
  - [ ] Integration tests with real database
  - [ ] Test data fixtures created

---

## Production Deployment Checklist

### Infrastructure Preparation

- [ ] **Compute resources provisioned**
  - [ ] Instance type selected (CPU, memory)
  - [ ] Storage type and size configured
  - [ ] Network bandwidth adequate
  - [ ] Resource limits set

- [ ] **Network configuration**
  - [ ] VPC/network created
  - [ ] Subnets configured (public/private)
  - [ ] Security groups/firewall rules
  - [ ] Load balancer configured (if needed)

- [ ] **Storage configuration**
  - [ ] Persistent volumes created
  - [ ] Storage class selected (SSD recommended)
  - [ ] Backup storage location
  - [ ] Encryption at rest enabled

### Deployment

- [ ] **Container/pod configuration**
  - [ ] Resource requests and limits set
  - [ ] Health checks configured (liveness, readiness)
  - [ ] Restart policy defined
  - [ ] Graceful shutdown configured

- [ ] **Database configuration**
  - [ ] Production config applied (not defaults)
  - [ ] Index parameters tuned
  - [ ] Memory limits appropriate
  - [ ] Logging level set (info, not debug)

- [ ] **Scaling configuration**
  - [ ] Horizontal scaling enabled (if supported)
  - [ ] Auto-scaling rules defined
  - [ ] Capacity limits understood
  - [ ] Scale testing completed

### Validation

- [ ] **Functional testing**
  - [ ] CRUD operations verified
  - [ ] Search accuracy validated
  - [ ] Filtering works correctly
  - [ ] Batch operations tested

- [ ] **Performance testing**
  - [ ] Load testing completed
  - [ ] Latency under load acceptable
  - [ ] Throughput meets requirements
  - [ ] No memory leaks detected

- [ ] **Failover testing**
  - [ ] Node failure simulated
  - [ ] Recovery time acceptable
  - [ ] Data integrity preserved
  - [ ] Alerts triggered correctly

---

## Security Hardening Checklist

### Authentication

- [ ] **Access control configured**
  - [ ] Anonymous access disabled
  - [ ] API key authentication enabled
  - [ ] Keys stored securely (secrets manager)
  - [ ] Key rotation policy defined

- [ ] **Service accounts**
  - [ ] Separate accounts for different services
  - [ ] Minimal permissions per account
  - [ ] No shared credentials
  - [ ] Regular credential audits

### Network Security

- [ ] **Encryption in transit**
  - [ ] TLS enabled for all connections
  - [ ] Valid certificates installed
  - [ ] Certificate renewal automated
  - [ ] Strong cipher suites only

- [ ] **Network isolation**
  - [ ] Database in private subnet
  - [ ] No public IP (if possible)
  - [ ] VPC peering for app access
  - [ ] Firewall rules restrictive

- [ ] **Access restrictions**
  - [ ] IP allowlist configured (if applicable)
  - [ ] VPN required for admin access
  - [ ] Bastion host for SSH (if needed)
  - [ ] No direct internet exposure

### Data Security

- [ ] **Encryption at rest**
  - [ ] Storage encryption enabled
  - [ ] Backup encryption enabled
  - [ ] Key management configured
  - [ ] Keys stored securely

- [ ] **Audit logging**
  - [ ] Access logs enabled
  - [ ] Query logs enabled (if needed)
  - [ ] Logs shipped to central location
  - [ ] Log retention policy set

- [ ] **Data handling**
  - [ ] PII identification documented
  - [ ] Data classification applied
  - [ ] Retention policies implemented
  - [ ] Deletion procedures tested

---

## High Availability Checklist

### Replication

- [ ] **Replica configuration**
  - [ ] Replication enabled
  - [ ] Replication factor appropriate (2-3)
  - [ ] Sync vs async replication decided
  - [ ] Replica placement across zones

- [ ] **Failover configuration**
  - [ ] Automatic failover enabled
  - [ ] Failover timeout configured
  - [ ] Manual failover procedure documented
  - [ ] Failover tested successfully

### Backup and Recovery

- [ ] **Backup configuration**
  - [ ] Automated backups enabled
  - [ ] Backup schedule defined (daily minimum)
  - [ ] Backup retention period set
  - [ ] Backup location secure and separate

- [ ] **Recovery procedures**
  - [ ] Restore procedure documented
  - [ ] Restore tested successfully
  - [ ] RPO validated (data loss acceptable)
  - [ ] RTO validated (downtime acceptable)

- [ ] **Disaster recovery**
  - [ ] DR site identified (if needed)
  - [ ] Cross-region replication (if needed)
  - [ ] DR runbook documented
  - [ ] DR drill completed

### Load Balancing

- [ ] **Traffic distribution**
  - [ ] Load balancer configured
  - [ ] Health checks defined
  - [ ] Session affinity (if needed)
  - [ ] Connection draining enabled

- [ ] **Capacity planning**
  - [ ] Baseline metrics established
  - [ ] Growth projections documented
  - [ ] Scaling triggers defined
  - [ ] Capacity headroom maintained (30%+)

---

## Monitoring Setup Checklist

### Metrics Collection

- [ ] **Infrastructure metrics**
  - [ ] CPU utilization
  - [ ] Memory usage
  - [ ] Disk I/O and usage
  - [ ] Network throughput

- [ ] **Database metrics**
  - [ ] Query latency (p50, p95, p99)
  - [ ] Queries per second
  - [ ] Error rates
  - [ ] Index size and coverage

- [ ] **Application metrics**
  - [ ] Request latency
  - [ ] Error rates
  - [ ] Throughput
  - [ ] Cache hit rates

### Alerting

- [ ] **Critical alerts configured**
  - [ ] Database down
  - [ ] High error rate (> 1%)
  - [ ] Latency SLA breach
  - [ ] Disk space critical (> 85%)

- [ ] **Warning alerts configured**
  - [ ] High latency (p95 > threshold)
  - [ ] Elevated error rate (> 0.1%)
  - [ ] Memory pressure (> 80%)
  - [ ] Replication lag (> 1s)

- [ ] **Alert routing**
  - [ ] On-call rotation defined
  - [ ] Escalation policy set
  - [ ] Alert channels configured (Slack, PagerDuty)
  - [ ] Alert fatigue addressed

### Dashboards

- [ ] **Operational dashboard**
  - [ ] Key metrics visible
  - [ ] Time range selectable
  - [ ] Drill-down capability
  - [ ] Shared with team

- [ ] **Runbooks**
  - [ ] Common issues documented
  - [ ] Troubleshooting steps clear
  - [ ] Escalation paths defined
  - [ ] Updated regularly

---

## Database-Specific Checklists

### Qdrant Setup

- [ ] **Installation**
  - [ ] Docker/K8s deployment configured
  - [ ] Ports 6333 (HTTP) and 6334 (gRPC) exposed
  - [ ] Storage volume mounted
  - [ ] Config file applied

- [ ] **Configuration**
  - [ ] HNSW parameters tuned (M, ef_construct)
  - [ ] Quantization enabled (if needed)
  - [ ] On-disk payload configured (large payloads)
  - [ ] Telemetry disabled (production)

- [ ] **Security**
  - [ ] API key configured
  - [ ] TLS enabled
  - [ ] gRPC preferred for performance

- [ ] **Payload indexes created**
  - [ ] Keyword indexes for categorical filters
  - [ ] Integer indexes for range queries
  - [ ] DateTime indexes for temporal queries

### Weaviate Setup

- [ ] **Installation**
  - [ ] Docker/Helm deployment configured
  - [ ] Ports 8080 (HTTP) and 50051 (gRPC) exposed
  - [ ] Persistence volume mounted
  - [ ] Modules selected and enabled

- [ ] **Schema**
  - [ ] Classes defined with properties
  - [ ] Vectorizer configured (or none for BYOV)
  - [ ] Cross-references defined (if needed)
  - [ ] Inverted indexes configured

- [ ] **Security**
  - [ ] Anonymous access disabled
  - [ ] API key or OIDC configured
  - [ ] CORS configured for web clients

### Milvus Setup

- [ ] **Installation**
  - [ ] Deployment mode selected (standalone/cluster)
  - [ ] etcd, MinIO, Pulsar configured (cluster)
  - [ ] Resource limits set
  - [ ] Persistence configured

- [ ] **Collection**
  - [ ] Schema defined with field types
  - [ ] Primary key field set
  - [ ] Partition strategy planned
  - [ ] Consistency level selected

- [ ] **Indexes**
  - [ ] Index type selected (HNSW, IVF_FLAT)
  - [ ] Index parameters configured
  - [ ] Index built after data load
  - [ ] Index coverage verified

### pgvector Setup

- [ ] **Extension**
  - [ ] PostgreSQL 14+ installed
  - [ ] `vector` extension enabled
  - [ ] Appropriate PostgreSQL configuration

- [ ] **Table design**
  - [ ] Vector column with correct dimensions
  - [ ] Appropriate data types for metadata
  - [ ] Primary key defined

- [ ] **Indexing**
  - [ ] HNSW index created (not IVFFlat)
  - [ ] Operator class selected correctly
  - [ ] Index parameters tuned
  - [ ] Partial indexes for common filters

- [ ] **Performance**
  - [ ] Connection pooling configured
  - [ ] `maintenance_work_mem` set for indexing
  - [ ] `hnsw.ef_search` configured
  - [ ] VACUUM ANALYZE scheduled

### Pinecone Setup

- [ ] **Account**
  - [ ] API key generated
  - [ ] Environment/region selected
  - [ ] Billing configured

- [ ] **Index**
  - [ ] Dimension matches embedding model
  - [ ] Metric selected (cosine, euclidean, dotproduct)
  - [ ] Serverless vs pod-based decided
  - [ ] Replicas configured (if pod-based)

- [ ] **Namespaces**
  - [ ] Multi-tenancy strategy defined
  - [ ] Naming convention established
  - [ ] Namespace limits understood

### Chroma Setup

- [ ] **Client mode**
  - [ ] Persistence mode for non-ephemeral data
  - [ ] Storage path configured
  - [ ] Collection created

- [ ] **Production note**
  - [ ] Evaluated migration to production DB
  - [ ] Scale limitations understood
  - [ ] Not used for production workloads

---

## Post-Deployment Checklist

### Validation

- [ ] Application connectivity verified
- [ ] Sample queries working correctly
- [ ] Performance meets expectations
- [ ] Monitoring showing data

### Documentation

- [ ] Architecture documented
- [ ] Configuration documented
- [ ] Runbooks created
- [ ] Team trained

### Handoff

- [ ] On-call rotation established
- [ ] Escalation paths clear
- [ ] Knowledge transfer completed
- [ ] Maintenance schedule defined

---

*Checklists v1.0*
*Part of vector-database-setup skill*
