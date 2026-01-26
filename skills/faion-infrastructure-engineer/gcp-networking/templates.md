# GCP Networking Templates

## Terraform Templates

### Template 1: Complete VPC Module

```hcl
# modules/vpc/main.tf

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "subnets" {
  description = "List of subnets to create"
  type = list(object({
    name                  = string
    region                = string
    ip_cidr_range         = string
    secondary_ip_ranges   = optional(list(object({
      range_name    = string
      ip_cidr_range = string
    })), [])
  }))
}

variable "enable_flow_logs" {
  description = "Enable VPC flow logs"
  type        = bool
  default     = true
}

# VPC Network
resource "google_compute_network" "vpc" {
  project                 = var.project_id
  name                    = var.vpc_name
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

# Subnets
resource "google_compute_subnetwork" "subnets" {
  for_each = { for s in var.subnets : s.name => s }

  project       = var.project_id
  name          = each.value.name
  network       = google_compute_network.vpc.id
  region        = each.value.region
  ip_cidr_range = each.value.ip_cidr_range

  private_ip_google_access = true

  dynamic "secondary_ip_range" {
    for_each = each.value.secondary_ip_ranges
    content {
      range_name    = secondary_ip_range.value.range_name
      ip_cidr_range = secondary_ip_range.value.ip_cidr_range
    }
  }

  dynamic "log_config" {
    for_each = var.enable_flow_logs ? [1] : []
    content {
      aggregation_interval = "INTERVAL_5_SEC"
      flow_sampling        = 0.5
      metadata             = "INCLUDE_ALL_METADATA"
    }
  }
}

# Outputs
output "vpc_id" {
  value = google_compute_network.vpc.id
}

output "vpc_self_link" {
  value = google_compute_network.vpc.self_link
}

output "subnet_ids" {
  value = { for k, v in google_compute_subnetwork.subnets : k => v.id }
}
```

### Template 2: Firewall Rules Module

```hcl
# modules/firewall/main.tf

variable "project_id" {
  type = string
}

variable "network" {
  type = string
}

variable "enable_iap" {
  type    = bool
  default = true
}

variable "internal_ranges" {
  type    = list(string)
  default = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
}

# Allow IAP SSH
resource "google_compute_firewall" "allow_iap_ssh" {
  count   = var.enable_iap ? 1 : 0
  project = var.project_id
  name    = "${var.network}-allow-iap-ssh"
  network = var.network

  direction = "INGRESS"
  priority  = 100

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["ssh-iap"]

  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }
}

# Allow health checks
resource "google_compute_firewall" "allow_health_checks" {
  project = var.project_id
  name    = "${var.network}-allow-health-checks"
  network = var.network

  direction = "INGRESS"
  priority  = 200

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }

  source_ranges = [
    "130.211.0.0/22",
    "35.191.0.0/16"
  ]
  target_tags = ["lb-backend"]
}

# Allow internal traffic
resource "google_compute_firewall" "allow_internal" {
  project = var.project_id
  name    = "${var.network}-allow-internal"
  network = var.network

  direction = "INGRESS"
  priority  = 500

  allow {
    protocol = "tcp"
  }
  allow {
    protocol = "udp"
  }
  allow {
    protocol = "icmp"
  }

  source_ranges = var.internal_ranges
}

# Default deny ingress
resource "google_compute_firewall" "deny_all_ingress" {
  project = var.project_id
  name    = "${var.network}-deny-all-ingress"
  network = var.network

  direction = "INGRESS"
  priority  = 65534

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]

  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }
}
```

### Template 3: Cloud NAT Module

