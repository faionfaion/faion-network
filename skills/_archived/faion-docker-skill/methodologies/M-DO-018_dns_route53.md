# M-DO-018: DNS Management with Route 53

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #dns, #route53, #aws, #methodology
- **Agent:** faion-devops-agent

---

## Problem

DNS misconfigurations break websites. Manual DNS management is error-prone. No health checks mean users hit dead endpoints.

## Promise

After this methodology, you will manage DNS with Route 53 as code. Your domains will have health checks, failover, and geographic routing.

## Overview

Route 53 provides DNS hosting, domain registration, and health checking. This methodology covers record types, routing policies, and Terraform automation.

---

## Framework

### Step 1: Hosted Zone

```bash
# AWS CLI
aws route53 create-hosted-zone --name example.com --caller-reference $(date +%s)

# Get name servers
aws route53 get-hosted-zone --id Z123456 --query "DelegationSet.NameServers"

# List hosted zones
aws route53 list-hosted-zones
```

```hcl
# Terraform
resource "aws_route53_zone" "main" {
  name = "example.com"

  tags = {
    Environment = var.environment
  }
}

output "name_servers" {
  value = aws_route53_zone.main.name_servers
}
```

### Step 2: Record Types

```hcl
# A Record (IPv4)
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = 300
  records = ["1.2.3.4"]
}

# AAAA Record (IPv6)
resource "aws_route53_record" "www_ipv6" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "AAAA"
  ttl     = 300
  records = ["2001:0db8::1"]
}

# CNAME Record
resource "aws_route53_record" "blog" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "blog.example.com"
  type    = "CNAME"
  ttl     = 300
  records = ["example.com"]
}

# MX Records
resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "MX"
  ttl     = 3600
  records = [
    "10 mail1.example.com",
    "20 mail2.example.com"
  ]
}

# TXT Record (SPF, DKIM, etc.)
resource "aws_route53_record" "spf" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "TXT"
  ttl     = 3600
  records = ["v=spf1 include:_spf.google.com ~all"]
}

# Alias Record (AWS resources)
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}
```

### Step 3: Routing Policies

```hcl
# Simple Routing (default)
resource "aws_route53_record" "simple" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"
  ttl     = 300
  records = ["1.2.3.4"]
}

# Weighted Routing
resource "aws_route53_record" "weighted_a" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "server-a"
  records        = ["1.2.3.4"]

  weighted_routing_policy {
    weight = 70
  }
}

resource "aws_route53_record" "weighted_b" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "server-b"
  records        = ["5.6.7.8"]

  weighted_routing_policy {
    weight = 30
  }
}

# Latency Routing
resource "aws_route53_record" "latency_us" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "us-east-1"

  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }

  latency_routing_policy {
    region = "us-east-1"
  }
}

resource "aws_route53_record" "latency_eu" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "eu-west-1"

  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }

  latency_routing_policy {
    region = "eu-west-1"
  }
}

# Geolocation Routing
resource "aws_route53_record" "geo_eu" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "eu"

  alias {
    name                   = aws_lb.eu.dns_name
    zone_id                = aws_lb.eu.zone_id
    evaluate_target_health = true
  }

  geolocation_routing_policy {
    continent = "EU"
  }
}

resource "aws_route53_record" "geo_default" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "default"

  alias {
    name                   = aws_lb.us.dns_name
    zone_id                = aws_lb.us.zone_id
    evaluate_target_health = true
  }

  geolocation_routing_policy {
    country = "*"
  }
}
```

### Step 4: Health Checks

```hcl
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "primary-health-check"
  }
}

resource "aws_route53_health_check" "calculated" {
  type                   = "CALCULATED"
  child_health_threshold = 2
  child_healthchecks     = [
    aws_route53_health_check.primary.id,
    aws_route53_health_check.secondary.id,
  ]

  tags = {
    Name = "calculated-health-check"
  }
}

# CloudWatch alarm for health check
resource "aws_cloudwatch_metric_alarm" "health_check" {
  alarm_name          = "route53-health-check-failed"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "HealthCheckStatus"
  namespace           = "AWS/Route53"
  period              = 60
  statistic           = "Minimum"
  threshold           = 1

  dimensions = {
    HealthCheckId = aws_route53_health_check.primary.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

### Step 5: Failover Routing

```hcl
# Primary record
resource "aws_route53_record" "primary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "primary"

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
}

# Secondary record
resource "aws_route53_record" "secondary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "secondary"

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type = "SECONDARY"
  }
}
```

### Step 6: DNS Validation for ACM

```hcl
resource "aws_acm_certificate" "main" {
  domain_name               = "example.com"
  subject_alternative_names = ["*.example.com"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  zone_id = aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
}
```

---

## Templates

### Complete Domain Setup

```hcl
# Zone
resource "aws_route53_zone" "main" {
  name = var.domain
}

# Apex -> ALB
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# www -> apex
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain}"
  type    = "CNAME"
  ttl     = 300
  records = [var.domain]
}

# API subdomain
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_lb.api.dns_name
    zone_id                = aws_lb.api.zone_id
    evaluate_target_health = true
  }
}

# Email records
resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "MX"
  ttl     = 3600
  records = var.mx_records
}

resource "aws_route53_record" "spf" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "TXT"
  ttl     = 3600
  records = ["v=spf1 include:_spf.google.com ~all"]
}

resource "aws_route53_record" "dkim" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "google._domainkey.${var.domain}"
  type    = "TXT"
  ttl     = 3600
  records = [var.dkim_record]
}

resource "aws_route53_record" "dmarc" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "_dmarc.${var.domain}"
  type    = "TXT"
  ttl     = 3600
  records = ["v=DMARC1; p=quarantine; rua=mailto:dmarc@${var.domain}"]
}
```

---

## Common Mistakes

1. **Long TTLs during migration** - Use short TTL before changes
2. **Missing health checks** - Failover doesn't work
3. **Naked CNAME** - Can't use CNAME at apex
4. **No backup nameservers** - Update registrar with all NS
5. **Forgetting propagation time** - Allow 48 hours for changes

---

## Checklist

- [ ] Hosted zone created
- [ ] Name servers updated at registrar
- [ ] A/AAAA records for apex
- [ ] CNAME/Alias for subdomains
- [ ] MX records for email
- [ ] SPF, DKIM, DMARC for email auth
- [ ] Health checks configured
- [ ] Failover routing for HA
- [ ] Low TTL during migrations

---

## Next Steps

- M-DO-017: Cloud Networking
- M-DO-015: SSL Certificates
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-018 v1.0*
