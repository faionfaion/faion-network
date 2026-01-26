# Cloud Run LLM Prompts

## Service Deployment

### Deploy New Service

```
Deploy a Cloud Run service with the following requirements:
- Service name: {service_name}
- Region: {region}
- Image: {image_url}
- Memory: {memory} (e.g., 512Mi, 2Gi)
- CPU: {cpu} (e.g., 1, 2)
- Min instances: {min_instances}
- Max instances: {max_instances}
- Environment variables: {env_vars}
- Secrets from Secret Manager: {secrets}
- Public/private: {access_type}

Generate:
1. gcloud command for deployment
2. Terraform configuration
3. YAML configuration

Include best practices for production deployment.
```

### Migrate to Direct VPC Egress

```
Migrate Cloud Run service from Serverless VPC Access connector to Direct VPC egress:
- Service: {service_name}
- Region: {region}
- VPC network: {vpc_name}
- Subnet: {subnet_name}
- Current connector: {connector_name}

Provide:
1. Pre-migration checklist
2. Required firewall rules
3. gcloud commands for migration
4. Terraform configuration updates
5. Post-migration validation steps
6. Connector cleanup steps
```

### Configure Health Checks

```
Configure health checks for Cloud Run service:
- Service: {service_name}
- Startup time: approximately {startup_seconds} seconds
- Health endpoint: {health_path}
- Protocol: {http/tcp/grpc}

Generate:
1. Appropriate startup probe configuration
2. Liveness probe configuration (if needed)
3. Code example for health endpoint (Python/Node.js/Go)
4. gcloud deployment command with probes
5. YAML configuration
```

---

## Job Configuration

### Create Parallel Job

```
Create a Cloud Run job for parallel batch processing:
- Job name: {job_name}
- Total items to process: {total_items}
- Desired parallelism: {parallelism}
- Processing time per item: approximately {seconds} seconds
- Image: {image_url}
- Memory per task: {memory}

Provide:
1. Job configuration (task count, parallelism)
2. gcloud command for job creation
3. Terraform configuration
4. Python/Node.js code template for task index handling
5. Checkpointing strategy
```

### Schedule Job with Cloud Scheduler

```
Schedule a Cloud Run job to run on a recurring schedule:
- Job name: {job_name}
- Schedule: {cron_expression} (e.g., "0 6 * * *" for daily at 6 AM)
- Timezone: {timezone}
- Service account: {sa_email}

Generate:
1. gcloud commands for job and scheduler creation
2. Terraform configuration
3. IAM permissions required
4. Retry and error handling configuration
```

---

## Security Configuration

### Enable Binary Authorization

```
Enable Binary Authorization for Cloud Run:
- Project: {project_id}
- Service: {service_name}
- Attestor name: {attestor_name}
- Signing approach: {kms/pkix}

Provide:
1. Step-by-step setup instructions
2. gcloud commands for attestor creation
3. Policy configuration
4. Attestation creation workflow
5. CI/CD integration example (Cloud Build)
```

### Configure CMEK

```
Configure customer-managed encryption keys (CMEK) for Cloud Run:
- Project: {project_id}
- Region: {region}
- Key ring name: {keyring_name}
- Key name: {key_name}

Generate:
1. KMS key creation commands
2. IAM permissions for Cloud Run service agent
3. Deployment command with CMEK
4. Terraform configuration
5. Key rotation policy
```

### Implement Least Privilege IAM

```
Set up IAM for Cloud Run service with least privilege:
- Service: {service_name}
- Service needs access to: {resources} (e.g., Cloud SQL, Pub/Sub, Storage)
- Invokers: {invoker_types} (e.g., users, service accounts, public)

Provide:
1. Dedicated service account creation
2. Required IAM roles for each resource
3. Invoker IAM bindings
4. gcloud commands
5. Terraform configuration
```

---

## Multi-Container Patterns

### Add Cloud SQL Proxy Sidecar

```
Add Cloud SQL Proxy sidecar to Cloud Run service:
- Service: {service_name}
- Database instance: {project}:{region}:{instance}
- Database type: {postgres/mysql}

Generate:
1. Complete YAML configuration with container dependencies
2. Startup probe configuration for proxy
3. Application environment variables
4. gcloud deployment command
5. Terraform configuration
```

