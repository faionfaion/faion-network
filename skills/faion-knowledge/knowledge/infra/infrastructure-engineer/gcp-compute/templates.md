# GCP Compute Engine Templates

Terraform and YAML templates for VMs, instance groups, autoscaling, and Spot VMs.

## Terraform Templates

### Basic VM

```hcl
# Basic Compute Engine VM
resource "google_compute_instance" "default" {
  name         = "my-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
      size  = 50
      type  = "pd-balanced"
    }
  }

  network_interface {
    network    = "default"
    subnetwork = "default"

    # Remove for internal-only VM
    access_config {
      # Ephemeral public IP
    }
  }

  service_account {
    email  = google_service_account.vm_sa.email
    scopes = ["cloud-platform"]
  }

  tags = ["http-server", "https-server"]

  labels = {
    environment = "production"
    team        = "platform"
  }

  metadata_startup_script = file("${path.module}/scripts/startup.sh")
}
```

### Spot VM

```hcl
# Spot VM with termination handling
resource "google_compute_instance" "spot" {
  name         = "spot-worker"
  machine_type = "n2-standard-4"
  zone         = "us-central1-a"

  scheduling {
    preemptible                 = false
    provisioning_model          = "SPOT"
    instance_termination_action = "STOP"
    automatic_restart           = false
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
      size  = 50
      type  = "pd-balanced"
    }
  }

  network_interface {
    network    = "default"
    subnetwork = "default"
  }

  service_account {
    email  = google_service_account.spot_sa.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    shutdown-script = file("${path.module}/scripts/shutdown.sh")
  }

  labels = {
    provisioning = "spot"
    environment  = "batch"
  }
}
```

### Instance Template

