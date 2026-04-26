locals {
  instance_name = "${var.project_id}-postgres-${var.environment}"
  is_prod       = var.environment == "prod"
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}

resource "google_sql_database_instance" "main" {
  name             = local.instance_name
  database_version = var.database_version
  region           = var.region

  deletion_protection = local.is_prod

  settings {
    tier              = local.is_prod ? var.tier : "db-f1-micro"
    availability_type = local.is_prod ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = var.disk_size
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = local.is_prod
      backup_retention_settings {
        retained_backups = local.is_prod ? 30 : 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
      require_ssl     = true
    }

    insights_config {
      query_insights_enabled = true
      query_string_length    = 1024
    }

    database_flags { name = "log_checkpoints";   value = "on" }
    database_flags { name = "log_connections";   value = "on" }
    database_flags { name = "log_disconnections"; value = "on" }
    database_flags { name = "log_lock_waits";    value = "on" }
  }
}

resource "google_sql_database" "databases" {
  for_each = toset(var.databases)
  name     = each.value
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "app"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
