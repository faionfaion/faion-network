variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
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

variable "network_name" {
  description = "VPC network name"
  type        = string
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
}

variable "admin_cidr" {
  description = "CIDR for master authorized networks"
  type        = string
  default     = "10.0.0.0/8"
}

variable "node_pools" {
  description = "Node pool configurations"
  type = list(object({
    name         = string
    machine_type = string
    min_count    = number
    max_count    = number
    disk_size_gb = number
    spot         = bool
    labels       = map(string)
    taints = list(object({
      key    = string
      value  = string
      effect = string
    }))
  }))
  default = [{
    name         = "general"
    machine_type = "e2-standard-4"
    min_count    = 1
    max_count    = 10
    disk_size_gb = 100
    spot         = false
    labels       = { workload = "general" }
    taints       = []
  }]
}
