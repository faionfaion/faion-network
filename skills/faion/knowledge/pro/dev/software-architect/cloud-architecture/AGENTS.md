# Cloud Architecture

## Summary

Best practices for designing cloud-native applications using the Well-Architected Framework (six pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, sustainability). Covers AWS/Azure/GCP selection, multi-cloud patterns, landing zone components, VPC network design, zero-trust security layers, FinOps cost strategies, and DR strategies (Backup/Restore → Pilot Light → Warm Standby → Active-Active).

## Why

Cloud architecture decisions made at design time are expensive to reverse: VPC CIDR ranges cannot be resized, IAM designs propagate across all services, and storage choices (object vs block vs file) affect performance and egress costs for years. The Well-Architected Framework provides a structured lens to surface trade-offs before implementation rather than after an incident.

## When To Use

- Designing a new cloud-native application or migrating workloads to cloud
- Choosing between AWS, Azure, and GCP based on technical and organisational constraints
- Setting up a landing zone for a new cloud environment (accounts, VPC, IAM, logging)
- Optimising cloud costs using FinOps (right-sizing, reserved instances, spot)
- Designing a DR strategy with explicit RTO/RPO targets

## When NOT To Use

- On-premise-only environments where cloud primitives do not apply
- Single-function serverless refactoring — use serverless-architecture methodology instead
- Application-level performance tuning — this covers infrastructure/architecture, not code
- When the team has no cloud budget or access — design without deployment context is premature

## Content

| File | What's inside |
|------|---------------|
| `content/01-well-architected-and-provider-selection.xml` | Six pillars summary, general design principles, AWS vs Azure vs GCP selection matrix, multi-cloud patterns and challenges |
| `content/02-network-and-security.xml` | VPC design principles, hub-and-spoke vs shared VPC topologies, subnet tiers, multi-region active-passive vs active-active, zero-trust layers, security group design |
| `content/03-finops-and-dr.xml` | FinOps three-phase cycle, cost optimisation strategies with savings ranges, tagging taxonomy, DR strategy comparison (RTO/RPO/cost), landing zone components |

## Templates

| File | Purpose |
|------|---------|
| `templates/landing-zone-vpc.tf` | Terraform module for three-tier VPC with public/app/data subnets across AZs |
| `templates/cost-tagging-policy.json` | AWS Tag Policy enforcing mandatory cost allocation tags |
