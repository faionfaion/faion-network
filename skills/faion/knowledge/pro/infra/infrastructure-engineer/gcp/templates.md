# GCP Templates

Terraform templates for common GCP infrastructure patterns (2025-2026).

## Terraform Templates

### VPC Module (Production-Ready)

```hcl
# modules/vpc/main.tf

variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

locals {
  name = "${var.project}-${var.environment}"
}

# VPC
resource "google_compute_network" "main" {
  project                 = var.project
  name                    = local.name
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

# Public Subnet
resource "google_compute_subnetwork" "public" {
  project       = var.project
  name          = "${local.name}-public"
  network       = google_compute_network.main.id
  region        = var.region
  ip_cidr_range = "10.0.1.0/24"

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Private Subnet (Applications)
resource "google_compute_subnetwork" "private" {
  project                  = var.project
  name                     = "${local.name}-private"
  network                  = google_compute_network.main.id
  region                   = var.region
  ip_cidr_range            = "10.0.10.0/24"
  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# GKE Subnet with Secondary Ranges
resource "google_compute_subnetwork" "gke" {
  project                  = var.project
  name                     = "${local.name}-gke"
  network                  = google_compute_network.main.id
  region                   = var.region
  ip_cidr_range            = "10.0.20.0/24"
  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/20"
  }

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Database Subnet
resource "google_compute_subnetwork" "database" {
  project                  = var.project
  name                     = "${local.name}-database"
  network                  = google_compute_network.main.id
  region                   = var.region
  ip_cidr_range            = "10.0.30.0/24"
  private_ip_google_access = true
}

# Cloud Router
resource "google_compute_router" "main" {
  project = var.project
  name    = "${local.name}-router"
  network = google_compute_network.main.id
  region  = var.region
}

# Cloud NAT
resource "google_compute_router_nat" "main" {
  project                            = var.project
  name                               = "${local.name}-nat"
  router                             = google_compute_router.main.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

output "network_id" {
  value = google_compute_network.main.id
}

output "network_name" {
  value = google_compute_network.main.name
}

output "private_subnet_id" {
  value = google_compute_subnetwork.private.id
}

output "gke_subnet_id" {
  value = google_compute_subnetwork.gke.id
}

output "pods_range_name" {
  value = "pods"
}

output "services_range_name" {
  value = "services"
}
```

### Firewall Rules Module

```hcl
# modules/firewall/main.tf

variable "project" {
  type = string
}

variable "network" {
  type = string
}

variable "private_subnet_cidr" {
  type    = string
  default = "10.0.10.0/24"
}

# Allow IAP for SSH (no direct SSH)
resource "google_compute_firewall" "allow_iap_ssh" {
  project     = var.project
  name        = "${var.network}-allow-iap-ssh"
  network     = var.network
  description = "Allow SSH via IAP"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["allow-iap-ssh"]
  priority      = 1000
}

# Allow health checks from GCP load balancers
resource "google_compute_firewall" "allow_health_check" {
  project     = var.project
  name        = "${var.network}-allow-health-check"
  network     = var.network
  description = "Allow health checks from GCP LB"

  allow {
    protocol = "tcp"
    ports    = ["8080", "80", "443"]
  }

  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
  target_tags   = ["allow-health-check"]
  priority      = 1000
}

# Allow internal traffic
resource "google_compute_firewall" "allow_internal" {
  project     = var.project
  name        = "${var.network}-allow-internal"
  network     = var.network
  description = "Allow internal traffic"

  allow {
    protocol = "tcp"
  }

  allow {
    protocol = "udp"
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/8"]
  priority      = 1000
}

# Allow app to database
resource "google_compute_firewall" "allow_app_to_db" {
  project     = var.project
  name        = "${var.network}-allow-app-to-db"
  network     = var.network
  description = "Allow app tier to database"

  allow {
    protocol = "tcp"
    ports    = ["5432", "3306"]
  }

  source_ranges = [var.private_subnet_cidr]
  target_tags   = ["database"]
  priority      = 1000
}

# Deny all other ingress (explicit)
resource "google_compute_firewall" "deny_all_ingress" {
  project     = var.project
  name        = "${var.network}-deny-all-ingress"
  network     = var.network
  description = "Deny all other ingress"

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  priority      = 65534
}
```

### Service Account Module (Least Privilege)

```hcl
# modules/service-account/main.tf

variable "project" {
  type = string
}

variable "name" {
  type = string
}

variable "display_name" {
  type = string
}

variable "roles" {
  type    = list(string)
  default = []
}

variable "secret_ids" {
  type        = list(string)
  default     = []
  description = "Secret Manager secret IDs to grant access"
}

# Service Account
resource "google_service_account" "main" {
  project      = var.project
  account_id   = var.name
  display_name = var.display_name
}

# Project-level role bindings
resource "google_project_iam_member" "roles" {
  for_each = toset(var.roles)

  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.main.email}"
}

# Secret Manager access
resource "google_secret_manager_secret_iam_member" "secret_access" {
  for_each = toset(var.secret_ids)

  project   = var.project
  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.main.email}"
}

output "email" {
  value = google_service_account.main.email
}

output "id" {
  value = google_service_account.main.id
}

output "name" {
  value = google_service_account.main.name
}
```

