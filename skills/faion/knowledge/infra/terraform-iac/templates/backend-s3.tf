# purpose: Template fixture for terraform-iac: backend-s3.tf
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
terraform {
  required_version = ">= 1.10.0"

  backend "s3" {
    bucket       = "mycompany-terraform-state"
    key          = "environments/prod/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true  # S3 native locking (Terraform 1.10+)
    # role_arn = "arn:aws:iam::123456789012:role/TerraformRole"  # cross-account
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
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
    }
  }
}
