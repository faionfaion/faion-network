# GCP Architecture Basics Templates

## Terraform: Organization Bootstrap

```hcl
# variables.tf
variable "org_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "billing_account" {
  description = "Billing account ID"
  type        = string
}

variable "region" {
  description = "Default region"
  type        = string
  default     = "europe-west1"
}

variable "environments" {
  description = "Environment folders to create"
  type        = list(string)
  default     = ["production", "staging", "development"]
}

# folders.tf
resource "google_folder" "bootstrap" {
  display_name = "bootstrap"
  parent       = "organizations/${var.org_id}"
}

resource "google_folder" "common" {
  display_name = "common"
  parent       = "organizations/${var.org_id}"
}

resource "google_folder" "environments" {
  for_each     = toset(var.environments)
  display_name = each.value
  parent       = "organizations/${var.org_id}"
}

# projects.tf - Seed project for Terraform state
resource "google_project" "seed" {
  name            = "Bootstrap Seed"
  project_id      = "prj-b-seed-${random_id.seed.hex}"
  folder_id       = google_folder.bootstrap.name
  billing_account = var.billing_account

  labels = {
    env        = "bootstrap"
    managed_by = "terraform"
  }

  auto_create_network = false
}

resource "random_id" "seed" {
  byte_length = 2
}

# Enable APIs for seed project
resource "google_project_service" "seed_apis" {
  for_each = toset([
    "cloudresourcemanager.googleapis.com",
    "cloudbilling.googleapis.com",
    "iam.googleapis.com",
    "serviceusage.googleapis.com",
    "storage.googleapis.com",
  ])

  project = google_project.seed.project_id
  service = each.value
}

# Terraform state bucket
resource "google_storage_bucket" "tfstate" {
  name     = "tfstate-${google_project.seed.project_id}"
  location = var.region
  project  = google_project.seed.project_id

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }
    action {
      type = "Delete"
    }
  }
}

# outputs.tf
output "seed_project_id" {
  value = google_project.seed.project_id
}

output "tfstate_bucket" {
  value = google_storage_bucket.tfstate.name
}

output "folder_ids" {
  value = {
    bootstrap   = google_folder.bootstrap.folder_id
    common      = google_folder.common.folder_id
    environments = { for k, v in google_folder.environments : k => v.folder_id }
  }
}
```

## Terraform: Project Factory Module

```hcl
# modules/project/variables.tf
variable "project_name" {
  description = "Human-readable project name"
  type        = string
}

variable "project_id_prefix" {
  description = "Project ID prefix"
  type        = string
}

variable "folder_id" {
  description = "Folder ID to place project in"
  type        = string
}

variable "billing_account" {
  description = "Billing account ID"
  type        = string
}

variable "environment" {
  description = "Environment (prod/staging/dev)"
  type        = string
}

variable "team" {
  description = "Team owning the project"
  type        = string
}

variable "cost_center" {
  description = "Cost center for billing"
  type        = string
}

variable "apis" {
  description = "List of APIs to enable"
  type        = list(string)
  default     = []
}

variable "iam_bindings" {
  description = "IAM bindings for project"
  type = map(object({
    role    = string
    members = list(string)
  }))
  default = {}
}

# modules/project/main.tf
resource "random_id" "project" {
  byte_length = 2
}

resource "google_project" "main" {
  name            = var.project_name
  project_id      = "${var.project_id_prefix}-${random_id.project.hex}"
  folder_id       = var.folder_id
  billing_account = var.billing_account

  labels = {
    env         = var.environment
    team        = var.team
    cost_center = var.cost_center
    managed_by  = "terraform"
  }

  auto_create_network = false
}

resource "google_project_service" "apis" {
  for_each = toset(var.apis)

  project = google_project.main.project_id
  service = each.value

  disable_dependent_services = false
  disable_on_destroy         = false
}

resource "google_project_iam_binding" "bindings" {
  for_each = var.iam_bindings

  project = google_project.main.project_id
  role    = each.value.role
  members = each.value.members
}

# modules/project/outputs.tf
output "project_id" {
  value = google_project.main.project_id
}

output "project_number" {
  value = google_project.main.number
}

output "project_name" {
  value = google_project.main.name
}
```

## Terraform: IAM Module

```hcl
# modules/iam/variables.tf
variable "project_id" {
  description = "Project ID"
  type        = string
}

variable "service_accounts" {
  description = "Service accounts to create"
  type = map(object({
    display_name = string
    description  = optional(string)
    roles        = list(string)
  }))
  default = {}
}

variable "workload_identity_bindings" {
  description = "Workload Identity bindings"
  type = map(object({
    namespace           = string
    kubernetes_sa       = string
    gcp_service_account = string
  }))
  default = {}
}

# modules/iam/main.tf
resource "google_service_account" "accounts" {
  for_each = var.service_accounts

  account_id   = each.key
  display_name = each.value.display_name
  description  = each.value.description
  project      = var.project_id
}

resource "google_project_iam_member" "sa_roles" {
  for_each = {
    for binding in flatten([
      for sa_key, sa in var.service_accounts : [
        for role in sa.roles : {
          key  = "${sa_key}-${role}"
          sa   = sa_key
          role = role
        }
      ]
    ]) : binding.key => binding
  }

  project = var.project_id
  role    = each.value.role
  member  = "serviceAccount:${google_service_account.accounts[each.value.sa].email}"
}

resource "google_service_account_iam_member" "workload_identity" {
  for_each = var.workload_identity_bindings

  service_account_id = google_service_account.accounts[each.value.gcp_service_account].name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${each.value.namespace}/${each.value.kubernetes_sa}]"
}

# modules/iam/outputs.tf
output "service_account_emails" {
  value = { for k, v in google_service_account.accounts : k => v.email }
}
```

