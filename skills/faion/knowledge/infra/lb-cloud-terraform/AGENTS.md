# Cloud Load Balancer Provisioning with Terraform

## Summary

**One-sentence:** Generates Terraform HCL for AWS ALB/NLB or GCP Global HTTP(S) LB with TLS-1.2+ listener, S3/CS access logs, deletion protection, target groups, and WAF wiring.

**One-paragraph:** Terraform modules for AWS ALB (Application Load Balancer), AWS NLB (Network Load Balancer), and GCP Global HTTP(S) Load Balancer. Covers: `aws_lb` resource with deletion protection and access logs to S3, target groups with health-check configuration, HTTPS listener with `ELBSecurityPolicy-TLS13-1-2-2021-06`, HTTP-to-HTTPS redirect listener, security groups, and GCP backend services with CDN policy, URL maps, managed SSL certificates, and Cloud Armor binding. Aimed at cloud-native teams replacing self-hosted HAProxy/Nginx with managed LBs.

**Ефективно для:**

- Greenfield AWS/GCP service: ALB або Global LB як точка входу.
- Migration: HAProxy / Nginx self-hosted → AWS ALB або GCP Cloud LB через Terraform.
- WAF + Shield (AWS) / Cloud Armor (GCP) attachment поверх існуючого LB.
- NLB для TCP/UDP workloads (DB proxies, Redis, gaming) на AWS.
- Modular Terraform: dev/stage/prod через `terraform workspace` + var-files.

## Applies If (ALL must hold)

- Provisioning a new cloud LB for a service on AWS or GCP using Terraform.
- Migrating from self-hosted HAProxy / Nginx to AWS ALB or GCP Cloud LB.
- Adding WAF, Shield, or Cloud Armor to an existing cloud LB via Terraform.
- Setting up NLB for TCP/UDP workloads (databases, Redis) on AWS.

## Skip If (ANY kills it)

- Kubernetes workloads — use AWS Load Balancer Controller or GKE Ingress; the controllers manage target group registration automatically.
- Self-hosted bare-metal environments — Terraform AWS/GCP providers need cloud API access; use HAProxy + keepalived.
- Azure — use `azurerm_application_gateway` or `azurerm_frontdoor`; patterns differ from AWS/GCP.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPC + subnet IDs | strings | network module |
| ACM / GCS-managed cert ARN/ID | string | cert module |
| Backend target list | IPs / instance IDs / NEG | service module |
| Access-log bucket | S3 / GCS bucket | logging module |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-technology-selection]] | Confirms ALB vs NLB vs Global LB before writing Terraform. |
| [[lb-monitoring]] | Access-log + metric wiring depends on LB choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: deletion-protection-on, tls-1-2-min-policy, access-logs-enabled, http-to-https-redirect, security-group-tight | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-lb-product` | sonnet | ALB vs NLB vs Global LB decision tree. |
| `emit-terraform` | sonnet | Structured HCL authoring. |
| `lint-tfsec-tflint` | haiku | Mechanical static analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alb.tf` | Complete AWS ALB module: lb + listener + target group + redirect + S3 logs |
| `templates/gcp-global-lb.tf` | GCP Global HTTP(S) LB: backend service + URL map + managed cert + Cloud Armor |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-cloud-terraform.py` | Validate the Terraform artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-technology-selection]]
- [[lb-monitoring]]
- [[lb-layer-selection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (cloud provider, protocol, geographic reach, WAF need) to a concrete LB product + Terraform shape, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/alb.tf`

```hcl
variable "environment"        { type = string }
variable "vpc_id"             { type = string }
variable "public_subnet_ids"  { type = list(string) }
variable "certificate_arn"    { type = string }
variable "access_logs_bucket" { type = string }

resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb"
  description = "ALB ingress: 80 (redirect) + 443 (TLS)"
  vpc_id      = var.vpc_id

  ingress { from_port = 80  to_port = 80  protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 443 to_port = 443 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0   to_port = 0   protocol = "-1"  cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_lb" "main" {
  name                       = "${var.environment}-alb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.alb.id]
  subnets                    = var.public_subnet_ids
  enable_deletion_protection = true
  enable_http2               = true
  idle_timeout               = 60

  access_logs {
    bucket  = var.access_logs_bucket
    prefix  = "alb-${var.environment}"
    enabled = true
  }

  lifecycle { prevent_destroy = true }

  tags = { Name = "${var.environment}-alb", Environment = var.environment }
}

resource "aws_lb_target_group" "web" {
  name        = "${var.environment}-web-tg"
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    enabled             = true
    path                = "/health"
    port                = "traffic-port"
    matcher             = "200"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
    timeout             = 5
  }

  deregistration_delay = 30
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_security_group" "backend" {
  name        = "${var.environment}-backend"
  description = "Backend SG — only ALB SG may ingress"
  vpc_id      = var.vpc_id

  ingress {
    from_port                = 8080
    to_port                  = 8080
    protocol                 = "tcp"
    security_groups          = [aws_security_group.alb.id]
  }
  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}

output "alb_dns_name" { value = aws_lb.main.dns_name }
```

### `templates/gcp-global-lb.tf`

```hcl
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
```
