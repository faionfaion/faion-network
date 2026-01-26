# GCP Architecture Patterns Templates

## Project Structure

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── gke/
│   ├── cloudsql/
│   ├── storage/
│   ├── networking/
│   └── microservices/
└── shared/
    ├── providers.tf
    └── backend.tf
```

---

## Module: GKE Cluster

### modules/gke/variables.tf

```hcl
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

  default = [
    {
      name         = "general"
      machine_type = "e2-standard-4"
      min_count    = 1
      max_count    = 10
      disk_size_gb = 100
      spot         = false
      labels       = { workload = "general" }
      taints       = []
    }
  ]
}
```

### modules/gke/main.tf

```hcl
locals {
  cluster_name = "${var.project_id}-gke-${var.environment}"
}

resource "google_service_account" "gke_nodes" {
  account_id   = "gke-nodes-${var.environment}"
  display_name = "GKE Node Service Account"
}

resource "google_project_iam_member" "gke_nodes" {
  for_each = toset([
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/artifactregistry.reader",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_container_cluster" "main" {
  name     = local.cluster_name
  location = var.region

  node_locations = [
    "${var.region}-a",
    "${var.region}-b",
    "${var.region}-c"
  ]

  network    = var.network_name
  subnetwork = var.subnet_name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"

    master_global_access_config {
      enabled = true
    }
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.admin_cidr
      display_name = "Admin access"
    }
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  binary_authorization {
    evaluation_mode = var.environment == "prod" ? "PROJECT_SINGLETON_POLICY_ENFORCE" : "DISABLED"
  }

  release_channel {
    channel = var.environment == "prod" ? "STABLE" : "REGULAR"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SU"
    }
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
  }

  datapath_provider = "ADVANCED_DATAPATH"

  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  remove_default_node_pool = true
  initial_node_count       = 1
  enable_shielded_nodes    = true

  lifecycle {
    ignore_changes = [node_pool, initial_node_count]
  }
}

resource "google_container_node_pool" "pools" {
  for_each = { for pool in var.node_pools : pool.name => pool }

  name     = each.value.name
  location = var.region
  cluster  = google_container_cluster.main.name

  autoscaling {
    min_node_count  = each.value.min_count
    max_node_count  = each.value.max_count
    location_policy = each.value.spot ? "ANY" : "BALANCED"
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  upgrade_settings {
    strategy        = "SURGE"
    max_surge       = 1
    max_unavailable = 0
  }

  node_config {
    spot         = each.value.spot
    machine_type = each.value.machine_type
    disk_size_gb = each.value.disk_size_gb
    disk_type    = each.value.spot ? "pd-standard" : "pd-ssd"
    image_type   = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = merge(
      { environment = var.environment },
      each.value.labels
    )

    dynamic "taint" {
      for_each = each.value.taints
      content {
        key    = taint.value.key
        value  = taint.value.value
        effect = taint.value.effect
      }
    }

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
```

### modules/gke/outputs.tf

```hcl
output "cluster_name" {
  description = "GKE cluster name"
  value       = google_container_cluster.main.name
}

output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.main.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "GKE cluster CA certificate"
  value       = google_container_cluster.main.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "service_account_email" {
  description = "GKE node service account email"
  value       = google_service_account.gke_nodes.email
}
```

---

## Module: Cloud SQL

### modules/cloudsql/variables.tf

```hcl
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
}

variable "network_id" {
  description = "VPC network ID for private IP"
  type        = string
}

variable "database_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "POSTGRES_15"
}

variable "tier" {
  description = "Machine type"
  type        = string
  default     = "db-custom-4-16384"
}

variable "disk_size" {
  description = "Disk size in GB"
  type        = number
  default     = 100
}

variable "enable_replica" {
  description = "Enable read replica"
  type        = bool
  default     = false
}

variable "databases" {
  description = "List of databases to create"
  type        = list(string)
  default     = ["app"]
}
```

### modules/cloudsql/main.tf

```hcl
locals {
  instance_name = "${var.project_id}-postgres-${var.environment}"
  is_prod       = var.environment == "prod"
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}

resource "google_sql_database_instance" "main" {
  name             = local.instance_name
  database_version = var.database_version
  region           = var.region

  deletion_protection = local.is_prod

  settings {
    tier              = local.is_prod ? var.tier : "db-f1-micro"
    availability_type = local.is_prod ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = var.disk_size
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = local.is_prod
      backup_retention_settings {
        retained_backups = local.is_prod ? 30 : 7
      }
    }

    maintenance_window {
      day          = 7
      hour         = 4
      update_track = "stable"
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
      require_ssl     = true
    }

    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
    database_flags {
      name  = "log_connections"
      value = "on"
    }
    database_flags {
      name  = "log_disconnections"
      value = "on"
    }
    database_flags {
      name  = "log_lock_waits"
      value = "on"
    }
  }
}

resource "google_sql_database_instance" "replica" {
  count = var.enable_replica ? 1 : 0

  name                 = "${local.instance_name}-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = var.region
  database_version     = var.database_version

  replica_configuration {
    failover_target = true
  }

  settings {
    tier              = var.tier
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = var.disk_size

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
      require_ssl     = true
    }
  }
}

