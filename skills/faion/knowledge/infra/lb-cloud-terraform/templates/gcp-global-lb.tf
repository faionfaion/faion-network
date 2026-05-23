# purpose: GCP Global HTTP(S) LB Terraform module (backend service + URL map + managed cert + Cloud Armor)
# consumes: see content/02-output-contract.xml inputs (provider=gcp, lb_type=gcp-global-http, tls_policy=MODERN)
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml (deletion-protection-on, tls-1-2-min-policy, access-logs-enabled)
# token-budget-impact: ~700 tokens when loaded as context

variable "project" { type = string }
variable "domain"  { type = string }

resource "google_compute_managed_ssl_certificate" "default" {
  name    = "managed-cert-${var.domain}"
  managed { domains = [var.domain] }
}

resource "google_compute_ssl_policy" "modern" {
  name            = "modern-tls-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}

resource "google_compute_security_policy" "armor" {
  name = "default-armor"

  rule {
    action   = "allow"
    priority = 2147483647
    match {
      versioned_expr = "SRC_IPS_V1"
      config { src_ip_ranges = ["*"] }
    }
    description = "default allow"
  }

  rule {
    action   = "rate_based_ban"
    priority = 1000
    match {
      versioned_expr = "SRC_IPS_V1"
      config { src_ip_ranges = ["*"] }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      enforce_on_key = "IP"
      rate_limit_threshold { count = 600 interval_sec = 60 }
    }
    description = "rate limit 600/min/IP"
  }
}

resource "google_compute_backend_service" "web" {
  name                  = "web-backend"
  protocol              = "HTTP"
  port_name             = "http"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30
  security_policy       = google_compute_security_policy.armor.id

  log_config {
    enable      = true
    sample_rate = 1.0
  }

  health_checks = [google_compute_health_check.default.id]

  lifecycle { prevent_destroy = true }
}

resource "google_compute_health_check" "default" {
  name = "web-hc"

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}

resource "google_compute_url_map" "default" {
  name            = "web-url-map"
  default_service = google_compute_backend_service.web.id
}

resource "google_compute_target_https_proxy" "default" {
  name             = "web-https-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
  ssl_policy       = google_compute_ssl_policy.modern.id
}

resource "google_compute_global_forwarding_rule" "https" {
  name                  = "web-https-fr"
  target                = google_compute_target_https_proxy.default.id
  port_range            = "443"
  load_balancing_scheme = "EXTERNAL_MANAGED"

  lifecycle { prevent_destroy = true }
}

resource "google_compute_url_map" "http_redirect" {
  name = "web-http-redirect"
  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "redirect" {
  name    = "web-http-proxy"
  url_map = google_compute_url_map.http_redirect.id
}

resource "google_compute_global_forwarding_rule" "http_redirect" {
  name                  = "web-http-fr"
  target                = google_compute_target_http_proxy.redirect.id
  port_range            = "80"
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

output "global_lb_ip" {
  value = google_compute_global_forwarding_rule.https.ip_address
}
