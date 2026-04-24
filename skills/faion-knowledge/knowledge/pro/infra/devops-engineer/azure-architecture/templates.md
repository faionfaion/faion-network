# Azure Architecture Templates

Reusable templates for Azure Landing Zones, Governance, and Well-Architected implementations.

## Table of Contents

1. [Naming Conventions](#naming-conventions)
2. [Tagging Strategy](#tagging-strategy)
3. [Variables Template](#variables-template)
4. [Locals Template](#locals-template)
5. [Module Structure](#module-structure)
6. [Landing Zone Template](#landing-zone-template)
7. [ADR Templates](#adr-templates)
8. [Governance Documents](#governance-documents)

---

## Naming Conventions

### Resource Naming Pattern

```
{resource-prefix}-{project}-{environment}-{region}-{instance}
```

### Naming Table

| Resource Type | Prefix | Example |
|---------------|--------|---------|
| Resource Group | rg | rg-contoso-prod-weu-001 |
| Virtual Network | vnet | vnet-contoso-prod-weu-001 |
| Subnet | snet | snet-contoso-prod-weu-app |
| Network Security Group | nsg | nsg-contoso-prod-weu-app |
| Route Table | rt | rt-contoso-prod-weu-001 |
| Public IP | pip | pip-contoso-prod-weu-001 |
| Load Balancer | lb | lb-contoso-prod-weu-001 |
| Application Gateway | agw | agw-contoso-prod-weu-001 |
| Azure Firewall | afw | afw-contoso-prod-weu-001 |
| VPN Gateway | vgw | vgw-contoso-prod-weu-001 |
| ExpressRoute Gateway | ergw | ergw-contoso-prod-weu-001 |
| Azure Bastion | bas | bas-contoso-prod-weu-001 |
| Virtual Machine | vm | vm-contoso-prod-weu-001 |
| VM Scale Set | vmss | vmss-contoso-prod-weu-001 |
| Availability Set | avail | avail-contoso-prod-weu-001 |
| AKS Cluster | aks | aks-contoso-prod-weu-001 |
| Container Registry | cr | crcontosoprodweu001 |
| Storage Account | st | stcontosoprodweu001 |
| Key Vault | kv | kv-contoso-prod-weu-001 |
| Log Analytics | log | log-contoso-prod-weu-001 |
| Application Insights | appi | appi-contoso-prod-weu-001 |
| SQL Server | sql | sql-contoso-prod-weu-001 |
| SQL Database | sqldb | sqldb-contoso-prod-weu-001 |
| PostgreSQL Server | psql | psql-contoso-prod-weu-001 |
| Cosmos DB | cosmos | cosmos-contoso-prod-weu-001 |
| Service Bus | sb | sb-contoso-prod-weu-001 |
| Event Hub | evh | evh-contoso-prod-weu-001 |
| Function App | func | func-contoso-prod-weu-001 |
| App Service | app | app-contoso-prod-weu-001 |
| App Service Plan | asp | asp-contoso-prod-weu-001 |
| API Management | apim | apim-contoso-prod-weu-001 |
| Front Door | fd | fd-contoso-prod-001 |
| CDN Profile | cdn | cdn-contoso-prod-001 |
| User Assigned Identity | id | id-contoso-prod-weu-001 |

### Region Codes

| Region | Code |
|--------|------|
| West Europe | weu |
| North Europe | neu |
| Germany West Central | gwc |
| UK South | uks |
| East US | eus |
| West US | wus |
| Southeast Asia | sea |

---

## Tagging Strategy

### Required Tags

```hcl
locals {
  required_tags = {
    Environment   = var.environment           # dev, staging, prod
    Project       = var.project               # Project name
    CostCenter    = var.cost_center           # Financial tracking
    Owner         = var.owner                 # Team/person responsible
    ManagedBy     = "Terraform"               # IaC tool
    CreatedDate   = formatdate("YYYY-MM-DD", timestamp())
  }
}
```

### Optional Tags

```hcl
locals {
  optional_tags = {
    Application   = var.application           # Application name
    BusinessUnit  = var.business_unit         # Business unit
    Criticality   = var.criticality           # High, Medium, Low
    DataClass     = var.data_classification   # Public, Internal, Confidential
    Compliance    = var.compliance            # GDPR, SOC2, HIPAA
    SLA           = var.sla                   # 99.9%, 99.95%, 99.99%
  }
}
```

### Combined Tags

```hcl
locals {
  common_tags = merge(
    local.required_tags,
    var.additional_tags
  )
}
```

---

## Variables Template

### variables.tf

```hcl
# -----------------------------------------------------------------------------
# General
# -----------------------------------------------------------------------------

variable "project" {
  description = "Project name for resource naming"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project))
    error_message = "Project name must be lowercase alphanumeric with hyphens."
  }
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "westeurope"
}

variable "location_short" {
  description = "Short code for Azure region"
  type        = string
  default     = "weu"
}

# -----------------------------------------------------------------------------
# Tags
# -----------------------------------------------------------------------------

variable "cost_center" {
  description = "Cost center for billing"
  type        = string
}

variable "owner" {
  description = "Owner email or team name"
  type        = string
}

variable "additional_tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}

# -----------------------------------------------------------------------------
# Networking
# -----------------------------------------------------------------------------

variable "address_space" {
  description = "VNet address space"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_prefixes" {
  description = "Subnet address prefixes"
  type        = map(string)
  default = {
    app              = "10.0.1.0/24"
    database         = "10.0.2.0/24"
    private_endpoints = "10.0.3.0/24"
  }
}

# -----------------------------------------------------------------------------
# AKS
# -----------------------------------------------------------------------------

variable "kubernetes_version" {
  description = "Kubernetes version for AKS"
  type        = string
  default     = "1.29"
}

variable "aks_admin_group_id" {
  description = "Microsoft Entra ID group ID for AKS administrators"
  type        = string
}

variable "authorized_ip_ranges" {
  description = "Authorized IP ranges for AKS API server"
  type        = list(string)
  default     = []
}

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

variable "db_admin_username" {
  description = "Database administrator username"
  type        = string
  default     = "pgadmin"
}

variable "database_name" {
  description = "Database name"
  type        = string
  default     = "app"
}

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------

variable "allowed_ips" {
  description = "IP addresses allowed through network rules"
  type        = list(string)
  default     = []
}
```

---

## Locals Template

### locals.tf

```hcl
locals {
  # Naming
  name_prefix = "${var.project}-${var.environment}-${var.location_short}"

  # Tags
  common_tags = {
    Environment = var.environment
    Project     = var.project
    CostCenter  = var.cost_center
    Owner       = var.owner
    ManagedBy   = "Terraform"
    Repository  = var.repository_url
  }

  # Environment-specific settings
  is_production = var.environment == "prod"

  # SKU mappings
  sku_map = {
    dev = {
      aks_vm_size     = "Standard_D2s_v5"
      aks_node_count  = 1
      postgres_sku    = "B_Standard_B2s"
      storage_tier    = "Standard_LRS"
    }
    staging = {
      aks_vm_size     = "Standard_D4s_v5"
      aks_node_count  = 2
      postgres_sku    = "GP_Standard_D2s_v3"
      storage_tier    = "Standard_LRS"
    }
    prod = {
      aks_vm_size     = "Standard_D4s_v5"
      aks_node_count  = 3
      postgres_sku    = "GP_Standard_D4s_v3"
      storage_tier    = "Standard_GRS"
    }
  }

  current_sku = local.sku_map[var.environment]

  # Backup retention
  backup_retention_days = local.is_production ? 35 : 7

  # High availability
  enable_ha = local.is_production

  # Zones
  availability_zones = local.is_production ? ["1", "2", "3"] : ["1"]
}
```

---

## Module Structure

### Directory Layout

```
modules/
├── landing-zone/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── aks-cluster/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── networking/
│   ├── hub/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── spoke/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── database/
│   ├── postgresql/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── cosmosdb/
├── security/
│   ├── key-vault/
│   └── managed-identity/
└── monitoring/
    ├── log-analytics/
    └── alerts/
```

### Module README Template

```markdown
# Module Name

Brief description of what this module creates.

## Usage

\`\`\`hcl
module "example" {
  source = "./modules/module-name"

  project     = "contoso"
  environment = "prod"
  location    = "westeurope"

  # Required variables
  required_var = "value"

  # Optional variables with defaults
  optional_var = "custom-value"

  tags = local.common_tags
}
\`\`\`

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5 |
| azurerm | >= 3.80 |

## Providers

| Name | Version |
|------|---------|
| azurerm | >= 3.80 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| project | Project name | string | n/a | yes |
| environment | Environment | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource ID |
| name | Resource name |

## Resources Created

- Resource Type 1
- Resource Type 2
\`\`\`
```

---

## Landing Zone Template

### Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
│       ├── main.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── modules/
│   └── (as above)
├── shared/
│   ├── providers.tf
│   ├── variables.tf
│   └── locals.tf
└── .github/
    └── workflows/
        └── terraform.yml
```

### Environment main.tf Template

```hcl
# environments/prod/main.tf

terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstateprod"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
      recover_soft_deleted_key_vaults = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

# Data sources
data "azurerm_client_config" "current" {}
data "azurerm_subscription" "current" {}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project}-${var.environment}-${var.location_short}"
  location = var.location

  tags = local.common_tags
}

# Modules
module "networking" {
  source = "../../modules/networking/spoke"

  project       = var.project
  environment   = var.environment
  location      = var.location
  address_space = var.address_space

  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

module "aks" {
  source = "../../modules/aks-cluster"

  project              = var.project
  environment          = var.environment
  location             = var.location
  resource_group_name  = azurerm_resource_group.main.name
  subnet_id            = module.networking.aks_subnet_id
  kubernetes_version   = var.kubernetes_version
  aks_admin_group_id   = var.aks_admin_group_id
  log_analytics_id     = module.monitoring.workspace_id

  tags = local.common_tags

  depends_on = [module.networking]
}

module "database" {
  source = "../../modules/database/postgresql"

  project             = var.project
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = module.networking.database_subnet_id
  vnet_id             = module.networking.vnet_id

  tags = local.common_tags

  depends_on = [module.networking]
}

module "monitoring" {
  source = "../../modules/monitoring/log-analytics"

  project             = var.project
  environment         = var.environment
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  retention_days      = local.is_production ? 90 : 30

  tags = local.common_tags
}
```

---

## ADR Templates

### ADR-001: Network Architecture

```markdown
# ADR-001: Network Architecture Decision

## Status

Accepted

## Context

We need to design the network architecture for our Azure landing zone that supports:
- Multiple environments (dev, staging, prod)
- Secure connectivity between services
- Controlled internet egress
- Hybrid connectivity (future)

## Decision

We will implement a **Hub-Spoke topology** with:

1. **Hub VNet** in the Connectivity subscription:
   - Azure Firewall for centralized egress
   - Azure Bastion for secure management
   - VPN Gateway (prepared for hybrid connectivity)

2. **Spoke VNets** per environment:
   - Dedicated address space per environment
   - Peered to hub with gateway transit
   - All internet traffic routed through hub firewall

3. **Private Endpoints** for all PaaS services:
   - Private DNS zones in hub
   - Private Link for storage, Key Vault, databases

## Consequences

**Positive:**
- Centralized security controls
- Reduced public surface area
- Easy to add hybrid connectivity
- Clear traffic inspection point

**Negative:**
- Additional hub VNet cost
- Potential bandwidth bottleneck at firewall
- Increased complexity

## Alternatives Considered

1. **Flat network**: Rejected - no security segmentation
2. **Virtual WAN**: Considered for future if scale requires
3. **Per-environment firewalls**: Rejected - cost prohibitive
```

### ADR-002: Identity Strategy

```markdown
# ADR-002: Identity and Access Management Strategy

## Status

Accepted

## Context

We need to define how identities authenticate and authorize access to Azure resources and workloads running on AKS.

## Decision

We will implement **Workload Identity** with the following approach:

1. **Microsoft Entra ID** as the central identity provider
2. **Managed Identities** for Azure resource authentication
3. **Workload Identity** for AKS pod authentication
4. **PIM (Privileged Identity Management)** for privileged access
5. **RBAC** for authorization at all scopes

### Implementation Details

- No service principal secrets stored anywhere
- Federated credentials for GitHub Actions CI/CD
- Conditional Access policies for human users
- Just-in-time (JIT) access for production

## Consequences

**Positive:**
- No secrets to manage or rotate
- Audit trail for all access
- Least privilege principle enforced
- Consistent identity model

**Negative:**
- Requires Microsoft Entra ID P2 for PIM
- Learning curve for workload identity
- More complex initial setup
```

---

## Governance Documents

### Policy Assignment Matrix

| Policy | Root | Platform | Landing Zones | Sandbox |
|--------|:----:|:--------:|:-------------:|:-------:|
| Allowed Locations | X | | | |
| Required Tags | | | X | |
| Diagnostic Settings | | X | X | |
| Disable Public IP | | | X | |
| Enforce HTTPS | | | X | |
| Key Vault Soft Delete | | X | X | |
| AKS Policies | | | X | |
| SQL Audit | | | X | |

### RBAC Assignment Matrix

| Role | Scope | Group | Access Type |
|------|-------|-------|-------------|
| Owner | Tenant Root | Platform Team | PIM Eligible |
| Contributor | Platform MG | Platform Ops | PIM Eligible |
| Reader | Landing Zones MG | All IT | Permanent |
| Contributor | Application Sub | App Team | PIM Eligible |
| Key Vault Secrets User | Key Vault | App Identity | Permanent |

### Compliance Checklist Template

```markdown
# Compliance Assessment: [Workload Name]

## Assessment Date: YYYY-MM-DD

## Compliance Frameworks

- [ ] SOC 2 Type II
- [ ] ISO 27001
- [ ] GDPR
- [ ] PCI DSS (if applicable)

## Security Controls

### Identity & Access

- [ ] MFA enforced for all users
- [ ] PIM configured for privileged roles
- [ ] Service accounts use managed identities
- [ ] Access reviews scheduled

### Data Protection

- [ ] Encryption at rest enabled
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Customer-managed keys (if required)
- [ ] Data classification applied

### Network Security

- [ ] Private endpoints for PaaS services
- [ ] NSGs configured
- [ ] Azure Firewall rules reviewed
- [ ] DDoS protection enabled

### Monitoring & Logging

- [ ] Diagnostic settings enabled
- [ ] Log retention meets requirements
- [ ] Alerts configured for security events
- [ ] Microsoft Defender enabled

### Business Continuity

- [ ] Backups configured and tested
- [ ] RTO/RPO documented and tested
- [ ] Disaster recovery plan exists
- [ ] Failover tested (date: ___)

## Findings

| ID | Finding | Severity | Remediation | Due Date |
|----|---------|----------|-------------|----------|
| 1 | | | | |

## Sign-off

- [ ] Security Team
- [ ] Compliance Team
- [ ] Platform Team
```
