# GCP Cloud Storage Templates

## Terraform Templates

### Basic Bucket

```hcl
# variables.tf
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Name of the bucket"
  type        = string
}

# main.tf
resource "google_storage_bucket" "main" {
  name                        = var.bucket_name
  location                    = var.region
  project                     = var.project_id
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  labels = {
    environment = "production"
    managed_by  = "terraform"
  }
}

output "bucket_url" {
  value = google_storage_bucket.main.url
}

output "bucket_self_link" {
  value = google_storage_bucket.main.self_link
}
```

### Bucket with Lifecycle Rules

```hcl
resource "google_storage_bucket" "with_lifecycle" {
  name                        = "${var.project_id}-data-${var.environment}"
  location                    = var.region
  project                     = var.project_id
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  # Transition to Nearline after 30 days
  lifecycle_rule {
    condition {
      age                   = 30
      matches_storage_class = ["STANDARD"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  # Transition to Coldline after 90 days
  lifecycle_rule {
    condition {
      age                   = 90
      matches_storage_class = ["NEARLINE"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  # Transition to Archive after 365 days
  lifecycle_rule {
    condition {
      age                   = 365
      matches_storage_class = ["COLDLINE"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  # Delete old versions
  lifecycle_rule {
    condition {
      num_newer_versions = 3
      with_state         = "ARCHIVED"
    }
    action {
      type = "Delete"
    }
  }

  # Delete noncurrent versions after 90 days
  lifecycle_rule {
    condition {
      age        = 90
      with_state = "ARCHIVED"
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}
```

### Bucket with CMEK Encryption

```hcl
# KMS Keyring
resource "google_kms_key_ring" "storage" {
  name     = "${var.project_id}-storage-keyring"
  location = var.region
  project  = var.project_id
}

# KMS Key
resource "google_kms_crypto_key" "storage" {
  name            = "${var.project_id}-storage-key"
  key_ring        = google_kms_key_ring.storage.id
  rotation_period = "7776000s" # 90 days
  purpose         = "ENCRYPT_DECRYPT"

  lifecycle {
    prevent_destroy = true
  }
}

# Get project service account
data "google_storage_project_service_account" "gcs_account" {
  project = var.project_id
}

# Grant KMS access to GCS service account
resource "google_kms_crypto_key_iam_binding" "gcs_binding" {
  crypto_key_id = google_kms_crypto_key.storage.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"

  members = [
    "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}",
  ]
}

# Bucket with CMEK
resource "google_storage_bucket" "encrypted" {
  name                        = "${var.project_id}-secure-data"
  location                    = var.region
  project                     = var.project_id
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  encryption {
    default_kms_key_name = google_kms_crypto_key.storage.id
  }

  versioning {
    enabled = true
  }

  depends_on = [google_kms_crypto_key_iam_binding.gcs_binding]

  labels = {
    security    = "cmek"
    environment = var.environment
  }
}
```

### Bucket with Cloud CDN

