# ELK Stack Checklist

## Pre-Deployment Checklist

### Infrastructure Requirements

- [ ] **Hardware sizing calculated**
  - Elasticsearch: Min 4GB RAM per node, SSD storage
  - Logstash: Min 2GB RAM, CPU-bound for parsing
  - Kibana: Min 1GB RAM
  - Calculate storage: daily log volume x retention days x 1.1 (overhead)

- [ ] **Network configuration**
  - Port 9200 (Elasticsearch HTTP)
  - Port 9300 (Elasticsearch transport)
  - Port 5044 (Beats input)
  - Port 5601 (Kibana)
  - Port 9600 (Logstash monitoring)

- [ ] **Security prerequisites**
  - TLS certificates generated
  - CA certificate available
  - Passwords for built-in users defined
  - Network firewall rules configured

### Elasticsearch Cluster

- [ ] **Cluster topology defined**
  - Number of master nodes (3 for HA)
  - Number of data nodes
  - Ingest node requirements
  - Coordinating node requirements

- [ ] **Node configuration**
  - `cluster.name` set consistently
  - `node.name` unique per node
  - `node.roles` assigned appropriately
  - `discovery.seed_hosts` configured
  - `cluster.initial_master_nodes` set

- [ ] **Memory settings**
  - JVM heap: 50% of available RAM (max 32GB)
  - `bootstrap.memory_lock: true` enabled
  - Swap disabled or minimized

- [ ] **Storage configuration**
  - `path.data` on fast storage (SSD/NVMe)
  - `path.logs` configured
  - Sufficient disk space for retention

### Security Configuration

- [ ] **X-Pack security enabled**
  - `xpack.security.enabled: true`
  - Transport layer SSL/TLS
  - HTTP layer SSL/TLS

- [ ] **Authentication configured**
  - Built-in users passwords set
  - Service accounts created
  - API keys generated

- [ ] **Authorization configured**
  - Roles defined
  - Role mappings created
  - Field-level security (if needed)

### Index Management

- [ ] **Index templates created**
  - Mapping definitions
  - Settings (shards, replicas)
  - ILM policy attached

- [ ] **ILM policies defined**
  - Hot phase (rollover criteria)
  - Warm phase (shrink, force merge)
  - Cold phase (freeze)
  - Delete phase (retention)

- [ ] **Aliases configured**
  - Write alias for ingestion
  - Read alias for queries

## Logstash Checklist

- [ ] **Pipeline configuration**
  - Input plugins configured
  - Filter plugins for parsing
  - Output to Elasticsearch

- [ ] **Performance tuning**
  - `pipeline.workers` set
  - `pipeline.batch.size` optimized
  - `pipeline.batch.delay` configured

- [ ] **Error handling**
  - Dead letter queue enabled
  - Failed event logging
  - Retry policies defined

- [ ] **Security**
  - SSL for Beats input
  - Elasticsearch credentials secured
  - Sensitive data masking in filters

## Filebeat Checklist

- [ ] **Input configuration**
  - Log paths defined
  - Multiline patterns (if needed)
  - Fields and tags added

- [ ] **Processors configured**
  - `add_host_metadata`
  - `add_cloud_metadata`
  - `add_docker_metadata` (if applicable)
  - `add_kubernetes_metadata` (if applicable)

- [ ] **Output configured**
  - Elasticsearch or Logstash target
  - SSL/TLS settings
  - Credentials secured

- [ ] **Modules enabled** (if using)
  - System module
  - Nginx module
  - Application-specific modules

## Kibana Checklist

- [ ] **Server configuration**
  - `server.host` and `server.port` set
  - `server.name` defined
  - Base path configured (if reverse proxy)

- [ ] **Elasticsearch connection**
  - Hosts configured
  - Credentials set
  - SSL/TLS enabled

- [ ] **Security**
  - `xpack.security.enabled: true`
  - Encryption key set
  - Session timeout configured

- [ ] **Spaces and roles** (if multi-tenant)
  - Spaces created
  - Role-based access configured

## Kubernetes (ECK) Checklist

- [ ] **ECK operator deployed**
  - CRDs installed
  - Operator running

- [ ] **Elasticsearch CR configured**
  - Node sets defined
  - Resources (CPU, memory) set
  - Volume claims configured
  - Pod disruption budgets

- [ ] **Kibana CR configured**
  - Elasticsearch reference set
  - Ingress/service configured

- [ ] **Beats/Agents deployed**
  - DaemonSet for Filebeat
  - Autodiscover configured
  - RBAC for Kubernetes metadata

## Post-Deployment Checklist

### Verification

- [ ] **Cluster health green**
  - `GET _cluster/health`
  - All shards allocated
  - No unassigned shards

- [ ] **Indices receiving data**
  - Data streams active
  - Rollover working

- [ ] **Kibana accessible**
  - Login working
  - Index patterns created
  - Dashboards loading

- [ ] **Alerts configured**
  - Error rate alerts
  - Disk space alerts
  - Cluster health alerts

### Documentation

- [ ] **Runbooks created**
  - Common troubleshooting steps
  - Scaling procedures
  - Backup/restore procedures

- [ ] **Dashboards documented**
  - Purpose of each dashboard
  - Key metrics explained

- [ ] **On-call procedures**
  - Alert escalation paths
  - Contact information

## Operational Checklist

### Daily Operations

- [ ] Check cluster health
- [ ] Review error dashboards
- [ ] Verify data ingestion rates
- [ ] Check disk space usage

### Weekly Operations

- [ ] Review ILM policy execution
- [ ] Check for slow queries
- [ ] Review resource utilization
- [ ] Validate backup completion

### Monthly Operations

- [ ] Capacity planning review
- [ ] Security audit (access logs)
- [ ] Index template review
- [ ] Performance tuning assessment

## Troubleshooting Checklist

### Cluster Issues

- [ ] Check Elasticsearch logs for errors
- [ ] Verify node connectivity
- [ ] Check shard allocation
- [ ] Review JVM heap usage
- [ ] Check disk watermarks

### Ingestion Issues

- [ ] Verify Beats/Logstash connectivity
- [ ] Check for parsing errors
- [ ] Review dead letter queue
- [ ] Validate index permissions

### Query Performance

- [ ] Check slow log
- [ ] Review query patterns
- [ ] Analyze shard sizes
- [ ] Consider index optimization

---

*ELK Stack Checklist | faion-cicd-engineer*
