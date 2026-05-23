# purpose: Production-ready AWS ALB Terraform module (lb + listener + TG + redirect + S3 logs + SG)
# consumes: see content/02-output-contract.xml inputs (provider=aws, lb_type=alb, tls_policy, access_logs_bucket)
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml (deletion-protection-on, tls-1-2-min-policy, access-logs-enabled, http-to-https-redirect, security-group-tight)
# token-budget-impact: ~800 tokens when loaded as context

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
