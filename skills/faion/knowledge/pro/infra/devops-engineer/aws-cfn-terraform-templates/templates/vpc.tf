# purpose: VPC Terraform module skeleton (multi-AZ)
# consumes: inputs declared in content/02-output-contract.xml
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~300-800 tokens when loaded as context

# AWS Infrastructure-as-Code Templates (CloudFormation and Terraform) — vpc.tf
# Terraform skeleton. Customise variables + tags before apply.

variable "project" {
  type    = string
  default = "faion-net"
}

variable "environment" {
  type    = string
  default = "dev"
}

locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
    Methodology = "aws-cfn-terraform-templates"
  }
}

# Resource block goes here. See AGENTS.md for the canonical pattern.
