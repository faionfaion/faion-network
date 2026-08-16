# AWS Three-Tier Architecture (VPC, ALB, App, Database)

## Summary

**One-sentence:** Produces Terraform for a three-tier VPC: public ALB, private app tier (Fargate/EKS), isolated DB subnets with Aurora Serverless v2 + SG-by-reference + multi-AZ.

**One-paragraph:** The three-tier pattern places the ALB in public subnets, app workloads (Fargate / EKS) in private subnets, and Aurora Serverless v2 in isolated DB subnets. Security groups reference each other by ID (not CIDR) — self-documenting + no CIDR drift. Prod VPC spans ≥2 AZs per tier; NAT GW per AZ in prod (shared in dev). Output is a Terraform skeleton + SG matrix + VPC module call that gives you a compliant HA baseline.

**Ефективно для:**

- Нові cloud-native web apps — HA prod baseline.
- On-prem 3-tier migration → AWS, minimal arch change.
- Scalable microservices з shared relational DB.
- Compliance isolation (PCI / HIPAA) між tiers.

## Applies If (ALL must hold)

- Workload is a web app or microservice fronted by HTTP.
- Relational DB needed (Aurora Serverless v2 acceptable).
- AZ-redundancy is a hard requirement (prod SLO ≥ 99.9%).

## Skip If (ANY kills it)

- Pure serverless workload — use devops-aws-serverless-api.
- Single-AZ dev env where cost > HA — one NAT GW suffices.
- Event-driven pipeline with no persistent HTTP layer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CIDR plan | /16 VPC + subnets per tier per AZ | network team |
| Compute decision | Fargate / EKS | see devops-aws-service-selection |
| DB requirements | Aurora MySQL / Postgres + ACU range | data team |
| Domain + cert | ACM cert ARN | DNS |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[devops-aws-service-selection]] | Compute + DB picks live there |
| [[devops-aws-terraform-cicd]] | IaC delivery owned upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: multi-az-per-tier, nat-gw-per-az-prod, sg-reference-by-id, isolated-db-subnets, aurora-serverless-v2-default, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for 3-tier config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: single-az-prod, sg-by-cidr, db-internet-route, single-nat-gw-prod | 800 |
| `content/04-procedure.xml` | essential | 5 steps: VPC/subnets → ALB → app → DB → SG matrix | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on env + AZ count → topology | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-cidrs` | haiku | Mechanical /16 → /22 split per AZ. |
| `compose-tf-modules` | sonnet | Assemble terraform-aws-modules/vpc + alb + aurora calls. |
| `audit-sgs` | sonnet | SG matrix review + by-ID conversion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vpc.tf` | Terraform VPC using terraform-aws-modules/vpc with 3 tiers + 2 AZs |
| `templates/alb.tf` | Terraform ALB in public subnets with HTTPS listener |
| `templates/aurora.tf` | Terraform Aurora Serverless v2 in isolated DB subnets |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-aws-three-tier.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-aws-three-tier.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[devops-aws-service-selection]]
- [[devops-aws-terraform-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when standing up a new HA web-app baseline on AWS.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/vpc.tf`

```hcl
module "vpc" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "~> 5.8"
  name               = "${var.project}-vpc"
  cidr               = "10.0.0.0/16"
  azs                = ["${var.region}a", "${var.region}b"]
  public_subnets     = ["10.0.0.0/24",  "10.0.1.0/24"]
  private_subnets    = ["10.0.10.0/24", "10.0.11.0/24"]
  database_subnets   = ["10.0.20.0/24", "10.0.21.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"   # per-AZ NAT in prod
  create_database_subnet_group = true
}
```

### `templates/alb.tf`

```hcl
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"
  name    = "${var.project}-alb"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets
  enable_deletion_protection = true
  listeners = {
    https = {
      port     = 443
      protocol = "HTTPS"
      certificate_arn = var.acm_cert_arn
      forward = { target_group_key = "app" }
    }
  }
  target_groups = {
    app = { name_prefix = "app-", protocol = "HTTP", port = 8080, target_type = "ip", health_check = { path = "/health" } }
  }
}
```

### `templates/aurora.tf`

```hcl
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"
  name    = "${var.project}-db"
  engine  = "aurora-postgresql"
  engine_mode = "provisioned"
  serverlessv2_scaling_configuration = { min_capacity = 0.5, max_capacity = 8 }
  vpc_id                = module.vpc.vpc_id
  db_subnet_group_name  = module.vpc.database_subnet_group_name
  storage_encrypted     = true
  apply_immediately     = false
  skip_final_snapshot   = false
}
```

### `templates/_smoke-test.json`

```json
{
  "project": "checkout-app",
  "az_count": 2,
  "tiers": {
    "public": [
      "alb"
    ],
    "private": [
      "app"
    ],
    "database": [
      "aurora"
    ]
  },
  "nat_gateway_per_az_prod": true,
  "sg_reference_by_id": true,
  "aurora_serverless_v2": true,
  "encryption_at_rest": true
}
```
