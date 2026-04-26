# Azure Compute Examples

Production-ready Terraform and Bicep examples for Azure compute services.

---

## Virtual Machines

### Terraform: Production VM with Managed Identity

```hcl
# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = var.location
  tags     = local.common_tags
}

# User Assigned Identity
resource "azurerm_user_assigned_identity" "vm" {
  name                = "${var.project}-${var.environment}-vm-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

# Network Security Group
resource "azurerm_network_security_group" "vm" {
  name                = "${var.project}-${var.environment}-vm-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefixes    = var.allowed_ssh_ips
    destination_address_prefix = "*"
  }

  tags = local.common_tags
}

# Network Interface
resource "azurerm_network_interface" "vm" {
  name                = "${var.project}-${var.environment}-vm-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.private.id
    private_ip_address_allocation = "Dynamic"
  }

  tags = local.common_tags
}

resource "azurerm_network_interface_security_group_association" "vm" {
  network_interface_id      = azurerm_network_interface.vm.id
  network_security_group_id = azurerm_network_security_group.vm.id
}

# Linux Virtual Machine
resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.project}-${var.environment}-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_D4s_v5"
  zone                = "1"
  admin_username      = "azureadmin"

  network_interface_ids = [azurerm_network_interface.vm.id]

  admin_ssh_key {
    username   = "azureadmin"
    public_key = var.ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 128
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.vm.id]
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.diagnostics.primary_blob_endpoint
  }

  tags = local.common_tags
}

# Azure Backup
resource "azurerm_recovery_services_vault" "main" {
  name                = "${var.project}-${var.environment}-rsv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  soft_delete_enabled = true
  tags                = local.common_tags
}

resource "azurerm_backup_policy_vm" "daily" {
  name                = "daily-backup"
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.main.name

  backup {
    frequency = "Daily"
    time      = "02:00"
  }

  retention_daily {
    count = 30
  }

  retention_weekly {
    count    = 12
    weekdays = ["Sunday"]
  }
}

resource "azurerm_backup_protected_vm" "main" {
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.main.name
  source_vm_id        = azurerm_linux_virtual_machine.main.id
  backup_policy_id    = azurerm_backup_policy_vm.daily.id
}
```

---

## Virtual Machine Scale Sets (VMSS)

### Terraform: Flexible VMSS with Spot Priority Mix

```hcl
# User Assigned Identity
resource "azurerm_user_assigned_identity" "vmss" {
  name                = "${var.project}-${var.environment}-vmss-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

# Load Balancer
resource "azurerm_lb" "main" {
  name                = "${var.project}-${var.environment}-lb"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.lb.id
  }

  tags = local.common_tags
}

resource "azurerm_lb_backend_address_pool" "main" {
  loadbalancer_id = azurerm_lb.main.id
  name            = "vmss-backend"
}

resource "azurerm_lb_probe" "http" {
  loadbalancer_id = azurerm_lb.main.id
  name            = "http-probe"
  port            = 80
  protocol        = "Http"
  request_path    = "/health"
}

resource "azurerm_lb_rule" "http" {
  loadbalancer_id                = azurerm_lb.main.id
  name                           = "http-rule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "PublicIPAddress"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.main.id]
  probe_id                       = azurerm_lb_probe.http.id
}

# Virtual Machine Scale Set (Flexible)
resource "azurerm_orchestrated_virtual_machine_scale_set" "main" {
  name                        = "${var.project}-${var.environment}-vmss"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  platform_fault_domain_count = 1  # Max spreading
  zones                       = ["1", "2", "3"]

  sku_name  = "Standard_D4s_v5"
  instances = var.vmss_instance_count

  # Spot Priority Mix
  priority        = "Spot"
  eviction_policy = "Deallocate"
  max_bid_price   = -1

  priority_mix {
    base_regular_count            = 2
    regular_percentage_above_base = 25
  }

  os_profile {
    linux_configuration {
      admin_username                  = "azureadmin"
      disable_password_authentication = true

      admin_ssh_key {
        username   = "azureadmin"
        public_key = var.ssh_public_key
      }
    }
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  os_disk {
    storage_account_type = "Premium_LRS"
    caching              = "ReadWrite"
  }

  network_interface {
    name    = "nic"
    primary = true

    ip_configuration {
      name                                   = "internal"
      primary                                = true
      subnet_id                              = azurerm_subnet.private.id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.main.id]
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.vmss.id]
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.diagnostics.primary_blob_endpoint
  }

  extension {
    name                 = "HealthExtension"
    publisher            = "Microsoft.ManagedServices"
    type                 = "ApplicationHealthLinux"
    type_handler_version = "1.0"

    settings = jsonencode({
      protocol    = "http"
      port        = 80
      requestPath = "/health"
    })
  }

  automatic_instance_repair {
    enabled      = true
    grace_period = "PT30M"
  }

  tags = local.common_tags
}

# Autoscale Settings
resource "azurerm_monitor_autoscale_setting" "vmss" {
  name                = "${var.project}-${var.environment}-autoscale"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  target_resource_id  = azurerm_orchestrated_virtual_machine_scale_set.main.id

  profile {
    name = "defaultProfile"

    capacity {
      default = var.vmss_instance_count
      minimum = var.vmss_min_count
      maximum = var.vmss_max_count
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_orchestrated_virtual_machine_scale_set.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 75
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "2"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_orchestrated_virtual_machine_scale_set.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 25
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }
  }
}
```

