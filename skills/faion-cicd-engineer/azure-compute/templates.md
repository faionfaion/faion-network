# Azure Compute Templates

Reusable templates for Azure compute infrastructure. Copy and customize for your projects.

---

## Quick Reference: Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `${PROJECT}` | Project name | `myapp` |
| `${ENV}` | Environment | `dev`, `staging`, `prod` |
| `${REGION}` | Azure region | `westeurope` |
| `${SUBSCRIPTION_ID}` | Azure subscription ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |

---

## Terraform Module Structure

```
modules/
├── vm/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── vmss/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── aks/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── container-apps/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── app-service/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## VM Module Template

### modules/vm/main.tf

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85"
    }
  }
}

# User Assigned Identity
resource "azurerm_user_assigned_identity" "main" {
  name                = "${var.name}-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# Network Interface
resource "azurerm_network_interface" "main" {
  name                = "${var.name}-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
  }

  tags = var.tags
}

# Linux VM
resource "azurerm_linux_virtual_machine" "main" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  size                = var.vm_size
  zone                = var.zone
  admin_username      = var.admin_username

  network_interface_ids = [azurerm_network_interface.main.id]

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  os_disk {
    caching              = var.os_disk_caching
    storage_account_type = var.os_disk_type
    disk_size_gb         = var.os_disk_size_gb
  }

  source_image_reference {
    publisher = var.image_publisher
    offer     = var.image_offer
    sku       = var.image_sku
    version   = var.image_version
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }

  boot_diagnostics {
    storage_account_uri = var.diagnostics_storage_uri
  }

  tags = var.tags
}
```

### modules/vm/variables.tf

```hcl
variable "name" {
  description = "VM name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for the VM"
  type        = string
}

variable "vm_size" {
  description = "VM size"
  type        = string
  default     = "Standard_D4s_v5"
}

variable "zone" {
  description = "Availability zone"
  type        = string
  default     = "1"
}

variable "admin_username" {
  description = "Admin username"
  type        = string
  default     = "azureadmin"
}

variable "ssh_public_key" {
  description = "SSH public key"
  type        = string
  sensitive   = true
}

variable "os_disk_type" {
  description = "OS disk storage type"
  type        = string
  default     = "Premium_LRS"
}

variable "os_disk_size_gb" {
  description = "OS disk size in GB"
  type        = number
  default     = 128
}

variable "os_disk_caching" {
  description = "OS disk caching"
  type        = string
  default     = "ReadWrite"
}

variable "image_publisher" {
  description = "Image publisher"
  type        = string
  default     = "Canonical"
}

variable "image_offer" {
  description = "Image offer"
  type        = string
  default     = "0001-com-ubuntu-server-jammy"
}

variable "image_sku" {
  description = "Image SKU"
  type        = string
  default     = "22_04-lts-gen2"
}

variable "image_version" {
  description = "Image version"
  type        = string
  default     = "latest"
}

variable "diagnostics_storage_uri" {
  description = "Storage account URI for diagnostics"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

### modules/vm/outputs.tf

```hcl
output "vm_id" {
  description = "VM resource ID"
  value       = azurerm_linux_virtual_machine.main.id
}

output "private_ip_address" {
  description = "Private IP address"
  value       = azurerm_network_interface.main.private_ip_address
}

output "identity_principal_id" {
  description = "Managed identity principal ID"
  value       = azurerm_user_assigned_identity.main.principal_id
}

