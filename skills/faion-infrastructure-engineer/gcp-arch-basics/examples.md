# GCP Architecture Basics Examples

## Resource Hierarchy Examples

### Enterprise Organization Structure

```
acme-corp (Organization)
├── bootstrap/
│   ├── prj-b-seed            # Terraform state, automation
│   └── prj-b-cicd            # CI/CD pipelines
│
├── common/
│   ├── prj-c-logging         # Centralized logging
│   ├── prj-c-monitoring      # Shared monitoring
│   ├── prj-c-networking-hub  # Hub VPC, interconnect
│   └── prj-c-security        # Security tools
│
├── production/
│   ├── prj-p-app1            # Production app 1
│   ├── prj-p-app2            # Production app 2
│   └── prj-p-data            # Production data platform
│
├── staging/
│   ├── prj-s-app1            # Staging app 1
│   ├── prj-s-app2            # Staging app 2
│   └── prj-s-data            # Staging data platform
│
└── development/
    ├── prj-d-app1            # Development app 1
    ├── prj-d-app2            # Development app 2
    └── prj-d-sandbox         # Developer sandbox
```

### Startup Organization Structure

```
startup-io (Organization)
├── shared/
│   └── prj-shared-infra      # Shared networking, logging
│
├── prod/
│   └── prj-prod-main         # Production workloads
│
└── nonprod/
    ├── prj-staging           # Staging environment
    └── prj-dev               # Development environment
```

### Multi-Team Organization

```
company-xyz (Organization)
├── platform/
│   ├── prj-platform-prod     # Platform team prod
│   └── prj-platform-dev      # Platform team dev
│
├── team-alpha/
│   ├── prj-alpha-prod        # Team Alpha prod
│   └── prj-alpha-dev         # Team Alpha dev
│
└── team-beta/
    ├── prj-beta-prod         # Team Beta prod
    └── prj-beta-dev          # Team Beta dev
```

## IAM Examples

### Organization-Level IAM

```bash
# Assign Organization Admin (break-glass)
gcloud organizations add-iam-policy-binding ORG_ID \
  --member="user:admin@company.com" \
  --role="roles/resourcemanager.organizationAdmin" \
  --condition="expression=request.time < timestamp('2025-12-31T00:00:00Z'),title=temporary-access"

# Assign Billing Admin
gcloud organizations add-iam-policy-binding ORG_ID \
  --member="group:billing-admins@company.com" \
  --role="roles/billing.admin"

# Assign Security Reviewer (read-only)
gcloud organizations add-iam-policy-binding ORG_ID \
  --member="group:security-team@company.com" \
  --role="roles/iam.securityReviewer"
```

### Folder-Level IAM

```bash
# Grant folder admin to team lead
gcloud resource-manager folders add-iam-policy-binding FOLDER_ID \
  --member="user:lead@company.com" \
  --role="roles/resourcemanager.folderAdmin"

# Grant project creator to developers in folder
gcloud resource-manager folders add-iam-policy-binding FOLDER_ID \
  --member="group:developers@company.com" \
  --role="roles/resourcemanager.projectCreator"
```

### Project-Level IAM

```bash
# Grant Editor to team
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="group:team@company.com" \
  --role="roles/editor"

# Grant specific role with condition
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:app@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer" \
  --condition="expression=resource.name.startsWith('projects/_/buckets/my-bucket'),title=bucket-access-only"
```

### Workload Identity Setup

```bash
# Create service account
gcloud iam service-accounts create app-sa \
  --display-name="Application Service Account" \
  --project=PROJECT_ID

# Grant Workload Identity binding
gcloud iam service-accounts add-iam-policy-binding \
  app-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"

# Grant required permissions to SA
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:app-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

## Project Setup Examples

### Create Project with Labels

```bash
# Create project in folder
gcloud projects create prj-prod-app1 \
  --folder=FOLDER_ID \
  --name="Production App 1" \
  --labels="env=prod,team=platform,cost-center=cc-001"