## Terraform: Billing Budget

```hcl
# modules/billing/variables.tf
variable "billing_account" {
  description = "Billing account ID"
  type        = string
}

variable "project_id" {
  description = "Project ID to monitor"
  type        = string
}

variable "project_number" {
  description = "Project number"
  type        = string
}

variable "budget_amount" {
  description = "Monthly budget in USD"
  type        = number
}

variable "alert_emails" {
  description = "Email addresses for alerts"
  type        = list(string)
}

# modules/billing/main.tf
resource "google_monitoring_notification_channel" "email" {
  for_each = toset(var.alert_emails)

  project      = var.project_id
  display_name = "Budget Alert - ${each.value}"
  type         = "email"

  labels = {
    email_address = each.value
  }
}

resource "google_billing_budget" "project" {
  billing_account = var.billing_account
  display_name    = "Budget - ${var.project_id}"

  budget_filter {
    projects = ["projects/${var.project_number}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.budget_amount)
    }
  }

  threshold_rules {
    threshold_percent = 0.5
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.75
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.9
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "CURRENT_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      for channel in google_monitoring_notification_channel.email : channel.id
    ]
    disable_default_iam_recipients = false
  }
}
```

## Terraform: Organization Policies

```hcl
# modules/org-policies/variables.tf
variable "org_id" {
  description = "Organization ID"
  type        = string
}

variable "allowed_regions" {
  description = "Allowed GCP regions"
  type        = list(string)
  default     = ["in:europe-locations", "in:us-locations"]
}

variable "require_os_login" {
  description = "Require OS Login for VMs"
  type        = bool
  default     = true
}

variable "disable_sa_key_creation" {
  description = "Disable service account key creation"
  type        = bool
  default     = true
}

# modules/org-policies/main.tf
resource "google_org_policy_policy" "resource_locations" {
  name   = "organizations/${var.org_id}/policies/gcp.resourceLocations"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      values {
        allowed_values = var.allowed_regions
      }
    }
  }
}

resource "google_org_policy_policy" "require_os_login" {
  count  = var.require_os_login ? 1 : 0
  name   = "organizations/${var.org_id}/policies/compute.requireOsLogin"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}

resource "google_org_policy_policy" "disable_sa_key_creation" {
  count  = var.disable_sa_key_creation ? 1 : 0
  name   = "organizations/${var.org_id}/policies/iam.disableServiceAccountKeyCreation"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}

resource "google_org_policy_policy" "uniform_bucket_level_access" {
  name   = "organizations/${var.org_id}/policies/storage.uniformBucketLevelAccess"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}
```

## gcloud: Project Setup Script

```bash
#!/bin/bash
set -euo pipefail

# Variables
PROJECT_ID="${1:?Project ID required}"
FOLDER_ID="${2:?Folder ID required}"
BILLING_ACCOUNT="${3:?Billing account required}"
ENVIRONMENT="${4:-dev}"
TEAM="${5:-platform}"
COST_CENTER="${6:-cc-001}"

# Create project
gcloud projects create "$PROJECT_ID" \
  --folder="$FOLDER_ID" \
  --name="$PROJECT_ID" \
  --labels="env=$ENVIRONMENT,team=$TEAM,cost_center=$COST_CENTER,managed_by=gcloud"

# Link billing
gcloud billing projects link "$PROJECT_ID" \
  --billing-account="$BILLING_ACCOUNT"

# Enable common APIs
gcloud services enable \
  compute.googleapis.com \
  container.googleapis.com \
  cloudsql.googleapis.com \
  secretmanager.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  --project="$PROJECT_ID"

# Disable default service account
DEFAULT_SA="$(gcloud iam service-accounts list \
  --filter="email:compute@developer.gserviceaccount.com" \
  --format="value(email)" \
  --project="$PROJECT_ID")"

if [ -n "$DEFAULT_SA" ]; then
  gcloud iam service-accounts disable "$DEFAULT_SA" \
    --project="$PROJECT_ID" || true
fi

echo "Project $PROJECT_ID created successfully"
```

## Label Enforcement Policy Template

```hcl
# Required labels organization policy
resource "google_org_policy_custom_constraint" "require_labels" {
  name         = "organizations/${var.org_id}/customConstraints/custom.requireProjectLabels"
  parent       = "organizations/${var.org_id}"
  display_name = "Require Project Labels"
  description  = "Projects must have env, team, and cost_center labels"

  action_type    = "DENY"
  condition      = "!has(resource.labels.env) || !has(resource.labels.team) || !has(resource.labels.cost_center)"
  method_types   = ["CREATE", "UPDATE"]
  resource_types = ["cloudresourcemanager.googleapis.com/Project"]
}

resource "google_org_policy_policy" "require_labels" {
  name   = "organizations/${var.org_id}/policies/custom.requireProjectLabels"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }

  depends_on = [google_org_policy_custom_constraint.require_labels]
}
```

---

*GCP Architecture Basics Templates | faion-infrastructure-engineer*
