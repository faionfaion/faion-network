# AWS EC2 & ECS LLM Prompts

Structured prompts for LLM-assisted AWS infrastructure tasks.

## Task Definition Generation

### Generate ECS Task Definition

```
Generate an ECS Fargate task definition with:

Application: {app_name}
Image: {ecr_repo}:{tag}
Port: {port}
CPU: {cpu_units} (256, 512, 1024, 2048, 4096)
Memory: {memory_mb}
Environment: {env} (development, staging, production)

Requirements:
- {requirement_1}
- {requirement_2}
- {requirement_3}

Secrets needed:
- {secret_1} (source: Secrets Manager / Parameter Store)
- {secret_2}

AWS Account: {account_id}
Region: {region}

Include:
- Health check configuration
- CloudWatch Logs setup
- Security hardening (non-root user, read-only filesystem)
- Proper IAM role references
```

### Multi-Container Task

```
Generate an ECS task definition with multiple containers:

Main container:
- Name: {main_name}
- Image: {main_image}
- Port: {main_port}
- Role: {main_role}

Sidecar containers:
1. Name: {sidecar_1_name}
   Image: {sidecar_1_image}
   Purpose: {sidecar_1_purpose}

2. Name: {sidecar_2_name}
   Image: {sidecar_2_image}
   Purpose: {sidecar_2_purpose}

Container dependencies:
- {dependency_1}
- {dependency_2}

Total resources:
- CPU: {total_cpu}
- Memory: {total_memory}

Include container-level resource limits.
```

---

## Service Configuration

### Create ECS Service

```
Create an ECS Fargate service configuration:

Cluster: {cluster_name}
Service name: {service_name}
Task definition: {task_family}:{revision}

Deployment:
- Desired count: {count}
- Min healthy: {min_percent}%
- Max percent: {max_percent}%
- Enable circuit breaker with rollback

Network:
- VPC: {vpc_id}
- Subnets: {subnet_ids} (private)
- Security groups: {sg_ids}

Load balancer:
- Type: {alb/nlb}
- Target group ARN: {tg_arn}
- Health check grace period: {seconds}

Auto scaling:
- Min: {min_tasks}
- Max: {max_tasks}
- Target CPU: {cpu_percent}%
- Scale out cooldown: {scale_out_seconds}s
- Scale in cooldown: {scale_in_seconds}s
```

---

## EC2 Configuration

### Launch EC2 Instance

```
Generate AWS CLI command to launch EC2 instance:

Purpose: {purpose}
Instance type: {type} (prefer Graviton if compatible)
AMI: {ami_id or "latest Amazon Linux 2023"}

Network:
- VPC: {vpc_id}
- Subnet: {subnet_id}
- Security groups: {sg_ids}
- Public IP: {yes/no}

Storage:
- Root volume: {size}GB {type}
- Additional volumes: {volumes}

IAM:
- Instance profile: {profile_name}

Tags:
- Name: {name}
- Environment: {env}
- Project: {project}
- Owner: {owner}

User data script to:
- {action_1}
- {action_2}
- {action_3}
```

### Security Group Rules

```
Generate security group configuration for:

Application type: {type}
Environment: {env}

Inbound rules needed:
- {source_1} -> port {port_1} ({protocol_1})
- {source_2} -> port {port_2} ({protocol_2})

Outbound rules:
- {destination_1} -> port {port_1}
- {destination_2} -> port {port_2}

Reference other security groups:
- {sg_1} for {purpose_1}
- {sg_2} for {purpose_2}

Follow least-privilege principle.
```

---

## Troubleshooting

### Debug ECS Task Failures

```
ECS task is failing to start. Analyze and provide solutions:

Cluster: {cluster}
Service: {service}
Task definition: {task_def}

Error message:
{error_message}

Stopped reason:
{stopped_reason}

Recent events:
{events}

Check:
1. Task definition configuration
2. IAM permissions (execution role, task role)
3. Network configuration (subnets, security groups, VPC endpoints)
4. Container health checks
5. Resource limits (CPU, memory)
6. Secrets/parameters access
7. ECR image pull permissions
8. CloudWatch Logs permissions
```

