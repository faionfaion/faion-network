# purpose: common locals (name prefix, tags) for the aws-architecture-services bundle
# consumes: see ../AGENTS.md ## Prerequisites + content/02-output-contract.xml
# produces: provisioned AWS resources conforming to the methodology spec
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~600-1500 tokens when loaded as context
locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}