```hcl
# Instance template for MIG
resource "google_compute_instance_template" "default" {
  name_prefix  = "app-template-"
  machine_type = "e2-medium"

  disk {
    source_image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
    auto_delete  = true
    boot         = true
    disk_size_gb = 50
    disk_type    = "pd-balanced"
  }

  network_interface {
    network    = google_compute_network.vpc.id
    subnetwork = google_compute_subnetwork.private.id
  }

  service_account {
    email  = google_service_account.app_sa.email
    scopes = ["cloud-platform"]
  }

  tags = ["app-server"]

  labels = {
    environment = var.environment
    version     = var.app_version
  }

  metadata = {
    startup-script = file("${path.module}/scripts/startup.sh")
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

### Spot Instance Template

```hcl
# Instance template for Spot VMs
resource "google_compute_instance_template" "spot" {
  name_prefix  = "spot-template-"
  machine_type = "n2-standard-4"

  scheduling {
    preemptible                 = false
    provisioning_model          = "SPOT"
    instance_termination_action = "STOP"
    automatic_restart           = false
  }

  disk {
    source_image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
    auto_delete  = true
    boot         = true
    disk_size_gb = 50
    disk_type    = "pd-balanced"
  }

  network_interface {
    network    = google_compute_network.vpc.id
    subnetwork = google_compute_subnetwork.private.id
  }

  service_account {
    email  = google_service_account.spot_sa.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    startup-script  = file("${path.module}/scripts/startup.sh")
    shutdown-script = file("${path.module}/scripts/shutdown.sh")
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

### Regional Managed Instance Group

```hcl
# Regional MIG with autoscaling
resource "google_compute_region_instance_group_manager" "app" {
  name   = "app-mig"
  region = "us-central1"

  base_instance_name = "app"

  version {
    instance_template = google_compute_instance_template.default.id
  }

  target_size = 3

  distribution_policy_zones = [
    "us-central1-a",
    "us-central1-b",
    "us-central1-c"
  ]

  distribution_policy_target_shape = "EVEN"

  named_port {
    name = "http"
    port = 8080
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.http.id
    initial_delay_sec = 300
  }

  update_policy {
    type                           = "PROACTIVE"
    minimal_action                 = "REPLACE"
    most_disruptive_allowed_action = "REPLACE"
    max_surge_fixed                = 3
    max_unavailable_fixed          = 0
    instance_redistribution_type   = "PROACTIVE"
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

### Autoscaler

```hcl
# CPU-based autoscaler
resource "google_compute_region_autoscaler" "app" {
  name   = "app-autoscaler"
  region = "us-central1"
  target = google_compute_region_instance_group_manager.app.id

  autoscaling_policy {
    min_replicas    = 3
    max_replicas    = 20
    cooldown_period = 60

    cpu_utilization {
      target            = 0.6
      predictive_method = "OPTIMIZE_AVAILABILITY"
    }

    scale_in_control {
      max_scaled_in_replicas {
        fixed = 2
      }
      time_window_sec = 600
    }
  }
}
```

### Multi-Signal Autoscaler

```hcl
# Autoscaler with multiple signals
resource "google_compute_region_autoscaler" "multi_signal" {
  name   = "multi-signal-autoscaler"
  region = "us-central1"
  target = google_compute_region_instance_group_manager.app.id

  autoscaling_policy {
    min_replicas    = 3
    max_replicas    = 50
    cooldown_period = 60

    # CPU signal
    cpu_utilization {
      target            = 0.6
      predictive_method = "OPTIMIZE_AVAILABILITY"
    }

    # Load balancing signal
    load_balancing_utilization {
      target = 0.8
    }

    # Custom metric signal
    metric {
      name   = "custom.googleapis.com/queue_messages"
      type   = "GAUGE"
      target = 100
    }

    scale_in_control {
      max_scaled_in_replicas {
        percent = 10
      }
      time_window_sec = 900
    }
  }
}
```

### Schedule-Based Autoscaler

```hcl
# Autoscaler with schedule
resource "google_compute_region_autoscaler" "scheduled" {
  name   = "scheduled-autoscaler"
  region = "us-central1"
  target = google_compute_region_instance_group_manager.app.id

  autoscaling_policy {
    min_replicas    = 2
    max_replicas    = 30
    cooldown_period = 60

    cpu_utilization {
      target = 0.6
    }

    scaling_schedules {
      name                  = "business-hours"
      min_required_replicas = 10
      schedule              = "0 9 * * MON-FRI"
      duration_sec          = 32400 # 9 hours
      time_zone             = "America/New_York"
    }

    scaling_schedules {
      name                  = "peak-traffic"
      min_required_replicas = 20
      schedule              = "0 12 * * *"
      duration_sec          = 7200 # 2 hours
      time_zone             = "America/New_York"
    }
  }
}
```

### Health Check

```hcl
# HTTP health check
resource "google_compute_health_check" "http" {
  name = "app-health-check"

  timeout_sec         = 5
  check_interval_sec  = 10
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}

# HTTPS health check
resource "google_compute_health_check" "https" {
  name = "app-https-health-check"

  timeout_sec         = 5
  check_interval_sec  = 10
  healthy_threshold   = 2
  unhealthy_threshold = 3

  https_health_check {
    port         = 443
    request_path = "/health"
  }
}
```

### Complete Module: Production MIG

```hcl
# variables.tf
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "environment" {
  type = string
}

variable "app_version" {
  type = string
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

variable "min_replicas" {
  type    = number
  default = 3
}

variable "max_replicas" {
  type    = number
  default = 20
}

variable "spot_enabled" {
  type    = bool
  default = false
}

# main.tf
resource "google_compute_instance_template" "app" {
  name_prefix  = "${var.environment}-app-"
  machine_type = var.machine_type
  project      = var.project_id

  dynamic "scheduling" {
    for_each = var.spot_enabled ? [1] : []
    content {
      preemptible                 = false
      provisioning_model          = "SPOT"
      instance_termination_action = "STOP"
      automatic_restart           = false
    }
  }

  disk {
    source_image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
    auto_delete  = true
    boot         = true
    disk_size_gb = 50
    disk_type    = "pd-balanced"
  }

  network_interface {
    network    = "default"
    subnetwork = "default"
  }

  service_account {
    email  = google_service_account.app.email
    scopes = ["cloud-platform"]
  }

  tags = ["${var.environment}-app"]

  labels = {
    environment = var.environment
    version     = var.app_version
    spot        = var.spot_enabled ? "true" : "false"
  }

  metadata = {
    startup-script  = file("${path.module}/scripts/startup.sh")
    shutdown-script = var.spot_enabled ? file("${path.module}/scripts/shutdown.sh") : ""
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_region_instance_group_manager" "app" {
  name    = "${var.environment}-app-mig"
  region  = var.region
  project = var.project_id

  base_instance_name = "${var.environment}-app"

  version {
    instance_template = google_compute_instance_template.app.id
  }

  target_size = var.min_replicas

  distribution_policy_target_shape = "EVEN"

  named_port {
    name = "http"
    port = 8080
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.app.id
    initial_delay_sec = 300
  }

  update_policy {
    type                           = "PROACTIVE"
    minimal_action                 = "REPLACE"
    most_disruptive_allowed_action = "REPLACE"
    max_surge_fixed                = 3
    max_unavailable_fixed          = 0
    instance_redistribution_type   = "PROACTIVE"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_region_autoscaler" "app" {
  name    = "${var.environment}-app-autoscaler"
  region  = var.region
  project = var.project_id
  target  = google_compute_region_instance_group_manager.app.id

  autoscaling_policy {
    min_replicas    = var.min_replicas
    max_replicas    = var.max_replicas
    cooldown_period = 60

    cpu_utilization {
      target            = 0.6
      predictive_method = "OPTIMIZE_AVAILABILITY"
    }

    scale_in_control {
      max_scaled_in_replicas {
        fixed = 2
      }
      time_window_sec = 600
    }
  }
}

resource "google_compute_health_check" "app" {
  name    = "${var.environment}-app-health-check"
  project = var.project_id

  timeout_sec         = 5
  check_interval_sec  = 10
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}

resource "google_service_account" "app" {
  account_id   = "${var.environment}-app-sa"
  display_name = "App Service Account for ${var.environment}"
  project      = var.project_id
}

# outputs.tf
output "instance_group" {
  value = google_compute_region_instance_group_manager.app.instance_group
}

output "instance_template" {
  value = google_compute_instance_template.app.id
}
```

---

## Startup/Shutdown Scripts

### Startup Script Template

```bash
#!/bin/bash
set -e

# startup.sh - VM initialization script

# Configure logging
exec 1> >(logger -s -t startup-script) 2>&1
echo "Starting initialization..."

# Update packages
apt-get update -qq

# Install dependencies
apt-get install -y -qq \
    docker.io \
    docker-compose \
    google-cloud-sdk

# Start Docker
systemctl enable docker
systemctl start docker

# Pull application image
REGISTRY="gcr.io/${PROJECT_ID}"
IMAGE="${REGISTRY}/app:${VERSION}"
docker pull "${IMAGE}"

# Start application
docker run -d \
    --name app \
    --restart unless-stopped \
    -p 8080:8080 \
    -e ENVIRONMENT="${ENVIRONMENT}" \
    "${IMAGE}"

# Signal ready
curl -s "http://localhost:8080/health" || exit 1

echo "Initialization complete"
```

### Shutdown Script Template (for Spot VMs)

```bash
#!/bin/bash
# shutdown.sh - Must complete within 30 seconds

# Log start
echo "Shutdown script started at $(date)" >> /var/log/shutdown.log

# Gracefully stop application
docker stop -t 10 app 2>/dev/null || true

# Save state to GCS
HOSTNAME=$(hostname)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BUCKET="gs://my-bucket/checkpoints"

if [ -f /var/lib/app/state.json ]; then
    gsutil -q cp /var/lib/app/state.json \
        "${BUCKET}/${HOSTNAME}/${TIMESTAMP}/state.json"
fi

# Mark shutdown complete
echo "Shutdown script completed at $(date)" >> /var/log/shutdown.log
```

---

## Kubernetes Manifests for Spot VMs

### Pod with Spot Toleration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: batch-worker
spec:
  nodeSelector:
    cloud.google.com/gke-spot: "true"
  tolerations:
    - key: cloud.google.com/gke-spot
      operator: Equal
      value: "true"
      effect: NoSchedule
  containers:
    - name: worker
      image: gcr.io/my-project/worker:latest
      resources:
        requests:
          cpu: "1"
          memory: "2Gi"
        limits:
          cpu: "2"
          memory: "4Gi"
```

### Deployment with Mixed Node Pools

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 10
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      # Prefer Spot nodes but can run on standard
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: cloud.google.com/gke-spot
                    operator: In
                    values:
                      - "true"
      tolerations:
        - key: cloud.google.com/gke-spot
          operator: Equal
          value: "true"
          effect: NoSchedule
      containers:
        - name: web
          image: gcr.io/my-project/web:latest
          ports:
            - containerPort: 8080
```

### PodDisruptionBudget for Spot

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
spec:
  minAvailable: 50%
  selector:
    matchLabels:
      app: web-app
```

---

*Templates v2.0 | GCP Compute Engine*
