# Cloud Architecture Examples

Real-world cloud architecture examples across different scales, industries, and cloud providers.

## Example 1: E-Commerce Platform (AWS)

### Overview

**Scale:** 100K daily active users, 10K peak concurrent, 5M product catalog
**Requirements:** High availability, PCI-DSS compliance, global reach
**Budget:** $50-80K/month

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CloudFront (CDN)                               │
│                     Static assets, edge caching                          │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│                           Route 53                                       │
│                    DNS, health checks, failover                          │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│   us-east-1    │    │   eu-west-1    │    │ ap-southeast-1 │
│   (Primary)    │    │   (Secondary)  │    │   (Secondary)  │
└───────┬────────┘    └───────┬────────┘    └───────┬────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────────────────────────────────────────────────────────────┐
│                      Application Load Balancer                         │
│                        WAF, SSL termination                            │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────────┐
│                           EKS Cluster                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Frontend   │  │   API       │  │  Catalog    │  │   Orders    │  │
│  │  (React)    │  │  Gateway    │  │  Service    │  │  Service    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Cart      │  │  Payment    │  │  Inventory  │  │Notification │  │
│  │  Service    │  │  Service    │  │  Service    │  │  Service    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│                       Istio Service Mesh                               │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐       ┌───────────────┐
│  Aurora       │      │  ElastiCache  │       │  OpenSearch   │
│  PostgreSQL   │      │  (Redis)      │       │  (Search)     │
│  Multi-AZ     │      │  Cluster      │       │  Cluster      │
└───────────────┘      └───────────────┘       └───────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    S3 (Product images, backups)                        │
│                    Versioning, lifecycle policies                      │
└───────────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| EKS over ECS | Team Kubernetes expertise, portability |
| Aurora PostgreSQL | PCI compliance, automatic failover |
| ElastiCache Redis | Session storage, cart caching |
| Multi-region active-passive | Lower cost than active-active, <1min RTO |
| Istio service mesh | mTLS between services for PCI |

### Cost Breakdown

| Component | Monthly Cost |
|-----------|-------------|
| EKS (3 clusters) | $15,000 |
| Aurora (Multi-AZ) | $8,000 |
| ElastiCache | $3,000 |
| CloudFront | $5,000 |
| ALB + WAF | $2,000 |
| S3 + data transfer | $4,000 |
| OpenSearch | $6,000 |
| Monitoring | $2,000 |
| **Total** | **$45,000** |

### Lessons Learned

- Start with single region, add regions based on latency data
- Use Aurora Serverless v2 for dev/staging (70% savings)
- Implement circuit breakers early for payment service
- Cache product catalog aggressively (95% hit rate)

---

## Example 2: SaaS Analytics Platform (GCP)

### Overview

**Scale:** 500 enterprise customers, 50TB daily data ingestion
**Requirements:** Real-time analytics, data isolation, SOC2 compliance
**Budget:** $100-150K/month

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Cloud Load Balancing                             │
│                    Global anycast, SSL, Cloud Armor                      │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│                           GKE Autopilot                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Web UI    │  │  API        │  │  Ingestion  │  │   Query     │    │
│  │  (Next.js)  │  │  Gateway    │  │  Service    │  │   Engine    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐       ┌───────────────┐
│   Pub/Sub     │      │   Dataflow    │       │   BigQuery    │
│  (Ingestion)  │      │  (Processing) │       │  (Analytics)  │
│   500K msg/s  │      │  Streaming    │       │  Per-tenant   │
└───────────────┘      └───────────────┘       └───────────────┘
                                                       │
                                                       ▼
                                               ┌───────────────┐
                                               │    Looker     │
                                               │  (Embedded)   │
                                               └───────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        Supporting Services                               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │
│  │  Cloud SQL    │  │  Memorystore  │  │  Secret       │                │
│  │  (Metadata)   │  │  (Redis)      │  │  Manager      │                │
│  └───────────────┘  └───────────────┘  └───────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Multi-Tenancy Strategy

