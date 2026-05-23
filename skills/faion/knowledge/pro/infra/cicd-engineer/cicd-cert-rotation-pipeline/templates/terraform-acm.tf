# purpose: Terraform aws_acm_certificate skeleton with validation
# consumes: input variables + provider creds
# produces: provisioned cloud resources
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150 tokens when loaded as context

terraform {
  required_version = ">= 1.6"
}
