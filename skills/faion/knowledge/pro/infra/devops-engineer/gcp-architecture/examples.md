# GCP Architecture Examples

Terraform and gcloud examples for GCP architecture patterns including landing zones, GKE, Cloud SQL, and CDN.

---

## Landing Zone Examples

### Create Organization Structure (gcloud)

```bash
# Create folders for environments
gcloud resource-manager folders create \
    --display-name="Production" \
    --organization=ORGANIZATION_ID

gcloud resource-manager folders create \
    --display-name="Staging" \
    --organization=ORGANIZATION_ID

gcloud resource-manager folders create \
    --display-name="Development" \
    --organization=ORGANIZATION_ID

gcloud resource-manager folders create \
    --display-name="Shared Infrastructure" \
    --organization=ORGANIZATION_ID

# Create shared VPC host project
gcloud projects create shared-vpc-host-prod \
    --folder=SHARED_FOLDER_ID \
    --name="Shared VPC Host"

# Enable Shared VPC
gcloud compute shared-vpc enable shared-vpc-host-prod
```

### Organization Policies (gcloud)

```bash
# Restrict resource locations
gcloud org-policies set-policy policy.yaml --organization=ORGANIZATION_ID

# policy.yaml
# constraint: constraints/gcp.resourceLocations
# listPolicy:
#   allowedValues:
#     - in:us-locations
#     - in:europe-locations

# Disable service account key creation
gcloud org-policies set-policy - --organization=ORGANIZATION_ID <<EOF
constraint: constraints/iam.disableServiceAccountKeyCreation
booleanPolicy:
  enforced: true
EOF

# Require OS Login for VMs
gcloud org-policies set-policy - --organization=ORGANIZATION_ID <<EOF
constraint: constraints/compute.requireOsLogin
booleanPolicy:
  enforced: true
EOF

# Disable VM external IPs
gcloud org-policies set-policy - --organization=ORGANIZATION_ID <<EOF
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  allValues: DENY
EOF

# Disable default network
gcloud org-policies set-policy - --organization=ORGANIZATION_ID <<EOF
constraint: constraints/compute.skipDefaultNetworkCreation
booleanPolicy:
  enforced: true
EOF
```

---

## GKE Regional Cluster with Private Nodes

### Terraform

```hcl
# gke-regional-private.tf
resource "google_container_cluster" "main" {
  name     = "${var.project_id}-gke"
  location = var.region
  project  = var.project_id

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
      start_time = "2025-01-01T02:00:00Z"
      end_time   = "2025-01-01T06:00:00Z"
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

  # Deletion protection for production
  deletion_protection = var.environment == "production"

  resource_labels = {
    environment = var.environment
    team        = var.team
  }
}

# General node pool
resource "google_container_node_pool" "general" {
  name     = "general"
  location = var.region
  cluster  = google_container_cluster.main.name
  project  = var.project_id

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

# Spot node pool
resource "google_container_node_pool" "spot" {
  name     = "spot"
  location = var.region
  cluster  = google_container_cluster.main.name
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

### gcloud Equivalent

```bash
# Create private regional cluster
gcloud container clusters create my-cluster \
    --region=us-central1 \
    --node-locations=us-central1-a,us-central1-b,us-central1-c \
    --num-nodes=1 \
    --enable-private-nodes \
    --master-ipv4-cidr=172.16.0.0/28 \
    --enable-ip-alias \
    --network=my-vpc \
    --subnetwork=my-subnet \
    --cluster-secondary-range-name=pods \
    --services-secondary-range-name=services \
    --workload-pool=PROJECT_ID.svc.id.goog \
    --enable-master-authorized-networks \
    --master-authorized-networks=10.0.0.0/8 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10 \
    --release-channel=regular \
    --enable-shielded-nodes \
    --enable-network-policy \
    --enable-dataplane-v2

# Create spot node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --region=us-central1 \
    --spot \
    --num-nodes=0 \
    --enable-autoscaling \
    --min-nodes=0 \
    --max-nodes=20 \
    --machine-type=e2-standard-4
```

---

## Cloud SQL PostgreSQL with HA

### Terraform

```hcl
# cloud-sql-postgres.tf
resource "google_sql_database_instance" "main" {
  name             = "${var.project_id}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region
  project          = var.project_id

  deletion_protection = var.environment == "production"

  settings {
    tier              = var.environment == "production" ? "db-custom-4-16384" : "db-f1-micro"
    availability_type = var.environment == "production" ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    # Backup
    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = var.environment == "production"
      backup_retention_settings {
        retained_backups = var.environment == "production" ? 30 : 7
      }
      transaction_log_retention_days = var.environment == "production" ? 7 : 1
    }

    # Maintenance
    maintenance_window {
      day          = 7  # Sunday
      hour         = 4
      update_track = "stable"
    }

    # Network - private IP only
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    # Query Insights
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }

    # Database flags for logging
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
    database_flags {
      name  = "log_min_duration_statement"
      value = "1000"  # Log queries > 1 second
    }

    user_labels = {
      environment = var.environment
      team        = var.team
    }
  }

  depends_on = [google_service_networking_connection.private_vpc_connection]
}