```hcl
# modules/cloud-nat/main.tf

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "network" {
  type = string
}

variable "name" {
  type = string
}

variable "subnetworks" {
  description = "Subnets to enable NAT for"
  type        = list(string)
  default     = []
}

variable "nat_ip_allocate_option" {
  description = "AUTO_ONLY or MANUAL_ONLY"
  type        = string
  default     = "AUTO_ONLY"
}

variable "nat_ips" {
  description = "List of self_links of external IPs (for MANUAL_ONLY)"
  type        = list(string)
  default     = []
}

# Cloud Router
resource "google_compute_router" "router" {
  project = var.project_id
  name    = "${var.name}-router"
  region  = var.region
  network = var.network

  bgp {
    asn = 64514
  }
}

# Cloud NAT
resource "google_compute_router_nat" "nat" {
  project = var.project_id
  name    = var.name
  router  = google_compute_router.router.name
  region  = var.region

  nat_ip_allocate_option = var.nat_ip_allocate_option
  nat_ips                = var.nat_ip_allocate_option == "MANUAL_ONLY" ? var.nat_ips : null

  source_subnetwork_ip_ranges_to_nat = length(var.subnetworks) > 0 ? "LIST_OF_SUBNETWORKS" : "ALL_SUBNETWORKS_ALL_IP_RANGES"

  dynamic "subnetwork" {
    for_each = var.subnetworks
    content {
      name                    = subnetwork.value
      source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
    }
  }

  min_ports_per_vm                 = 64
  max_ports_per_vm                 = 4096
  enable_endpoint_independent_mapping = false

  tcp_established_idle_timeout_sec = 1200
  tcp_transitory_idle_timeout_sec  = 30
  udp_idle_timeout_sec             = 30

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

output "router_name" {
  value = google_compute_router.router.name
}

output "nat_name" {
  value = google_compute_router_nat.nat.name
}
```

### Template 4: Global HTTPS Load Balancer

```hcl
# modules/https-lb/main.tf

variable "project_id" {
  type = string
}

variable "name" {
  type = string
}

variable "domains" {
  type = list(string)
}

variable "backend_service_name" {
  type = string
}

variable "health_check_path" {
  type    = string
  default = "/health"
}

variable "enable_cdn" {
  type    = bool
  default = false
}

variable "enable_cloud_armor" {
  type    = bool
  default = true
}

# Global IP
resource "google_compute_global_address" "lb_ip" {
  project = var.project_id
  name    = "${var.name}-ip"
}

# Health Check
resource "google_compute_health_check" "default" {
  project = var.project_id
  name    = "${var.name}-health-check"

  timeout_sec         = 5
  check_interval_sec  = 10
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 80
    request_path = var.health_check_path
  }
}

# Backend Service
resource "google_compute_backend_service" "default" {
  project = var.project_id
  name    = var.backend_service_name

  protocol    = "HTTP"
  port_name   = "http"
  timeout_sec = 30

  health_checks = [google_compute_health_check.default.id]

  enable_cdn = var.enable_cdn

  dynamic "cdn_policy" {
    for_each = var.enable_cdn ? [1] : []
    content {
      cache_mode                   = "CACHE_ALL_STATIC"
      default_ttl                  = 3600
      client_ttl                   = 3600
      max_ttl                      = 86400
      negative_caching             = true
      serve_while_stale            = 86400
    }
  }

  security_policy = var.enable_cloud_armor ? google_compute_security_policy.default[0].id : null

  log_config {
    enable      = true
    sample_rate = 1.0
  }
}

# Cloud Armor Security Policy
resource "google_compute_security_policy" "default" {
  count   = var.enable_cloud_armor ? 1 : 0
  project = var.project_id
  name    = "${var.name}-security-policy"

  # XSS Protection
  rule {
    action   = "deny(403)"
    priority = 1000
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('xss-v33-stable')"
      }
    }
    description = "Block XSS attacks"
  }

  # SQL Injection Protection
  rule {
    action   = "deny(403)"
    priority = 1001
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sqli-v33-stable')"
      }
    }
    description = "Block SQL injection attacks"
  }

  # Rate Limiting
  rule {
    action   = "throttle"
    priority = 2000
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      rate_limit_threshold {
        count        = 100
        interval_sec = 60
      }
    }
    description = "Rate limit to 100 requests per minute"
  }

  # Default allow
  rule {
    action   = "allow"
    priority = 2147483647
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    description = "Default allow rule"
  }
}

# Managed SSL Certificate
resource "google_compute_managed_ssl_certificate" "default" {
  project = var.project_id
  name    = "${var.name}-cert"

  managed {
    domains = var.domains
  }
}

# URL Map
resource "google_compute_url_map" "default" {
  project         = var.project_id
  name            = "${var.name}-url-map"
  default_service = google_compute_backend_service.default.id
}

# HTTPS Proxy
resource "google_compute_target_https_proxy" "default" {
  project          = var.project_id
  name             = "${var.name}-https-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

# Forwarding Rule
resource "google_compute_global_forwarding_rule" "default" {
  project    = var.project_id
  name       = "${var.name}-https-rule"
  target     = google_compute_target_https_proxy.default.id
  ip_address = google_compute_global_address.lb_ip.address
  port_range = "443"
}

# HTTP to HTTPS Redirect
resource "google_compute_url_map" "http_redirect" {
  project = var.project_id
  name    = "${var.name}-http-redirect"

  default_url_redirect {
    https_redirect = true
    strip_query    = false
  }
}

resource "google_compute_target_http_proxy" "http_redirect" {
  project = var.project_id
  name    = "${var.name}-http-proxy"
  url_map = google_compute_url_map.http_redirect.id
}

resource "google_compute_global_forwarding_rule" "http_redirect" {
  project    = var.project_id
  name       = "${var.name}-http-rule"
  target     = google_compute_target_http_proxy.http_redirect.id
  ip_address = google_compute_global_address.lb_ip.address
  port_range = "80"
}

output "lb_ip" {
  value = google_compute_global_address.lb_ip.address
}
```

