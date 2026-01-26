# GCP Architecture Templates

Reusable Terraform modules and configuration templates for GCP landing zones and architecture patterns.

---

## Landing Zone Foundation Module

### Module Structure

```
modules/
  landing-zone/
    main.tf
    variables.tf
    outputs.tf
    folders.tf
    iam.tf
    networking.tf
    security.tf
```

### Main Configuration

```hcl
# modules/landing-zone/main.tf

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

# Enable required APIs
resource "google_project_service" "services" {
  for_each = toset([
    "compute.googleapis.com",
    "container.googleapis.com",
    "servicenetworking.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "dns.googleapis.com",
    "sqladmin.googleapis.com",
  ])

  project                    = var.project_id
  service                    = each.value
  disable_on_destroy         = false
  disable_dependent_services = false
}
```

### Variables

```hcl
# modules/landing-zone/variables.tf

variable "organization_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "billing_account" {
  description = "Billing account ID"
  type        = string
}

variable "project_id" {
  description = "Host project ID"
  type        = string
}

variable "region" {
  description = "Default region"
  type        = string
  default     = "us-central1"
}

variable "environments" {
  description = "List of environments to create"
  type        = list(string)
  default     = ["production", "staging", "development"]
}

variable "enable_shared_vpc" {
  description = "Enable Shared VPC"
  type        = bool
  default     = true
}

variable "vpc_cidr_ranges" {
  description = "CIDR ranges per environment"
  type = map(object({
    primary  = string
    pods     = string
    services = string
  }))
  default = {
    production = {
      primary  = "10.0.0.0/20"
      pods     = "10.0.16.0/14"
      services = "10.0.32.0/20"
    }
    staging = {
      primary  = "10.1.0.0/20"
      pods     = "10.1.16.0/14"
      services = "10.1.32.0/20"
    }
    development = {
      primary  = "10.2.0.0/20"
      pods     = "10.2.16.0/14"
      services = "10.2.32.0/20"
    }
  }
}

variable "admin_members" {
  description = "List of admin members"
  type        = list(string)
  default     = []
}

variable "labels" {
  description = "Labels to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### Folders

```hcl
# modules/landing-zone/folders.tf

# Environment folders
resource "google_folder" "environments" {
  for_each = toset(var.environments)

  display_name = title(each.value)
  parent       = "organizations/${var.organization_id}"
}

# Shared infrastructure folder
resource "google_folder" "shared" {
  display_name = "Shared Infrastructure"
  parent       = "organizations/${var.organization_id}"
}

# Output folder IDs
output "folder_ids" {
  value = {
    for env, folder in google_folder.environments : env => folder.id
  }
}

output "shared_folder_id" {
  value = google_folder.shared.id
}
```

### Networking

```hcl
# modules/landing-zone/networking.tf

# Main VPC
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  project                 = var.project_id
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"

  depends_on = [google_project_service.services]
}

# Subnets per environment
resource "google_compute_subnetwork" "subnets" {
  for_each = var.vpc_cidr_ranges

  name          = "${each.key}-subnet"
  project       = var.project_id
  region        = var.region
  network       = google_compute_network.main.name
  ip_cidr_range = each.value.primary

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = each.value.pods
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = each.value.services
  }

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud Router
resource "google_compute_router" "router" {
  name    = "main-router"
  project = var.project_id
  region  = var.region
  network = google_compute_network.main.name
}

# Cloud NAT
resource "google_compute_router_nat" "nat" {
  name                               = "main-nat"
  project                            = var.project_id
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# Private Service Access for managed services
resource "google_compute_global_address" "private_service_access" {
  name          = "private-service-access"
  project       = var.project_id
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.main.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.main.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_service_access.name]
}

# Shared VPC (optional)
resource "google_compute_shared_vpc_host_project" "host" {
  count   = var.enable_shared_vpc ? 1 : 0
  project = var.project_id

  depends_on = [google_project_service.services]
}
```

### Security

```hcl
# modules/landing-zone/security.tf

# Default firewall rules
resource "google_compute_firewall" "deny_all_ingress" {
  name     = "deny-all-ingress"
  project  = var.project_id
  network  = google_compute_network.main.name
  priority = 65534

  direction = "INGRESS"

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_internal" {
  name     = "allow-internal"
  project  = var.project_id
  network  = google_compute_network.main.name
  priority = 1000

  direction = "INGRESS"

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
}

