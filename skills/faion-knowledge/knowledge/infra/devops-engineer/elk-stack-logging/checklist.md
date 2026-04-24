# ELK Stack Checklists

## Pre-Deployment Checklist

### Requirements Gathering

- [ ] Define log retention requirements (days/months)
- [ ] Estimate daily log volume (GB/day)
- [ ] Identify log sources (applications, infrastructure, cloud)
- [ ] Define search patterns and query requirements
- [ ] Determine alerting needs
- [ ] Identify compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Plan for data masking/redaction of PII

### Capacity Planning

- [ ] Calculate storage requirements (volume x retention x replication)
- [ ] Size Elasticsearch cluster (nodes, RAM, CPU, storage)
- [ ] Plan shard strategy (shards per index, replicas)
- [ ] Determine node roles (master, data, ingest, coordinating)
- [ ] Plan hot-warm-cold architecture if needed

### Infrastructure

- [ ] Provision dedicated nodes/VMs for Elasticsearch
- [ ] Configure fast storage (SSD/NVMe for hot nodes)
- [ ] Set up network (private network for cluster)
- [ ] Configure load balancer for coordinating nodes
- [ ] Plan backup strategy (snapshots)

---

## Elasticsearch Setup Checklist

### Cluster Configuration

- [ ] Set `cluster.name` (unique, descriptive)
- [ ] Configure `node.name` for each node
- [ ] Set `node.roles` appropriately
- [ ] Configure `discovery.seed_hosts`
- [ ] Set `cluster.initial_master_nodes` (first start only)
- [ ] Enable `bootstrap.memory_lock: true`
- [ ] Set `path.data` and `path.logs`

### JVM Configuration

- [ ] Set heap size to 50% of RAM (max 32GB)
- [ ] Configure `-Xms` and `-Xmx` to same value
- [ ] Enable G1GC for heaps > 6GB
- [ ] Set `ES_JAVA_OPTS` environment variable

### Security Configuration

- [ ] Enable `xpack.security.enabled: true`
- [ ] Generate certificates for TLS
- [ ] Configure transport layer TLS
- [ ] Configure HTTP layer TLS
- [ ] Set up built-in users (elastic, kibana_system, etc.)
- [ ] Create application-specific users and roles
- [ ] Enable audit logging if required

### Index Management

- [ ] Create index templates for each log type
- [ ] Define field mappings (keyword vs text)
- [ ] Create ILM policies
- [ ] Set up rollover aliases
- [ ] Configure index settings (shards, replicas, refresh_interval)

---

## Logstash Setup Checklist

### Pipeline Configuration

- [ ] Define input plugins (beats, kafka, file, etc.)
- [ ] Configure filter plugins (grok, json, mutate, date)
- [ ] Set up output plugins (elasticsearch)
- [ ] Configure pipeline workers and batch size
- [ ] Set up dead letter queue for failed events

### Security

- [ ] Configure SSL/TLS for inputs
- [ ] Set up authentication to Elasticsearch
- [ ] Store credentials securely (keystore)
- [ ] Implement data masking for PII

### Performance

- [ ] Tune `pipeline.workers` (CPU cores)
- [ ] Adjust `pipeline.batch.size` (125-1000)
- [ ] Configure `pipeline.batch.delay`
- [ ] Monitor JVM heap usage

---

## Filebeat/Beats Setup Checklist

### Basic Configuration

- [ ] Define input paths/sources
- [ ] Configure multiline handling
- [ ] Set up processors (add_host_metadata, add_cloud_metadata)
- [ ] Configure output (Elasticsearch or Logstash)
- [ ] Set up index template loading

### Kubernetes/Container

- [ ] Deploy as DaemonSet
- [ ] Configure autodiscover provider
- [ ] Set container input paths
- [ ] Add Kubernetes metadata processor
- [ ] Configure resource limits

### Security

- [ ] Configure SSL/TLS certificates
- [ ] Set up authentication credentials
- [ ] Store secrets securely

---

## Kibana Setup Checklist

### Configuration

- [ ] Set `server.host` and `server.port`
- [ ] Configure `elasticsearch.hosts`
- [ ] Set up authentication (`elasticsearch.username`, `elasticsearch.password`)
- [ ] Configure SSL/TLS
- [ ] Set `xpack.encryptedSavedObjects.encryptionKey`

### Post-Installation

- [ ] Create data views (index patterns)
- [ ] Set up default time filter
- [ ] Create saved searches
- [ ] Build dashboards for key metrics
- [ ] Configure alerting rules
- [ ] Set up user spaces if multi-tenant
- [ ] Create roles and assign users

---

## Operational Checklist

### Daily Monitoring

- [ ] Check cluster health (green/yellow/red)
- [ ] Review index stats (doc count, size)
- [ ] Monitor node stats (CPU, memory, disk)
- [ ] Check indexing rate and latency
- [ ] Review search latency
- [ ] Check for rejected threads
- [ ] Monitor JVM heap usage

### Weekly Tasks

- [ ] Review ILM policy execution
- [ ] Check snapshot success/failure
- [ ] Review slow logs
- [ ] Analyze top queries for optimization
- [ ] Check disk space projections
- [ ] Review alerting rule effectiveness

### Monthly Tasks

- [ ] Capacity planning review
- [ ] Performance tuning assessment
- [ ] Security audit (users, roles, access)
- [ ] Update Elastic Stack if needed
- [ ] Review and optimize mappings
- [ ] Analyze cost optimization opportunities

---

## Troubleshooting Checklist

### Cluster Red/Yellow Status

- [ ] Check `_cluster/health` for unassigned shards
- [ ] Run `_cluster/allocation/explain` for allocation issues
- [ ] Verify disk space on all nodes
- [ ] Check for node failures
- [ ] Review recent changes (mapping, settings)

### High Latency

- [ ] Check thread pool rejections
- [ ] Review GC logs for long pauses
- [ ] Analyze slow logs
- [ ] Check shard sizes (too large/small)
- [ ] Monitor CPU and I/O wait

### Indexing Issues

- [ ] Check for mapping conflicts
- [ ] Review bulk request sizes
- [ ] Check for version conflicts
- [ ] Monitor refresh and merge operations
- [ ] Review ingest pipeline errors

### Memory Issues

- [ ] Check heap usage and GC frequency
- [ ] Review fielddata cache size
- [ ] Check query cache usage
- [ ] Monitor request cache
- [ ] Analyze circuit breaker trips

---

## Security Checklist

### Network Security

- [ ] Elasticsearch on private network only
- [ ] Kibana behind reverse proxy with auth
- [ ] TLS for all communications
- [ ] Firewall rules restricting access
- [ ] No public exposure of cluster ports

### Authentication & Authorization

- [ ] Built-in users passwords changed
- [ ] Role-based access control configured
- [ ] Minimal privileges principle applied
- [ ] Service accounts for automation
- [ ] API keys for programmatic access

### Data Protection

- [ ] PII masking in Logstash/ingest
- [ ] Document-level security if needed
- [ ] Field-level security for sensitive data
- [ ] Audit logging enabled
- [ ] Snapshot encryption configured

### Compliance

- [ ] Data retention policies align with regulations
- [ ] Right to deletion process documented
- [ ] Access logs retained
- [ ] Security certifications maintained