### Cloud Run Service Module

```hcl
# modules/cloud-run/main.tf

variable "project" {
  type = string
}

variable "name" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "image" {
  type = string
}

variable "service_account_email" {
  type = string
}

variable "vpc_connector_id" {
  type    = string
  default = null
}

variable "env_vars" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  type = map(object({
    secret_id = string
    version   = string
  }))
  default = {}
}

variable "min_instances" {
  type    = number
  default = 0
}

variable "max_instances" {
  type    = number
  default = 10
}

variable "cpu" {
  type    = string
  default = "1"
}

variable "memory" {
  type    = string
  default = "512Mi"
}

variable "concurrency" {
  type    = number
  default = 80
}

variable "allow_unauthenticated" {
  type    = bool
  default = false
}

resource "google_cloud_run_v2_service" "main" {
  project  = var.project
  name     = var.name
  location = var.region

  template {
    service_account = var.service_account_email

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    dynamic "vpc_access" {
      for_each = var.vpc_connector_id != null ? [1] : []
      content {
        connector = var.vpc_connector_id
        egress    = "ALL_TRAFFIC"
      }
    }

    containers {
      image = var.image

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
        cpu_idle = true
      }

      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = var.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret_id
              version = env.value.version
            }
          }
        }
      }

      startup_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 10
        timeout_seconds       = 5
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        timeout_seconds   = 5
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    max_instance_request_concurrency = var.concurrency
    timeout                          = "60s"
    execution_environment            = "EXECUTION_ENVIRONMENT_GEN2"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

# IAM binding for public access
resource "google_cloud_run_service_iam_member" "public" {
  count = var.allow_unauthenticated ? 1 : 0

  project  = var.project
  location = var.region
  service  = google_cloud_run_v2_service.main.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "url" {
  value = google_cloud_run_v2_service.main.uri
}

output "name" {
  value = google_cloud_run_v2_service.main.name
}
```

### GKE Autopilot Cluster Module

```hcl
# modules/gke-autopilot/main.tf

variable "project" {
  type = string
}

variable "name" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "network" {
  type = string
}

variable "subnetwork" {
  type = string
}

variable "pods_range_name" {
  type = string
}

variable "services_range_name" {
  type = string
}

variable "master_ipv4_cidr" {
  type    = string
  default = "172.16.0.0/28"
}

variable "authorized_networks" {
  type = list(object({
    cidr_block   = string
    display_name = string
  }))
  default = []
}

resource "google_container_cluster" "autopilot" {
  project  = var.project
  name     = var.name
  location = var.region

  enable_autopilot = true

  network    = var.network
  subnetwork = var.subnetwork

  ip_allocation_policy {
    cluster_secondary_range_name  = var.pods_range_name
    services_secondary_range_name = var.services_range_name
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = var.master_ipv4_cidr
  }

  master_authorized_networks_config {
    dynamic "cidr_blocks" {
      for_each = var.authorized_networks
      content {
        cidr_block   = cidr_blocks.value.cidr_block
        display_name = cidr_blocks.value.display_name
      }
    }
  }

  workload_identity_config {
    workload_pool = "${var.project}.svc.id.goog"
  }

  release_channel {
    channel = "REGULAR"
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

  deletion_protection = true
}

output "cluster_id" {
  value = google_container_cluster.autopilot.id
}

output "cluster_endpoint" {
  value     = google_container_cluster.autopilot.endpoint
  sensitive = true
}

output "cluster_ca_certificate" {
  value     = google_container_cluster.autopilot.master_auth[0].cluster_ca_certificate
  sensitive = true
}
```

### Workload Identity Module

```hcl
# modules/workload-identity/main.tf

variable "project" {
  type = string
}

variable "gke_sa_name" {
  type        = string
  description = "Name for both GCP and K8s service accounts"
}

variable "namespace" {
  type    = string
  default = "default"
}

variable "roles" {
  type        = list(string)
  default     = []
  description = "IAM roles to grant"
}

variable "secret_ids" {
  type        = list(string)
  default     = []
  description = "Secret Manager secrets to grant access"
}

# GCP Service Account
resource "google_service_account" "main" {
  project      = var.project
  account_id   = var.gke_sa_name
  display_name = "GKE Workload Identity SA for ${var.gke_sa_name}"
}

# Workload Identity binding
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.main.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project}.svc.id.goog[${var.namespace}/${var.gke_sa_name}]"
}

# Project-level roles
resource "google_project_iam_member" "roles" {
  for_each = toset(var.roles)

  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.main.email}"
}

# Secret access
resource "google_secret_manager_secret_iam_member" "secrets" {
  for_each = toset(var.secret_ids)

  project   = var.project
  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.main.email}"
}

output "gcp_sa_email" {
  value = google_service_account.main.email
}

output "k8s_sa_annotation" {
  value = "iam.gke.io/gcp-service-account=${google_service_account.main.email}"
}
```

