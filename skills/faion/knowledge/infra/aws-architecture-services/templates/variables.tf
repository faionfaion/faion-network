# purpose: standard variables: project, environment, region for the reference architecture
# consumes: see ../AGENTS.md ## Prerequisites + content/02-output-contract.xml
# produces: provisioned AWS resources conforming to the methodology spec
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~600-1500 tokens when loaded as context
variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "domain" {
  description = "Primary domain name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
}

variable "owner" {
  description = "Team or individual owning this infrastructure"
  type        = string
  default     = "platform"
}
