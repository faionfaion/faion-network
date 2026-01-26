# GCP Architecture Patterns Examples

## GKE Cluster

### Regional Cluster with Private Nodes

```hcl
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
```

### General Purpose Node Pool

```hcl
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
      workload    = "general"
    }

    tags = ["gke-node", var.environment]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
```

### Spot Node Pool for Batch Workloads

```hcl
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

---

## Cloud SQL

### PostgreSQL with Regional HA

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

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = var.environment == "prod"
      backup_retention_settings {
        retained_backups = var.environment == "prod" ? 30 : 7
      }
    }

    maintenance_window {
      day          = 7  # Sunday
      hour         = 4
      update_track = "stable"
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
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

  depends_on = [google_service_networking_connection.private_vpc_connection]
}
```

### Read Replica

```hcl
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
```

---

## Cloud Storage and CDN

### Storage Bucket with Lifecycle Management

```hcl
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
```

### CDN Backend Bucket

```hcl
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
```

### Global HTTPS Load Balancer

```hcl
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

resource "google_compute_target_https_proxy" "main" {
  name             = "${var.project_id}-https-proxy"
  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

resource "google_compute_managed_ssl_certificate" "main" {
  name = "${var.project_id}-cert"

  managed {
    domains = ["static.${var.domain}"]
  }
}

resource "google_compute_global_forwarding_rule" "https" {
  name                  = "${var.project_id}-https-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.main.id
  ip_address            = google_compute_global_address.main.id
}
```

---

## Microservices on Cloud Run

### Cloud Run Service

```hcl
resource "google_cloud_run_v2_service" "api" {
  name     = "${var.project_id}-api"
  location = var.region

  template {
    service_account = google_service_account.api.email

    scaling {
      min_instance_count = var.environment == "prod" ? 2 : 0
      max_instance_count = 100
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/app/api:${var.image_tag}"

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
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

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_url.secret_id
            version = "latest"
          }
        }
      }
    }

    vpc_access {
      connector = google_vpc_access_connector.main.id
      egress    = "PRIVATE_RANGES_ONLY"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}
```

### Pub/Sub for Event-Driven Architecture

```hcl
resource "google_pubsub_topic" "orders" {
  name = "orders"

  message_retention_duration = "604800s"  # 7 days

  schema_settings {
    schema   = google_pubsub_schema.order.id
    encoding = "JSON"
  }
}

resource "google_pubsub_schema" "order" {
  name       = "order-schema"
  type       = "AVRO"
  definition = file("${path.module}/schemas/order.avsc")
}

resource "google_pubsub_subscription" "orders_push" {
  name  = "orders-push"
  topic = google_pubsub_topic.orders.id

  push_config {
    push_endpoint = google_cloud_run_v2_service.order_processor.uri

    oidc_token {
      service_account_email = google_service_account.pubsub_invoker.email
    }
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.orders_dlq.id
    max_delivery_attempts = 5
  }

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }

  ack_deadline_seconds = 60
}
```

---

## Data Pipeline

### Dataflow Streaming Pipeline

```hcl
resource "google_dataflow_flex_template_job" "streaming" {
  name                    = "events-to-bigquery"
  container_spec_gcs_path = "gs://${var.project_id}-dataflow/templates/events-streaming.json"
  region                  = var.region

  parameters = {
    inputSubscription = google_pubsub_subscription.events.id
    outputTable       = "${var.project_id}:analytics.events"
    tempLocation      = "gs://${var.project_id}-dataflow/temp"
  }

  environment {
    service_account_email = google_service_account.dataflow.email
    network               = google_compute_network.main.name
    subnetwork            = "regions/${var.region}/subnetworks/${google_compute_subnetwork.dataflow.name}"
    ip_configuration      = "WORKER_IP_PRIVATE"
    enable_streaming_engine = true
  }

  labels = {
    environment = var.environment
    pipeline    = "events-streaming"
  }
}
```

### BigQuery Dataset with Access Controls

```hcl
resource "google_bigquery_dataset" "analytics" {
  dataset_id  = "analytics"
  location    = var.region
  description = "Analytics data warehouse"

  default_partition_expiration_ms = 2592000000  # 30 days
  delete_contents_on_destroy      = false

  access {
    role          = "OWNER"
    user_by_email = google_service_account.dataflow.email
  }

  access {
    role           = "READER"
    group_by_email = var.analytics_group
  }

  labels = {
    environment = var.environment
  }
}

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "events"

  time_partitioning {
    type  = "DAY"
    field = "event_timestamp"
  }

  clustering = ["event_type", "user_id"]

  schema = file("${path.module}/schemas/events.json")

  labels = {
    environment = var.environment
  }
}
```

---

## Configuration Reference

### GKE Node Pool Strategies

| Pattern | Use Case | Node Type |
|---------|----------|-----------|
| General pool | Stateless apps, always-on services | Standard instances |
| Spot pool | Batch jobs, fault-tolerant workloads | Spot instances (60-91% cheaper) |
| GPU pool | ML inference, video processing | GPU-attached nodes |
| High-memory pool | Caching, in-memory databases | Memory-optimized instances |

### Cloud SQL Availability

| Environment | Configuration | RPO | RTO |
|-------------|---------------|-----|-----|
| Development | ZONAL, no replica | Hours | Minutes |
| Staging | REGIONAL, no replica | Seconds | Minutes |
| Production | REGIONAL + replica | 0 | Seconds |

### Storage Classes

| Class | Use Case | Retrieval | Monthly Cost/GB |
|-------|----------|-----------|-----------------|
| STANDARD | Frequently accessed | Instant | $0.020 |
| NEARLINE | < 1/month access | Instant | $0.010 |
| COLDLINE | < 1/quarter access | Instant | $0.004 |
| ARCHIVE | < 1/year access | Hours | $0.0012 |

---

*GCP Architecture Patterns Examples | faion-infrastructure-engineer*