---

## Azure Kubernetes Service (AKS)

### Terraform: Production AKS with Workload Identity and KEDA

```hcl
# User Assigned Identity for AKS
resource "azurerm_user_assigned_identity" "aks" {
  name                = "${var.project}-${var.environment}-aks-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.project}-${var.environment}-law"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.common_tags
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
    outbound_type       = "loadBalancer"
  }

  # System node pool
  default_node_pool {
    name                         = "system"
    vm_size                      = "Standard_D2s_v5"
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

  # Azure AD RBAC
  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }

  # Workload Identity (enable BEFORE KEDA)
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
    secret_rotation_enabled  = true
    rotation_poll_interval   = "2m"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  microsoft_defender {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  monitor_metrics {}

  # KEDA (enabled after workload identity)
  workload_autoscaler_profile {
    keda_enabled = true
  }

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
  max_count           = 20

  upgrade_settings {
    max_surge = "33%"
  }

  node_labels = {
    "nodepool-type" = "user"
    "workload"      = "general"
  }

  tags = local.common_tags
}

# Spot Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "spot" {
  name                  = "spot"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D4s_v5"
  vnet_subnet_id        = azurerm_subnet.aks.id
  zones                 = ["1", "2", "3"]

  enable_auto_scaling = true
  min_count           = 0
  max_count           = 50

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

  tags = local.common_tags
}

# Workload Identity for Application
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.project}-${var.environment}-app-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

resource "azurerm_federated_identity_credential" "app" {
  name                = "kubernetes-federated-credential"
  resource_group_name = azurerm_resource_group.main.name
  parent_id           = azurerm_user_assigned_identity.app.id
  audience            = ["api://AzureADTokenExchange"]
  issuer              = azurerm_kubernetes_cluster.main.oidc_issuer_url
  subject             = "system:serviceaccount:${var.namespace}:${var.service_account_name}"
}

# Role assignments for app identity
resource "azurerm_role_assignment" "app_keyvault" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

### Kubernetes: Workload with Spot Toleration and HPA

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: app
      tolerations:
        - key: "kubernetes.azure.com/scalesetpriority"
          operator: "Equal"
          value: "spot"
          effect: "NoSchedule"
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: "kubernetes.azure.com/scalesetpriority"
                    operator: In
                    values:
                      - "spot"
      containers:
        - name: app
          image: myregistry.azurecr.io/app:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
---
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
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

### KEDA: Azure Service Bus Queue Scaler

```yaml
# keda-scaledobject.yaml
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: azure-servicebus-auth
  namespace: default
spec:
  podIdentity:
    provider: azure-workload
    identityId: <app-identity-client-id>
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: app-scaledobject
  namespace: default
spec:
  scaleTargetRef:
    name: app
  pollingInterval: 15
  cooldownPeriod: 300
  minReplicaCount: 0
  maxReplicaCount: 50
  triggers:
    - type: azure-servicebus
      metadata:
        queueName: orders
        namespace: myservicebus
        messageCount: "5"
      authenticationRef:
        name: azure-servicebus-auth
```

---

## Azure Container Apps

### Terraform: Container App with Dapr and KEDA

```hcl
# Container Apps Environment
resource "azurerm_container_app_environment" "main" {
  name                       = "${var.project}-${var.environment}-cae"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  infrastructure_subnet_id = azurerm_subnet.container_apps.id

  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
  }

  tags = local.common_tags
}

# Dapr Component: State Store (Azure Blob)
resource "azurerm_container_app_environment_dapr_component" "statestore" {
  name                         = "statestore"
  container_app_environment_id = azurerm_container_app_environment.main.id
  component_type               = "state.azure.blobstorage"
  version                      = "v1"

  metadata {
    name  = "accountName"
    value = azurerm_storage_account.main.name
  }

  metadata {
    name  = "containerName"
    value = "state"
  }

  metadata {
    name        = "azureClientId"
    secret_name = "azure-client-id"
  }

  secret {
    name  = "azure-client-id"
    value = azurerm_user_assigned_identity.app.client_id
  }
}

