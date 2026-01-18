# M-DO-019: CDN with CloudFront

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #cdn, #cloudfront, #performance, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Serving assets from a single location creates latency for global users. Origin servers handle all traffic, limiting scalability. No caching means repeated computation.

## Promise

After this methodology, you will accelerate content delivery with CloudFront. Your assets will be cached globally, improving performance and reducing origin load.

## Overview

CloudFront is AWS's CDN with edge locations worldwide. It caches content, terminates TLS, and provides DDoS protection. Works with S3, ALB, and custom origins.

---

## Framework

### Step 1: S3 Origin Distribution

```hcl
# S3 bucket for static assets
resource "aws_s3_bucket" "static" {
  bucket = "my-app-static-assets"
}

resource "aws_s3_bucket_public_access_block" "static" {
  bucket = aws_s3_bucket.static.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Origin Access Control
resource "aws_cloudfront_origin_access_control" "static" {
  name                              = "static-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "static" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = "PriceClass_100"  # US, Canada, Europe
  aliases             = ["static.example.com"]

  origin {
    domain_name              = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id                = "S3-static"
    origin_access_control_id = aws_cloudfront_origin_access_control.static.id
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-static"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    cache_policy_id          = aws_cloudfront_cache_policy.static.id
    origin_request_policy_id = aws_cloudfront_origin_request_policy.static.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}

# S3 bucket policy for CloudFront
resource "aws_s3_bucket_policy" "static" {
  bucket = aws_s3_bucket.static.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowCloudFrontOAC"
      Effect    = "Allow"
      Principal = {
        Service = "cloudfront.amazonaws.com"
      }
      Action   = "s3:GetObject"
      Resource = "${aws_s3_bucket.static.arn}/*"
      Condition = {
        StringEquals = {
          "AWS:SourceArn" = aws_cloudfront_distribution.static.arn
        }
      }
    }]
  })
}
```

### Step 2: Cache Policies

```hcl
# Cache policy for static assets
resource "aws_cloudfront_cache_policy" "static" {
  name        = "static-assets"
  min_ttl     = 86400      # 1 day
  default_ttl = 604800     # 7 days
  max_ttl     = 31536000   # 1 year

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "none"
    }
    query_strings_config {
      query_string_behavior = "none"
    }
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }
}

# Cache policy for API
resource "aws_cloudfront_cache_policy" "api" {
  name        = "api-caching"
  min_ttl     = 0
  default_ttl = 0
  max_ttl     = 60

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = ["Authorization"]
      }
    }
    query_strings_config {
      query_string_behavior = "all"
    }
  }
}

# Origin request policy
resource "aws_cloudfront_origin_request_policy" "api" {
  name = "api-origin-request"

  cookies_config {
    cookie_behavior = "all"
  }
  headers_config {
    header_behavior = "allViewer"
  }
  query_strings_config {
    query_string_behavior = "all"
  }
}
```

### Step 3: ALB Origin

```hcl
resource "aws_cloudfront_distribution" "app" {
  enabled         = true
  is_ipv6_enabled = true
  aliases         = ["app.example.com"]

  # ALB origin
  origin {
    domain_name = aws_lb.app.dns_name
    origin_id   = "ALB"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-Origin-Verify"
      value = var.origin_verify_header
    }
  }

  # S3 origin for static assets
  origin {
    domain_name              = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id                = "S3-static"
    origin_access_control_id = aws_cloudfront_origin_access_control.static.id
  }

  # Default behavior -> ALB
  default_cache_behavior {
    target_origin_id       = "ALB"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]

    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"  # CachingDisabled
    origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa07d3"  # AllViewer
  }

  # Static assets -> S3
  ordered_cache_behavior {
    path_pattern           = "/static/*"
    target_origin_id       = "S3-static"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    cache_policy_id = aws_cloudfront_cache_policy.static.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

### Step 4: Lambda@Edge

```javascript
// Origin Request - Add authentication
exports.handler = async (event) => {
  const request = event.Records[0].cf.request;

  // Add auth header for origin
  request.headers['x-api-key'] = [{
    key: 'X-API-Key',
    value: 'secret-api-key',
  }];

  return request;
};

