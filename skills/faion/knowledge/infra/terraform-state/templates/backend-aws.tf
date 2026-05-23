terraform {
  backend "s3" {
    bucket         = "COMPANY-terraform-state"
    key            = "ENV/COMPONENT/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    kms_key_id     = "alias/terraform-state"
    # For cross-account state access:
    # role_arn = "arn:aws:iam::STATE_ACCOUNT_ID:role/TerraformStateAccess"
  }
}
