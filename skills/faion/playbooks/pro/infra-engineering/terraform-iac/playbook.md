---
name: terraform-iac
description: Install Terraform, provision an AWS VPC + EC2 + RDS with remote state in S3+DynamoDB, extract reusable modules, and deploy across environments via tfvars.
tier: pro
group: infra-engineering
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Terraform project that provisions a private AWS VPC with public/private subnets, one EC2 instance, one RDS PostgreSQL instance, stores state in S3 with DynamoDB locking, and separates network and compute concerns into reusable modules deployable across `staging` and `production` environments via `.tfvars` files.

## Prerequisites

- AWS account with IAM credentials that have `AmazonEC2FullAccess`, `AmazonRDSFullAccess`, `AmazonS3FullAccess`, `AmazonDynamoDBFullAccess`, and `AmazonVPCFullAccess` policies (or equivalent).
- AWS CLI v2 configured (`aws configure`) with a default region (this playbook uses `eu-central-1`).
- Terraform >= 1.6.0 (instructions in Step 1).
- A key pair named `myapp-prod` already created in EC2 (or replace with your own in Step 4).
- Understanding of HCL variable blocks and tfvars files — see [terraform-basics](../../../knowledge/pro/infra/infrastructure-engineer/terraform-basics).

## Steps

### 1. Install Terraform

```bash
# Ubuntu / Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install terraform

# macOS
brew tap hashicorp/tap && brew install hashicorp/tap/terraform

terraform version   # must print >= 1.6.0
```

### 2. Create the S3 bucket and DynamoDB table for remote state

Run this once per AWS account. Replace `myapp-tfstate-eu` with a globally unique bucket name.

```bash
aws s3api create-bucket \
  --bucket myapp-tfstate-eu \
  --region eu-central-1 \
  --create-bucket-configuration LocationConstraint=eu-central-1

aws s3api put-bucket-versioning \
  --bucket myapp-tfstate-eu \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket myapp-tfstate-eu \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'

aws dynamodb create-table \
  --table-name myapp-tf-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-central-1
```

### 3. Scaffold the project layout

```
myapp-infra/
├── main.tf                  # root: backend + module calls
├── variables.tf             # root input variables
├── outputs.tf               # root outputs
├── versions.tf              # terraform + provider version pins
├── staging.tfvars           # staging environment values
├── production.tfvars        # production environment values
└── modules/
    ├── network/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── compute/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

```bash
mkdir -p myapp-infra/modules/network myapp-infra/modules/compute
cd myapp-infra
```

### 4. Write `versions.tf` — pin Terraform and the AWS provider

```hcl
# versions.tf
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

### 5. Write `variables.tf` and `*.tfvars` files

```hcl
# variables.tf
variable "aws_region"    { default = "eu-central-1" }
variable "project_name"  { default = "myapp" }
variable "environment"   {}   # required — no default
variable "vpc_cidr"      { default = "10.0.0.0/16" }
variable "db_password"   { sensitive = true }
variable "instance_type" { default = "t3.micro" }
variable "db_instance_class" { default = "db.t3.micro" }
```

```hcl
# staging.tfvars
environment       = "staging"
instance_type     = "t3.micro"
db_instance_class = "db.t3.micro"
db_password       = "StagingPass2024!"   # use Secrets Manager in production
```

```hcl
# production.tfvars
environment       = "production"
instance_type     = "t3.small"
db_instance_class = "db.t3.small"
db_password       = "ProdPass2024!"
```

### 6. Write `modules/network/main.tf` — VPC, subnets, IGW, route tables

```hcl
# modules/network/main.tf
data "aws_availability_zones" "available" { state = "available" }

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "public" {
  for_each                = toset(slice(data.aws_availability_zones.available.names, 0, 2))
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, index(data.aws_availability_zones.available.names, each.key))
  availability_zone       = each.key
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private" {
  for_each          = toset(slice(data.aws_availability_zones.available.names, 0, 2))
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, index(data.aws_availability_zones.available.names, each.key) + 10)
  availability_zone = each.key
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
```

```hcl
# modules/network/variables.tf
variable "vpc_cidr" {}

# modules/network/outputs.tf
output "vpc_id"          { value = aws_vpc.main.id }
output "public_subnets"  { value = [for s in aws_subnet.public : s.id] }
output "private_subnets" { value = [for s in aws_subnet.private : s.id] }
```

### 7. Write `modules/compute/main.tf` — EC2 and RDS

```hcl
# modules/compute/main.tf

# Security group: EC2 — allow SSH from your office IP only
resource "aws_security_group" "ec2" {
  name   = "${var.project_name}-${var.environment}-ec2"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.office_cidr]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security group: RDS — allow 5432 from EC2 SG only
resource "aws_security_group" "rds" {
  name   = "${var.project_name}-${var.environment}-rds"
  vpc_id = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]   # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_ids[0]
  vpc_security_group_ids = [aws_security_group.ec2.id]
  key_name               = var.key_pair_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-${var.environment}"
  engine                 = "postgres"
  engine_version         = "16.2"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  storage_encrypted      = true
  username               = "myapp"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot    = var.environment != "production"
  deletion_protection    = var.environment == "production"
}
```

