# AWS Networking

## Summary

VPC architecture, subnet segmentation, security groups, NACLs, Transit Gateway, and VPC endpoints for AWS. The concrete rule is: always deploy across 3 AZs with public/private/data subnet tiers; never use `0.0.0.0/0` in security group ingress rules except on ALB port 80/443; use VPC endpoints for S3/DynamoDB/Secrets Manager to eliminate NAT Gateway costs and keep traffic on AWS backbone.

## Why

Single-AZ deployments fail entirely during AZ outages. Overly permissive security groups (`0.0.0.0/0`) are the most common cause of data breaches in AWS. Data transfer through NAT Gateways to AWS services is expensive and unnecessary — VPC endpoints provide private connectivity at no data transfer cost.

## When To Use

- Designing a new VPC with subnet segmentation (public/private/data tiers)
- Selecting connectivity pattern: VPC Peering vs Transit Gateway vs VPC Lattice
- Auditing security group rules for least-privilege compliance
- Setting up VPC endpoints (Gateway for S3/DynamoDB, Interface for other services)
- Configuring Transit Gateway for multi-VPC or hybrid on-prem connectivity
- Enabling VPC Flow Logs and GuardDuty for network visibility

## When NOT To Use

- GCP networking (VPC, Cloud NAT, firewall rules) — use `gcp-networking`
- ALB/NLB configuration and target groups — use `aws-architecture-services`
- Route53 DNS design — not covered here; use AWS Route53 documentation directly
- Security group rules for specific services (EKS, RDS) — covered in service-specific methodologies

## Content

| File | What's inside |
|------|---------------|
| `content/01-vpc-design.xml` | 3-tier subnet architecture, CIDR planning, multi-AZ rules, Zero-Trust networking principles |
| `content/02-security-controls.xml` | Security group rules, NACL design, VPC endpoints, Flow Logs, GuardDuty integration |
| `content/03-connectivity.xml` | VPC Peering vs Transit Gateway decision, VPC Lattice, IPAM, Network Firewall patterns |

## Templates

none
