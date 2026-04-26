locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  azs = slice(data.aws_availability_zones.available.names, 0, 3)

  public_subnets = [
    for i, az in local.azs : cidrsubnet(var.vpc_cidr, 8, i)
  ]
  private_subnets = [
    for i, az in local.azs : cidrsubnet(var.vpc_cidr, 8, i + 10)
  ]
}

data "aws_availability_zones" "available" {
  state = "available"
}