resource "google_compute_firewall" "allow_iap_ssh" {
  name     = "allow-iap-ssh"
  project  = var.project_id
  network  = google_compute_network.main.name
  priority = 1000

  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["allow-iap"]
}

resource "google_compute_firewall" "allow_health_checks" {
  name     = "allow-health-checks"
  project  = var.project_id
  network  = google_compute_network.main.name
  priority = 1000

  direction = "INGRESS"

  allow {
    protocol = "tcp"
  }

  source_ranges = [
    "35.191.0.0/16",
    "130.211.0.0/22",
    "209.85.152.0/22",
    "209.85.204.0/22"
  ]

  target_tags = ["allow-health-check"]
}

# Private Service Connect for Google APIs
resource "google_compute_global_address" "psc_apis" {
  name         = "psc-google-apis"
  project      = var.project_id
  purpose      = "PRIVATE_SERVICE_CONNECT"
  address_type = "INTERNAL"
  network      = google_compute_network.main.id
  address      = "10.255.255.254"
}

resource "google_compute_global_forwarding_rule" "psc_apis" {
  name                  = "psc-google-apis"
  project               = var.project_id
  network               = google_compute_network.main.id
  ip_address            = google_compute_global_address.psc_apis.id
  target                = "all-apis"
  load_balancing_scheme = ""
}
```

### IAM

```hcl
# modules/landing-zone/iam.tf

# Organization-level IAM
resource "google_organization_iam_member" "org_admins" {
  for_each = toset(var.admin_members)

  org_id = var.organization_id
  role   = "roles/resourcemanager.organizationAdmin"
  member = each.value
}

# Project-level IAM for network admins
resource "google_project_iam_member" "network_admins" {
  for_each = toset(var.admin_members)

  project = var.project_id
  role    = "roles/compute.networkAdmin"
  member  = each.value
}

# GKE service account
resource "google_service_account" "gke_nodes" {
  account_id   = "gke-nodes"
  display_name = "GKE Node Service Account"
  project      = var.project_id
}

resource "google_project_iam_member" "gke_nodes_roles" {
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
```

### Outputs

```hcl
# modules/landing-zone/outputs.tf

output "vpc_id" {
  description = "VPC network ID"
  value       = google_compute_network.main.id
}

output "vpc_name" {
  description = "VPC network name"
  value       = google_compute_network.main.name
}

output "subnet_ids" {
  description = "Subnet IDs by environment"
  value = {
    for env, subnet in google_compute_subnetwork.subnets : env => subnet.id
  }
}

output "subnet_names" {
  description = "Subnet names by environment"
  value = {
    for env, subnet in google_compute_subnetwork.subnets : env => subnet.name
  }
}

output "nat_ip" {
  description = "Cloud NAT external IPs"
  value       = google_compute_router_nat.nat.nat_ips
}

output "gke_service_account" {
  description = "GKE nodes service account email"
  value       = google_service_account.gke_nodes.email
}

output "private_service_connection" {
  description = "Private service connection name"
  value       = google_service_networking_connection.private_vpc_connection.network
}
```

---

## GKE Cluster Module

```hcl
# modules/gke-cluster/main.tf

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "vpc_name" {
  type = string
}

variable "subnet_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "node_service_account" {
  type = string
}

variable "enable_autopilot" {
  type    = bool
  default = true
}

variable "master_authorized_cidr" {
  type    = string
  default = "10.0.0.0/8"
}

# Autopilot cluster
resource "google_container_cluster" "autopilot" {
  count = var.enable_autopilot ? 1 : 0

  name     = var.cluster_name
  location = var.region
  project  = var.project_id

  enable_autopilot = true

  network    = var.vpc_name
  subnetwork = var.subnet_name

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.master_authorized_cidr
      display_name = "Internal"
    }
  }

  release_channel {
    channel = "REGULAR"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2025-01-01T09:00:00Z"
      end_time   = "2025-01-01T17:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }

  resource_labels = {
    environment = var.environment
  }

  deletion_protection = var.environment == "production"
}

