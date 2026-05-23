# purpose: Terraform ALB in public subnets with HTTPS listener
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"
  name    = "${var.project}-alb"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets
  enable_deletion_protection = true
  listeners = {
    https = {
      port     = 443
      protocol = "HTTPS"
      certificate_arn = var.acm_cert_arn
      forward = { target_group_key = "app" }
    }
  }
  target_groups = {
    app = { name_prefix = "app-", protocol = "HTTP", port = 8080, target_type = "ip", health_check = { path = "/health" } }
  }
}