output "identity_client_id" {
  description = "Managed identity client ID"
  value       = azurerm_user_assigned_identity.main.client_id
}
```

---

## AKS Module Template

### modules/aks/main.tf

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85"
    }
  }
}

# AKS Identity
resource "azurerm_user_assigned_identity" "aks" {
  name                = "${var.cluster_name}-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  network_profile {
    network_plugin      = var.network_plugin
    network_plugin_mode = var.network_plugin_mode
    network_policy      = var.network_policy
    load_balancer_sku   = "standard"
  }

  default_node_pool {
    name                         = "system"
    vm_size                      = var.system_node_size
    node_count                   = var.system_node_count
    vnet_subnet_id               = var.subnet_id
    only_critical_addons_enabled = true
    zones                        = var.availability_zones

    upgrade_settings {
      max_surge = var.upgrade_max_surge
    }

    node_labels = {
      "nodepool-type" = "system"
    }

    tags = var.tags
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks.id]
  }

  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = var.azure_rbac_enabled
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  automatic_channel_upgrade = var.auto_upgrade_channel

  dynamic "maintenance_window" {
    for_each = var.maintenance_window != null ? [1] : []
    content {
      allowed {
        day   = var.maintenance_window.day
        hours = var.maintenance_window.hours
      }
    }
  }

  azure_policy_enabled = var.azure_policy_enabled

  dynamic "key_vault_secrets_provider" {
    for_each = var.keyvault_secrets_provider_enabled ? [1] : []
    content {
      secret_rotation_enabled  = true
      rotation_poll_interval   = "2m"
    }
  }

  dynamic "oms_agent" {
    for_each = var.log_analytics_workspace_id != null ? [1] : []
    content {
      log_analytics_workspace_id = var.log_analytics_workspace_id
    }
  }

  dynamic "microsoft_defender" {
    for_each = var.defender_enabled && var.log_analytics_workspace_id != null ? [1] : []
    content {
      log_analytics_workspace_id = var.log_analytics_workspace_id
    }
  }

  dynamic "workload_autoscaler_profile" {
    for_each = var.keda_enabled ? [1] : []
    content {
      keda_enabled = true
    }
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [
      default_node_pool[0].node_count
    ]
  }
}

# User Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "user" {
  count                 = var.create_user_node_pool ? 1 : 0
  name                  = "user"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.user_node_size
  node_count            = var.user_node_count
  vnet_subnet_id        = var.subnet_id
  zones                 = var.availability_zones

  enable_auto_scaling = var.user_node_autoscaling
  min_count           = var.user_node_autoscaling ? var.user_node_min_count : null
  max_count           = var.user_node_autoscaling ? var.user_node_max_count : null

  upgrade_settings {
    max_surge = var.upgrade_max_surge
  }

  node_labels = {
    "nodepool-type" = "user"
    "workload"      = "general"
  }

  tags = var.tags
}

# Spot Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "spot" {
  count                 = var.create_spot_node_pool ? 1 : 0
  name                  = "spot"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.spot_node_size
  vnet_subnet_id        = var.subnet_id
  zones                 = var.availability_zones

  enable_auto_scaling = true
  min_count           = 0
  max_count           = var.spot_node_max_count

  priority        = "Spot"
  eviction_policy = "Delete"
  spot_max_price  = -1

  node_labels = {
    "nodepool-type"                          = "spot"
    "kubernetes.azure.com/scalesetpriority" = "spot"
  }

  node_taints = [
    "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"
  ]

  tags = var.tags
}
```

### modules/aks/variables.tf

```hcl
variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "dns_prefix" {
  description = "DNS prefix for cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.29"
}

variable "subnet_id" {
  description = "Subnet ID for nodes"
  type        = string
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["1", "2", "3"]
}

# Network
variable "network_plugin" {
  description = "Network plugin (azure or kubenet)"
  type        = string
  default     = "azure"
}

variable "network_plugin_mode" {
  description = "Network plugin mode"
  type        = string
  default     = "overlay"
}

variable "network_policy" {
  description = "Network policy (calico or azure)"
  type        = string
  default     = "calico"
}

# System Node Pool
variable "system_node_size" {
  description = "System node pool VM size"
  type        = string
  default     = "Standard_D2s_v5"
}

variable "system_node_count" {
  description = "System node pool count"
  type        = number
  default     = 2
}

# User Node Pool
variable "create_user_node_pool" {
  description = "Create user node pool"
  type        = bool
  default     = true
}

variable "user_node_size" {
  description = "User node pool VM size"
  type        = string
  default     = "Standard_D4s_v5"
}

variable "user_node_count" {
  description = "User node pool initial count"
  type        = number
  default     = 2
}

variable "user_node_autoscaling" {
  description = "Enable autoscaling for user pool"
  type        = bool
  default     = true
}

variable "user_node_min_count" {
  description = "User node pool min count"
  type        = number
  default     = 2
}

variable "user_node_max_count" {
  description = "User node pool max count"
  type        = number
  default     = 20
}

# Spot Node Pool
variable "create_spot_node_pool" {
  description = "Create spot node pool"
  type        = bool
  default     = false
}

variable "spot_node_size" {
  description = "Spot node pool VM size"
  type        = string
  default     = "Standard_D4s_v5"
}

variable "spot_node_max_count" {
  description = "Spot node pool max count"
  type        = number
  default     = 50
}

# Upgrades
variable "upgrade_max_surge" {
  description = "Max surge during upgrades"
  type        = string
  default     = "33%"
}

variable "auto_upgrade_channel" {
  description = "Auto upgrade channel"
  type        = string
  default     = "patch"
}

variable "maintenance_window" {
  description = "Maintenance window configuration"
  type = object({
    day   = string
    hours = list(number)
  })
  default = {
    day   = "Sunday"
    hours = [2, 3, 4]
  }
}

# Features
variable "azure_rbac_enabled" {
  description = "Enable Azure RBAC"
  type        = bool
  default     = true
}

variable "azure_policy_enabled" {
  description = "Enable Azure Policy"
  type        = bool
  default     = true
}

variable "keyvault_secrets_provider_enabled" {
  description = "Enable Key Vault secrets provider"
  type        = bool
  default     = true
}

variable "keda_enabled" {
  description = "Enable KEDA"
  type        = bool
  default     = false
}

variable "defender_enabled" {
  description = "Enable Microsoft Defender"
  type        = bool
  default     = true
}

variable "log_analytics_workspace_id" {
  description = "Log Analytics workspace ID"
  type        = string
  default     = null
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

### modules/aks/outputs.tf

```hcl
output "cluster_id" {
  description = "AKS cluster ID"
  value       = azurerm_kubernetes_cluster.main.id
}

