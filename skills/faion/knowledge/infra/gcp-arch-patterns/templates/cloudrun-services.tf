resource "google_service_account" "services" {
  for_each = var.services

  account_id   = "${each.key}-sa-${var.environment}"
  display_name = "${each.key} Service Account"
}

resource "google_cloud_run_v2_service" "services" {
  for_each = var.services

  name     = "${each.key}-${var.environment}"
  location = var.region

  template {
    service_account = google_service_account.services[each.key].email

    scaling {
      min_instance_count = each.value.min_instances
      max_instance_count = each.value.max_instances
    }

    containers {
      image = each.value.image

      ports { container_port = each.value.port }

      resources {
        limits   = { cpu = each.value.cpu, memory = each.value.memory }
        cpu_idle = true
      }

      startup_probe {
        http_get { path = "/health" }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get { path = "/health" }
        period_seconds = 30
      }

      dynamic "env" {
        for_each = each.value.env_vars
        content { name = env.key; value = env.value }
      }

      dynamic "env" {
        for_each = each.value.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref { secret = env.value; version = "latest" }
          }
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}
