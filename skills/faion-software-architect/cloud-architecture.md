# Cloud Architecture

Best practices for designing cloud-native applications.

## Cloud Design Principles

1. **Design for failure** - Assume things will fail
2. **Decouple components** - Loose coupling, async
3. **Implement elasticity** - Scale up and down
4. **Think parallel** - Horizontal over vertical
5. **Keep data close** - Minimize latency

## Well-Architected Framework

### Pillars

| Pillar | Focus |
|--------|-------|
| Operational Excellence | Run and monitor systems |
| Security | Protect data and systems |
| Reliability | Recover from failures |
| Performance | Use resources efficiently |
| Cost Optimization | Avoid unnecessary costs |
| Sustainability | Minimize environmental impact |

## Common Patterns

### Three-Tier Architecture

```
┌─────────────────────────────────────────┐
│            Presentation Tier             │
│         (Load Balancer + Web)            │
├─────────────────────────────────────────┤
│            Application Tier              │
│           (Auto-scaling Group)           │
├─────────────────────────────────────────┤
│              Data Tier                   │
│     (Database + Cache + Storage)         │
└─────────────────────────────────────────┘
```

### Serverless

```
API Gateway ─▶ Lambda ─▶ DynamoDB
                 │
                 ▼
              S3 (files)
```

### Microservices on Kubernetes

```
┌─────────────────────────────────────────┐
│            Kubernetes Cluster            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │Service A│  │Service B│  │Service C│  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │       │
│  ┌────┴────────────┴────────────┴────┐  │
│  │         Service Mesh (Istio)       │  │
│  └────────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Multi-Region Architecture

```
                    Global Load Balancer
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
      ┌────────┐      ┌────────┐      ┌────────┐
      │Region A│      │Region B│      │Region C│
      │(Primary)│      │(Secondary)    │(Secondary)
      └────┬───┘      └────┬───┘      └────┬───┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    Database Replication
```

**Strategies:**
- **Active-Passive:** One primary, others standby
- **Active-Active:** All serve traffic, sync data

## Networking

### VPC Design

```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Load Balancer
│   ├── NAT Gateway
│   └── Bastion Host
├── Private Subnet (10.0.2.0/24)
│   └── Application Servers
└── Database Subnet (10.0.3.0/24)
    └── RDS, ElastiCache
```

### Security Groups

```
Internet ─▶ ALB (443) ─▶ App (8080) ─▶ DB (5432)
            │             │              │
            public        private        private
            sg-web        sg-app         sg-db
```

## Storage Options

| Service | Use Case |
|---------|----------|
| S3 / Cloud Storage | Objects, backups, static files |
| EBS / Persistent Disk | Block storage for VMs |
| EFS / Filestore | Shared file system |
| RDS / Cloud SQL | Managed relational DB |
| DynamoDB / Firestore | NoSQL, serverless |
| ElastiCache / Memorystore | In-memory cache |

## Cost Optimization

### Right-sizing
- Monitor utilization
- Use appropriate instance types
- Resize under-utilized resources

### Reserved / Committed Use
- 1-3 year commitments
- 30-70% savings
- Use for stable workloads

### Spot / Preemptible
- 60-90% savings
- For fault-tolerant workloads
- Batch processing, CI/CD

### Auto-scaling
```yaml
# Scale based on CPU
minReplicas: 2
maxReplicas: 10
targetCPUUtilization: 70%
```

## Security Best Practices

1. **Least privilege** - Minimal permissions
2. **Encryption** - At rest and in transit
3. **Network isolation** - VPCs, security groups
4. **Secrets management** - Vault, Secrets Manager
5. **Audit logging** - CloudTrail, audit logs
6. **Regular updates** - Patch vulnerabilities

## Disaster Recovery

| Strategy | RTO | RPO | Cost |
|----------|-----|-----|------|
| Backup & Restore | Hours | Hours | Low |
| Pilot Light | Minutes | Minutes | Medium |
| Warm Standby | Seconds | Seconds | High |
| Active-Active | Zero | Zero | Highest |

**RTO:** Recovery Time Objective (downtime)
**RPO:** Recovery Point Objective (data loss)

## Related

- [container-orchestration.md](container-orchestration.md) - Kubernetes
- [serverless-architecture.md](serverless-architecture.md) - Serverless
- [reliability-architecture.md](reliability-architecture.md) - Reliability