---

## gcloud Script Templates

### Template 5: VPC Setup Script

```bash
#!/bin/bash
# setup-vpc.sh - Create production VPC with subnets

set -euo pipefail

# Configuration
PROJECT_ID="${PROJECT_ID:-my-project}"
VPC_NAME="${VPC_NAME:-production-vpc}"
REGIONS=("us-central1" "europe-west1" "asia-east1")

# Set project
gcloud config set project "$PROJECT_ID"

# Create VPC
echo "Creating VPC: $VPC_NAME"
gcloud compute networks create "$VPC_NAME" \
    --subnet-mode=custom \
    --bgp-routing-mode=global

# Create subnets
CIDR_BASE=0
for REGION in "${REGIONS[@]}"; do
    SUBNET_NAME="${VPC_NAME}-${REGION}"
    CIDR="10.${CIDR_BASE}.0.0/20"
    POD_CIDR="10.$((CIDR_BASE + 4)).0.0/14"
    SVC_CIDR="10.$((CIDR_BASE + 8)).0.0/20"

    echo "Creating subnet: $SUBNET_NAME ($CIDR)"
    gcloud compute networks subnets create "$SUBNET_NAME" \
        --network="$VPC_NAME" \
        --region="$REGION" \
        --range="$CIDR" \
        --secondary-range="pods=$POD_CIDR,services=$SVC_CIDR" \
        --enable-private-ip-google-access \
        --enable-flow-logs \
        --logging-aggregation-interval=interval-5-sec \
        --logging-flow-sampling=0.5

    CIDR_BASE=$((CIDR_BASE + 16))
done

echo "VPC setup complete!"
```

### Template 6: Firewall Setup Script

```bash
#!/bin/bash
# setup-firewall.sh - Configure secure firewall rules

set -euo pipefail

PROJECT_ID="${PROJECT_ID:-my-project}"
VPC_NAME="${VPC_NAME:-production-vpc}"

gcloud config set project "$PROJECT_ID"

echo "Creating firewall rules for $VPC_NAME"

# IAP SSH
gcloud compute firewall-rules create "${VPC_NAME}-allow-iap-ssh" \
    --network="$VPC_NAME" \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=35.235.240.0/20 \
    --target-tags=ssh-iap \
    --priority=100 \
    --enable-logging \
    --description="Allow SSH via IAP"

# Health checks
gcloud compute firewall-rules create "${VPC_NAME}-allow-health-checks" \
    --network="$VPC_NAME" \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:80,tcp:443,tcp:8080 \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-tags=lb-backend \
    --priority=200 \
    --description="Allow GCP health checks"

# Internal
gcloud compute firewall-rules create "${VPC_NAME}-allow-internal" \
    --network="$VPC_NAME" \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8 \
    --priority=500 \
    --description="Allow internal traffic"

# Default deny
gcloud compute firewall-rules create "${VPC_NAME}-deny-all-ingress" \
    --network="$VPC_NAME" \
    --direction=INGRESS \
    --action=DENY \
    --rules=all \
    --source-ranges=0.0.0.0/0 \
    --priority=65534 \
    --enable-logging \
    --description="Default deny all"

echo "Firewall rules created!"
```