output "cluster_name" {
  description = "AKS cluster name"
  value       = azurerm_kubernetes_cluster.main.name
}

output "cluster_fqdn" {
  description = "AKS cluster FQDN"
  value       = azurerm_kubernetes_cluster.main.fqdn
}

output "kube_config" {
  description = "Kubernetes config"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true
}

output "oidc_issuer_url" {
  description = "OIDC issuer URL for workload identity"
  value       = azurerm_kubernetes_cluster.main.oidc_issuer_url
}

output "kubelet_identity" {
  description = "Kubelet identity"
  value       = azurerm_kubernetes_cluster.main.kubelet_identity[0]
}

output "aks_identity_principal_id" {
  description = "AKS identity principal ID"
  value       = azurerm_user_assigned_identity.aks.principal_id
}

output "node_resource_group" {
  description = "Node resource group name"
  value       = azurerm_kubernetes_cluster.main.node_resource_group
}
```

---

## Container Apps Module Template

### modules/container-apps/main.tf

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85"
    }
  }
}

# Container Apps Environment
resource "azurerm_container_app_environment" "main" {
  name                       = var.environment_name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  log_analytics_workspace_id = var.log_analytics_workspace_id

  infrastructure_subnet_id = var.subnet_id

  dynamic "workload_profile" {
    for_each = var.workload_profiles
    content {
      name                  = workload_profile.value.name
      workload_profile_type = workload_profile.value.type
      minimum_count         = lookup(workload_profile.value, "min_count", null)
      maximum_count         = lookup(workload_profile.value, "max_count", null)
    }
  }

  tags = var.tags
}

# User Assigned Identity
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.app_name}-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# Container App
resource "azurerm_container_app" "main" {
  name                         = var.app_name
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = var.resource_group_name
  revision_mode                = var.revision_mode

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  template {
    container {
      name   = var.container_name
      image  = var.container_image
      cpu    = var.cpu
      memory = var.memory

      dynamic "env" {
        for_each = var.environment_variables
        content {
          name        = env.key
          value       = lookup(env.value, "value", null)
          secret_name = lookup(env.value, "secret_name", null)
        }
      }

      dynamic "liveness_probe" {
        for_each = var.liveness_probe != null ? [1] : []
        content {
          transport = var.liveness_probe.transport
          path      = var.liveness_probe.path
          port      = var.liveness_probe.port
        }
      }

      dynamic "readiness_probe" {
        for_each = var.readiness_probe != null ? [1] : []
        content {
          transport = var.readiness_probe.transport
          path      = var.readiness_probe.path
          port      = var.readiness_probe.port
        }
      }
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    dynamic "http_scale_rule" {
      for_each = var.http_scale_rule != null ? [1] : []
      content {
        name                = var.http_scale_rule.name
        concurrent_requests = var.http_scale_rule.concurrent_requests
      }
    }

    dynamic "custom_scale_rule" {
      for_each = var.custom_scale_rules
      content {
        name             = custom_scale_rule.value.name
        custom_rule_type = custom_scale_rule.value.type
        metadata         = custom_scale_rule.value.metadata

        dynamic "authentication" {
          for_each = lookup(custom_scale_rule.value, "authentication", null) != null ? [1] : []
          content {
            secret_name       = custom_scale_rule.value.authentication.secret_name
            trigger_parameter = custom_scale_rule.value.authentication.trigger_parameter
          }
        }
      }
    }
  }

  dynamic "ingress" {
    for_each = var.ingress != null ? [1] : []
    content {
      external_enabled = var.ingress.external
      target_port      = var.ingress.target_port
      transport        = var.ingress.transport

      traffic_weight {
        percentage      = 100
        latest_revision = true
      }
    }
  }

  dynamic "dapr" {
    for_each = var.dapr != null ? [1] : []
    content {
      app_id       = var.dapr.app_id
      app_port     = var.dapr.app_port
      app_protocol = var.dapr.app_protocol
    }
  }

  dynamic "secret" {
    for_each = var.secrets
    content {
      name  = secret.key
      value = secret.value
    }
  }

  dynamic "registry" {
    for_each = var.registries
    content {
      server   = registry.value.server
      identity = registry.value.identity_id
    }
  }

  tags = var.tags
}
```

