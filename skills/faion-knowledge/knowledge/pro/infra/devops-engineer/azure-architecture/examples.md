# Azure Architecture Examples

Terraform and Bicep code examples for Azure Landing Zones, Governance, and Well-Architected patterns.

## Table of Contents

1. [Management Groups & Subscriptions](#management-groups--subscriptions)
2. [Azure Policy](#azure-policy)
3. [Network Hub-Spoke](#network-hub-spoke)
4. [Identity & RBAC](#identity--rbac)
5. [AKS with Workload Identity](#aks-with-workload-identity)
6. [Key Vault & Secrets](#key-vault--secrets)
7. [Storage & CDN](#storage--cdn)
8. [PostgreSQL Flexible Server](#postgresql-flexible-server)
9. [Monitoring & Logging](#monitoring--logging)

---

## Management Groups & Subscriptions

### Management Group Hierarchy (Terraform)

```hcl
# Management group hierarchy following ALZ recommendations
resource "azurerm_management_group" "platform" {
  display_name               = "Platform"
  parent_management_group_id = data.azurerm_management_group.root.id

  subscription_ids = []
}

resource "azurerm_management_group" "platform_identity" {
  display_name               = "Identity"
  parent_management_group_id = azurerm_management_group.platform.id

  subscription_ids = var.identity_subscription_ids
}

resource "azurerm_management_group" "platform_management" {
  display_name               = "Management"
  parent_management_group_id = azurerm_management_group.platform.id

  subscription_ids = var.management_subscription_ids
}

resource "azurerm_management_group" "platform_connectivity" {
  display_name               = "Connectivity"
  parent_management_group_id = azurerm_management_group.platform.id

  subscription_ids = var.connectivity_subscription_ids
}

resource "azurerm_management_group" "landing_zones" {
  display_name               = "Landing Zones"
  parent_management_group_id = data.azurerm_management_group.root.id

  subscription_ids = []
}

resource "azurerm_management_group" "landing_zones_corp" {
  display_name               = "Corp"
  parent_management_group_id = azurerm_management_group.landing_zones.id

  subscription_ids = var.corp_subscription_ids
}

resource "azurerm_management_group" "landing_zones_online" {
  display_name               = "Online"
  parent_management_group_id = azurerm_management_group.landing_zones.id

  subscription_ids = var.online_subscription_ids
}

resource "azurerm_management_group" "sandbox" {
  display_name               = "Sandbox"
  parent_management_group_id = data.azurerm_management_group.root.id

  subscription_ids = var.sandbox_subscription_ids
}

resource "azurerm_management_group" "decommissioned" {
  display_name               = "Decommissioned"
  parent_management_group_id = data.azurerm_management_group.root.id

  subscription_ids = []
}
```

### Management Group Hierarchy (Bicep)

```bicep
targetScope = 'tenant'

@description('Root management group ID')
param rootManagementGroupId string

resource platformMg 'Microsoft.Management/managementGroups@2021-04-01' = {
  name: 'Platform'
  properties: {
    displayName: 'Platform'
    details: {
      parent: {
        id: tenantResourceId('Microsoft.Management/managementGroups', rootManagementGroupId)
      }
    }
  }
}

resource identityMg 'Microsoft.Management/managementGroups@2021-04-01' = {
  name: 'Identity'
  properties: {
    displayName: 'Identity'
    details: {
      parent: {
        id: platformMg.id
      }
    }
  }
}

resource managementMg 'Microsoft.Management/managementGroups@2021-04-01' = {
  name: 'Management'
  properties: {
    displayName: 'Management'
    details: {
      parent: {
        id: platformMg.id
      }
    }
  }
}

resource connectivityMg 'Microsoft.Management/managementGroups@2021-04-01' = {
  name: 'Connectivity'
  properties: {
    displayName: 'Connectivity'
    details: {
      parent: {
        id: platformMg.id
      }
    }
  }
}

resource landingZonesMg 'Microsoft.Management/managementGroups@2021-04-01' = {
  name: 'LandingZones'
  properties: {
    displayName: 'Landing Zones'
    details: {
      parent: {
        id: tenantResourceId('Microsoft.Management/managementGroups', rootManagementGroupId)
      }
    }
  }
}
```

---

## Azure Policy

### Tagging Policy Initiative

```hcl
# Policy initiative for required tags
resource "azurerm_policy_set_definition" "tagging" {
  name         = "required-tags-initiative"
  policy_type  = "Custom"
  display_name = "Required Tags Initiative"
  description  = "Ensures required tags are applied to all resources"

  management_group_id = azurerm_management_group.landing_zones.id

  parameters = <<PARAMETERS
{
  "environment": {
    "type": "String",
    "metadata": {
      "displayName": "Environment",
      "description": "Environment tag value"
    },
    "allowedValues": ["dev", "staging", "prod"]
  }
}
PARAMETERS

  policy_definition_reference {
    policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/726aca4c-86e9-4b04-b0c5-073027359532"
    parameter_values     = <<VALUES
{
  "tagName": { "value": "Environment" }
}
VALUES
  }

  policy_definition_reference {
    policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/726aca4c-86e9-4b04-b0c5-073027359532"
    parameter_values     = <<VALUES
{
  "tagName": { "value": "CostCenter" }
}
VALUES
  }

  policy_definition_reference {
    policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/726aca4c-86e9-4b04-b0c5-073027359532"
    parameter_values     = <<VALUES
{
  "tagName": { "value": "Owner" }
}
VALUES
  }
}

resource "azurerm_management_group_policy_assignment" "tagging" {
  name                 = "required-tags"
  management_group_id  = azurerm_management_group.landing_zones.id
  policy_definition_id = azurerm_policy_set_definition.tagging.id
  description          = "Enforce required tags on all resources"
  display_name         = "Required Tags"

  non_compliance_message {
    content = "Required tags (Environment, CostCenter, Owner) must be applied to all resources."
  }
}
```

### Diagnostic Settings Policy

```hcl
# Policy to enforce diagnostic settings
resource "azurerm_policy_definition" "diagnostic_settings" {
  name         = "deploy-diagnostic-settings"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Deploy Diagnostic Settings to Log Analytics"

  management_group_id = azurerm_management_group.platform.id

  metadata = <<METADATA
{
  "category": "Monitoring"
}
METADATA

  parameters = <<PARAMETERS
{
  "logAnalyticsWorkspaceId": {
    "type": "String",
    "metadata": {
      "displayName": "Log Analytics Workspace ID",
      "description": "The resource ID of the Log Analytics workspace"
    }
  }
}
PARAMETERS

  policy_rule = <<POLICY_RULE
{
  "if": {
    "allOf": [
      {
        "field": "type",
        "equals": "Microsoft.KeyVault/vaults"
      }
    ]
  },
  "then": {
    "effect": "deployIfNotExists",
    "details": {
      "type": "Microsoft.Insights/diagnosticSettings",
      "name": "setByPolicy",
      "existenceCondition": {
        "allOf": [
          {
            "field": "Microsoft.Insights/diagnosticSettings/workspaceId",
            "equals": "[parameters('logAnalyticsWorkspaceId')]"
          }
        ]
      },
      "roleDefinitionIds": [
        "/providers/Microsoft.Authorization/roleDefinitions/749f88d5-cbae-40b8-bcfc-e573ddc772fa",
        "/providers/Microsoft.Authorization/roleDefinitions/92aaf0da-9dab-42b6-94a3-d43ce8d16293"
      ],
      "deployment": {
        "properties": {
          "mode": "incremental",
          "template": {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
              "resourceName": { "type": "string" },
              "logAnalyticsWorkspaceId": { "type": "string" }
            },
            "resources": [
              {
                "type": "Microsoft.KeyVault/vaults/providers/diagnosticSettings",
                "apiVersion": "2021-05-01-preview",
                "name": "[concat(parameters('resourceName'), '/Microsoft.Insights/setByPolicy')]",
                "properties": {
                  "workspaceId": "[parameters('logAnalyticsWorkspaceId')]",
                  "logs": [
                    {
                      "category": "AuditEvent",
                      "enabled": true
                    }
                  ],
                  "metrics": [
                    {
                      "category": "AllMetrics",
                      "enabled": true
                    }
                  ]
                }
              }
            ]
          },
          "parameters": {
            "resourceName": { "value": "[field('name')]" },
            "logAnalyticsWorkspaceId": { "value": "[parameters('logAnalyticsWorkspaceId')]" }
          }
        }
      }
    }
  }
}
POLICY_RULE
}
```

### Allowed Locations Policy

```hcl
# Assign built-in allowed locations policy
resource "azurerm_management_group_policy_assignment" "allowed_locations" {
  name                 = "allowed-locations"
  management_group_id  = azurerm_management_group.landing_zones.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/e56962a6-4747-49cd-b67b-bf8b01975c4c"
  description          = "Restrict resource deployment to specific regions"
  display_name         = "Allowed Locations"

  parameters = <<PARAMETERS
{
  "listOfAllowedLocations": {
    "value": ["westeurope", "northeurope", "germanywestcentral"]
  }
}
PARAMETERS

  non_compliance_message {
    content = "Resources can only be deployed in West Europe, North Europe, or Germany West Central."
  }
}
```

---

## Network Hub-Spoke

### Hub VNet with Azure Firewall

```hcl
# Hub Virtual Network
resource "azurerm_virtual_network" "hub" {
  name                = "${var.project}-hub-vnet"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  address_space       = ["10.0.0.0/16"]

  tags = local.common_tags
}

# Azure Firewall Subnet (must be named AzureFirewallSubnet)
resource "azurerm_subnet" "firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.0.0/26"]
}

# Gateway Subnet
resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.1.0/27"]
}

# Bastion Subnet
resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.2.0/26"]
}

# Management Subnet
resource "azurerm_subnet" "management" {
  name                 = "management"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.3.0/24"]
}

# Azure Firewall
resource "azurerm_public_ip" "firewall" {
  name                = "${var.project}-firewall-pip"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = ["1", "2", "3"]

  tags = local.common_tags
}

resource "azurerm_firewall_policy" "main" {
  name                = "${var.project}-firewall-policy"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  sku                 = "Premium"

  dns {
    proxy_enabled = true
  }

  threat_intelligence_mode = "Deny"

  tags = local.common_tags
}

resource "azurerm_firewall" "main" {
  name                = "${var.project}-firewall"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Premium"
  firewall_policy_id  = azurerm_firewall_policy.main.id
  zones               = ["1", "2", "3"]

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.firewall.id
    public_ip_address_id = azurerm_public_ip.firewall.id
  }

  tags = local.common_tags
}

# Azure Bastion
resource "azurerm_public_ip" "bastion" {
  name                = "${var.project}-bastion-pip"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = local.common_tags
}

resource "azurerm_bastion_host" "main" {
  name                = "${var.project}-bastion"
  location            = azurerm_resource_group.hub.location
  resource_group_name = azurerm_resource_group.hub.name
  sku                 = "Standard"

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.bastion.id
    public_ip_address_id = azurerm_public_ip.bastion.id
  }

  tunneling_enabled    = true
  file_copy_enabled    = true
  copy_paste_enabled   = true
  shareable_link_enabled = false

  tags = local.common_tags
}
```

### Spoke VNet with Peering

```hcl
# Spoke Virtual Network
resource "azurerm_virtual_network" "spoke" {
  name                = "${var.project}-${var.environment}-spoke-vnet"
  location            = azurerm_resource_group.spoke.location
  resource_group_name = azurerm_resource_group.spoke.name
  address_space       = [var.spoke_address_space]

  tags = local.common_tags
}

# Application Subnet
resource "azurerm_subnet" "app" {
  name                 = "app"
  resource_group_name  = azurerm_resource_group.spoke.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = [cidrsubnet(var.spoke_address_space, 2, 0)]

  service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault",
    "Microsoft.Sql"
  ]
}

# Database Subnet
resource "azurerm_subnet" "database" {
  name                 = "database"
  resource_group_name  = azurerm_resource_group.spoke.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = [cidrsubnet(var.spoke_address_space, 2, 1)]

  delegation {
    name = "postgresql-delegation"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

# Private Endpoints Subnet
resource "azurerm_subnet" "private_endpoints" {
  name                 = "private-endpoints"
  resource_group_name  = azurerm_resource_group.spoke.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = [cidrsubnet(var.spoke_address_space, 2, 2)]
}

# Hub to Spoke Peering
resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                         = "hub-to-${var.environment}-spoke"
  resource_group_name          = data.azurerm_resource_group.hub.name
  virtual_network_name         = data.azurerm_virtual_network.hub.name
  remote_virtual_network_id    = azurerm_virtual_network.spoke.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = true
}

# Spoke to Hub Peering
resource "azurerm_virtual_network_peering" "spoke_to_hub" {
  name                         = "${var.environment}-spoke-to-hub"
  resource_group_name          = azurerm_resource_group.spoke.name
  virtual_network_name         = azurerm_virtual_network.spoke.name
  remote_virtual_network_id    = data.azurerm_virtual_network.hub.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  use_remote_gateways          = var.use_remote_gateways
}

# Route Table for Spoke (routes traffic through firewall)
resource "azurerm_route_table" "spoke" {
  name                          = "${var.project}-${var.environment}-spoke-rt"
  location                      = azurerm_resource_group.spoke.location
  resource_group_name           = azurerm_resource_group.spoke.name
  disable_bgp_route_propagation = true

  route {
    name                   = "to-internet"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = data.azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }

  route {
    name                   = "to-hub"
    address_prefix         = data.azurerm_virtual_network.hub.address_space[0]
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = data.azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }

  tags = local.common_tags
}

resource "azurerm_subnet_route_table_association" "app" {
  subnet_id      = azurerm_subnet.app.id
  route_table_id = azurerm_route_table.spoke.id
}
```

---

## Identity & RBAC

### Custom RBAC Role

```hcl
# Custom role for landing zone operators
resource "azurerm_role_definition" "landing_zone_operator" {
  name        = "Landing Zone Operator"
  scope       = azurerm_management_group.landing_zones.id
  description = "Can manage resources in landing zones but not modify networking or policies"

  permissions {
    actions = [
      "Microsoft.Resources/subscriptions/resourceGroups/*",
      "Microsoft.Compute/*",
      "Microsoft.Storage/*",
      "Microsoft.Web/*",
      "Microsoft.ContainerService/*",
      "Microsoft.KeyVault/vaults/read",
      "Microsoft.KeyVault/vaults/secrets/*",
      "Microsoft.Insights/*",
      "Microsoft.OperationalInsights/*",
    ]
    not_actions = [
      "Microsoft.Network/virtualNetworks/write",
      "Microsoft.Network/virtualNetworks/delete",
      "Microsoft.Network/virtualNetworks/peer/*",
      "Microsoft.Authorization/policyAssignments/*",
      "Microsoft.Authorization/policyDefinitions/*",
    ]
  }

  assignable_scopes = [
    azurerm_management_group.landing_zones.id
  ]
}
```

### PIM Role Assignment

```hcl
# Eligible role assignment (requires PIM)
resource "azurerm_pim_eligible_role_assignment" "contributor" {
  scope              = azurerm_subscription.main.id
  role_definition_id = data.azurerm_role_definition.contributor.id
  principal_id       = var.admin_group_object_id

  schedule {
    start_date_time = timestamp()
    expiration {
      duration_days = 365
    }
  }

  justification = "Platform administrator access"

  ticket {
    number = "ITSM-001"
    system = "ServiceNow"
  }
}
```

---

## AKS with Workload Identity

### AKS Cluster

```hcl
# User Assigned Identity for AKS
resource "azurerm_user_assigned_identity" "aks" {
  name                = "${var.project}-${var.environment}-aks-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project}-${var.environment}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.project}-${var.environment}"
  kubernetes_version  = var.kubernetes_version

  # Network configuration
  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    network_policy      = "calico"
    load_balancer_sku   = "standard"
    outbound_type       = "userAssignedNATGateway"

    load_balancer_profile {
      managed_outbound_ip_count = 1
    }
  }

  # Default node pool (system)
  default_node_pool {
    name                         = "system"
    vm_size                      = "Standard_D4s_v5"
    node_count                   = 2
    vnet_subnet_id               = azurerm_subnet.aks.id
    only_critical_addons_enabled = true
    zones                        = ["1", "2", "3"]

    upgrade_settings {
      max_surge = "33%"
    }

    node_labels = {
      "nodepool-type" = "system"
    }

    tags = local.common_tags
  }

  # Identity
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks.id]
  }

  # Microsoft Entra ID integration
  azure_active_directory_role_based_access_control {
    managed                = true
    azure_rbac_enabled     = true
    admin_group_object_ids = [var.aks_admin_group_id]
  }

  # Workload Identity
  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  # API server access
  api_server_access_profile {
    authorized_ip_ranges = var.authorized_ip_ranges
  }

  # Auto-upgrade
  automatic_channel_upgrade = "patch"

  # Maintenance window
  maintenance_window {
    allowed {
      day   = "Sunday"
      hours = [2, 3, 4]
    }
  }

  # Add-ons
  azure_policy_enabled = true

  key_vault_secrets_provider {
    secret_rotation_enabled = true
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  microsoft_defender {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  monitor_metrics {}

  tags = local.common_tags

  lifecycle {
    ignore_changes = [
      default_node_pool[0].node_count
    ]
  }
}

# User Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "user" {
  name                  = "user"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D4s_v5"
  node_count            = 2
  vnet_subnet_id        = azurerm_subnet.aks.id
  zones                 = ["1", "2", "3"]

  enable_auto_scaling = true
  min_count           = 2
  max_count           = 10

  upgrade_settings {
    max_surge = "33%"
  }

  node_labels = {
    "nodepool-type" = "user"
    "workload"      = "general"
  }

  tags = local.common_tags
}

# Spot Node Pool (for cost optimization)
resource "azurerm_kubernetes_cluster_node_pool" "spot" {
  name                  = "spot"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D4s_v5"
  vnet_subnet_id        = azurerm_subnet.aks.id
  zones                 = ["1", "2", "3"]

  enable_auto_scaling = true
  min_count           = 0
  max_count           = 20

  priority        = "Spot"
  eviction_policy = "Delete"
  spot_max_price  = -1 # Pay up to on-demand price

  node_labels = {
    "nodepool-type"                          = "spot"
    "kubernetes.azure.com/scalesetpriority" = "spot"
  }

  node_taints = [
    "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"
  ]

  tags = local.common_tags
}
```

### Workload Identity for Application

```hcl
# User Assigned Identity for application
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.project}-${var.environment}-app-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

# Federated credential for Kubernetes
resource "azurerm_federated_identity_credential" "app" {
  name                = "kubernetes-federated-credential"
  resource_group_name = azurerm_resource_group.main.name
  parent_id           = azurerm_user_assigned_identity.app.id
  audience            = ["api://AzureADTokenExchange"]
  issuer              = azurerm_kubernetes_cluster.main.oidc_issuer_url
  subject             = "system:serviceaccount:${var.namespace}:${var.service_account_name}"
}

# Role assignments for the application identity
resource "azurerm_role_assignment" "app_keyvault" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

resource "azurerm_role_assignment" "app_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

---

## Key Vault & Secrets

### Key Vault with Private Endpoint

```hcl
# Key Vault
resource "azurerm_key_vault" "main" {
  name                        = "${var.project}-${var.environment}-kv"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 90
  purge_protection_enabled    = var.environment == "prod"
  enable_rbac_authorization   = true

  network_acls {
    bypass                     = "AzureServices"
    default_action             = "Deny"
    ip_rules                   = var.allowed_ips
    virtual_network_subnet_ids = [azurerm_subnet.app.id]
  }

  tags = local.common_tags
}

# Private DNS Zone for Key Vault
resource "azurerm_private_dns_zone" "keyvault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "keyvault" {
  name                  = "${var.project}-keyvault-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.keyvault.name
  virtual_network_id    = azurerm_virtual_network.main.id
}

# Private Endpoint for Key Vault
resource "azurerm_private_endpoint" "keyvault" {
  name                = "${var.project}-${var.environment}-kv-pe"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "${var.project}-${var.environment}-kv-psc"
    private_connection_resource_id = azurerm_key_vault.main.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.keyvault.id]
  }

  tags = local.common_tags
}
```

---

## Storage & CDN

### Storage Account with CDN

```hcl
# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "${replace(var.project, "-", "")}${var.environment}sa"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = var.environment == "prod" ? "GRS" : "LRS"
  account_kind             = "StorageV2"
  access_tier              = "Hot"

  min_tls_version                 = "TLS1_2"
  enable_https_traffic_only       = true
  allow_nested_items_to_be_public = false

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 30
    }

    container_delete_retention_policy {
      days = 30
    }
  }

  network_rules {
    default_action             = "Deny"
    ip_rules                   = var.allowed_ips
    virtual_network_subnet_ids = [azurerm_subnet.app.id]
    bypass                     = ["AzureServices"]
  }

  tags = local.common_tags
}

# Azure Front Door CDN
resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = "${var.project}-${var.environment}-cdn"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Standard_AzureFrontDoor"

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_endpoint" "static" {
  name                     = "static"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_origin_group" "storage" {
  name                     = "storage-origin-group"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  load_balancing {
    sample_size                 = 4
    successful_samples_required = 3
  }

  health_probe {
    interval_in_seconds = 100
    path                = "/"
    protocol            = "Https"
    request_type        = "HEAD"
  }
}

resource "azurerm_cdn_frontdoor_origin" "storage" {
  name                          = "storage-origin"
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.storage.id

  enabled                        = true
  certificate_name_check_enabled = true
  host_name                      = azurerm_storage_account.main.primary_blob_host
  origin_host_header             = azurerm_storage_account.main.primary_blob_host
  http_port                      = 80
  https_port                     = 443
  priority                       = 1
  weight                         = 1000

  private_link {
    location               = azurerm_storage_account.main.location
    private_link_target_id = azurerm_storage_account.main.id
    target_type            = "blob"
    request_message        = "CDN Private Link"
  }
}

resource "azurerm_cdn_frontdoor_route" "static" {
  name                          = "static-route"
  cdn_frontdoor_endpoint_id     = azurerm_cdn_frontdoor_endpoint.static.id
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.storage.id
  cdn_frontdoor_origin_ids      = [azurerm_cdn_frontdoor_origin.storage.id]

  supported_protocols    = ["Http", "Https"]
  patterns_to_match      = ["/*"]
  forwarding_protocol    = "HttpsOnly"
  link_to_default_domain = true
  https_redirect_enabled = true

  cache {
    query_string_caching_behavior = "IgnoreQueryString"
    compression_enabled           = true
    content_types_to_compress     = ["text/html", "text/css", "application/javascript", "application/json"]
  }
}
```

---

## PostgreSQL Flexible Server

```hcl
# Private DNS Zone for PostgreSQL
resource "azurerm_private_dns_zone" "postgres" {
  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = "${var.project}-postgres-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  virtual_network_id    = azurerm_virtual_network.main.id
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.project}-${var.environment}-postgres"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "16"
  delegated_subnet_id    = azurerm_subnet.database.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgres.id
  administrator_login    = var.db_admin_username
  administrator_password = random_password.db_password.result
  zone                   = "1"

  storage_mb   = 32768
  storage_tier = "P30"

  sku_name = var.environment == "prod" ? "GP_Standard_D4s_v3" : "B_Standard_B2s"

  # High availability for production
  dynamic "high_availability" {
    for_each = var.environment == "prod" ? [1] : []
    content {
      mode                      = "ZoneRedundant"
      standby_availability_zone = "2"
    }
  }

  # Backup
  backup_retention_days        = var.environment == "prod" ? 35 : 7
  geo_redundant_backup_enabled = var.environment == "prod"

  # Maintenance
  maintenance_window {
    day_of_week  = 0
    start_hour   = 2
    start_minute = 0
  }

  tags = local.common_tags

  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgres]
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Security configurations
resource "azurerm_postgresql_flexible_server_configuration" "log_checkpoints" {
  name      = "log_checkpoints"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

resource "azurerm_postgresql_flexible_server_configuration" "log_connections" {
  name      = "log_connections"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}

resource "azurerm_postgresql_flexible_server_configuration" "connection_throttling" {
  name      = "connection_throttle.enable"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "on"
}
```

---

## Monitoring & Logging

### Log Analytics Workspace

```hcl
# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.project}-${var.environment}-law"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = var.environment == "prod" ? 90 : 30

  tags = local.common_tags
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "${var.project}-${var.environment}-appinsights"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"

  tags = local.common_tags
}

# Action Group for Alerts
resource "azurerm_monitor_action_group" "main" {
  name                = "${var.project}-${var.environment}-action-group"
  resource_group_name = azurerm_resource_group.main.name
  short_name          = "alerts"

  email_receiver {
    name                    = "ops-team"
    email_address           = var.alert_email
    use_common_alert_schema = true
  }

  webhook_receiver {
    name                    = "slack"
    service_uri             = var.slack_webhook_url
    use_common_alert_schema = true
  }

  tags = local.common_tags
}

# Metric Alert for High CPU
resource "azurerm_monitor_metric_alert" "high_cpu" {
  name                = "${var.project}-${var.environment}-high-cpu"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_kubernetes_cluster.main.id]
  description         = "Alert when CPU exceeds 80%"
  severity            = 2
  frequency           = "PT5M"
  window_size         = "PT15M"

  criteria {
    metric_namespace = "Microsoft.ContainerService/managedClusters"
    metric_name      = "node_cpu_usage_percentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id
  }

  tags = local.common_tags
}