### Template 7: Cloud NAT Setup Script

```bash
#!/bin/bash
# setup-nat.sh - Configure Cloud NAT for private instances

set -euo pipefail

PROJECT_ID="${PROJECT_ID:-my-project}"
VPC_NAME="${VPC_NAME:-production-vpc}"
REGIONS=("us-central1" "europe-west1")

gcloud config set project "$PROJECT_ID"

for REGION in "${REGIONS[@]}"; do
    ROUTER_NAME="${VPC_NAME}-nat-router-${REGION}"
    NAT_NAME="${VPC_NAME}-nat-${REGION}"

    echo "Creating Cloud Router: $ROUTER_NAME"
    gcloud compute routers create "$ROUTER_NAME" \
        --network="$VPC_NAME" \
        --region="$REGION"

    echo "Creating Cloud NAT: $NAT_NAME"
    gcloud compute routers nats create "$NAT_NAME" \
        --router="$ROUTER_NAME" \
        --region="$REGION" \
        --nat-all-subnet-ip-ranges \
        --auto-allocate-nat-external-ips \
        --min-ports-per-vm=64 \
        --enable-logging
done

echo "Cloud NAT setup complete!"
```

---

## YAML Templates

### Template 8: VPC Configuration YAML

```yaml
# vpc-config.yaml - VPC configuration for reference/automation

vpc:
  name: production-vpc
  project: my-project-id
  routing_mode: GLOBAL

subnets:
  - name: prod-us-central1
    region: us-central1
    ip_cidr_range: 10.0.0.0/20
    private_ip_google_access: true
    flow_logs:
      enabled: true
      aggregation_interval: INTERVAL_5_SEC
      flow_sampling: 0.5
    secondary_ranges:
      - name: pods
        ip_cidr_range: 10.4.0.0/14
      - name: services
        ip_cidr_range: 10.8.0.0/20

  - name: prod-europe-west1
    region: europe-west1
    ip_cidr_range: 10.16.0.0/20
    private_ip_google_access: true
    flow_logs:
      enabled: true
    secondary_ranges:
      - name: pods
        ip_cidr_range: 10.20.0.0/14
      - name: services
        ip_cidr_range: 10.24.0.0/20

firewall_rules:
  - name: allow-iap-ssh
    direction: INGRESS
    priority: 100
    action: ALLOW
    rules:
      - protocol: tcp
        ports: ["22"]
    source_ranges: ["35.235.240.0/20"]
    target_tags: ["ssh-iap"]
    logging: true

  - name: allow-health-checks
    direction: INGRESS
    priority: 200
    action: ALLOW
    rules:
      - protocol: tcp
        ports: ["80", "443", "8080"]
    source_ranges:
      - 130.211.0.0/22
      - 35.191.0.0/16
    target_tags: ["lb-backend"]

  - name: allow-internal
    direction: INGRESS
    priority: 500
    action: ALLOW
    rules:
      - protocol: tcp
      - protocol: udp
      - protocol: icmp
    source_ranges: ["10.0.0.0/8"]

  - name: deny-all-ingress
    direction: INGRESS
    priority: 65534
    action: DENY
    rules:
      - protocol: all
    source_ranges: ["0.0.0.0/0"]
    logging: true

cloud_nat:
  - name: nat-us-central1
    region: us-central1
    router: nat-router-us-central1
    nat_ip_allocate_option: AUTO_ONLY
    source_subnetwork_ip_ranges_to_nat: ALL_SUBNETWORKS_ALL_IP_RANGES
    min_ports_per_vm: 64
    max_ports_per_vm: 4096
    logging: true
```

---

*GCP Networking Templates | faion-infrastructure-engineer*
