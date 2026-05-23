variable "name_prefix" {
  description = "Name prefix for all resources"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "vpc_cidr must be a valid CIDR block."
  }
}

variable "azs" {
  description = "List of availability zones (min 3)"
  type        = list(string)

  validation {
    condition     = length(var.azs) >= 3
    error_message = "At least 3 availability zones required for HA."
  }
}

variable "enable_nat_per_az" {
  description = "Create one NAT Gateway per AZ (true for prod, false for non-prod)"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
