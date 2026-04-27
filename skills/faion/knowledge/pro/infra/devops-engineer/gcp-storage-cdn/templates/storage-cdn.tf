# templates/storage-cdn.tf
# Cloud Storage bucket with lifecycle rules + Cloud CDN + HTTPS LB.
# Variables required: project_id, region, environment, team, domain

resource "google_storage_bucket" "static" {
  name     = "${var.project_id}-static"
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true

  versioning { enabled = true }

  lifecycle_rule {
    condition { age = 90 }
    action { type = "SetStorageClass"; storage_class = "NEARLINE" }
  }
  lifecycle_rule {
    condition { age = 365 }
    action { type = "SetStorageClass"; storage_class = "COLDLINE" }
  }
  lifecycle_rule {
    condition { num_newer_versions = 3 }
    action { type = "Delete" }
  }

  cors {
    origin          = ["https://${var.domain}"]
    method          = ["GET", "HEAD"]
    response_header = ["Content-Type", "Cache-Control"]
    max_age_seconds = 3600
  }

  labels = { environment = var.environment, team = var.team }
}

resource "google_compute_backend_bucket" "static" {
  name        = "${var.project_id}-static-backend"
  bucket_name = google_storage_bucket.static.name
  enable_cdn  = true
  project     = var.project_id

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    max_ttl           = 86400
    client_ttl        = 3600
    negative_caching  = true
    serve_while_stale = 86400

    cache_key_policy {
      include_host         = true
      include_protocol     = true
      include_query_string = false
    }
  }
}

resource "google_compute_global_address" "cdn" {
  name    = "${var.project_id}-cdn-ip"
  project = var.project_id
}

resource "google_compute_managed_ssl_certificate" "cdn" {
  name    = "${var.project_id}-cdn-cert"
  project = var.project_id
  managed { domains = ["static.${var.domain}"] }
}

resource "google_compute_url_map" "cdn" {
  name            = "${var.project_id}-cdn-url-map"
  default_service = google_compute_backend_bucket.static.id
  project         = var.project_id
  host_rule {
    hosts        = ["static.${var.domain}"]
    path_matcher = "static"
  }
  path_matcher {
    name            = "static"
    default_service = google_compute_backend_bucket.static.id
  }
}

resource "google_compute_target_https_proxy" "cdn" {
  name             = "${var.project_id}-cdn-https-proxy"
  url_map          = google_compute_url_map.cdn.id
  ssl_certificates = [google_compute_managed_ssl_certificate.cdn.id]
  project          = var.project_id
}

resource "google_compute_global_forwarding_rule" "cdn" {
  name                  = "${var.project_id}-cdn-https-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.cdn.id
  ip_address            = google_compute_global_address.cdn.id
  project               = var.project_id
}

resource "google_compute_url_map" "http_redirect" {
  name    = "${var.project_id}-cdn-http-redirect"
  project = var.project_id
  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "http_redirect" {
  name    = "${var.project_id}-cdn-http-proxy"
  url_map = google_compute_url_map.http_redirect.id
  project = var.project_id
}

resource "google_compute_global_forwarding_rule" "http_redirect" {
  name                  = "${var.project_id}-cdn-http-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_target_http_proxy.http_redirect.id
  ip_address            = google_compute_global_address.cdn.id
  project               = var.project_id
}

output "cdn_ip" {
  value = google_compute_global_address.cdn.address
}