# Standard cluster
resource "google_container_cluster" "standard" {
  count = var.enable_autopilot ? 0 : 1

  name     = var.cluster_name
  location = var.region
  project  = var.project_id

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.vpc_name
  subnetwork = var.subnet_name

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.master_authorized_cidr
      display_name = "Internal"
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

  release_channel {
    channel = "REGULAR"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2025-01-01T09:00:00Z"
      end_time   = "2025-01-01T17:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
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

  enable_shielded_nodes = true

  resource_labels = {
    environment = var.environment
  }

  deletion_protection = var.environment == "production"
}

# Node pools for standard cluster
resource "google_container_node_pool" "general" {
  count = var.enable_autopilot ? 0 : 1

  name     = "general"
  location = var.region
  cluster  = google_container_cluster.standard[0].name
  project  = var.project_id

  autoscaling {
    min_node_count  = 1
    max_node_count  = 10
    location_policy = "BALANCED"
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-balanced"
    image_type   = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    service_account = var.node_service_account
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = {
      environment = var.environment
      pool        = "general"
    }

    tags = ["gke-node"]
  }
}

resource "google_container_node_pool" "spot" {
  count = var.enable_autopilot ? 0 : 1

  name     = "spot"
  location = var.region
  cluster  = google_container_cluster.standard[0].name
  project  = var.project_id

  autoscaling {
    min_node_count  = 0
    max_node_count  = 20
    location_policy = "ANY"
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    spot         = true
    machine_type = "n2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-balanced"
    image_type   = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    service_account = var.node_service_account
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = {
      environment = var.environment
      pool        = "spot"
    }

    taint {
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }

    tags = ["gke-node", "spot"]
  }
}

output "cluster_name" {
  value = var.enable_autopilot ? google_container_cluster.autopilot[0].name : google_container_cluster.standard[0].name
}

output "cluster_endpoint" {
  value     = var.enable_autopilot ? google_container_cluster.autopilot[0].endpoint : google_container_cluster.standard[0].endpoint
  sensitive = true
}
```

---

## Usage Example

```hcl
# main.tf

module "landing_zone" {
  source = "./modules/landing-zone"

  organization_id = "123456789012"
  billing_account = "XXXXXX-XXXXXX-XXXXXX"
  project_id      = "my-project"
  region          = "us-central1"

  environments     = ["production", "staging", "development"]
  enable_shared_vpc = true

  admin_members = [
    "group:platform-admins@example.com",
  ]

  labels = {
    managed_by = "terraform"
    team       = "platform"
  }
}

module "gke_production" {
  source = "./modules/gke-cluster"

  project_id           = "my-project"
  region               = "us-central1"
  cluster_name         = "production-cluster"
  vpc_name             = module.landing_zone.vpc_name
  subnet_name          = module.landing_zone.subnet_names["production"]
  environment          = "production"
  node_service_account = module.landing_zone.gke_service_account
  enable_autopilot     = true

  depends_on = [module.landing_zone]
}
```

---

## Organization Policy Templates

```yaml
# org-policies/security.yaml

# Disable service account key creation
- constraint: constraints/iam.disableServiceAccountKeyCreation
  enforcement: true

# Disable service account key upload
- constraint: constraints/iam.disableServiceAccountKeyUpload
  enforcement: true

# Require OS Login
- constraint: constraints/compute.requireOsLogin
  enforcement: true

# Restrict external IPs on VMs
- constraint: constraints/compute.vmExternalIpAccess
  listPolicy:
    deniedValues:
      - all

# Restrict resource locations
- constraint: constraints/gcp.resourceLocations
  listPolicy:
    allowedValues:
      - in:us-locations
      - in:europe-locations

# Skip default network creation
- constraint: constraints/compute.skipDefaultNetworkCreation
  enforcement: true

# Uniform bucket-level access
- constraint: constraints/storage.uniformBucketLevelAccess
  enforcement: true

# Disable public IP for Cloud SQL
- constraint: constraints/sql.restrictPublicIp
  enforcement: true
```

---

## Terraform Backend Configuration

```hcl
# backend.tf

terraform {
  backend "gcs" {
    bucket = "my-project-terraform-state"
    prefix = "landing-zone"
  }
}

# Create state bucket (run once)
resource "google_storage_bucket" "terraform_state" {
  name     = "${var.project_id}-terraform-state"
  location = var.region
  project  = var.project_id

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }
    action {
      type = "Delete"
    }
  }
}
```

---

*GCP Architecture Templates v2.0 | Updated: 2026-01*
