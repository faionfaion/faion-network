---
id: gcp-arch-patterns
name: "GCP Architecture Patterns"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# GCP Architecture Patterns

## Overview

Advanced GCP architectural patterns for GKE clusters, Cloud SQL databases, and Cloud Storage with CDN. This methodology covers production-ready configurations for container orchestration, database management, and content delivery.

## When to Use

- Deploying production GKE clusters
- Setting up highly available databases
- Implementing global CDN for static assets
- Multi-zone and multi-region deployments

## GKE Cluster

### Regional Cluster with Private Nodes

```hcl
# GKE Cluster
resource "google_container_cluster" "main" {
  name     = "${var.project_id}-gke"
  location = var.region

  # Regional cluster for high availability
  node_locations = [
    "${var.region}-a",
    "${var.region}-b",
    "${var.region}-c"
  ]

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.private.name

  # VPC-native cluster
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"

    master_global_access_config {
      enabled = true
    }
  }

  # Master authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.admin_cidr
      display_name = "Admin access"
    }
  }

  # Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Binary Authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Release channel
  release_channel {
    channel = "REGULAR"
  }

  # Maintenance window
  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SU"
    }
  }

  # Cluster addons
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
    gcs_fuse_csi_driver_config {
      enabled = true
    }
  }

  # Enable Dataplane V2 (eBPF)
  datapath_provider = "ADVANCED_DATAPATH"

  # Network policy
  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  # Logging and monitoring
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  # Remove default node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  # Security
  enable_shielded_nodes = true
}

# Node pool
resource "google_container_node_pool" "general" {
  name     = "general"
  location = var.region
  cluster  = google_container_cluster.main.name

  node_count = 1

  autoscaling {
    min_node_count  = 1
    max_node_count  = 10
    location_policy = "BALANCED"
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
    preemptible  = false
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"

    # Use containerd
    image_type = "COS_CONTAINERD"

    # Security
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    # Workload Identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    # Service account
    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
      workload    = "general"
    }

    tags = ["gke-node", var.environment]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

# Spot node pool
resource "google_container_node_pool" "spot" {
  name     = "spot"
  location = var.region
  cluster  = google_container_cluster.main.name

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
    machine_type = "e2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-standard"

    image_type = "COS_CONTAINERD"

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

    labels = {
      environment = var.environment
      workload    = "spot"
    }

    taint {
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  }
}
```

## Cloud SQL

### PostgreSQL with Regional HA and Read Replicas

```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project_id}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region

  deletion_protection = var.environment == "prod"

  settings {
    tier              = var.environment == "prod" ? "db-custom-4-16384" : "db-f1-micro"
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    # Backup
    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = var.environment == "prod"
      backup_retention_settings {
        retained_backups = var.environment == "prod" ? 30 : 7
      }
    }

    # Maintenance
    maintenance_window {
      day          = 7  # Sunday
      hour         = 4
      update_track = "stable"
    }

    # Network
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    # Insights
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }

    # Flags
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

  depends_on = [google_service_networking_connection.private_vpc_connection]
}

# Read replica for production
resource "google_sql_database_instance" "replica" {
  count = var.environment == "prod" ? 1 : 0

  name                 = "${var.project_id}-postgres-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = var.region
  database_version     = "POSTGRES_15"

  replica_configuration {
    failover_target = true
  }

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }
  }
}

# Database
resource "google_sql_database" "main" {
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}

# User
resource "google_sql_user" "main" {
  name     = var.database_user
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
```

## Cloud Storage and CDN

### Global CDN with Lifecycle Management

```hcl
# Storage bucket
resource "google_storage_bucket" "static" {
  name     = "${var.project_id}-static"
  location = var.region

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }

  cors {
    origin          = ["https://${var.domain}"]
    method          = ["GET", "HEAD"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

# CDN Backend bucket
resource "google_compute_backend_bucket" "static" {
  name        = "${var.project_id}-static-backend"
  bucket_name = google_storage_bucket.static.name
  enable_cdn  = true

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    max_ttl           = 86400
    client_ttl        = 3600
    negative_caching  = true
    serve_while_stale = 86400

    cache_key_policy {
      include_host         = true
      include_protocol     = true
      include_query_string = false
    }
  }
}

# URL map
resource "google_compute_url_map" "main" {
  name            = "${var.project_id}-url-map"
  default_service = google_compute_backend_bucket.static.id

  host_rule {
    hosts        = ["static.${var.domain}"]
    path_matcher = "static"
  }

  path_matcher {
    name            = "static"
    default_service = google_compute_backend_bucket.static.id
  }
}

# HTTPS proxy
resource "google_compute_target_https_proxy" "main" {
  name             = "${var.project_id}-https-proxy"
  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

# SSL certificate
resource "google_compute_managed_ssl_certificate" "main" {
  name = "${var.project_id}-cert"

  managed {
    domains = ["static.${var.domain}"]
  }
}

# Global forwarding rule
resource "google_compute_global_forwarding_rule" "https" {
  name                  = "${var.project_id}-https-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.main.id
  ip_address            = google_compute_global_address.main.id
}
```

## Configuration Patterns

### GKE Node Pool Strategies

| Pattern | Use Case | Node Type |
|---------|----------|-----------|
| General pool | Stateless apps, always-on services | Standard instances |
| Spot pool | Batch jobs, fault-tolerant workloads | Spot instances (80% cheaper) |
| GPU pool | ML inference, video processing | GPU-attached nodes |
| High-memory pool | Caching, in-memory databases | Memory-optimized instances |

### Cloud SQL Availability

| Environment | Configuration | RPO | RTO |
|-------------|---------------|-----|-----|
| Development | ZONAL, no replica | Hours | Minutes |
| Staging | REGIONAL, no replica | Seconds | Minutes |
| Production | REGIONAL + replica | 0 | Seconds |

### Storage Classes

| Class | Use Case | Latency | Cost |
|-------|----------|---------|------|
| STANDARD | Frequently accessed data | ms | $$$ |
| NEARLINE | < 1/month access | ms | $$ |
| COLDLINE | < 1/quarter access | ms | $ |
| ARCHIVE | < 1/year access | ms | ¢ |

## References

- [GKE Node Pool Design](https://cloud.google.com/kubernetes-engine/docs/concepts/node-pools)
- [Cloud SQL High Availability](https://cloud.google.com/sql/docs/postgres/high-availability)
- [Cloud Storage Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle)
- [Cloud CDN Best Practices](https://cloud.google.com/cdn/docs/best-practices)

## Sources

- [GCP Reference Architectures](https://cloud.google.com/architecture)
- [GCP Solutions](https://cloud.google.com/solutions)
- [Microservices on GCP](https://cloud.google.com/solutions/microservices)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