```hcl
# Public bucket for CDN
resource "google_storage_bucket" "cdn" {
  name                        = "${var.project_id}-cdn-assets"
  location                    = "US"
  project                     = var.project_id
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  cors {
    origin          = ["https://example.com"]
    method          = ["GET", "HEAD"]
    response_header = ["Content-Type", "Cache-Control"]
    max_age_seconds = 3600
  }

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  labels = {
    purpose = "cdn"
  }
}

# Public access for CDN
resource "google_storage_bucket_iam_member" "cdn_public" {
  bucket = google_storage_bucket.cdn.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Backend bucket for CDN
resource "google_compute_backend_bucket" "cdn" {
  name        = "${var.project_id}-cdn-backend"
  bucket_name = google_storage_bucket.cdn.name
  enable_cdn  = true

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    client_ttl        = 3600
    default_ttl       = 3600
    max_ttl           = 86400
    negative_caching  = true
    serve_while_stale = 86400
  }
}

# URL map
resource "google_compute_url_map" "cdn" {
  name            = "${var.project_id}-cdn-url-map"
  default_service = google_compute_backend_bucket.cdn.id
}

# Managed SSL certificate
resource "google_compute_managed_ssl_certificate" "cdn" {
  name = "${var.project_id}-cdn-cert"

  managed {
    domains = ["cdn.${var.domain}"]
  }
}

# HTTPS proxy
resource "google_compute_target_https_proxy" "cdn" {
  name             = "${var.project_id}-cdn-https-proxy"
  url_map          = google_compute_url_map.cdn.id
  ssl_certificates = [google_compute_managed_ssl_certificate.cdn.id]
}

# Global forwarding rule
resource "google_compute_global_forwarding_rule" "cdn" {
  name       = "${var.project_id}-cdn-forwarding-rule"
  target     = google_compute_target_https_proxy.cdn.id
  port_range = "443"
}

output "cdn_ip" {
  value = google_compute_global_forwarding_rule.cdn.ip_address
}
```

### Module: Secure Application Bucket

```hcl
# modules/secure-bucket/variables.tf
variable "project_id" {
  type = string
}

variable "name" {
  type = string
}

variable "location" {
  type    = string
  default = "us-central1"
}

variable "storage_class" {
  type    = string
  default = "STANDARD"
}

variable "enable_versioning" {
  type    = bool
  default = true
}

variable "enable_cmek" {
  type    = bool
  default = false
}

variable "kms_key_id" {
  type    = string
  default = ""
}

variable "lifecycle_rules" {
  type = list(object({
    age                   = number
    storage_class         = string
    matches_storage_class = list(string)
  }))
  default = []
}

variable "service_accounts" {
  type        = list(string)
  default     = []
  description = "Service accounts to grant objectAdmin access"
}

variable "labels" {
  type    = map(string)
  default = {}
}

# modules/secure-bucket/main.tf
resource "google_storage_bucket" "main" {
  name                        = var.name
  location                    = var.location
  project                     = var.project_id
  storage_class               = var.storage_class
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = var.enable_versioning
  }

  dynamic "encryption" {
    for_each = var.enable_cmek && var.kms_key_id != "" ? [1] : []
    content {
      default_kms_key_name = var.kms_key_id
    }
  }

  dynamic "lifecycle_rule" {
    for_each = var.lifecycle_rules
    content {
      condition {
        age                   = lifecycle_rule.value.age
        matches_storage_class = lifecycle_rule.value.matches_storage_class
      }
      action {
        type          = "SetStorageClass"
        storage_class = lifecycle_rule.value.storage_class
      }
    }
  }

  labels = merge(var.labels, {
    managed_by = "terraform"
  })
}

resource "google_storage_bucket_iam_member" "service_accounts" {
  for_each = toset(var.service_accounts)

  bucket = google_storage_bucket.main.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${each.value}"
}

# modules/secure-bucket/outputs.tf
output "name" {
  value = google_storage_bucket.main.name
}

output "url" {
  value = google_storage_bucket.main.url
}

output "self_link" {
  value = google_storage_bucket.main.self_link
}
```

### Module Usage

```hcl
module "app_data_bucket" {
  source = "./modules/secure-bucket"

  project_id        = var.project_id
  name              = "${var.project_id}-app-data"
  location          = "us-central1"
  enable_versioning = true
  enable_cmek       = true
  kms_key_id        = google_kms_crypto_key.storage.id

  lifecycle_rules = [
    {
      age                   = 30
      storage_class         = "NEARLINE"
      matches_storage_class = ["STANDARD"]
    },
    {
      age                   = 365
      storage_class         = "COLDLINE"
      matches_storage_class = ["NEARLINE"]
    }
  ]

  service_accounts = [
    google_service_account.app.email
  ]

  labels = {
    environment = var.environment
    application = "my-app"
  }
}
```

## Lifecycle Configuration JSON Templates

### Standard Cost Optimization

