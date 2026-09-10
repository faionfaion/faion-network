# purpose: Template fixture for terraform: versions.tf
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
#
# r1-provider-pinning: providers AND terraform are pinned with the `=` operator.
# `~> 5.50` accepts any 5.x above 5.50 and `>= 1.9.0` accepts every future
# release, so two runs a week apart can plan differently with no change to this
# repository. A pin is one version; bumps arrive as a PR with `terraform plan`
# output attached, which is the second half of the same rule.

terraform {
  required_version = "= 1.9.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 5.70.0"
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
