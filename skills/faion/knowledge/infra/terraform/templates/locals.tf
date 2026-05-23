# purpose: Template fixture for terraform: locals.tf
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  env_config = {
    dev = {
      instance_type = "t3.micro"
      min_size      = 1
      max_size      = 2
    }
    staging = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
    }
    prod = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 10
    }
  }

  config = local.env_config[var.environment]
}