# Link billing account
gcloud billing projects link prj-prod-app1 \
  --billing-account=BILLING_ACCOUNT_ID

# Enable required APIs
gcloud services enable \
  compute.googleapis.com \
  container.googleapis.com \
  cloudsql.googleapis.com \
  secretmanager.googleapis.com \
  --project=prj-prod-app1
```

### Terraform Project Configuration

```hcl
# Project with proper configuration
resource "google_project" "app" {
  name            = "Production App 1"
  project_id      = "prj-prod-app1"
  folder_id       = google_folder.production.name
  billing_account = var.billing_account

  labels = {
    env         = "prod"
    team        = "platform"
    cost_center = "cc-001"
    managed_by  = "terraform"
  }

  auto_create_network = false  # Disable default VPC
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "compute.googleapis.com",
    "container.googleapis.com",
    "cloudsql.googleapis.com",
    "secretmanager.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
  ])

  project = google_project.app.project_id
  service = each.value

  disable_dependent_services = false
  disable_on_destroy         = false
}
```

## Billing Examples

### Budget Alert Configuration

```bash
# Create budget with alerts
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Project Monthly Budget" \
  --budget-amount=1000USD \
  --threshold-rules="percent=0.5,basis=current-spend" \
  --threshold-rules="percent=0.9,basis=current-spend" \
  --threshold-rules="percent=1.0,basis=current-spend" \
  --filter-projects="projects/PROJECT_ID" \
  --notifications-rule="monitoringNotificationChannels=CHANNEL_ID"
```

### Terraform Budget

```hcl
resource "google_billing_budget" "project" {
  billing_account = var.billing_account
  display_name    = "Monthly Budget - ${google_project.app.name}"

  budget_filter {
    projects = ["projects/${google_project.app.number}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "1000"
    }
  }

  threshold_rules {
    threshold_percent = 0.5
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
      google_monitoring_notification_channel.email.id
    ]
    disable_default_iam_recipients = false
  }
}
```

## Organization Policy Examples

### Enforce Labels

```hcl
resource "google_org_policy_policy" "require_labels" {
  name   = "organizations/${var.org_id}/policies/compute.requireLabels"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}
```

### Restrict VM External IP

```hcl
resource "google_org_policy_policy" "vm_external_ip" {
  name   = "organizations/${var.org_id}/policies/compute.vmExternalIpAccess"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      deny_all = "TRUE"
    }
  }
}

# Allow exception for specific folder
resource "google_org_policy_policy" "vm_external_ip_exception" {
  name   = "folders/${google_folder.dmz.folder_id}/policies/compute.vmExternalIpAccess"
  parent = "folders/${google_folder.dmz.folder_id}"

  spec {
    rules {
      allow_all = "TRUE"
    }
  }
}
```

### Restrict Resource Locations

```hcl
resource "google_org_policy_policy" "resource_locations" {
  name   = "organizations/${var.org_id}/policies/gcp.resourceLocations"
  parent = "organizations/${var.org_id}"

  spec {
    rules {
      values {
        allowed_values = [
          "in:europe-locations",
          "in:us-locations"
        ]
      }
    }
  }
}
```

## Naming Convention Examples

### Standard Naming Pattern

```
{resource-type}-{environment}-{application}-{component}

Examples:
- prj-prod-ecommerce           # Project
- vpc-prod-ecommerce           # VPC
- gke-prod-ecommerce-primary   # GKE cluster
- sql-prod-ecommerce-main      # Cloud SQL
- sa-prod-ecommerce-api        # Service account
- bkt-prod-ecommerce-assets    # Storage bucket
```

### Label Standards

```yaml
Required Labels:
  env: prod|staging|dev
  team: platform|backend|frontend|data
  cost_center: cc-NNN
  managed_by: terraform|manual

Optional Labels:
  app: application-name
  component: api|web|worker
  owner: team-email
```

---

*GCP Architecture Basics Examples | faion-infrastructure-engineer*
