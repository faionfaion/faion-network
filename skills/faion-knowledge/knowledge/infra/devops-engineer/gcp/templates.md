# GCP Templates

Reusable configuration templates for Google Cloud Platform infrastructure.

---

## Terraform Templates

### GKE Autopilot Cluster

```hcl
# gke-autopilot.tf
resource "google_container_cluster" "autopilot" {
  name     = var.cluster_name
  location = var.region
  project  = var.project_id

  # Enable Autopilot
  enable_autopilot = true

  # Network configuration
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # IP allocation
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Maintenance window
  maintenance_policy {
    recurring_window {
      start_time = "2025-01-01T09:00:00Z"
      end_time   = "2025-01-01T17:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }

  # Release channel
  release_channel {
    channel = "REGULAR"
  }

  # Resource labels
  resource_labels = {
    environment = var.environment
    team        = var.team
  }

  # Deletion protection
  deletion_protection = var.environment == "production" ? true : false
}

variable "cluster_name" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "project_id" {
  type = string
}

variable "environment" {
  type = string
}

variable "team" {
  type = string
}
```

### GKE Standard Cluster with Node Pools

```hcl
# gke-standard.tf
resource "google_container_cluster" "standard" {
  name     = var.cluster_name
  location = var.zone
  project  = var.project_id

  # Remove default node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  # Network configuration
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # IP allocation
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Addons
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

  # Maintenance window
  maintenance_policy {
    recurring_window {
      start_time = "2025-01-01T09:00:00Z"
      end_time   = "2025-01-01T17:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SA,SU"
    }
  }

  # Release channel
  release_channel {
    channel = "REGULAR"
  }
}

# General-purpose node pool
resource "google_container_node_pool" "general" {
  name       = "general"
  cluster    = google_container_cluster.standard.name
  location   = var.zone
  project    = var.project_id

  # Autoscaling
  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-balanced"

    # Workload Identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      pool = "general"
    }

    tags = ["gke-node"]
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}

# Spot node pool for batch workloads
resource "google_container_node_pool" "spot" {
  name       = "spot"
  cluster    = google_container_cluster.standard.name
  location   = var.zone
  project    = var.project_id

  autoscaling {
    min_node_count = 0
    max_node_count = 20
  }

  node_config {
    machine_type = "n2-standard-8"
    spot         = true
    disk_size_gb = 100
    disk_type    = "pd-balanced"

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      pool = "spot"
    }

    taint {
      key    = "cloud.google.com/gke-spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }

    tags = ["gke-node", "spot"]
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}
```

### VPC with Subnets

```hcl
# vpc.tf
resource "google_compute_network" "vpc" {
  name                    = var.vpc_name
  project                 = var.project_id
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.vpc_name}-subnet"
  project       = var.project_id
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = var.subnet_cidr

  # Private Google Access
  private_ip_google_access = true

  # Secondary ranges for GKE
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = var.pods_cidr
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = var.services_cidr
  }

  # VPC Flow Logs
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud NAT for private instances
resource "google_compute_router" "router" {
  name    = "${var.vpc_name}-router"
  project = var.project_id
  region  = var.region
  network = google_compute_network.vpc.name
}

resource "google_compute_router_nat" "nat" {
  name                               = "${var.vpc_name}-nat"
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

variable "vpc_name" {
  type = string
}

variable "subnet_cidr" {
  type    = string
  default = "10.0.0.0/24"
}

variable "pods_cidr" {
  type    = string
  default = "10.1.0.0/16"
}

variable "services_cidr" {
  type    = string
  default = "10.2.0.0/20"
}
```

### Cloud Run Service

```hcl
# cloud-run.tf
resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  project  = var.project_id
  location = var.region
  ingress  = var.public ? "INGRESS_TRAFFIC_ALL" : "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.image

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
        cpu_idle = var.cpu_idle
      }

      # Environment variables
      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      # Secrets
      dynamic "env" {
        for_each = var.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret
              version = env.value.version
            }
          }
        }
      }

      ports {
        container_port = var.port
      }

      startup_probe {
        http_get {
          path = "/health"
          port = var.port
        }
        initial_delay_seconds = 5
        timeout_seconds       = 3
        period_seconds        = 10
        failure_threshold     = 3
      }
    }

    # VPC connector for private resources
    dynamic "vpc_access" {
      for_each = var.vpc_connector != null ? [1] : []
      content {
        connector = var.vpc_connector
        egress    = "ALL_TRAFFIC"
      }
    }

    # Service account
    service_account = var.service_account
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# IAM binding for public access
resource "google_cloud_run_v2_service_iam_member" "public" {
  count    = var.public ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

variable "service_name" {
  type = string
}

variable "image" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "cpu" {
  type    = string
  default = "1"
}

variable "memory" {
  type    = string
  default = "512Mi"
}

variable "min_instances" {
  type    = number
  default = 0
}

variable "max_instances" {
  type    = number
  default = 10
}

variable "port" {
  type    = number
  default = 8080
}

variable "public" {
  type    = bool
  default = false
}

variable "cpu_idle" {
  type    = bool
  default = true
}

variable "env_vars" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  type = map(object({
    secret  = string
    version = string
  }))
  default = {}
}

variable "vpc_connector" {
  type    = string
  default = null
}

variable "service_account" {
  type    = string
  default = null
}
```