# Dapr Component: Pub/Sub (Azure Service Bus)
resource "azurerm_container_app_environment_dapr_component" "pubsub" {
  name                         = "pubsub"
  container_app_environment_id = azurerm_container_app_environment.main.id
  component_type               = "pubsub.azure.servicebus.topics"
  version                      = "v1"

  metadata {
    name  = "namespaceName"
    value = "${azurerm_servicebus_namespace.main.name}.servicebus.windows.net"
  }

  scopes = ["api", "worker"]
}

# Container App: API
resource "azurerm_container_app" "api" {
  name                         = "${var.project}-api"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Multiple"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  template {
    container {
      name   = "api"
      image  = "${azurerm_container_registry.main.login_server}/api:${var.api_version}"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "ASPNETCORE_ENVIRONMENT"
        value = var.environment
      }

      env {
        name        = "ConnectionStrings__Database"
        secret_name = "db-connection"
      }

      liveness_probe {
        transport = "HTTP"
        path      = "/health/live"
        port      = 8080
      }

      readiness_probe {
        transport = "HTTP"
        path      = "/health/ready"
        port      = 8080
      }
    }

    min_replicas = var.environment == "prod" ? 2 : 1
    max_replicas = 20

    http_scale_rule {
      name                = "http-scaling"
      concurrent_requests = 100
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    transport        = "http"

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  dapr {
    app_id       = "api"
    app_port     = 8080
    app_protocol = "http"
  }

  secret {
    name  = "db-connection"
    value = "Server=${azurerm_postgresql_flexible_server.main.fqdn};Database=${var.database_name};Port=5432;User Id=${var.db_admin_username};Password=${random_password.db_password.result};Ssl Mode=Require;"
  }

  registry {
    server   = azurerm_container_registry.main.login_server
    identity = azurerm_user_assigned_identity.app.id
  }

  tags = local.common_tags
}

# Container App: Worker (with KEDA scaling)
resource "azurerm_container_app" "worker" {
  name                         = "${var.project}-worker"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  template {
    container {
      name   = "worker"
      image  = "${azurerm_container_registry.main.login_server}/worker:${var.worker_version}"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "ASPNETCORE_ENVIRONMENT"
        value = var.environment
      }
    }

    min_replicas = 0  # Scale to zero
    max_replicas = 30

    # KEDA Azure Service Bus scaler
    custom_scale_rule {
      name             = "servicebus-scaling"
      custom_rule_type = "azure-servicebus"

      metadata = {
        queueName    = "orders"
        namespace    = azurerm_servicebus_namespace.main.name
        messageCount = "5"
      }

      authentication {
        secret_name       = "servicebus-connection"
        trigger_parameter = "connection"
      }
    }
  }

  dapr {
    app_id       = "worker"
    app_port     = 8080
    app_protocol = "http"
  }

  secret {
    name  = "servicebus-connection"
    value = azurerm_servicebus_namespace.main.default_primary_connection_string
  }

  registry {
    server   = azurerm_container_registry.main.login_server
    identity = azurerm_user_assigned_identity.app.id
  }

  tags = local.common_tags
}
```

---

## Azure App Service

### Terraform: App Service with Deployment Slots

```hcl
# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.project}-${var.environment}-asp"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = var.environment == "prod" ? "P1v3" : "B1"

  tags = local.common_tags
}

# User Assigned Identity
resource "azurerm_user_assigned_identity" "app" {
  name                = "${var.project}-${var.environment}-app-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

# Linux Web App
resource "azurerm_linux_web_app" "main" {
  name                = "${var.project}-${var.environment}-app"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  site_config {
    always_on                = var.environment == "prod"
    http2_enabled            = true
    minimum_tls_version      = "1.2"
    ftps_state               = "Disabled"
    health_check_path        = "/health"
    health_check_eviction_time_in_min = 5

    application_stack {
      docker_image_name        = "app:${var.app_version}"
      docker_registry_url      = "https://${azurerm_container_registry.main.login_server}"
      docker_registry_username = null  # Use Managed Identity
      docker_registry_password = null
    }

    ip_restriction {
      action      = "Allow"
      ip_address  = var.allowed_ip_range
      name        = "AllowedIPs"
      priority    = 100
    }
  }

  app_settings = {
    "ASPNETCORE_ENVIRONMENT"                      = var.environment
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE"         = "false"
    "DOCKER_REGISTRY_SERVER_URL"                  = "https://${azurerm_container_registry.main.login_server}"
    "AZURE_CLIENT_ID"                             = azurerm_user_assigned_identity.app.client_id
    "KeyVault__VaultUri"                          = azurerm_key_vault.main.vault_uri
  }

  connection_string {
    name  = "Database"
    type  = "PostgreSQL"
    value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_connection.id})"
  }

  logs {
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 100
      }
    }
    application_logs {
      file_system_level = "Information"
    }
  }

  tags = local.common_tags
}

