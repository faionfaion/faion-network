terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "project/environment/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
# Replace bucket, key, and dynamodb_table with actual values.
# Do not use variable interpolation here — backend config is resolved before variables.
# Use -backend-config flag or a partial backend config file per environment.
