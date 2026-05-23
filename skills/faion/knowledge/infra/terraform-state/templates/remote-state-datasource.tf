data "terraform_remote_state" "networking" {
  backend = "s3"

  config = {
    bucket = "COMPANY-terraform-state"
    key    = "ENV/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Usage in resources:
# subnet_id  = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
# vpc_id     = data.terraform_remote_state.networking.outputs.vpc_id
