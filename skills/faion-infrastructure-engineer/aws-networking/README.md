# AWS Networking

> Comprehensive reference for VPC architecture, subnets, security groups, and Transit Gateway.

## Overview

AWS networking forms the foundation of secure, scalable cloud infrastructure. This reference covers network design patterns, security controls, and connectivity solutions following 2025/2026 best practices.

## Core Components

| Component | Purpose |
|-----------|---------|
| **VPC** | Isolated virtual network in AWS cloud |
| **Subnets** | IP address ranges within VPC (public/private) |
| **Security Groups** | Instance-level stateful firewall |
| **NACLs** | Subnet-level stateless firewall |
| **Transit Gateway** | Central hub for multi-VPC connectivity |
| **VPC Endpoints** | Private connectivity to AWS services |

## Architecture Principles

### Network Segmentation

```
VPC (10.0.0.0/16)
├── Public Subnets (10.0.0.0/20)
│   ├── AZ-a: 10.0.0.0/24   (ALB, NAT Gateway, Bastion)
│   ├── AZ-b: 10.0.1.0/24
│   └── AZ-c: 10.0.2.0/24
├── Private Subnets (10.0.16.0/20)
│   ├── AZ-a: 10.0.16.0/24  (Application tier)
│   ├── AZ-b: 10.0.17.0/24
│   └── AZ-c: 10.0.18.0/24
└── Data Subnets (10.0.32.0/20)
    ├── AZ-a: 10.0.32.0/24  (RDS, ElastiCache)
    ├── AZ-b: 10.0.33.0/24
    └── AZ-c: 10.0.34.0/24
```

### Zero-Trust Networking

1. **Minimize attack surface** - Public subnets only for ALB/API Gateway
2. **Defense in depth** - Security Groups + NACLs + WAF
3. **Least privilege** - No `0.0.0.0/0` rules, audit monthly
4. **VPC Endpoints** - Route S3/DynamoDB/Secrets Manager via AWS backbone
5. **Encryption** - TLS 1.3 in transit, KMS for data at rest

## Key Services

### VPC Lattice (2025+)

Application-layer networking service that simplifies cross-VPC and cross-account service connectivity with built-in routing, security, and observability.

### IP Address Manager (IPAM)

Central IP planning, tracking, and overlap detection across multiple accounts and regions.

### VPC Block Public Access (BPA)

Declarative policies to block internet access at subnet or VPC level, enforceable via AWS Organizations.

### Network Firewall

Layer 7 inspection with IDS/IPS capabilities for all egress paths. Blocks C2 callbacks and malicious traffic.

## Files in This Reference

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Pre-deployment verification checklist |
| [examples.md](examples.md) | CLI commands and code examples |
| [templates.md](templates.md) | Terraform and CloudFormation templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts for networking tasks |

## Quick Decisions

| Scenario | Solution |
|----------|----------|
| 2-3 VPCs, same region | VPC Peering |
| 4+ VPCs or cross-region | Transit Gateway |
| Hybrid (on-prem) connectivity | Transit Gateway + Direct Connect/VPN |
| Service-to-service mesh | VPC Lattice |
| Private AWS service access | VPC Endpoints (Gateway/Interface) |

## Best Practices Summary

1. **IP Planning** - Use IPAM, plan for growth, avoid overlaps
2. **Multi-AZ** - Deploy across 3 AZs for high availability
3. **Security Groups** - Primary defense, specific rules only
4. **NACLs** - Subnet-level guardrails, use sparingly
5. **Flow Logs** - Enable on all VPCs for visibility
6. **GuardDuty** - Threat detection across all regions


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| VPC subnet calculation | haiku | Mathematical task |
| Security group rules audit | sonnet | Access control analysis |
| Transit Gateway design | opus | Complex multi-region networking |
| Load balancer configuration | sonnet | Standard pattern application |

## Sources

- [AWS VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [Building Scalable Multi-VPC Infrastructure](https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html)
- [VPC Security Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [AWS VPC Best Practices - Trend Micro](https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/VPC/)
- [AWS VPC Design Best Practices - GeeksforGeeks](https://www.geeksforgeeks.org/devops/aws-vpc-design-best-practices/)

---

*AWS Networking Reference | faion-infrastructure-engineer*
