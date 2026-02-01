# GCP Cloud Storage

## Overview

Google Cloud Storage is a managed object storage service for storing and accessing data on Google's infrastructure. It provides unified storage across storage classes, strong consistency, and integration with Google Cloud services.

## Storage Classes

| Class | Use Case | Min Duration | Retrieval Fee |
|-------|----------|--------------|---------------|
| Standard | Frequently accessed data, hot data | None | None |
| Nearline | Accessed < 1x/month | 30 days | Per GB |
| Coldline | Accessed < 1x/quarter | 90 days | Per GB |
| Archive | Accessed < 1x/year | 365 days | Per GB |

## Key Features (2025-2026)

### Rapid Storage (New)
- Zonal bucket with <1ms random read/write latency
- 20x faster data access vs competitors
- 6 TB/s throughput
- 5x lower latency for random reads/writes

### Anywhere Cache (New)
- Strongly consistent cache for regional buckets
- Cache data within selected zones
- Seamless integration with existing buckets

### Storage Batch Operations (GA)
- Operations on billions of objects
- Serverless execution
- No infrastructure management

### Storage Insights (GA)
- Resource insights and analytics
- BigQuery export
- Storage Intelligence subscription feature

## Bucket Types

| Type | Scope | Use Case |
|------|-------|----------|
| Regional | Single region | Low latency, compute co-location |
| Dual-region | Two regions | High availability, DR |
| Multi-regional | Continent | Global distribution |

## Core Components

```
Cloud Storage
    +-- Buckets (containers)
         +-- Objects (files)
              +-- Metadata (key-value pairs)
              +-- ACLs/IAM policies
```

## Access Methods

| Method | Use Case |
|--------|----------|
| Console | Manual operations, exploration |
| gsutil/gcloud | CLI automation, scripts |
| Client libraries | Application integration |
| REST API | Custom integrations |
| Transfer Service | Large-scale migrations |

## Integration Points

| Service | Integration |
|---------|-------------|
| BigQuery | External tables, export/import |
| Vertex AI | Training data, model artifacts |
| Cloud CDN | Content delivery, caching |
| Cloud Functions | Event triggers |
| Dataflow | Stream/batch processing |
| Cloud Run | Static assets, uploads |

## Pricing Components

| Component | Description |
|-----------|-------------|
| Storage | Per GB/month by class |
| Operations | Class A (write), Class B (read) |
| Network | Egress, inter-region |
| Retrieval | Nearline/Coldline/Archive |
| Early deletion | Objects deleted before min duration |

## Quick Commands

```bash
# List buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://my-bucket \
    --location=us-central1 \
    --uniform-bucket-level-access

# Upload file
gcloud storage cp local-file.txt gs://my-bucket/

# Sync directory
gcloud storage rsync -r ./local-dir gs://my-bucket/path

# View bucket details
gcloud storage buckets describe gs://my-bucket
```

## Best Practices Summary

1. **Security**: Enable uniform bucket-level access, use CMEK for sensitive data
2. **Cost**: Implement lifecycle policies, use Autoclass for variable access
3. **Performance**: Co-locate with compute, use Rapid Storage for low latency
4. **Reliability**: Enable versioning, use dual/multi-region for availability
5. **CDN**: Integrate Cloud CDN for global content delivery

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples and patterns |
| [templates.md](templates.md) | Terraform/gcloud templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI assistance |


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Cloud Storage bucket setup | haiku | Basic configuration |
| Lifecycle rule configuration | haiku | Policy application |
| CMEK encryption strategy | sonnet | Security decisions |

## Sources

- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Storage Best Practices](https://docs.cloud.google.com/storage/docs/best-practices)
- [Cloud CDN Integration](https://cloud.google.com/cdn/docs/setting-up-cdn-with-bucket)
- [CMEK Documentation](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys)
- [Lifecycle Management](https://docs.cloud.google.com/storage/docs/lifecycle)
- [Google Cloud Next 2025](https://cloud.google.com/blog/topics/google-cloud-next/google-cloud-next-2025-wrap-up)

---

*GCP Cloud Storage Reference v2.0*
*Updated: January 2026*