```
BigQuery Organization
├── Project: analytics-platform-prod
│   ├── Dataset: shared_reference  (shared lookup tables)
│   ├── Dataset: platform_metrics  (internal analytics)
│   │
│   ├── Dataset: tenant_abc123     (Customer A data)
│   │   ├── View: events           (row-level security)
│   │   ├── View: aggregations
│   │   └── Table: raw_events      (no direct access)
│   │
│   ├── Dataset: tenant_def456     (Customer B data)
│   │   └── ...
│   │
│   └── Dataset: tenant_ghi789     (Customer C data)
│       └── ...
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| GKE Autopilot | Focus on apps, not node management |
| BigQuery multi-tenant | Cost efficiency, shared compute |
| Dataflow (Apache Beam) | Unified batch/stream processing |
| Per-tenant datasets | Data isolation, compliance |
| Pub/Sub dead letter | Prevent data loss on failures |

### Cost Optimization

| Strategy | Savings |
|----------|---------|
| BigQuery flex slots | 50% vs on-demand for predictable queries |
| Committed use discounts | 37% on GKE nodes |
| Sustained use | Automatic 30% discount |
| Storage tiering | 60% on cold data |
| Preemptible for batch | 80% on Dataflow batch jobs |

---

## Example 3: FinTech Payment Gateway (Multi-Cloud)

### Overview

**Scale:** 10K TPS, 99.99% availability requirement
**Requirements:** PCI-DSS Level 1, multi-region DR, <100ms latency
**Providers:** Primary on AWS, DR on Azure

### Architecture Diagram

```
                              ┌─────────────────────┐
                              │   Cloudflare        │
                              │   (DNS + WAF)       │
                              └──────────┬──────────┘
                                         │
                   ┌─────────────────────┼─────────────────────┐
                   │                     │                     │
                   ▼                     │                     ▼
        ┌───────────────────┐            │          ┌───────────────────┐
        │      AWS          │            │          │      Azure        │
        │   (Primary)       │            │          │      (DR)         │
        └────────┬──────────┘            │          └────────┬──────────┘
                 │                       │                   │
┌────────────────▼───────────────────────│───────────────────▼───────────┐
│                AWS us-east-1           │         Azure East US          │
│  ┌─────────────────────────────────┐   │   ┌─────────────────────────┐  │
│  │     Network Load Balancer       │   │   │   Azure Load Balancer   │  │
│  └──────────────┬──────────────────┘   │   └───────────┬─────────────┘  │
│                 │                      │               │                │
│  ┌──────────────▼──────────────────┐   │   ┌───────────▼─────────────┐  │
│  │          EKS Cluster            │   │   │       AKS Cluster       │  │
│  │  ┌─────────┐  ┌─────────┐      │   │   │  ┌─────────┐           │  │
│  │  │Payment  │  │Fraud    │      │◄──┼───│  │Payment  │           │  │
│  │  │Processor│  │Detection│      │   │   │  │Processor│ (warm)    │  │
│  │  └─────────┘  └─────────┘      │   │   │  └─────────┘           │  │
│  │  ┌─────────┐  ┌─────────┐      │   │   └─────────────────────────┘  │
│  │  │Ledger   │  │Reporting│      │   │                                │
│  │  │Service  │  │Service  │      │   │   ┌───────────────────────────┐│
│  │  └─────────┘  └─────────┘      │   │   │   Azure SQL               ││
│  └────────────────────────────────┘   │   │   (Read Replica)          ││
│                                       │   └───────────────────────────┘│
│  ┌────────────────────────────────┐   │                                │
│  │      Aurora PostgreSQL         │───┼──► Cross-region replication   │
│  │      (Multi-AZ, encrypted)     │   │                                │
│  └────────────────────────────────┘   │                                │
│                                       │                                │
│  ┌────────────────────────────────┐   │                                │
│  │      HSM (CloudHSM)            │   │   ┌───────────────────────────┐│
│  │      (Key Management)          │   │   │   Azure Key Vault          ││
│  └────────────────────────────────┘   │   │   (HSM-backed)             ││
│                                       │   └───────────────────────────┘│
└───────────────────────────────────────┴────────────────────────────────┘
                                        │
                              ┌─────────▼──────────┐
                              │  AWS Direct Connect │
                              │  Azure ExpressRoute │
                              │  (Cross-cloud link) │
                              └────────────────────┘