// Viewer Response - Add security headers
exports.handler = async (event) => {
  const response = event.Records[0].cf.response;
  const headers = response.headers;

  headers['strict-transport-security'] = [{
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains',
  }];

  headers['x-content-type-options'] = [{
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  }];

  headers['x-frame-options'] = [{
    key: 'X-Frame-Options',
    value: 'DENY',
  }];

  return response;
};
```

```hcl
# Lambda@Edge function
resource "aws_lambda_function" "edge" {
  provider         = aws.us_east_1  # Must be us-east-1
  function_name    = "security-headers"
  role             = aws_iam_role.lambda_edge.arn
  handler          = "index.handler"
  runtime          = "nodejs20.x"
  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")
  publish          = true
}

# Attach to distribution
resource "aws_cloudfront_distribution" "app" {
  # ...

  default_cache_behavior {
    # ...

    lambda_function_association {
      event_type   = "viewer-response"
      lambda_arn   = aws_lambda_function.edge.qualified_arn
      include_body = false
    }
  }
}
```

### Step 5: Invalidation

```bash
# Invalidate specific paths
aws cloudfront create-invalidation \
  --distribution-id E123456 \
  --paths "/index.html" "/css/*"

# Invalidate everything
aws cloudfront create-invalidation \
  --distribution-id E123456 \
  --paths "/*"
```

```hcl
# Terraform null resource for invalidation
resource "null_resource" "invalidation" {
  triggers = {
    version = var.app_version
  }

  provisioner "local-exec" {
    command = <<EOF
      aws cloudfront create-invalidation \
        --distribution-id ${aws_cloudfront_distribution.app.id} \
        --paths "/*"
    EOF
  }
}
```

### Step 6: Monitoring

```hcl
# CloudWatch alarms
resource "aws_cloudwatch_metric_alarm" "error_rate" {
  alarm_name          = "cloudfront-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5xxErrorRate"
  namespace           = "AWS/CloudFront"
  period              = 300
  statistic           = "Average"
  threshold           = 5

  dimensions = {
    DistributionId = aws_cloudfront_distribution.app.id
    Region         = "Global"
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# Enable real-time logs
resource "aws_cloudfront_realtime_log_config" "main" {
  name          = "realtime-logs"
  sampling_rate = 100

  endpoint {
    stream_type = "Kinesis"
    kinesis_stream_config {
      role_arn   = aws_iam_role.cloudfront_realtime.arn
      stream_arn = aws_kinesis_stream.logs.arn
    }
  }

  fields = [
    "timestamp",
    "c-ip",
    "cs-method",
    "cs-uri-stem",
    "sc-status",
    "sc-bytes",
    "time-taken"
  ]
}
```

---

## Templates

### SPA Distribution

```hcl
resource "aws_cloudfront_distribution" "spa" {
  # ... origins, certificates ...

  default_cache_behavior {
    target_origin_id       = "S3"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    cache_policy_id = aws_cloudfront_cache_policy.static.id
  }

  # Custom error response for SPA routing
  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }
}
```

---

## Common Mistakes

1. **No compression** - Enable gzip/brotli
2. **Caching API responses** - Use CachingDisabled policy
3. **Long TTL for HTML** - Short TTL for dynamic content
4. **No invalidation strategy** - Use versioned URLs
5. **Missing security headers** - Add via Lambda@Edge

---

## Checklist

- [ ] Origins configured (S3, ALB)
- [ ] Cache policies defined
- [ ] Compression enabled
- [ ] HTTPS only
- [ ] Custom domain with ACM
- [ ] Security headers
- [ ] Error pages configured
- [ ] Monitoring and alarms
- [ ] Invalidation strategy

---

## Next Steps

- M-DO-018: DNS with Route 53
- M-DO-015: SSL Certificates
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-019 v1.0*