```hcl
# modules/compute/variables.tf
variable "project_name"       {}
variable "environment"        {}
variable "vpc_id"             {}
variable "public_subnet_ids"  { type = list(string) }
variable "private_subnet_ids" { type = list(string) }
variable "instance_type"      { default = "t3.micro" }
variable "db_instance_class"  { default = "db.t3.micro" }
variable "db_password"        { sensitive = true }
variable "office_cidr"        { default = "0.0.0.0/0" }   # restrict in production
variable "key_pair_name"      { default = "myapp-prod" }

# modules/compute/outputs.tf
output "ec2_public_ip"    { value = aws_instance.app.public_ip }
output "rds_endpoint"     { value = aws_db_instance.postgres.endpoint }
```

### 8. Write the root `main.tf` — backend + module calls

```hcl
# main.tf
terraform {
  backend "s3" {
    bucket         = "myapp-tfstate-eu"
    key            = "staging/core/terraform.tfstate"   # override per env
    region         = "eu-central-1"
    dynamodb_table = "myapp-tf-locks"
    encrypt        = true
  }
}

module "network" {
  source   = "./modules/network"
  vpc_cidr = var.vpc_cidr
}

module "compute" {
  source             = "./modules/compute"
  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.network.vpc_id
  public_subnet_ids  = module.network.public_subnets
  private_subnet_ids = module.network.private_subnets
  instance_type      = var.instance_type
  db_instance_class  = var.db_instance_class
  db_password        = var.db_password
}
```

```hcl
# outputs.tf
output "ec2_public_ip" { value = module.compute.ec2_public_ip }
output "rds_endpoint"  { value = module.compute.rds_endpoint }
```

### 9. Initialize, plan, and apply for staging

```bash
cd myapp-infra

# Initialize — downloads provider, configures backend
terraform init

# Validate HCL syntax
terraform validate

# Format check
terraform fmt -recursive

# Preview changes for staging
terraform plan -var-file=staging.tfvars -out=staging.plan

# Apply staging
terraform apply staging.plan
```

To deploy production, override the backend key first (use a workspace or a separate `init` per environment), then:

```bash
terraform init -reconfigure \
  -backend-config="key=production/core/terraform.tfstate"

terraform plan -var-file=production.tfvars -out=production.plan
terraform apply production.plan
```

## Verify

After `terraform apply` completes, run:

```bash
# EC2 reachable
ssh -i ~/.ssh/myapp-prod.pem ubuntu@$(terraform output -raw ec2_public_ip) "uname -a"

# State stored remotely
aws s3 ls s3://myapp-tfstate-eu/staging/core/

# Lock table has no orphaned locks
aws dynamodb scan --table-name myapp-tf-locks --region eu-central-1 \
  --query "Count" --output text   # should return 0 when no apply is running
```

Expected: SSH connects without errors; S3 shows `terraform.tfstate`; DynamoDB count is `0`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Error: No valid credential sources found` | AWS CLI not configured or wrong profile | Run `aws configure` or set `AWS_PROFILE=myapp` before terraform commands |
| `Error acquiring the state lock` + existing LockID | Previous apply crashed without releasing lock | `terraform force-unlock <LockID>` — copy LockID from the error message; verify no concurrent apply is running first |
| `InvalidClientTokenId` when creating S3 bucket | Region mismatch — bucket region differs from provider region | Add `--region eu-central-1` to the `aws s3api create-bucket` command and set `LocationConstraint` to the same region |
| `Error: creating DB Subnet Group: DBSubnetGroupDoesNotCoverEnoughAZs` | Only one private subnet AZ available | Ensure `private_subnets` span ≥ 2 AZs — the `for_each` loop uses 2 AZs from `data.aws_availability_zones` |
| `terraform plan` shows resource replacement on every run | `data.aws_ami.ubuntu` AMI ID changes with new Ubuntu releases | Pin the AMI by adding a `filter` on `image-id` or store the AMI ID in tfvars for production |
| Backend config error on second environment | `init` still points to old backend key | Re-run `terraform init -reconfigure -backend-config="key=production/..."` explicitly |

## Next

- [terraform-modules-composition](../../../knowledge/pro/infra/infrastructure-engineer/terraform-modules-composition) — layer modules into root stacks and share outputs across stacks at scale.
- Set up CI/CD: add a GitHub Actions workflow that runs `terraform plan` on PRs and `terraform apply` on merge to `main`.
- Add `aws_cloudwatch_metric_alarm` and `aws_sns_topic` to the compute module for CPU/memory alerting before going to production.

## References

- [knowledge/pro/infra/infrastructure-engineer/terraform-basics](../../../knowledge/pro/infra/infrastructure-engineer/terraform-basics) — HCL syntax, provider version pinning, and the four-step workflow (init → plan → apply) that underpins every step of this playbook.
- [knowledge/pro/infra/infrastructure-engineer/terraform-state](../../../knowledge/pro/infra/infrastructure-engineer/terraform-state) — S3+DynamoDB backend configuration, key path strategy, and encryption requirements applied in Steps 2 and 8.
- [knowledge/pro/infra/infrastructure-engineer/terraform-modules-structure](../../../knowledge/pro/infra/infrastructure-engineer/terraform-modules-structure) — single-responsibility module layout and file conventions (main.tf / variables.tf / outputs.tf) used to structure `modules/network` and `modules/compute` in Steps 6 and 7.
- [knowledge/pro/infra/infrastructure-engineer/aws-vpc-design](../../../knowledge/pro/infra/infrastructure-engineer/aws-vpc-design) — three-tier subnet segmentation and multi-AZ placement rules that drive the public/private subnet design in `modules/network`.
