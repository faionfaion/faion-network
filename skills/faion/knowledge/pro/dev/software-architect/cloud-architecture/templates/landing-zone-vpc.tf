# Terraform module: three-tier VPC with public/app/data subnets across 3 AZs.
# Intended as a landing zone foundation for a production environment.
# Replace: locals block values for your organisation.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

locals {
  environment = "production"
  region      = "eu-west-1"
  # Non-overlapping CIDR to allow peering with other VPCs and on-premise.
  vpc_cidr    = "10.10.0.0/16"

  # Subnet CIDRs per tier per AZ.
  # Pattern: 10.10.<tier*10 + az>.0/24
  # Tier 0 = public, Tier 1 = app, Tier 2 = data
  public_subnets = {
    az_a = "10.10.0.0/24"
    az_b = "10.10.1.0/24"
    az_c = "10.10.2.0/24"
  }
  app_subnets = {
    az_a = "10.10.10.0/24"
    az_b = "10.10.11.0/24"
    az_c = "10.10.12.0/24"
  }
  data_subnets = {
    az_a = "10.10.20.0/24"
    az_b = "10.10.21.0/24"
    az_c = "10.10.22.0/24"
  }

  # Mandatory cost allocation tags (enforced via Tag Policy)
  common_tags = {
    Environment = local.environment
    Team        = "platform"
    CostCenter  = "CC-INFRA"
    Owner       = "platform@company.com"
    Lifecycle   = "permanent"
    ManagedBy   = "terraform"
  }

  azs = ["${local.region}a", "${local.region}b", "${local.region}c"]
}

# ---- VPC ----

resource "aws_vpc" "main" {
  cidr_block           = local.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, { Name = "${local.environment}-vpc" })
}

# Flow logs: required for security incident investigation and anomaly detection
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_log.arn
  log_destination = aws_cloudwatch_log_group.flow_log.arn
}

resource "aws_cloudwatch_log_group" "flow_log" {
  name              = "/aws/vpc/flow-logs/${local.environment}"
  retention_in_days = 90
  tags              = local.common_tags
}

# ---- Internet Gateway (public tier only) ----

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = merge(local.common_tags, { Name = "${local.environment}-igw" })
}

# ---- Public Subnets (load balancers, NAT gateways, bastion) ----

resource "aws_subnet" "public" {
  for_each = local.public_subnets

  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.value
  availability_zone       = local.azs[index(keys(local.public_subnets), each.key)]
  map_public_ip_on_launch = false  # explicit assignment only; never auto-assign

  tags = merge(local.common_tags, {
    Name = "${local.environment}-public-${each.key}"
    Tier = "public"
    # Required for AWS Load Balancer Controller auto-discovery
    "kubernetes.io/role/elb" = "1"
  })
}

# ---- NAT Gateways (one per AZ for high availability) ----

resource "aws_eip" "nat" {
  for_each = local.public_subnets
  domain   = "vpc"
  tags     = merge(local.common_tags, { Name = "${local.environment}-nat-eip-${each.key}" })
}

resource "aws_nat_gateway" "main" {
  for_each      = local.public_subnets
  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = aws_subnet.public[each.key].id
  tags          = merge(local.common_tags, { Name = "${local.environment}-nat-${each.key}" })
}

# ---- App Subnets (application servers, containers) ----

resource "aws_subnet" "app" {
  for_each = local.app_subnets

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = local.azs[index(keys(local.app_subnets), each.key)]

  tags = merge(local.common_tags, {
    Name = "${local.environment}-app-${each.key}"
    Tier = "app"
    "kubernetes.io/role/internal-elb" = "1"
  })
}

# ---- Data Subnets (databases, caches — no internet route) ----

resource "aws_subnet" "data" {
  for_each = local.data_subnets

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = local.azs[index(keys(local.data_subnets), each.key)]

  tags = merge(local.common_tags, {
    Name = "${local.environment}-data-${each.key}"
    Tier = "data"
  })
}

# ---- Route Tables ----

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = merge(local.common_tags, { Name = "${local.environment}-rt-public" })
}

resource "aws_route_table" "app" {
  for_each = local.app_subnets
  vpc_id   = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[each.key].id
  }
  tags = merge(local.common_tags, { Name = "${local.environment}-rt-app-${each.key}" })
}

resource "aws_route_table" "data" {
  vpc_id = aws_vpc.main.id
  # No internet route — data tier is fully isolated
  tags = merge(local.common_tags, { Name = "${local.environment}-rt-data" })
}

# ---- Outputs ----

output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = [for s in aws_subnet.public : s.id]
}

output "app_subnet_ids" {
  value = [for s in aws_subnet.app : s.id]
}

output "data_subnet_ids" {
  value = [for s in aws_subnet.data : s.id]
}