```

### Compliance Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PCI-DSS Compliance Zones                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────┐  ┌─────────────────────────────────┐ │
│  │    CDE (Cardholder Data  │  │    Non-CDE                       │ │
│  │         Environment)     │  │    (All other systems)           │ │
│  │                          │  │                                   │ │
│  │  - Payment Processor     │  │  - Public Website                │ │
│  │  - HSM                   │  │  - Marketing                     │ │
│  │  - Tokenization Service  │  │  - Analytics                     │ │
│  │  - Card Vault            │  │  - Admin Portal                  │ │
│  │                          │  │                                   │ │
│  │  Isolated VPC            │  │  Separate VPC                    │ │
│  │  No internet egress      │  │  Standard egress                 │ │
│  │  HSM key management      │  │  KMS encryption                  │ │
│  │  Full audit logging      │  │  Standard logging                │ │
│  └──────────────────────────┘  └─────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Multi-cloud DR | Avoid single vendor failure, regulatory requirement |
| CloudHSM | PCI-DSS key management, FIPS 140-2 Level 3 |
| NLB over ALB | Lower latency for payment traffic |
| Kubernetes | Consistent deployment across clouds |
| Tokenization | Minimize CDE scope |

### Disaster Recovery

| Component | RPO | RTO | Strategy |
|-----------|-----|-----|----------|
| Payment processing | 0 | <5 min | Active-passive with automatic failover |
| Transaction database | <1 sec | <2 min | Synchronous replication |
| Card vault | 0 | <5 min | HSM cluster failover |
| Reporting | 5 min | 15 min | Async replication |

---

## Example 4: AI/ML Platform (AWS + GCP)

### Overview

**Scale:** 100+ ML models in production, 1PB training data
**Requirements:** GPU training, real-time inference, model versioning
**Budget:** $200-300K/month

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Development Environment                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │  JupyterHub   │  │   VS Code     │  │  SageMaker    │               │
│  │  (EKS)        │  │   Remote      │  │  Studio       │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
└───────────────────────────────────────┬─────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────┐
│                         Training Pipeline                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │   Kubeflow    │  │  Vertex AI    │  │   MLflow      │               │
│  │   Pipelines   │  │  Pipelines    │  │  Tracking     │               │
│  └───────┬───────┘  └───────┬───────┘  └───────────────┘               │
│          │                  │                                           │
│  ┌───────▼───────┐  ┌───────▼───────┐                                  │
│  │  AWS p5       │  │  GCP A3       │  GPU Clusters                    │
│  │  (H100)       │  │  (H100)       │  Spot/Preemptible               │
│  └───────────────┘  └───────────────┘                                  │
└───────────────────────────────────────┬─────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────┐
│                          Model Registry                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        MLflow / SageMaker Model Registry         │   │
│  │  - Model versioning                                              │   │
│  │  - Artifact storage (S3)                                         │   │
│  │  - Lineage tracking                                              │   │
│  │  - Approval workflows                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────┬─────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────┐
│                         Inference Platform                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  Real-time      │  │  Batch          │  │  Streaming      │         │
│  │  (SageMaker)    │  │  (EMR Spark)    │  │  (Flink)        │         │
│  │                 │  │                 │  │                 │         │
│  │  - Auto-scaling │  │  - S3 I/O       │  │  - Kinesis      │         │
│  │  - A/B testing  │  │  - Spot fleet   │  │  - Low latency  │         │
│  │  - Shadow mode  │  │  - Scheduled    │  │  - Continuous   │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
└───────────────────────────────────────┬─────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────────────┐
│                          Data Platform                                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │   S3 Data     │  │   BigQuery    │  │   Feature     │               │
│  │   Lake        │  │  (Analytics)  │  │   Store       │               │
│  │               │  │               │  │  (Feast)      │               │
│  │  - Raw        │  │  - BI queries │  │               │               │
│  │  - Processed  │  │  - Ad-hoc     │  │  - Online     │               │
│  │  - Features   │  │  - Dashboards │  │  - Offline    │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
```

