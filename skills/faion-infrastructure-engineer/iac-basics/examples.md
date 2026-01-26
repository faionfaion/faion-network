# IaC Examples

## Terraform Examples

### Basic Provider Configuration

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.25"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
      Team        = var.team
    }
  }
}
```

### Remote Backend with Locking

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "environments/prod/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # Cross-account access
    # role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }
}
```

### Variable Validation

```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string

  validation {
    condition     = can(regex("^t3\\.", var.instance_type)) || can(regex("^m5\\.", var.instance_type))
    error_message = "Instance type must be t3.* or m5.* family."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}
```

### Reusable Module Pattern

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.name_prefix}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index)
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name_prefix}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr_block, 8, count.index + 100)
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.name_prefix}-private-${count.index + 1}"
    Type = "private"
  }
}

# modules/vpc/variables.tf
variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### Module Usage

```hcl
module "vpc" {
  source = "../../modules/vpc"

  name_prefix        = "${var.project_name}-${var.environment}"
  cidr_block         = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "eks" {
  source = "../../modules/eks"

  cluster_name       = "${var.project_name}-${var.environment}"
  cluster_version    = var.eks_version
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  node_groups        = var.node_groups

  depends_on = [module.vpc]
}
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "app" {
  name        = "${var.name_prefix}-app-sg"
  description = "Application security group"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      description     = ingress.value.description
      from_port       = ingress.value.port
      to_port         = ingress.value.port
      protocol        = ingress.value.protocol
      cidr_blocks     = ingress.value.cidr_blocks
      security_groups = ingress.value.security_groups
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "ingress_rules" {
  description = "List of ingress rules"
  type = list(object({
    description     = string
    port            = number
    protocol        = string
    cidr_blocks     = optional(list(string), [])
    security_groups = optional(list(string), [])
  }))
  default = []
}
```

### Data Sources

```hcl
# Fetch latest AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Fetch existing VPC
data "aws_vpc" "existing" {
  filter {
    name   = "tag:Name"
    values = ["main-vpc"]
  }
}

# Fetch current caller identity
data "aws_caller_identity" "current" {}

# Fetch available AZs
data "aws_availability_zones" "available" {
  state = "available"
}
```

### Locals for Complex Logic

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center
  }

  is_production = var.environment == "prod"

  instance_type = local.is_production ? "m5.large" : "t3.medium"

  availability_zones = slice(data.aws_availability_zones.available.names, 0, 3)

  subnet_cidrs = {
    for idx, az in local.availability_zones :
    az => cidrsubnet(var.vpc_cidr, 8, idx)
  }
}
```

## OpenTofu Examples

### State Encryption (OpenTofu Feature)

```hcl
terraform {
  encryption {
    method "aes_gcm" "default" {
      keys = key_provider.pbkdf2.default
    }

    key_provider "pbkdf2" "default" {
      passphrase = var.state_encryption_passphrase
    }

    state {
      method   = method.aes_gcm.default
      enforced = true
    }
  }
}
```

## Pulumi Examples

### Python Infrastructure

```python
import pulumi
import pulumi_aws as aws

# Create VPC
vpc = aws.ec2.Vpc("main-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": f"{pulumi.get_project()}-vpc",
        "Environment": pulumi.get_stack(),
    }
)

# Create subnets using loops
availability_zones = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
public_subnets = []

for i, az in enumerate(availability_zones):
    subnet = aws.ec2.Subnet(f"public-subnet-{i}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i}.0/24",
        availability_zone=az,
        map_public_ip_on_launch=True,
        tags={
            "Name": f"public-subnet-{i+1}",
            "Type": "public",
        }
    )
    public_subnets.append(subnet)

# Export outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("public_subnet_ids", [s.id for s in public_subnets])
```

### TypeScript Infrastructure

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = pulumi.getStack();
const projectName = pulumi.getProject();

// Create VPC
const vpc = new aws.ec2.Vpc("main-vpc", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: `${projectName}-vpc`,
        Environment: environment,
    },
});

// Create subnets with map
const availabilityZones = ["eu-central-1a", "eu-central-1b", "eu-central-1c"];

const publicSubnets = availabilityZones.map((az, index) => {
    return new aws.ec2.Subnet(`public-subnet-${index}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${index}.0/24`,
        availabilityZone: az,
        mapPublicIpOnLaunch: true,
        tags: {
            Name: `public-subnet-${index + 1}`,
            Type: "public",
        },
    });
});

// Export outputs
export const vpcId = vpc.id;
export const publicSubnetIds = publicSubnets.map(s => s.id);
```

## Crossplane Examples

### AWS VPC via Crossplane

```yaml
apiVersion: ec2.aws.crossplane.io/v1beta1
kind: VPC
metadata:
  name: main-vpc
spec:
  forProvider:
    region: eu-central-1
    cidrBlock: 10.0.0.0/16
    enableDnsHostNames: true
    enableDnsSupport: true
    tags:
      - key: Name
        value: main-vpc
      - key: ManagedBy
        value: crossplane
  providerConfigRef:
    name: aws-provider
---
apiVersion: ec2.aws.crossplane.io/v1beta1
kind: Subnet
metadata:
  name: public-subnet-1
spec:
  forProvider:
    region: eu-central-1
    availabilityZone: eu-central-1a
    cidrBlock: 10.0.0.0/24
    mapPublicIpOnLaunch: true
    vpcIdRef:
      name: main-vpc
    tags:
      - key: Name
        value: public-subnet-1
  providerConfigRef:
    name: aws-provider
```

### Composite Resource Definition

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xnetworks.infrastructure.example.com
spec:
  group: infrastructure.example.com
  names:
    kind: XNetwork
    plural: xnetworks
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                region:
                  type: string
                cidrBlock:
                  type: string
                availabilityZones:
                  type: array
                  items:
                    type: string
```

## GitOps Integration Examples

### GitHub Actions Terraform Workflow

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: '1.6.0'
  AWS_REGION: 'eu-central-1'

jobs:
  terraform:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        working-directory: infrastructure/environments/prod
        run: terraform init

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        working-directory: infrastructure/environments/prod
        run: terraform validate

      - name: tfsec Security Scan
        uses: aquasecurity/tfsec-action@v1.0.3
        with:
          working_directory: infrastructure

      - name: Terraform Plan
        id: plan
        working-directory: infrastructure/environments/prod
        run: |
          terraform plan -no-color -out=tfplan 2>&1 | tee plan.txt
          echo "plan<<EOF" >> $GITHUB_OUTPUT
          cat plan.txt >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const plan = `${{ steps.plan.outputs.plan }}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Terraform Plan\n\`\`\`\n${plan}\n\`\`\``
            });

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        working-directory: infrastructure/environments/prod
        run: terraform apply -auto-approve tfplan
```

### Atlantis Configuration

```yaml
# atlantis.yaml
version: 3
projects:
  - name: prod
    dir: infrastructure/environments/prod
    workspace: default
    terraform_version: v1.6.0
    autoplan:
      when_modified: ["*.tf", "../modules/**/*.tf"]
      enabled: true
    apply_requirements: [approved, mergeable]
    workflow: custom

workflows:
  custom:
    plan:
      steps:
        - init
        - run: tflint
        - run: tfsec . --soft-fail
        - plan
    apply:
      steps:
        - apply
```

---

*IaC Examples | faion-infrastructure-engineer*