# Staging Slot
resource "azurerm_linux_web_app_slot" "staging" {
  name           = "staging"
  app_service_id = azurerm_linux_web_app.main.id
  https_only     = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  site_config {
    always_on                = false  # Save costs on staging
    http2_enabled            = true
    minimum_tls_version      = "1.2"
    ftps_state               = "Disabled"
    health_check_path        = "/health"

    application_stack {
      docker_image_name        = "app:${var.app_version}"
      docker_registry_url      = "https://${azurerm_container_registry.main.login_server}"
    }
  }

  app_settings = {
    "ASPNETCORE_ENVIRONMENT"              = "Staging"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://${azurerm_container_registry.main.login_server}"
    "AZURE_CLIENT_ID"                     = azurerm_user_assigned_identity.app.client_id
    "KeyVault__VaultUri"                  = azurerm_key_vault.main.vault_uri
  }

  connection_string {
    name  = "Database"
    type  = "PostgreSQL"
    value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_connection_staging.id})"
  }

  tags = local.common_tags
}

# Autoscale Settings (Production only)
resource "azurerm_monitor_autoscale_setting" "app" {
  count               = var.environment == "prod" ? 1 : 0
  name                = "${var.project}-${var.environment}-autoscale"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  target_resource_id  = azurerm_service_plan.main.id

  profile {
    name = "defaultProfile"

    capacity {
      default = 2
      minimum = 2
      maximum = 10
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 70
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT10M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT10M"
      }
    }
  }
}
```

### Bicep: App Service with Slots

```bicep
@description('Project name')
param project string

@description('Environment name')
@allowed(['dev', 'staging', 'prod'])
param environment string

@description('Location')
param location string = resourceGroup().location

@description('App version tag')
param appVersion string

@description('Container registry name')
param containerRegistryName string

var appServicePlanName = '${project}-${environment}-asp'
var webAppName = '${project}-${environment}-app'
var identityName = '${project}-${environment}-app-identity'

// User Assigned Identity
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: environment == 'prod' ? 'P1v3' : 'B1'
    tier: environment == 'prod' ? 'PremiumV3' : 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      alwaysOn: environment == 'prod'
      http20Enabled: true
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      healthCheckPath: '/health'
      linuxFxVersion: 'DOCKER|${containerRegistryName}.azurecr.io/app:${appVersion}'
      acrUseManagedIdentityCreds: true
      acrUserManagedIdentityID: identity.properties.clientId
    }
    clientAffinityEnabled: false
  }
}

// Staging Slot
resource stagingSlot 'Microsoft.Web/sites/slots@2023-01-01' = {
  parent: webApp
  name: 'staging'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      alwaysOn: false
      http20Enabled: true
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      healthCheckPath: '/health'
      linuxFxVersion: 'DOCKER|${containerRegistryName}.azurecr.io/app:${appVersion}'
      acrUseManagedIdentityCreds: true
      acrUserManagedIdentityID: identity.properties.clientId
    }
  }
}

// Slot Config Names (settings that stay with slot)
resource slotConfigNames 'Microsoft.Web/sites/config@2023-01-01' = {
  parent: webApp
  name: 'slotConfigNames'
  properties: {
    appSettingNames: [
      'ASPNETCORE_ENVIRONMENT'
    ]
    connectionStringNames: [
      'Database'
    ]
  }
}

output webAppName string = webApp.name
output webAppHostName string = webApp.properties.defaultHostName
output stagingSlotHostName string = stagingSlot.properties.defaultHostName
output identityClientId string = identity.properties.clientId
```

---

## Common Variables

### variables.tf

```hcl
variable "project" {
  description = "Project name"
  type        = string
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
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.29"
}

variable "authorized_ip_ranges" {
  description = "IP ranges authorized to access AKS API"
  type        = list(string)
  default     = []
}

variable "allowed_ssh_ips" {
  description = "IP addresses allowed for SSH access"
  type        = list(string)
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
  sensitive   = true
}

variable "vmss_instance_count" {
  description = "Initial VMSS instance count"
  type        = number
  default     = 2
}

variable "vmss_min_count" {
  description = "Minimum VMSS instances"
  type        = number
  default     = 2
}

variable "vmss_max_count" {
  description = "Maximum VMSS instances"
  type        = number
  default     = 20
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "default"
}

variable "service_account_name" {
  description = "Kubernetes service account name"
  type        = string
  default     = "app"
}

variable "app_version" {
  description = "Application version tag"
  type        = string
}

variable "api_version" {
  description = "API version tag"
  type        = string
}

variable "worker_version" {
  description = "Worker version tag"
  type        = string
}

variable "database_name" {
  description = "Database name"
  type        = string
}

variable "db_admin_username" {
  description = "Database admin username"
  type        = string
}

locals {
  common_tags = {
    project     = var.project
    environment = var.environment
    managed_by  = "terraform"
  }
}
```