### MLOps Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Code   │───▶│  Build  │───▶│  Test   │───▶│ Register│───▶│ Deploy  │
│  Commit │    │  Image  │    │  Model  │    │  Model  │    │  to Prod│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │  Quality    │
                            │  Gates      │
                            │             │
                            │ - Accuracy  │
                            │ - Latency   │
                            │ - Fairness  │
                            │ - Drift     │
                            └─────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Hybrid AWS + GCP | Use TPUs for specific models, H100 availability |
| Kubeflow | Portable pipelines across clouds |
| Feature Store | Consistency between training and serving |
| MLflow | Open-source, vendor-neutral tracking |
| Spot/Preemptible for training | 70% cost savings, checkpointing handles interrupts |

### Cost Optimization

| Component | Strategy | Savings |
|-----------|----------|---------|
| Training compute | Spot instances + checkpointing | 70% |
| Inference | Right-sized instances + auto-scaling | 40% |
| Storage | S3 Intelligent Tiering | 30% |
| Data transfer | Same-region processing | 50% |
| Development | Scheduled notebooks | 60% |

---

## Example 5: IoT Platform (AWS)

### Overview

**Scale:** 10M devices, 1M messages/second
**Requirements:** Edge processing, real-time alerts, 5-year data retention
**Budget:** $80-120K/month

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Edge Layer                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │  Greengrass   │  │  Greengrass   │  │  Greengrass   │  ... 1000+   │
│  │  Core Device  │  │  Core Device  │  │  Core Device  │               │
│  │               │  │               │  │               │               │
│  │  - Local ML   │  │  - Local ML   │  │  - Local ML   │               │
│  │  - Filtering  │  │  - Filtering  │  │  - Filtering  │               │
│  │  - Aggregation│  │  - Aggregation│  │  - Aggregation│               │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘               │
│          │                  │                  │                        │
│          └──────────────────┼──────────────────┘                        │
│                             │ (10K sensors each)                        │
└─────────────────────────────┼───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           IoT Core                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    MQTT Broker (IoT Core)                        │   │
│  │  - Device authentication (X.509)                                 │   │
│  │  - Topic routing                                                 │   │
│  │  - Message transformation                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐       ┌───────────────┐
│   Kinesis     │      │   IoT Rules   │       │    Lambda     │
│   Firehose    │      │   Engine      │       │  (Real-time)  │
│               │      │               │       │               │
│  - Batching   │      │  - Routing    │       │  - Alerts     │
│  - S3 delivery│      │  - Transform  │       │  - Actions    │
└───────┬───────┘      └───────┬───────┘       └───────┬───────┘
        │                      │                       │
        ▼                      ▼                       ▼
