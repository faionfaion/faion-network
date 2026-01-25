---
id: azure-networking
name: "Azure Networking & Monitoring"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Azure Networking & Monitoring

## Overview

Azure networking infrastructure (Virtual Network, NSG, NAT Gateway, private endpoints) and comprehensive monitoring with Log Analytics, Application Insights, and alerts. Follows the Azure Well-Architected Framework pillars.

## When to Use

- Network isolation and segmentation
- Outbound connectivity with NAT Gateway
- Security rules and network policies
- Log aggregation and analysis
- Application performance monitoring
- Metric-based alerting

## Azure Well-Architected Pillars

| Pillar | Focus Areas |
|--------|-------------|
| Reliability | Availability, resiliency, recovery |
| Security | Identity, network security, data protection |
| Cost Optimization | Cost management, efficiency |
| Operational Excellence | Monitoring, deployment, testing |
| Performance Efficiency | Scaling, optimization |

## Virtual Network

### Resource Group

```hcl
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}
```

### VNet and Subnets

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "${var.project}-${var.environment}-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]

  tags = local.common_tags
}

resource "azurerm_subnet" "public" {
  name                 = "public"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]

  service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.Sql",
    "Microsoft.KeyVault"
  ]
}

resource "azurerm_subnet" "private" {
  name                 = "private"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]

  service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.Sql",
    "Microsoft.KeyVault",
    "Microsoft.ContainerRegistry"
  ]

  delegation {
    name = "aks-delegation"
    service_delegation {
      name = "Microsoft.ContainerService/managedClusters"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

resource "azurerm_subnet" "database" {
  name                 = "database"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.3.0/24"]

  service_endpoints = ["Microsoft.Sql"]

  delegation {
    name = "fs"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}
```

## Network Security Group

```hcl
resource "azurerm_network_security_group" "private" {
  name                = "${var.project}-${var.environment}-private-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "AzureLoadBalancer"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = local.common_tags
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private.id
}
```

## NAT Gateway

```hcl
resource "azurerm_public_ip" "nat" {
  name                = "${var.project}-${var.environment}-nat-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = ["1", "2", "3"]

  tags = local.common_tags
}

resource "azurerm_nat_gateway" "main" {
  name                    = "${var.project}-${var.environment}-nat"
  location                = azurerm_resource_group.main.location
  resource_group_name     = azurerm_resource_group.main.name
  sku_name                = "Standard"
  idle_timeout_in_minutes = 10
  zones                   = ["1"]

  tags = local.common_tags
}

resource "azurerm_nat_gateway_public_ip_association" "main" {
  nat_gateway_id       = azurerm_nat_gateway.main.id
  public_ip_address_id = azurerm_public_ip.nat.id
}

resource "azurerm_subnet_nat_gateway_association" "private" {
  subnet_id      = azurerm_subnet.private.id
  nat_gateway_id = azurerm_nat_gateway.main.id
}
```

## Monitoring

### Log Analytics Workspace

```hcl
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.project}-${var.environment}-law"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = var.environment == "prod" ? 90 : 30

  tags = local.common_tags
}
```

### Application Insights

```hcl
resource "azurerm_application_insights" "main" {
  name                = "${var.project}-${var.environment}-appinsights"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"

  tags = local.common_tags
}
```

### Action Group

```hcl
resource "azurerm_monitor_action_group" "main" {
  name                = "${var.project}-${var.environment}-ag"
  resource_group_name = azurerm_resource_group.main.name
  short_name          = "alerts"

  email_receiver {
    name          = "devops"
    email_address = var.alert_email
  }

  tags = local.common_tags
}
```

### Metric Alerts

```hcl
# AKS cluster CPU alert
resource "azurerm_monitor_metric_alert" "aks_cpu" {
  name                = "${var.project}-${var.environment}-aks-cpu"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_kubernetes_cluster.main.id]
  description         = "AKS cluster CPU usage high"
  severity            = 2

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

# PostgreSQL CPU alert
resource "azurerm_monitor_metric_alert" "postgres_cpu" {
  name                = "${var.project}-${var.environment}-postgres-cpu"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_postgresql_flexible_server.main.id]
  description         = "PostgreSQL CPU usage high"
  severity            = 2

  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "cpu_percent"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id
  }

  tags = local.common_tags
}
```

## Best Practices

1. **Use Entra ID (Azure AD)** - Integrate all services with Entra ID for identity management
2. **Enable Azure RBAC** - Use built-in roles and custom role definitions
3. **Use managed identities** - Workload Identity for AKS, system-assigned for other services
4. **Implement private endpoints** - Keep traffic within Azure backbone
5. **Use availability zones** - Deploy across zones for high availability
6. **Enable Defender for Cloud** - Security posture management and threat protection
7. **Use Azure Policy** - Enforce compliance at scale
8. **Enable diagnostic settings** - Send logs to Log Analytics
9. **Tag all resources** - Consistent tagging for cost management
10. **Network segmentation** - Separate subnets for public, private, and database resources

## Common Pitfalls

1. **Service principal keys** - Use managed identities instead of service principal secrets
2. **Public endpoints** - Always use private endpoints for PaaS services in production
3. **Missing NSG rules** - Network security groups should follow least privilege
4. **No soft delete** - Enable soft delete on Key Vault and storage accounts
5. **Ignoring Azure Advisor** - Regular review of Advisor recommendations improves security and cost
6. **Single region deployments** - Critical workloads need multi-region or zone redundancy

## References

- [Azure Well-Architected Framework](https://docs.microsoft.com/azure/architecture/framework/)
- [Azure Virtual Network](https://docs.microsoft.com/azure/virtual-network/)
- [Azure Monitor](https://docs.microsoft.com/azure/azure-monitor/)
- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/fundamentals/best-practices-and-patterns)

## Sources

- [Azure Virtual Network Documentation](https://docs.microsoft.com/en-us/azure/virtual-network/)
- [Azure Load Balancer](https://docs.microsoft.com/en-us/azure/load-balancer/)
- [Azure Application Gateway](https://docs.microsoft.com/en-us/azure/application-gateway/)
- [Azure VPN Gateway](https://docs.microsoft.com/en-us/azure/vpn-gateway/)
- [Azure Networking Best Practices](https://docs.microsoft.com/en-us/azure/architecture/networking/)
