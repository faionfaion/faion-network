# LLM Prompts for Vector Database Setup

Prompts for setup assistance, configuration, troubleshooting, and deployment guidance.

---

## Table of Contents

- [Setup Planning Prompts](#setup-planning-prompts)
- [Configuration Prompts](#configuration-prompts)
- [Deployment Prompts](#deployment-prompts)
- [Troubleshooting Prompts](#troubleshooting-prompts)
- [Security Setup Prompts](#security-setup-prompts)
- [Scaling Prompts](#scaling-prompts)
- [Migration Prompts](#migration-prompts)

---

## Setup Planning Prompts

### Initial Setup Requirements

```
I need to set up a vector database for my project.

Project details:
- Use case: {rag_system/semantic_search/recommendation/other}
- Expected vectors: {count} (current), {count} (12-month projection)
- Vector dimensions: {dimensions} (or embedding model: {model_name})
- Query frequency: {qps} queries per second
- Latency requirement: {latency_ms}ms p95

Infrastructure context:
- Cloud provider: {aws/gcp/azure/on-prem}
- Existing infrastructure: {kubernetes/docker/vms/managed}
- Team expertise: {devops_level}
- Budget: ${monthly_budget}/month

Help me:
1. Choose the right database for my needs
2. Plan the deployment approach (managed vs self-hosted)
3. Estimate infrastructure requirements (CPU, memory, storage)
4. Create a setup checklist
5. Identify potential challenges
```

### Database Comparison for Setup

```
Compare setup complexity for {database_1} vs {database_2}:

Requirements:
- Environment: {production/development/testing}
- Deployment: {docker/kubernetes/managed}
- Team size: {team_size}
- DevOps experience: {beginner/intermediate/expert}

Compare:
1. Installation complexity
2. Initial configuration effort
3. Ongoing maintenance burden
4. Monitoring setup requirements
5. Upgrade process
6. Documentation quality
7. Community support
8. Time to first working query

Recommend which database would be easier to set up and maintain.
```

### Resource Estimation

```
Estimate infrastructure requirements for my vector database:

Data characteristics:
- Vector count: {count}
- Vector dimensions: {dimensions}
- Metadata size per vector: {size_kb}KB average
- Index type: {hnsw/ivf/flat}

Performance requirements:
- Query latency: {latency_ms}ms p95
- Throughput: {qps} queries per second
- Concurrent users: {concurrent_users}

Estimate:
1. Memory requirements
2. CPU requirements
3. Storage requirements
4. Network bandwidth
5. Recommended instance type (for {cloud_provider})
6. Cost estimate

Show calculations and assumptions.
```

---

## Configuration Prompts

### Index Parameter Tuning

```
Help me configure HNSW index parameters for optimal performance.

Current setup:
- Database: {database_name}
- Vector count: {count}
- Vector dimensions: {dimensions}
- Available memory: {memory_gb}GB

Performance requirements:
- Target latency: {latency_ms}ms p95
- Minimum recall: {recall}%
- Query pattern: {mostly_reads/balanced/write_heavy}

Current parameters:
- M: {current_m}
- ef_construct: {current_ef_construct}
- ef_search: {current_ef_search}

Recommend:
1. Optimal M value with reasoning
2. Optimal ef_construct value
3. Optimal ef_search value
4. Whether to enable quantization
5. Expected memory usage
6. Expected performance characteristics
```

### Collection/Schema Design

```
Design a collection schema for my use case.

Use case: {description}

Data structure:
- Document types: {types}
- Required metadata fields: {fields}
- Searchable text fields: {text_fields}
- Filter fields: {filter_fields}
- Date/time fields: {date_fields}

Query patterns:
- Vector search with filters: {yes/no}
- Hybrid search (vector + keyword): {yes/no}
- Common filter combinations: {filter_patterns}

Database: {database_name}

Provide:
1. Complete collection/table schema
2. Vector configuration (dimension, distance metric)
3. Index recommendations for filter fields
4. Payload/metadata structure
5. Sample code to create the collection
```

### Quantization Configuration

```
Configure quantization for my vector database.

Current state:
- Database: {database_name}
- Vector count: {count}
- Vector dimensions: {dimensions}
- Current memory usage: {memory_gb}GB
- Available memory: {available_gb}GB

Constraints:
- Maximum recall loss: {max_recall_loss}%
- Maximum latency increase: {max_latency_increase}%
- Budget constraints: {budget_constraints}

Recommend:
1. Quantization type (scalar/product/binary)
2. Specific configuration parameters
3. Expected memory reduction
4. Expected performance impact
5. Rescoring configuration
6. Step-by-step implementation guide
```

---

## Deployment Prompts

### Docker Deployment

```
Create a Docker deployment for {database_name}.

Requirements:
- Environment: {development/staging/production}
- Persistent storage: {yes/no}
- Resource limits: {memory}GB RAM, {cpu} CPU
- Networking: {expose_ports/internal_only}
- Security: {api_key/tls/both}

Provide:
1. docker-compose.yml file
2. Configuration files needed
3. Environment variables template
4. Health check configuration
5. Volume setup for persistence
6. Startup verification commands
```

### Kubernetes Deployment

```
Create a Kubernetes deployment for {database_name}.

Requirements:
- Environment: {development/staging/production}
- Replicas: {replica_count}
- Storage class: {storage_class}
- Storage size: {storage_gb}GB
- Resource limits: {memory}GB RAM, {cpu} CPU
- Ingress: {yes/no}
- TLS: {yes/no}

Provide:
1. Complete Kubernetes manifests (Deployment/StatefulSet, Service, PVC, ConfigMap, Secret)
2. Helm values.yaml (if using Helm)
3. Ingress configuration (if needed)
4. ServiceMonitor for Prometheus (if needed)
5. Deployment commands
6. Verification steps
```

### Managed Service Setup

```
Help me set up {managed_service} for vector storage.

Requirements:
- Cloud provider: {aws/gcp/azure}
- Expected usage: {vectors} vectors, {qps} QPS
- Region: {region}
- Compliance: {compliance_requirements}
- Budget: ${monthly_budget}/month

Provide:
1. Step-by-step setup guide
2. Recommended tier/configuration
3. Network configuration (VPC, security groups)
4. Authentication setup
5. Client connection code
6. Monitoring setup
7. Cost estimation
```

---

## Troubleshooting Prompts

### Connection Issues

```
Troubleshoot connection issues with my vector database.

Database: {database_name}
Client: {client_library} version {version}
Server: version {version}

Error:
```
{error_message}
```

Connection configuration:
```
{connection_config}
```

Environment:
- Client location: {client_location}
- Server location: {server_location}
- Network: {network_type}
- TLS: {enabled/disabled}

What I've tried:
{attempted_solutions}

Help me:
1. Identify the root cause
2. Provide diagnostic commands to run
3. Suggest configuration fixes
4. Recommend resilience patterns
```

### Startup Failures

```
My vector database container/pod won't start.

Database: {database_name}
Deployment: {docker/kubernetes}

Error logs:
```
{error_logs}
```

Container/pod status:
```
{status_output}
```

Configuration:
```
{config}
```

Help me:
1. Identify why startup is failing
2. Check for common configuration issues
3. Verify resource requirements
4. Suggest fixes
5. Provide verification commands
```

### Performance Issues

```
My vector database setup has performance issues.

Database: {database_name}
Deployment: {docker/kubernetes/managed}

Symptoms:
- Observed latency: {latency}ms (expected: {expected}ms)
- CPU usage: {cpu}%
- Memory usage: {memory}%
- Disk I/O: {disk_io}

Configuration:
- Instance type: {instance_type}
- Vector count: {count}
- Index type: {index_type}
- Index parameters: {params}

Help me:
1. Identify performance bottlenecks
2. Check configuration issues
3. Recommend resource adjustments
4. Suggest index optimizations
5. Provide monitoring recommendations
```

### Data Persistence Issues

```
My vector database is losing data.

Database: {database_name}
Deployment: {docker/kubernetes}

Symptoms:
- Data present before restart: {count_before}
- Data after restart: {count_after}
- Frequency: {always/sometimes}

Volume configuration:
```
{volume_config}
```

Startup logs:
```
{logs}
```

Help me:
1. Verify volume mount configuration
2. Check data persistence settings
3. Identify data loss cause
4. Recommend fixes
5. Set up proper backup
```

---

## Security Setup Prompts

### Authentication Configuration

```
Configure authentication for my vector database.

Database: {database_name}
Deployment: {docker/kubernetes/managed}
Environment: {development/staging/production}

Requirements:
- Authentication method: {api_key/oidc/basic}
- Multiple users/services: {yes/no}
- Audit logging: {required/optional}

Provide:
1. Authentication configuration
2. Secret/credential management
3. Client connection code with auth
4. Key rotation procedure
5. Audit logging setup (if required)
```

### TLS Configuration

```
Configure TLS encryption for my vector database.

Database: {database_name}
Deployment: {docker/kubernetes}

Requirements:
- Certificate source: {self_signed/letsencrypt/corporate_ca}
- Client verification: {yes/no}
- Internal/external exposure: {internal/external/both}

Provide:
1. Certificate generation/acquisition steps
2. Server TLS configuration
3. Client connection configuration
4. Certificate renewal automation
5. Verification commands
```

### Network Security

```
Configure network security for my vector database.

Database: {database_name}
Cloud provider: {aws/gcp/azure/on-prem}
Deployment: {docker/kubernetes}

Current network setup:
- VPC/Network: {network_details}
- Subnets: {subnet_details}
- Current firewall rules: {current_rules}

Requirements:
- Access from: {applications/services}
- Admin access: {vpn/bastion/direct}
- Public exposure: {none/limited/full}

Provide:
1. Security group/firewall rules
2. Network policy (for Kubernetes)
3. VPC peering/private endpoint setup
4. Bastion/jump host configuration (if needed)
5. Verification steps
```

---

## Scaling Prompts

### Vertical Scaling

```
Plan vertical scaling for my vector database.

Database: {database_name}
Current instance: {instance_type}
Current performance:
- CPU usage: {cpu}%
- Memory usage: {memory}%
- Disk I/O: {disk_io}
- Query latency: {latency}ms

Growth projections:
- Vectors in 6 months: {count}
- Expected QPS in 6 months: {qps}

Recommend:
1. New instance size
2. Memory requirements calculation
3. Storage requirements
4. Migration procedure
5. Downtime estimation
6. Rollback plan
```

### Horizontal Scaling

```
Plan horizontal scaling for my vector database.

Database: {database_name}
Current setup: {single_node/replicated}
Current performance: {current_metrics}

Requirements:
- High availability: {required/optional}
- Read scaling: {required/optional}
- Write scaling: {required/optional}
- Geographic distribution: {required/optional}

Provide:
1. Cluster architecture recommendation
2. Sharding/partitioning strategy
3. Replication configuration
4. Load balancing setup
5. Failover configuration
6. Step-by-step scaling procedure
```

### Auto-Scaling Configuration

```
Configure auto-scaling for my vector database.

Database: {database_name}
Deployment: {kubernetes/managed}
Cloud provider: {aws/gcp/azure}

Traffic patterns:
- Peak hours: {peak_times}
- Peak QPS: {peak_qps}
- Off-peak QPS: {offpeak_qps}

Constraints:
- Minimum replicas: {min}
- Maximum replicas: {max}
- Scale-up time: {max_scaleup_time}
- Budget ceiling: ${budget}/month

Provide:
1. HPA/auto-scaling configuration
2. Metrics to scale on
3. Scale-up/down thresholds
4. Cooldown periods
5. Cost estimation
6. Monitoring alerts
```

---

## Migration Prompts

### Development to Production Migration

```
Migrate my vector database from development to production.

Database: {database_name}

Development setup:
- Deployment: {docker_compose/local}
- Data volume: {dev_vectors} vectors
- Configuration: {dev_config}

Production requirements:
- Deployment: {kubernetes/managed}
- Expected scale: {prod_vectors} vectors
- Availability: {availability_sla}
- Security: {security_requirements}

Provide:
1. Production infrastructure setup
2. Data migration procedure
3. Configuration changes for production
4. Security hardening steps
5. Monitoring and alerting setup
6. Rollback plan
7. Go-live checklist
```

### Database Migration

```
Migrate from {source_db} to {target_db}.

Source database:
- Type: {source_db}
- Vectors: {count}
- Schema: {schema_description}
- Current deployment: {deployment_type}

Target database:
- Type: {target_db}
- Deployment: {target_deployment}
- Region: {region}

Requirements:
- Downtime tolerance: {max_downtime}
- Data validation: {validation_requirements}
- Rollback capability: {required/optional}

Provide:
1. Pre-migration checklist
2. Schema mapping
3. Data export procedure
4. Data import procedure
5. Validation queries
6. Application cutover steps
7. Rollback procedure
```

### Cloud Migration

```
Migrate my vector database to the cloud.

Current setup:
- Database: {database_name}
- Deployment: {on_prem/docker}
- Data size: {vectors} vectors, {storage}GB

Target:
- Cloud provider: {aws/gcp/azure}
- Deployment type: {managed/self_hosted_k8s/self_hosted_vms}
- Region: {region}

Requirements:
- Downtime tolerance: {max_downtime}
- Network connectivity: {vpn/direct_connect/public}
- Compliance: {compliance_requirements}

Provide:
1. Cloud infrastructure setup
2. Network connectivity setup
3. Data migration strategy
4. Step-by-step migration procedure
5. Validation steps
6. DNS/routing cutover
7. Cleanup of old infrastructure
```

---

## Usage Guidelines

### Filling Placeholders

Replace all `{placeholder}` values with actual data:
- `{database_name}`: qdrant, weaviate, milvus, pgvector, pinecone, chroma
- `{count}`: Actual vector counts (e.g., 1000000)
- `{dimensions}`: Vector dimensions (e.g., 1536)
- `{latency_ms}`: Milliseconds (e.g., 50)
- `{memory_gb}`: Gigabytes (e.g., 16)

### Iterative Problem Solving

For complex issues:
1. Start with a broad diagnostic prompt
2. Narrow down based on initial findings
3. Request specific solutions
4. Validate before implementing
5. Document the solution

### Best Practices

- Include relevant error messages and logs
- Specify your environment and constraints
- Mention what you've already tried
- Ask for verification steps
- Request rollback procedures for critical changes

---

*LLM Prompts v1.0*
*Part of vector-database-setup skill*