### modules/container-apps/variables.tf

```hcl
variable "environment_name" {
  description = "Container Apps environment name"
  type        = string
}

variable "app_name" {
  description = "Container app name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "Log Analytics workspace ID"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for environment"
  type        = string
  default     = null
}

variable "workload_profiles" {
  description = "Workload profiles"
  type = list(object({
    name      = string
    type      = string
    min_count = optional(number)
    max_count = optional(number)
  }))
  default = [{
    name = "Consumption"
    type = "Consumption"
  }]
}

variable "revision_mode" {
  description = "Revision mode (Single or Multiple)"
  type        = string
  default     = "Single"
}

variable "container_name" {
  description = "Container name"
  type        = string
}

variable "container_image" {
  description = "Container image"
  type        = string
}

variable "cpu" {
  description = "CPU cores"
  type        = number
  default     = 0.5
}

variable "memory" {
  description = "Memory (e.g., '1Gi')"
  type        = string
  default     = "1Gi"
}

variable "environment_variables" {
  description = "Environment variables"
  type        = map(object({
    value       = optional(string)
    secret_name = optional(string)
  }))
  default = {}
}

variable "min_replicas" {
  description = "Minimum replicas"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum replicas"
  type        = number
  default     = 10
}

variable "http_scale_rule" {
  description = "HTTP scale rule"
  type = object({
    name                = string
    concurrent_requests = number
  })
  default = null
}

variable "custom_scale_rules" {
  description = "Custom KEDA scale rules"
  type = list(object({
    name     = string
    type     = string
    metadata = map(string)
    authentication = optional(object({
      secret_name       = string
      trigger_parameter = string
    }))
  }))
  default = []
}

variable "liveness_probe" {
  description = "Liveness probe configuration"
  type = object({
    transport = string
    path      = string
    port      = number
  })
  default = null
}

variable "readiness_probe" {
  description = "Readiness probe configuration"
  type = object({
    transport = string
    path      = string
    port      = number
  })
  default = null
}

variable "ingress" {
  description = "Ingress configuration"
  type = object({
    external    = bool
    target_port = number
    transport   = string
  })
  default = null
}

variable "dapr" {
  description = "Dapr configuration"
  type = object({
    app_id       = string
    app_port     = number
    app_protocol = string
  })
  default = null
}

variable "secrets" {
  description = "Secrets"
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "registries" {
  description = "Container registries"
  type = list(object({
    server      = string
    identity_id = string
  }))
  default = []
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

---

## App Service Module Template

### modules/app-service/main.tf

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85"
    }
  }
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = var.plan_name
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = var.os_type
  sku_name            = var.sku_name
  tags                = var.tags
}

# User Assigned Identity
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.app_name}-identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

# Linux Web App
resource "azurerm_linux_web_app" "main" {
  count               = var.os_type == "Linux" ? 1 : 0
  name                = var.app_name
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  site_config {
    always_on                = var.always_on
    http2_enabled            = true
    minimum_tls_version      = "1.2"
    ftps_state               = "Disabled"
    health_check_path        = var.health_check_path

    dynamic "application_stack" {
      for_each = var.docker_image != null ? [1] : []
      content {
        docker_image_name        = var.docker_image
        docker_registry_url      = var.docker_registry_url
      }
    }
  }

  app_settings = merge(var.app_settings, {
    "AZURE_CLIENT_ID" = azurerm_user_assigned_identity.app.client_id
  })

  dynamic "connection_string" {
    for_each = var.connection_strings
    content {
      name  = connection_string.key
      type  = connection_string.value.type
      value = connection_string.value.value
    }
  }

  logs {
    http_logs {
      file_system {
        retention_in_days = var.log_retention_days
        retention_in_mb   = 100
      }
    }
    application_logs {
      file_system_level = var.log_level
    }
  }

  tags = var.tags
}

# Staging Slot
resource "azurerm_linux_web_app_slot" "staging" {
  count          = var.os_type == "Linux" && var.create_staging_slot ? 1 : 0
  name           = "staging"
  app_service_id = azurerm_linux_web_app.main[0].id
  https_only     = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  site_config {
    always_on                = false
    http2_enabled            = true
    minimum_tls_version      = "1.2"
    ftps_state               = "Disabled"
    health_check_path        = var.health_check_path

    dynamic "application_stack" {
      for_each = var.docker_image != null ? [1] : []
      content {
        docker_image_name        = var.docker_image
        docker_registry_url      = var.docker_registry_url
      }
    }
  }

  app_settings = merge(var.staging_app_settings, {
    "AZURE_CLIENT_ID" = azurerm_user_assigned_identity.app.client_id
  })

  tags = var.tags
}
```