┌───────────────┐      ┌───────────────┐       ┌───────────────┐
│   S3 Data     │      │   DynamoDB    │       │     SNS       │
│   Lake        │      │  (Device State)│      │  (Alerts)     │
│               │      │               │       │               │
│  - Raw data   │      │  - Latest state│      │  - SMS        │
│  - Parquet    │      │  - Metadata   │       │  - Email      │
│  - Partitioned│      │               │       │  - Webhook    │
└───────┬───────┘      └───────────────┘       └───────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                        Analytics Layer                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐             │
│  │   Athena      │  │   Timestream  │  │   QuickSight  │             │
│  │  (Ad-hoc)     │  │  (Time-series)│  │  (Dashboards) │             │
│  └───────────────┘  └───────────────┘  └───────────────┘             │
└───────────────────────────────────────────────────────────────────────┘
```

### Device Management

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Device Lifecycle                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│  │Provision│───▶│ Active  │───▶│ Update  │───▶│ Retire  │          │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
│       │              │              │                               │
│       ▼              ▼              ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    IoT Device Defender                       │   │
│  │  - Anomaly detection                                         │   │
│  │  - Security audit                                            │   │
│  │  - Compliance monitoring                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Greengrass at edge | Reduce bandwidth, local processing, offline support |
| X.509 certificates | Secure device identity, no passwords |
| Kinesis Firehose | Managed batching, compression, delivery |
| Timestream | Native time-series, automatic tiering |
| DynamoDB single-table | Device state with sub-ms latency |

### Storage Tiering

| Tier | Retention | Storage | Query Cost |
|------|-----------|---------|------------|
| Hot (Timestream memory) | 7 days | $0.50/GB/hr | Fast |
| Warm (Timestream magnetic) | 90 days | $0.03/GB/mo | Medium |
| Cold (S3 Standard) | 1 year | $0.023/GB/mo | Athena |
| Archive (S3 Glacier) | 5 years | $0.004/GB/mo | Slow |

---

## Example 6: Startup MVP (Serverless)

### Overview

**Scale:** 1K users, growing to 100K
**Requirements:** Minimal ops, fast iteration, low cost
**Budget:** <$500/month initially

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Vercel (Frontend)                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Next.js Application                           │   │
│  │  - SSR/SSG pages                                                 │   │
│  │  - API routes (for simple operations)                            │   │
│  │  - Edge functions (geo-routing)                                  │   │
│  └───────────────────────────────┬─────────────────────────────────┘   │
└───────────────────────────────────┼─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          AWS (Backend)                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      API Gateway                                 │   │
│  │  - REST API                                                      │   │
│  │  - CORS configuration                                            │   │
│  │  - Rate limiting                                                 │   │
│  └───────────────────────────────┬─────────────────────────────────┘   │
│                                  │                                      │
│          ┌───────────────────────┼───────────────────────┐             │
│          │                       │                       │             │
│          ▼                       ▼                       ▼             │
│  ┌───────────────┐      ┌───────────────┐       ┌───────────────┐     │
│  │   Lambda      │      │   Lambda      │       │   Lambda      │     │
│  │  (Users)      │      │  (Products)   │       │  (Orders)     │     │
│  └───────┬───────┘      └───────┬───────┘       └───────┬───────┘     │
│          │                      │                       │              │
│          └──────────────────────┼───────────────────────┘              │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        DynamoDB                                  │   │
│  │  - Single table design                                           │   │
│  │  - On-demand capacity                                            │   │
│  │  - Global secondary indexes                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐              │
│  │   S3          │  │   SES         │  │   Cognito     │              │
│  │  (Uploads)    │  │  (Email)      │  │  (Auth)       │              │
│  └───────────────┘  └───────────────┘  └───────────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cost at Scale

| Scale | Monthly Cost | Notes |
|-------|-------------|-------|
| 1K users | $50-100 | Free tier covers most |
| 10K users | $200-400 | DynamoDB on-demand |
| 50K users | $800-1,500 | Consider provisioned capacity |
| 100K users | $2,000-4,000 | Time to evaluate architecture |

### Evolution Path

```
Phase 1: MVP (Serverless)
├── Lambda + API Gateway
├── DynamoDB single-table
└── Vercel frontend

Phase 2: Growth (100K+ users)
├── Add ElastiCache for hot data
├── Aurora Serverless for complex queries
└── CloudFront for global distribution

Phase 3: Scale (1M+ users)
├── EKS for compute flexibility
├── Event-driven architecture
└── Multi-region deployment
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Vercel + AWS | Best of both: Vercel DX, AWS services |
| DynamoDB on-demand | Pay per request, no capacity planning |
| Single Lambda per route | Simple, easy to debug |
| Cognito | Managed auth, social login support |
| No VPC for Lambda | Faster cold starts, simpler networking |

---

## Architecture Decision Summary

### When to Use Each Pattern

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| Serverless | MVPs, variable load, event-driven | Consistent high load, long processes |
| Containers (K8s) | Microservices, portability, team expertise | Small teams, simple apps |
| Three-tier | Traditional web apps, known patterns | Need for independent scaling |
| Event-driven | Loose coupling, async processing | Simple CRUD, low volume |
| Multi-cloud | Compliance, best-of-breed, DR | Complexity cost too high |

### Cloud Provider Selection

| Provider | Best For |
|----------|----------|
| AWS | Broadest services, enterprise, regulated |
| GCP | AI/ML, analytics, Kubernetes |
| Azure | Microsoft ecosystem, enterprise hybrid |
| Multi-cloud | Global reach, regulatory, risk mitigation |
