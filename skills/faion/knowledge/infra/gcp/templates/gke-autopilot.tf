# GKE Autopilot cluster with Workload Identity + private networking
# Autopilot: Google manages nodes, automatic resource requests, enforced security
terraform {
  required_providers {
    google = { source = "hashicorp/google"; version = "~> 5.0" }
  }
}

variable "project_id" { type = string }
variable "region" { type = string; default = "us-central1" }
variable "cluster_name" { type = string; default = "autopilot-cluster" }
variable "network" { type = string; default = "default" }
variable "subnetwork" { type = string; default = "default" }

# Autopilot cluster — recommended over Standard for most workloads
resource "google_container_cluster" "autopilot" {
  name     = var.cluster_name
  project  = var.project_id
  location = var.region   # regional (multi-zone) for HA

  enable_autopilot = true

  # Private cluster: nodes have no public IPs
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false          # keep public API endpoint (use authorized networks)
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "10.0.0.0/8"           # allow internal VPC
      display_name = "internal"
    }
    # Add your CI/CD NAT IP here for kubectl access from pipelines
  }

  network    = var.network
  subnetwork = var.subnetwork

  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/17"
    services_ipv4_cidr_block = "/22"
  }

  # Workload Identity: enables Kubernetes SA → GCP SA binding
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Binary Authorization: require signed container images
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Shield nodes from rootkit/bootkit attacks
  # (Autopilot: shielded nodes always enabled, config here for documentation)
  release_channel {
    channel = "REGULAR"  # RAPID for latest, STABLE for conservative
  }

  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }

  # Vertical Pod Autoscaling included in Autopilot
  vertical_pod_autoscaling {
    enabled = true
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
    managed_prometheus {
      enabled = true    # Google-managed Prometheus (no operator needed)
    }
  }

  deletion_protection = true   # prevent accidental terraform destroy
}

# GCP Service Account for workloads (linked to K8s SA via WI)
resource "google_service_account" "workload" {
  account_id   = "gke-workload"
  display_name = "GKE Workload Service Account"
  project      = var.project_id
}

# Bind K8s SA to GCP SA (Workload Identity binding)
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.workload.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[production/myapp]"
  # Format: serviceAccount:<project>.svc.id.goog[<k8s-namespace>/<k8s-sa-name>]
}

# Grant workload SA access to needed resources (principle of least privilege)
resource "google_project_iam_member" "workload_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.workload.email}"
  condition {
    title      = "only-own-secrets"
    expression = "resource.name.startsWith(\"projects/${var.project_id}/secrets/myapp-\")"
  }
}

output "cluster_endpoint" {
  value     = google_container_cluster.autopilot.endpoint
  sensitive = true
}

output "workload_sa_email" {
  value = google_service_account.workload.email
}
