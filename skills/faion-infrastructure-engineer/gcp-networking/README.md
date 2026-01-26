# GCP Networking

> **Entry Point:** Invoked via [faion-infrastructure-engineer](../CLAUDE.md)

## Overview

Comprehensive reference for Google Cloud Platform networking: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices.

**Focus Areas:** VPC, subnets, firewall rules, Cloud NAT, load balancing

## Key Concepts

### GCP VPC Characteristics

| Feature | GCP Behavior | AWS/Azure Comparison |
|---------|--------------|----------------------|
| VPC Scope | **Global** | Regional |
| Subnets | Regional | Zonal/Regional |
| Firewall | VPC-level | Subnet-level |
| IP Ranges | Flexible expansion | Fixed at creation |

### VPC Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Auto** | Auto-creates subnets in all regions | Quick prototyping |
| **Custom** | Manual subnet creation | Production workloads |

**Best Practice:** Always use **custom mode** for production environments.

### Network Hierarchy

```
Organization
└── Folder (optional)
    └── Project
        └── VPC Network (global)
            ├── Subnet (regional) → us-central1
            ├── Subnet (regional) → europe-west1
            └── Subnet (regional) → asia-east1
```

## Quick Reference

### VPC Operations

```bash
# Create custom VPC
gcloud compute networks create my-vpc --subnet-mode=custom

# Create subnet with secondary ranges (GKE)
gcloud compute networks subnets create my-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.0.0/24 \
    --secondary-range=pods=10.1.0.0/16,services=10.2.0.0/20

# Enable Private Google Access
gcloud compute networks subnets update my-subnet \
    --region=us-central1 \
    --enable-private-ip-google-access

# Enable VPC Flow Logs
gcloud compute networks subnets update my-subnet \
    --region=us-central1 \
    --enable-flow-logs \
    --logging-aggregation-interval=interval-5-sec \
    --logging-flow-sampling=0.5
```

### Firewall Rules

```bash
# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --allow=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8 \
    --priority=1000

# Allow SSH with service account
gcloud compute firewall-rules create allow-ssh-sa \
    --network=my-vpc \
    --allow=tcp:22 \
    --source-ranges=35.235.240.0/20 \
    --target-service-accounts=my-sa@project.iam.gserviceaccount.com

# Deny all egress (then allow specific)
gcloud compute firewall-rules create deny-all-egress \
    --network=my-vpc \
    --direction=EGRESS \
    --action=DENY \
    --rules=all \
    --priority=65534
```

### Cloud NAT

```bash
# Create router
gcloud compute routers create nat-router \
    --network=my-vpc \
    --region=us-central1

# Create Cloud NAT
gcloud compute routers nats create my-nat \
    --router=nat-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
```

### Load Balancing

```bash
# Create health check
gcloud compute health-checks create http my-hc --port=80

# Create backend service
gcloud compute backend-services create my-backend \
    --protocol=HTTP \
    --health-checks=my-hc \
    --global

# Create URL map and forwarding rule
gcloud compute url-maps create my-url-map --default-service=my-backend
gcloud compute target-http-proxies create my-proxy --url-map=my-url-map
gcloud compute forwarding-rules create my-lb \
    --global --target-http-proxy=my-proxy --ports=80
```

## Best Practices Summary

| Category | Recommendation |
|----------|----------------|
| VPC Mode | Use custom mode, not auto |
| Default VPC | Delete or don't use default VPC |
| Legacy Networks | Never use legacy networks |
| Firewall | Service account filtering over network tags |
| IP Ranges | Plan ahead, use RFC 1918 |
| Logging | Enable VPC Flow Logs and firewall logging |
| Private Access | Enable Private Google Access |
| Egress | Use Cloud NAT for private instances |
| Security | VPC Service Controls for sensitive data |
| DDoS | Cloud Armor at load balancer edge |

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Real-world configurations |
| [templates.md](templates.md) | Terraform/gcloud templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI assistance |

## Sources

- [Best practices for VPC design](https://docs.cloud.google.com/architecture/best-practices-vpc-design)
- [GCP Security Best Practices](https://fidelissecurity.com/cybersecurity-101/best-practices/google-cloud-platform-gcp-security/)
- [GCP Networking Best Practices](https://quabyt.com/blog/gcp-networking-best-practices)
- [VPC Design Considerations](https://medium.com/@pbijjala/vpc-design-considerations-for-google-cloud-71ce67427256)
- [GCP VPC Best Practices](https://www.trendmicro.com/cloudoneconformity/knowledge-base/gcp/CloudVPC/)
- [VPC Release Notes](https://docs.cloud.google.com/vpc/docs/release-notes)

---

*GCP Networking Reference | faion-infrastructure-engineer*