### Add Observability Sidecar

```
Add OpenTelemetry/Prometheus sidecar for metrics:
- Service: {service_name}
- Metrics backend: {cloud_monitoring/custom}
- Application metrics endpoint: {metrics_path}

Provide:
1. Sidecar container configuration
2. YAML with container dependencies
3. Application instrumentation example
4. Cloud Monitoring integration
```

---

## Traffic Management

### Implement Blue-Green Deployment

```
Implement blue-green deployment for Cloud Run:
- Service: {service_name}
- New image: {new_image}
- Region: {region}

Generate:
1. Deploy new revision without traffic
2. Test new revision commands
3. Traffic shift commands
4. Rollback commands
5. CI/CD pipeline integration
```

### Implement Canary Deployment

```
Implement gradual canary rollout for Cloud Run:
- Service: {service_name}
- New image: {new_image}
- Traffic progression: {percentages} (e.g., 5%, 25%, 50%, 100%)

Provide:
1. Initial canary deployment
2. Traffic split commands for each stage
3. Metrics to monitor
4. Rollback procedure
5. Automation script for gradual rollout
```

---

## Performance Optimization

### Optimize Cold Start

```
Optimize Cloud Run service for minimal cold start:
- Current startup time: {seconds}
- Language/framework: {language_framework}
- Current container size: {size}

Provide:
1. Container optimization techniques
2. Dockerfile improvements
3. Application-level optimizations
4. Cloud Run configuration (min instances, CPU boost)
5. Startup probe configuration
6. Benchmarking commands
```

### Optimize for High Throughput

```
Optimize Cloud Run service for high throughput:
- Expected RPS: {requests_per_second}
- Request latency SLA: {latency_ms}
- Current bottlenecks: {bottlenecks}

Provide:
1. Concurrency configuration
2. Resource sizing (CPU, memory)
3. Scaling configuration
4. Connection pooling recommendations
5. Load testing approach
```

---

## Troubleshooting

### Debug Service Issues

```
Debug Cloud Run service issues:
- Service: {service_name}
- Region: {region}
- Issue type: {cold_start/errors/latency/scaling}
- Error messages: {error_messages}

Provide:
1. Relevant log queries
2. Metrics to check
3. Common causes and solutions
4. gcloud commands for investigation
5. Health check verification
```

### Debug Job Failures

```
Debug Cloud Run job failures:
- Job: {job_name}
- Execution ID: {execution_id}
- Failure pattern: {all_tasks/specific_tasks/random}
- Error messages: {error_messages}

Provide:
1. Log queries for failed tasks
2. Common failure causes
3. Retry configuration review
4. Checkpointing verification
5. Resource limit analysis
```

---

## Cost Optimization

### Analyze and Reduce Costs

```
Analyze and optimize Cloud Run costs:
- Services: {service_list}
- Current monthly cost: {cost}
- Traffic pattern: {pattern} (e.g., spiky, steady, off-hours low)

Provide:
1. Cost analysis queries
2. Optimization recommendations
3. Min/max instance tuning
4. Concurrency optimization
5. Billing mode selection (request-based vs instance-based)
6. Committed use discount analysis
```

---

## Migration

### Migrate from Cloud Functions

```
Migrate Cloud Function to Cloud Run:
- Function name: {function_name}
- Runtime: {runtime}
- Trigger type: {http/pubsub/storage/scheduler}
- Memory: {memory}

Provide:
1. Dockerfile for containerization
2. Code modifications needed
3. Cloud Run service configuration
4. Trigger migration (Eventarc if needed)
5. Testing and validation steps
```

### Migrate from GKE

```
Migrate GKE workload to Cloud Run:
- Workload type: {deployment/job}
- Current resource limits: {cpu}/{memory}
- Dependencies: {dependencies}
- Stateful: {yes/no}

Provide:
1. Cloud Run suitability assessment
2. Configuration mapping (K8s to Cloud Run)
3. Networking considerations
4. Service mesh implications
5. Migration steps
6. Rollback plan
```