### Cloud SQL Module

```hcl
# modules/cloud-sql/main.tf

variable "project" {
  type = string
}

variable "name" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "database_version" {
  type    = string
  default = "POSTGRES_15"
}

variable "tier" {
  type    = string
  default = "db-custom-2-7680"
}

variable "network" {
  type = string
}

variable "availability_type" {
  type    = string
  default = "REGIONAL"
}

variable "deletion_protection" {
  type    = bool
  default = true
}

# Private IP allocation
resource "google_compute_global_address" "private_ip" {
  project       = var.project
  name          = "${var.name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = var.network
}

# Private services connection
resource "google_service_networking_connection" "private_vpc" {
  network                 = var.network
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip.name]
}

# Cloud SQL instance
resource "google_sql_database_instance" "main" {
  project          = var.project
  name             = var.name
  database_version = var.database_version
  region           = var.region

  depends_on = [google_service_networking_connection.private_vpc]

  settings {
    tier              = var.tier
    availability_type = var.availability_type
    disk_size         = 100
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = var.network
      enable_private_path_for_google_cloud_services = true
    }

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = 30
        retention_unit   = "COUNT"
      }
    }

    maintenance_window {
      day          = 7
      hour         = 4
      update_track = "stable"
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = false
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
  }

  deletion_protection = var.deletion_protection
}

# Database
resource "google_sql_database" "main" {
  project  = var.project
  name     = var.name
  instance = google_sql_database_instance.main.name
}

# Random password
resource "random_password" "db_password" {
  length  = 32
  special = false
}

# Database user
resource "google_sql_user" "main" {
  project  = var.project
  name     = "app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}

# Store password in Secret Manager
resource "google_secret_manager_secret" "db_password" {
  project   = var.project
  secret_id = "${var.name}-db-password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

output "instance_name" {
  value = google_sql_database_instance.main.name
}

output "private_ip" {
  value = google_sql_database_instance.main.private_ip_address
}

output "connection_name" {
  value = google_sql_database_instance.main.connection_name
}

output "password_secret_id" {
  value = google_secret_manager_secret.db_password.secret_id
}
```

## Example Usage

### Complete Infrastructure

```hcl
# main.tf

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

# VPC
module "vpc" {
  source = "./modules/vpc"

  project     = var.project
  environment = var.environment
  region      = var.region
}

# Firewall
module "firewall" {
  source = "./modules/firewall"

  project             = var.project
  network             = module.vpc.network_name
  private_subnet_cidr = "10.0.10.0/24"
}

# Service Account for API
module "api_service_account" {
  source = "./modules/service-account"

  project      = var.project
  name         = "api-${var.environment}"
  display_name = "API Service Account (${var.environment})"
  roles = [
    "roles/cloudsql.client",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
  ]
  secret_ids = [module.cloud_sql.password_secret_id]
}

# Cloud SQL
module "cloud_sql" {
  source = "./modules/cloud-sql"

  project           = var.project
  name              = "db-${var.environment}"
  region            = var.region
  network           = module.vpc.network_id
  availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
}

# VPC Connector for Cloud Run
resource "google_vpc_access_connector" "main" {
  project       = var.project
  name          = "connector-${var.environment}"
  region        = var.region
  network       = module.vpc.network_name
  ip_cidr_range = "10.8.0.0/28"
  min_instances = 2
  max_instances = 10
}

# Cloud Run
module "api" {
  source = "./modules/cloud-run"

  project               = var.project
  name                  = "api-${var.environment}"
  region                = var.region
  image                 = "us-central1-docker.pkg.dev/${var.project}/repo/api:latest"
  service_account_email = module.api_service_account.email
  vpc_connector_id      = google_vpc_access_connector.main.id
  min_instances         = var.environment == "prod" ? 1 : 0
  max_instances         = var.environment == "prod" ? 10 : 3

  env_vars = {
    ENVIRONMENT = var.environment
    DB_HOST     = module.cloud_sql.private_ip
    DB_NAME     = "db-${var.environment}"
    DB_USER     = "app"
  }

  secrets = {
    DB_PASSWORD = {
      secret_id = module.cloud_sql.password_secret_id
      version   = "latest"
    }
  }

  allow_unauthenticated = false
}
```

## Sources

- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [GCP Terraform Modules](https://github.com/terraform-google-modules)
- [Cloud Foundation Toolkit](https://cloud.google.com/foundation-toolkit)
- [GCP Best Practices for Terraform](https://cloud.google.com/docs/terraform/best-practices-for-terraform)

---

*GCP Templates | faion-infrastructure-engineer*
