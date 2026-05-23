# purpose: Terraform VPC using terraform-aws-modules/vpc with 3 tiers + 2 AZs
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

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