### modules/app-service/variables.tf

```hcl
variable "plan_name" {
  description = "App Service Plan name"
  type        = string
}

variable "app_name" {
  description = "Web app name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "os_type" {
  description = "OS type (Linux or Windows)"
  type        = string
  default     = "Linux"
}

variable "sku_name" {
  description = "SKU name (B1, S1, P1v3, etc.)"
  type        = string
  default     = "B1"
}

variable "always_on" {
  description = "Keep app always on"
  type        = bool
  default     = false
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/health"
}

variable "docker_image" {
  description = "Docker image name (without registry)"
  type        = string
  default     = null
}

variable "docker_registry_url" {
  description = "Docker registry URL"
  type        = string
  default     = null
}

variable "app_settings" {
  description = "App settings"
  type        = map(string)
  default     = {}
}

variable "staging_app_settings" {
  description = "Staging slot app settings"
  type        = map(string)
  default     = {}
}

variable "connection_strings" {
  description = "Connection strings"
  type = map(object({
    type  = string
    value = string
  }))
  default   = {}
  sensitive = true
}

variable "create_staging_slot" {
  description = "Create staging deployment slot"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Log retention in days"
  type        = number
  default     = 7
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "Information"
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

---

## Usage Examples

### Using VM Module

```hcl
module "web_server" {
  source = "./modules/vm"

  name                    = "myapp-prod-web"
  location                = "westeurope"
  resource_group_name     = azurerm_resource_group.main.name
  subnet_id               = azurerm_subnet.private.id
  vm_size                 = "Standard_D4s_v5"
  zone                    = "1"
  ssh_public_key          = var.ssh_public_key
  diagnostics_storage_uri = azurerm_storage_account.diagnostics.primary_blob_endpoint

  tags = local.common_tags
}
```

### Using AKS Module

```hcl
module "aks" {
  source = "./modules/aks"

  cluster_name       = "myapp-prod-aks"
  dns_prefix         = "myapp-prod"
  location           = "westeurope"
  resource_group_name = azurerm_resource_group.main.name
  subnet_id          = azurerm_subnet.aks.id
  kubernetes_version = "1.29"

  system_node_size  = "Standard_D2s_v5"
  system_node_count = 2

  create_user_node_pool = true
  user_node_size        = "Standard_D4s_v5"
  user_node_autoscaling = true
  user_node_min_count   = 2
  user_node_max_count   = 20

  create_spot_node_pool = true
  spot_node_max_count   = 50

  keda_enabled               = true
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  tags = local.common_tags
}
```

### Using Container Apps Module

```hcl
module "api" {
  source = "./modules/container-apps"

  environment_name           = "myapp-prod-cae"
  app_name                   = "myapp-api"
  location                   = "westeurope"
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  container_name  = "api"
  container_image = "myregistry.azurecr.io/api:v1.0.0"
  cpu             = 0.5
  memory          = "1Gi"

  min_replicas = 2
  max_replicas = 20

  http_scale_rule = {
    name                = "http-scaling"
    concurrent_requests = 100
  }

  ingress = {
    external    = true
    target_port = 8080
    transport   = "http"
  }

  dapr = {
    app_id       = "api"
    app_port     = 8080
    app_protocol = "http"
  }

  registries = [{
    server      = "myregistry.azurecr.io"
    identity_id = azurerm_user_assigned_identity.app.id
  }]

  tags = local.common_tags
}
```