### Workload Identity Federation (GitHub Actions)

```hcl
# workload-identity-github.tf
resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Pool for GitHub Actions workflows"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions Provider"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository_owner == '${var.github_org}'"
}

resource "google_service_account" "github_actions" {
  project      = var.project_id
  account_id   = "github-actions"
  display_name = "GitHub Actions Service Account"
}

resource "google_service_account_iam_member" "github_actions_wif" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_org}/${var.github_repo}"
}

# Grant necessary roles to service account
resource "google_project_iam_member" "github_actions_roles" {
  for_each = toset(var.github_actions_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.github_actions.email}"
}

variable "github_org" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "github_actions_roles" {
  type = list(string)
  default = [
    "roles/run.developer",
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser"
  ]
}

output "workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}

output "service_account_email" {
  value = google_service_account.github_actions.email
}
```

---

## Kubernetes Manifests

### Workload Identity ServiceAccount

```yaml
# workload-identity-sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
  annotations:
    iam.gke.io/gcp-service-account: my-gsa@PROJECT_ID.iam.gserviceaccount.com
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      serviceAccountName: my-app
      containers:
        - name: my-app
          image: gcr.io/PROJECT_ID/my-app:latest
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

### HPA with Custom Metrics

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### VPA Configuration

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: default
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"  # or "Off" for recommendations only
  resourcePolicy:
    containerPolicies:
      - containerName: my-app
        minAllowed:
          cpu: "50m"
          memory: "64Mi"
        maxAllowed:
          cpu: "2"
          memory: "4Gi"
        controlledResources: ["cpu", "memory"]
```

### Network Policy

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-app-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### Pod Disruption Budget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
  namespace: default
spec:
  minAvailable: 1
  # or: maxUnavailable: 1
  selector:
    matchLabels:
      app: my-app
```

---

## GitHub Actions Workflow

### Deploy to Cloud Run

```yaml
# .github/workflows/deploy-cloud-run.yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: my-project
  REGION: us-central1
  SERVICE: my-service
  REPOSITORY: my-repo

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: github-actions@${{ env.PROJECT_ID }}.iam.gserviceaccount.com

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Configure Docker
        run: gcloud auth configure-docker ${{ env.REGION }}-docker.pkg.dev

      - name: Build and Push
        run: |
          docker build -t ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.SERVICE }}:${{ github.sha }} .
          docker push ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.SERVICE }}:${{ github.sha }}

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ${{ env.SERVICE }} \
            --image=${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.SERVICE }}:${{ github.sha }} \
            --region=${{ env.REGION }} \
            --platform=managed \
            --allow-unauthenticated
```

### Deploy to GKE

```yaml
# .github/workflows/deploy-gke.yaml
name: Deploy to GKE

on:
  push:
    branches: [main]

env:
  PROJECT_ID: my-project
  REGION: us-central1
  CLUSTER: my-cluster
  NAMESPACE: default
  DEPLOYMENT: my-app

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: github-actions@${{ env.PROJECT_ID }}.iam.gserviceaccount.com

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Install GKE auth plugin
        run: gcloud components install gke-gcloud-auth-plugin

      - name: Get GKE credentials
        run: |
          gcloud container clusters get-credentials ${{ env.CLUSTER }} \
            --region=${{ env.REGION }} \
            --project=${{ env.PROJECT_ID }}

      - name: Configure Docker
        run: gcloud auth configure-docker ${{ env.REGION }}-docker.pkg.dev

      - name: Build and Push
        run: |
          docker build -t ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/images/${{ env.DEPLOYMENT }}:${{ github.sha }} .
          docker push ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/images/${{ env.DEPLOYMENT }}:${{ github.sha }}

      - name: Deploy to GKE
        run: |
          kubectl set image deployment/${{ env.DEPLOYMENT }} \
            ${{ env.DEPLOYMENT }}=${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/images/${{ env.DEPLOYMENT }}:${{ github.sha }} \
            -n ${{ env.NAMESPACE }}
          kubectl rollout status deployment/${{ env.DEPLOYMENT }} -n ${{ env.NAMESPACE }}
```

---

## Cloud Storage Lifecycle Policy

```json
{
  "rule": [
    {
      "action": {
        "type": "SetStorageClass",
        "storageClass": "NEARLINE"
      },
      "condition": {
        "age": 30,
        "matchesStorageClass": ["STANDARD"]
      }
    },
    {
      "action": {
        "type": "SetStorageClass",
        "storageClass": "COLDLINE"
      },
      "condition": {
        "age": 90,
        "matchesStorageClass": ["NEARLINE"]
      }
    },
    {
      "action": {
        "type": "SetStorageClass",
        "storageClass": "ARCHIVE"
      },
      "condition": {
        "age": 365,
        "matchesStorageClass": ["COLDLINE"]
      }
    },
    {
      "action": {
        "type": "Delete"
      },
      "condition": {
        "age": 2555,
        "matchesStorageClass": ["ARCHIVE"]
      }
    },
    {
      "action": {
        "type": "Delete"
      },
      "condition": {
        "numNewerVersions": 3,
        "isLive": false
      }
    }
  ]
}
```

---

*GCP Templates v2.0 | Updated: 2026-01*
