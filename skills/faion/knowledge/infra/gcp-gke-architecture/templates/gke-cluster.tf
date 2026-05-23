# templates/gke-cluster.tf
# GKE regional private cluster with general + spot node pools.
# Variables required: project_id, region, environment, team, admin_cidr
# References google_compute_network.main and google_compute_subnetwork.private from network module.

resource "google_container_cluster" "main" {
  name     = "${var.project_id}-gke"
  location = var.region
  project  = var.project_id

  node_locations = [
    "${var.region}-a",
    "${var.region}-b",
    "${var.region}-c"
  ]

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.private.name

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
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  release_channel {
    channel = "REGULAR"
  }

  maintenance_policy {
    recurring_window {
      start_time = "2025-01-01T02:00:00Z"
      end_time   = "2025-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SU"
    }
  }

  addons_config {
    http_load_balancing          { disabled = false }
    horizontal_pod_autoscaling   { disabled = false }
    gce_persistent_disk_csi_driver_config { enabled = true }
    gcs_fuse_csi_driver_config   { enabled = true }
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
    managed_prometheus { enabled = true }
  }

  remove_default_node_pool = true
  initial_node_count       = 1
  enable_shielded_nodes    = true
  deletion_protection      = var.environment == "production"

  resource_labels = {
    environment = var.environment
    team        = var.team
  }
}

resource "google_container_node_pool" "general" {
  name       = "general"
  location   = var.region
  cluster    = google_container_cluster.main.name
  project    = var.project_id
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
    image_type   = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config { mode = "GKE_METADATA" }

    service_account = google_service_account.gke_nodes.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels   = { environment = var.environment, workload = "general" }
    tags     = ["gke-node", var.environment]
    metadata = { disable-legacy-endpoints = "true" }
  }
}

resource "google_container_node_pool" "spot" {
  name    = "spot"
  location = var.region
  cluster = google_container_cluster.main.name
  project = var.project_id

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
    image_type   = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config { mode = "GKE_METADATA" }

    service_account = google_service_account.gke_nodes.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = { environment = var.environment, workload = "spot" }

    taint {
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  }
}
