# templates/shared-vpc.tf
# Shared VPC host project, subnets with secondary ranges, Cloud NAT,
# firewall rules, and service project attachment.
# Variables required: host_project_id, production_project_id, production_project_number, region

resource "google_compute_network" "shared_vpc" {
  name                    = "shared-vpc"
  project                 = var.host_project_id
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_shared_vpc_host_project" "host" {
  project = var.host_project_id
}

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

resource "google_compute_shared_vpc_service_project" "production" {
  host_project    = var.host_project_id
  service_project = var.production_project_id

  depends_on = [google_compute_shared_vpc_host_project.host]
}

resource "google_project_iam_member" "production_network_user" {
  project = var.host_project_id
  role    = "roles/compute.networkUser"
  member  = "serviceAccount:${var.production_project_number}@cloudservices.gserviceaccount.com"
}

resource "google_compute_router" "router" {
  name    = "shared-vpc-router"
  project = var.host_project_id
  region  = var.region
  network = google_compute_network.shared_vpc.name
}

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

resource "google_compute_firewall" "deny_all_ingress" {
  name     = "deny-all-ingress"
  project  = var.host_project_id
  network  = google_compute_network.shared_vpc.name
  priority = 65534
  direction = "INGRESS"
  deny { protocol = "all" }
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_internal" {
  name     = "allow-internal"
  project  = var.host_project_id
  network  = google_compute_network.shared_vpc.name
  priority = 1000
  direction = "INGRESS"
  allow { protocol = "tcp" }
  allow { protocol = "udp" }
  allow { protocol = "icmp" }
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
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["allow-iap"]
}