```json
{
  "rule": [
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30, "matchesStorageClass": ["STANDARD"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 90, "matchesStorageClass": ["NEARLINE"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
      "condition": {"age": 365, "matchesStorageClass": ["COLDLINE"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 2555}
    }
  ]
}
```

### Compliance with Retention

```json
{
  "rule": [
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 90, "matchesStorageClass": ["STANDARD", "NEARLINE"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
      "condition": {"age": 365, "matchesStorageClass": ["COLDLINE"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 2555, "matchesStorageClass": ["ARCHIVE"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"numNewerVersions": 5, "isLive": false}
    }
  ]
}
```

### Temporary Files Cleanup

```json
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 1, "matchesPrefix": ["tmp/", "temp/", "cache/"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 7, "matchesSuffix": [".tmp", ".temp", ".bak"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"age": 30, "matchesPrefix": ["logs/"]}
    }
  ]
}
```

## gcloud Scripts

### Setup Script

```bash
#!/bin/bash
set -euo pipefail

PROJECT_ID="${1:?Usage: $0 <project-id> <bucket-name> <region>}"
BUCKET_NAME="${2:?Usage: $0 <project-id> <bucket-name> <region>}"
REGION="${3:-us-central1}"

echo "Creating bucket: gs://${BUCKET_NAME}"

# Create bucket
gcloud storage buckets create "gs://${BUCKET_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${REGION}" \
    --storage-class=standard \
    --uniform-bucket-level-access \
    --public-access-prevention

# Enable versioning
gcloud storage buckets update "gs://${BUCKET_NAME}" --versioning

# Apply lifecycle rules
cat > /tmp/lifecycle.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30, "matchesStorageClass": ["STANDARD"]}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
      "condition": {"age": 365, "matchesStorageClass": ["NEARLINE"]}
    },
    {
      "action": {"type": "Delete"},
      "condition": {"numNewerVersions": 3, "isLive": false}
    }
  ]
}
EOF

gcloud storage buckets update "gs://${BUCKET_NAME}" \
    --lifecycle-file=/tmp/lifecycle.json

echo "Bucket created and configured: gs://${BUCKET_NAME}"
```

### CMEK Setup Script

```bash
#!/bin/bash
set -euo pipefail

PROJECT_ID="${1:?Usage: $0 <project-id> <bucket-name> <region>}"
BUCKET_NAME="${2:?Usage: $0 <project-id> <bucket-name> <region>}"
REGION="${3:-us-central1}"
KEYRING_NAME="${BUCKET_NAME}-keyring"
KEY_NAME="${BUCKET_NAME}-key"

echo "Setting up CMEK encryption for bucket: ${BUCKET_NAME}"

# Create keyring
gcloud kms keyrings create "${KEYRING_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${REGION}" \
    2>/dev/null || echo "Keyring already exists"

# Create key
gcloud kms keys create "${KEY_NAME}" \
    --project="${PROJECT_ID}" \
    --keyring="${KEYRING_NAME}" \
    --location="${REGION}" \
    --purpose=encryption \
    --rotation-period=90d \
    2>/dev/null || echo "Key already exists"

# Get project number
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")

# Grant access to GCS service agent
gcloud kms keys add-iam-policy-binding "${KEY_NAME}" \
    --project="${PROJECT_ID}" \
    --keyring="${KEYRING_NAME}" \
    --location="${REGION}" \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com" \
    --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"

# Create bucket with CMEK
gcloud storage buckets create "gs://${BUCKET_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${REGION}" \
    --storage-class=standard \
    --uniform-bucket-level-access \
    --public-access-prevention \
    --default-encryption-key="projects/${PROJECT_ID}/locations/${REGION}/keyRings/${KEYRING_NAME}/cryptoKeys/${KEY_NAME}"

echo "CMEK-encrypted bucket created: gs://${BUCKET_NAME}"
```

---

*GCP Cloud Storage Templates v2.0*