# Activity Log Alert for Security Events
resource "azurerm_monitor_activity_log_alert" "security" {
  name                = "${var.project}-${var.environment}-security-alert"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [data.azurerm_subscription.current.id]
  description         = "Alert on security-related activities"

  criteria {
    category = "Security"
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id
  }

  tags = local.common_tags
}
```

### Diagnostic Settings

```hcl
# Diagnostic Settings for Key Vault
resource "azurerm_monitor_diagnostic_setting" "keyvault" {
  name                       = "diag-${azurerm_key_vault.main.name}"
  target_resource_id         = azurerm_key_vault.main.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  enabled_log {
    category = "AuditEvent"
  }

  enabled_log {
    category = "AzurePolicyEvaluationDetails"
  }

  metric {
    category = "AllMetrics"
  }
}

# Diagnostic Settings for AKS
resource "azurerm_monitor_diagnostic_setting" "aks" {
  name                       = "diag-${azurerm_kubernetes_cluster.main.name}"
  target_resource_id         = azurerm_kubernetes_cluster.main.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  enabled_log {
    category = "kube-apiserver"
  }

  enabled_log {
    category = "kube-audit"
  }

  enabled_log {
    category = "kube-controller-manager"
  }

  enabled_log {
    category = "kube-scheduler"
  }

  enabled_log {
    category = "cluster-autoscaler"
  }

  metric {
    category = "AllMetrics"
  }
}
```