# Read replica for production
resource "google_sql_database_instance" "replica" {
  count = var.environment == "production" ? 1 : 0

  name                 = "${var.project_id}-postgres-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = var.region
  database_version     = "POSTGRES_15"
  project              = var.project_id

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
  project  = var.project_id
}

# User with random password
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_sql_user" "main" {
  name     = var.database_user
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
  project  = var.project_id
}

# Store password in Secret Manager
resource "google_secret_manager_secret" "db_password" {
  secret_id = "${var.project_id}-db-password"
  project   = var.project_id

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}
```

### gcloud Equivalent

```bash
# Create PostgreSQL instance with HA
gcloud sql instances create my-postgres \
    --database-version=POSTGRES_15 \
    --tier=db-custom-4-16384 \
    --region=us-central1 \
    --availability-type=REGIONAL \
    --storage-type=SSD \
    --storage-size=100GB \
    --storage-auto-increase \
    --network=my-vpc \
    --no-assign-ip \
    --require-ssl \
    --backup \
    --backup-start-time=02:00 \
    --enable-point-in-time-recovery \
    --retained-backups-count=30

# Create database
gcloud sql databases create mydb --instance=my-postgres

# Create user
gcloud sql users create myuser \
    --instance=my-postgres \
    --password=SECURE_PASSWORD
```

---

## Cloud Storage with CDN

### Terraform

```hcl
# storage-cdn.tf
resource "google_storage_bucket" "static" {
  name     = "${var.project_id}-static"
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  # Lifecycle rules
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
    response_header = ["Content-Type", "Cache-Control"]
    max_age_seconds = 3600
  }

  labels = {
    environment = var.environment
    team        = var.team
  }
}

