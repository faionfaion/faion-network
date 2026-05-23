<!-- purpose: Markdown skeleton for the ELK architecture spec -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens when loaded -->

# ELK Architecture Spec

- **Cluster name:** 
- **Variant:** ELK / EFK / Elastic Stack
- **Volume:** GB/day
- **Retention:** days

## Node roles

| Role | Count | Instance | Disk |
|------|-------|----------|------|
| master | 3 | r6g.large | EBS gp3 50G |
| data-hot | 3 | r6gd.2xlarge | NVMe 1.9T |
| data-warm | 2 | r6g.xlarge | EBS gp3 4T |
| coordinating | 2 | c6g.large | EBS gp3 30G |

## Tiers

- Hot: 7 days, SSD/NVMe
- Warm: 30 days, EBS gp3
- Cold: 90 days, S3 snapshot (searchable snapshot)

## Deployment

- ECK 2.x on EKS / Docker Compose 8.x
