# purpose: Template fixture for terraform: variables.tf
# consumes: content/01-core-rules.xml
# produces: config
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "Must be a valid AWS region code (e.g. us-east-1)."
  }
}

variable "environment" {
  description = "Deployment environment: dev, staging, or prod"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

variable "project_name" {
  description = "Project name used in resource tags and name prefixes"
  type        = string
}