# Backend bucket for CDN
resource "google_compute_backend_bucket" "static" {
  name        = "${var.project_id}-static-backend"
  bucket_name = google_storage_bucket.static.name
  enable_cdn  = true
  project     = var.project_id

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600     # 1 hour
    max_ttl           = 86400    # 1 day
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

# Global IP address
resource "google_compute_global_address" "cdn" {
  name    = "${var.project_id}-cdn-ip"
  project = var.project_id
}

# Managed SSL certificate
resource "google_compute_managed_ssl_certificate" "cdn" {
  name    = "${var.project_id}-cdn-cert"
  project = var.project_id

  managed {
    domains = ["static.${var.domain}"]
  }
}

# URL map
resource "google_compute_url_map" "cdn" {
  name            = "${var.project_id}-cdn-url-map"
  default_service = google_compute_backend_bucket.static.id
  project         = var.project_id

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
resource "google_compute_target_https_proxy" "cdn" {
  name             = "${var.project_id}-cdn-https-proxy"
  url_map          = google_compute_url_map.cdn.id
  ssl_certificates = [google_compute_managed_ssl_certificate.cdn.id]
  project          = var.project_id
}

# Global forwarding rule
resource "google_compute_global_forwarding_rule" "cdn" {
  name                  = "${var.project_id}-cdn-https-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.cdn.id
  ip_address            = google_compute_global_address.cdn.id
  project               = var.project_id
}

# HTTP to HTTPS redirect
resource "google_compute_url_map" "http_redirect" {
  name    = "${var.project_id}-cdn-http-redirect"
  project = var.project_id

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "http_redirect" {
  name    = "${var.project_id}-cdn-http-proxy"
  url_map = google_compute_url_map.http_redirect.id
  project = var.project_id
}

resource "google_compute_global_forwarding_rule" "http_redirect" {
  name                  = "${var.project_id}-cdn-http-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_target_http_proxy.http_redirect.id
  ip_address            = google_compute_global_address.cdn.id
  project               = var.project_id
}

output "cdn_ip" {
  value = google_compute_global_address.cdn.address
}
```

### gcloud Equivalent

```bash
# Create bucket
gcloud storage buckets create gs://my-project-static \
    --location=us-central1 \
    --uniform-bucket-level-access

# Enable versioning
gcloud storage buckets update gs://my-project-static --versioning

# Create backend bucket with CDN
gcloud compute backend-buckets create static-backend \
    --gcs-bucket-name=my-project-static \
    --enable-cdn \
    --cache-mode=CACHE_ALL_STATIC \
    --default-ttl=3600 \
    --max-ttl=86400

# Create managed SSL certificate
gcloud compute ssl-certificates create cdn-cert \
    --domains=static.example.com \
    --global

# Create URL map
gcloud compute url-maps create cdn-url-map \
    --default-backend-bucket=static-backend

# Create HTTPS proxy
gcloud compute target-https-proxies create cdn-https-proxy \
    --url-map=cdn-url-map \
    --ssl-certificates=cdn-cert

# Reserve global IP
gcloud compute addresses create cdn-ip --global

# Create forwarding rule
gcloud compute forwarding-rules create cdn-https-rule \
    --global \
    --target-https-proxy=cdn-https-proxy \
    --ports=443 \
    --address=cdn-ip
```

---

## VPC with Shared VPC

### Terraform

```hcl
# shared-vpc.tf

# Host project VPC
resource "google_compute_network" "shared_vpc" {
  name                    = "shared-vpc"
  project                 = var.host_project_id
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

# Enable Shared VPC
resource "google_compute_shared_vpc_host_project" "host" {
  project = var.host_project_id
}

# Production subnet
resource "google_compute_subnetwork" "production" {
  name          = "production-subnet"
  project       = var.host_project_id
  region        = var.region
  network       = google_compute_network.shared_vpc.name
  ip_cidr_range = "10.0.0.0/20"

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.0.16.0/14"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.0.32.0/20"
  }

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Staging subnet
resource "google_compute_subnetwork" "staging" {
  name          = "staging-subnet"
  project       = var.host_project_id
  region        = var.region
  network       = google_compute_network.shared_vpc.name
  ip_cidr_range = "10.1.0.0/20"

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.16.0/14"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.1.32.0/20"
  }
}

# Attach service project
resource "google_compute_shared_vpc_service_project" "production" {
  host_project    = var.host_project_id
  service_project = var.production_project_id

  depends_on = [google_compute_shared_vpc_host_project.host]
}

# Grant network user role to service project
resource "google_project_iam_member" "production_network_user" {
  project = var.host_project_id
  role    = "roles/compute.networkUser"
  member  = "serviceAccount:${var.production_project_number}@cloudservices.gserviceaccount.com"
}

# Cloud Router
resource "google_compute_router" "router" {
  name    = "shared-vpc-router"
  project = var.host_project_id
  region  = var.region
  network = google_compute_network.shared_vpc.name
}

# Cloud NAT
resource "google_compute_router_nat" "nat" {
  name                               = "shared-vpc-nat"
  project                            = var.host_project_id
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# Firewall rules
resource "google_compute_firewall" "deny_all_ingress" {
  name     = "deny-all-ingress"
  project  = var.host_project_id
  network  = google_compute_network.shared_vpc.name
  priority = 65534

  direction = "INGRESS"

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_internal" {
  name     = "allow-internal"
  project  = var.host_project_id
  network  = google_compute_network.shared_vpc.name
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

resource "google_compute_firewall" "allow_iap" {
  name     = "allow-iap"
  project  = var.host_project_id
  network  = google_compute_network.shared_vpc.name
  priority = 1000

  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22", "3389"]
  }

  source_ranges = ["35.235.240.0/20"]  # IAP CIDR
  target_tags   = ["allow-iap"]
}
```

---

## Private Service Connect for Google APIs

### Terraform

```hcl
# private-service-connect.tf
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

# DNS zone for googleapis.com
resource "google_dns_managed_zone" "googleapis" {
  name        = "googleapis"
  project     = var.project_id
  dns_name    = "googleapis.com."
  description = "Private zone for Google APIs"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.id
    }
  }
}

resource "google_dns_record_set" "googleapis" {
  name         = "*.googleapis.com."
  project      = var.project_id
  managed_zone = google_dns_managed_zone.googleapis.name
  type         = "A"
  ttl          = 300
  rrdatas      = [google_compute_global_address.psc_apis.address]
}

# DNS zone for gcr.io
resource "google_dns_managed_zone" "gcr" {
  name        = "gcr-io"
  project     = var.project_id
  dns_name    = "gcr.io."
  description = "Private zone for GCR"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.id
    }
  }
}

resource "google_dns_record_set" "gcr" {
  name         = "*.gcr.io."
  project      = var.project_id
  managed_zone = google_dns_managed_zone.gcr.name
  type         = "A"
  ttl          = 300
  rrdatas      = [google_compute_global_address.psc_apis.address]
}
```

### gcloud Equivalent

```bash
# Reserve PSC address
gcloud compute addresses create psc-google-apis \
    --global \
    --purpose=PRIVATE_SERVICE_CONNECT \
    --network=my-vpc \
    --addresses=10.255.255.254

# Create PSC forwarding rule
gcloud compute forwarding-rules create psc-google-apis \
    --global \
    --network=my-vpc \
    --address=psc-google-apis \
    --target-google-apis-bundle=all-apis

# Create private DNS zone
gcloud dns managed-zones create googleapis \
    --dns-name="googleapis.com." \
    --visibility=private \
    --networks=my-vpc

# Create DNS record
gcloud dns record-sets create "*.googleapis.com." \
    --zone=googleapis \
    --type=A \
    --ttl=300 \
    --rrdatas=10.255.255.254
```

---

*GCP Architecture Examples v2.0 | Updated: 2026-01*