resource "google_sql_database" "databases" {
  for_each = toset(var.databases)

  name     = each.value
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
```

### modules/cloudsql/outputs.tf

```hcl
output "instance_name" {
  description = "Cloud SQL instance name"
  value       = google_sql_database_instance.main.name
}

output "connection_name" {
  description = "Cloud SQL connection name"
  value       = google_sql_database_instance.main.connection_name
}

output "private_ip" {
  description = "Cloud SQL private IP"
  value       = google_sql_database_instance.main.private_ip_address
}

output "db_password" {
  description = "Database password"
  value       = random_password.db_password.result
  sensitive   = true
}
```

---

## Module: Microservices (Cloud Run)

### modules/microservices/variables.tf

```hcl
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "environment" {
  description = "Environment"
  type        = string
}

variable "services" {
  description = "Map of services to deploy"
  type = map(object({
    image            = string
    cpu              = string
    memory           = string
    min_instances    = number
    max_instances    = number
    port             = number
    env_vars         = map(string)
    secrets          = map(string)
    vpc_connector_id = optional(string)
  }))
}
```

### modules/microservices/main.tf

```hcl
resource "google_service_account" "services" {
  for_each = var.services

  account_id   = "${each.key}-sa-${var.environment}"
  display_name = "${each.key} Service Account"
}

resource "google_cloud_run_v2_service" "services" {
  for_each = var.services

  name     = "${each.key}-${var.environment}"
  location = var.region

  template {
    service_account = google_service_account.services[each.key].email

    scaling {
      min_instance_count = each.value.min_instances
      max_instance_count = each.value.max_instances
    }

    containers {
      image = each.value.image

      ports {
        container_port = each.value.port
      }

      resources {
        limits = {
          cpu    = each.value.cpu
          memory = each.value.memory
        }
        cpu_idle = true
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        period_seconds = 30
      }

      dynamic "env" {
        for_each = each.value.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = each.value.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }
    }

    dynamic "vpc_access" {
      for_each = each.value.vpc_connector_id != null ? [1] : []
      content {
        connector = each.value.vpc_connector_id
        egress    = "PRIVATE_RANGES_ONLY"
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}
```

---

## Usage Example

### environments/prod/main.tf

```hcl
module "network" {
  source = "../../modules/networking"

  project_id  = var.project_id
  region      = var.region
  environment = "prod"
}

module "gke" {
  source = "../../modules/gke"

  project_id   = var.project_id
  region       = var.region
  environment  = "prod"
  network_name = module.network.network_name
  subnet_name  = module.network.subnet_name
  admin_cidr   = var.admin_cidr

  node_pools = [
    {
      name         = "general"
      machine_type = "e2-standard-4"
      min_count    = 3
      max_count    = 20
      disk_size_gb = 100
      spot         = false
      labels       = { workload = "general" }
      taints       = []
    },
    {
      name         = "spot"
      machine_type = "e2-standard-4"
      min_count    = 0
      max_count    = 50
      disk_size_gb = 50
      spot         = true
      labels       = { workload = "batch" }
      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  ]
}

module "database" {
  source = "../../modules/cloudsql"

  project_id     = var.project_id
  region         = var.region
  environment    = "prod"
  network_id     = module.network.network_id
  tier           = "db-custom-8-32768"
  disk_size      = 500
  enable_replica = true
  databases      = ["app", "analytics"]
}
```

---

*GCP Architecture Patterns Templates | faion-infrastructure-engineer*
