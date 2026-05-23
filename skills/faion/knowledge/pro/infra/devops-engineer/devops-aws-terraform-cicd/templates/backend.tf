# purpose: S3 + DynamoDB remote state backend
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

terraform {
  backend "s3" {
    bucket         = "acme-tfstate-prod"
    key            = "checkout-api/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "acme-tfstate-lock"
    encrypt        = true
  }
}