### Debug EC2 Connectivity

```
EC2 instance not accessible. Diagnose:

Instance ID: {instance_id}
Connection method: {ssh/ssm/http}
Error: {error}

Instance state:
- Status checks: {checks}
- Public IP: {public_ip}
- Private IP: {private_ip}

Network:
- VPC: {vpc_id}
- Subnet: {subnet_id} ({public/private})
- Security groups: {sg_ids}
- Route table: {rt_id}

Provide diagnostic commands and potential fixes.
```

---

## Cost Optimization

### Analyze ECS Costs

```
Analyze and optimize ECS costs:

Current setup:
- Cluster: {cluster}
- Services: {service_count}
- Average running tasks: {task_count}

Task configurations:
{task_configs}

Traffic patterns:
- Peak hours: {peak}
- Off-peak hours: {offpeak}
- Weekend traffic: {weekend}

Current monthly cost: ${cost}

Provide recommendations for:
1. Right-sizing task definitions
2. Fargate Spot usage opportunities
3. Auto-scaling optimization
4. Reserved capacity options
5. Bin-packing improvements (if EC2 launch type)
```

### EC2 Instance Optimization

```
Optimize EC2 instance selection:

Workload characteristics:
- CPU usage pattern: {pattern}
- Memory requirements: {memory}
- Network I/O: {network}
- Storage I/O: {storage}
- GPU requirements: {gpu}

Current instance: {current_type}
Current monthly cost: ${cost}

Constraints:
- {constraint_1}
- {constraint_2}

Recommend:
1. Instance type alternatives
2. Graviton migration benefits
3. Spot instance suitability
4. Reserved/Savings Plans options
```

---

## Migration

### Migrate to ECS Fargate

```
Plan migration from {source} to ECS Fargate:

Source: {ec2/kubernetes/docker-compose/on-prem}

Current architecture:
{architecture_description}

Services to migrate:
1. {service_1}: {description_1}
2. {service_2}: {description_2}
3. {service_3}: {description_3}

Dependencies:
- Databases: {databases}
- Caches: {caches}
- Queues: {queues}
- External services: {external}

Requirements:
- Zero-downtime migration: {yes/no}
- Data migration: {requirements}
- Timeline: {timeline}

Provide:
1. Migration phases
2. Task definitions for each service
3. Network architecture
4. Rollback strategy
5. Testing plan
```

---

## Infrastructure as Code

### Generate Terraform Module

```
Generate Terraform module for ECS service:

Module purpose: {purpose}

Inputs:
- {input_1}: {type} - {description}
- {input_2}: {type} - {description}
- {input_3}: {type} - {description}

Resources to create:
- ECS service
- Task definition
- Auto-scaling configuration
- CloudWatch alarms
- IAM roles

Outputs:
- {output_1}
- {output_2}

Follow:
- AWS best practices
- Security hardening
- Cost optimization defaults
- Proper tagging
```

### Generate CloudFormation Template

```
Generate CloudFormation template for:

Resources:
- {resource_1}
- {resource_2}
- {resource_3}

Parameters:
- {param_1}: {type} - {default}
- {param_2}: {type} - {default}

Conditions:
- {condition_1}

Outputs:
- {output_1}
- {output_2}

Include:
- Resource dependencies
- DeletionPolicy where appropriate
- UpdateReplacePolicy
- Proper tagging
```

---

## Security Audit

### ECS Security Review

```
Review ECS configuration for security:

Task definition:
{task_definition_json}

Service configuration:
{service_config}

Network:
- VPC: {vpc_id}
- Subnets: {subnets}
- Security groups: {sg_config}

Check for:
1. IAM least-privilege violations
2. Network exposure risks
3. Container hardening gaps
4. Secrets management issues
5. Logging/monitoring gaps
6. Image security concerns

Provide:
- Risk assessment
- Remediation steps
- Priority ranking
```

---

*AWS EC2 & ECS LLM Prompts | faion-infrastructure-engineer*
