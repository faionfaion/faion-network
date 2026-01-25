# Terraform State Management

Technical reference for Terraform state: remote backends, state operations, locking, and data sources.

---

## Remote State Configuration

### S3 Backend (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Role assumption for cross-account
    role_arn = "arn:aws:iam::ACCOUNT_ID:role/TerraformStateRole"
  }
}
```

### GCS Backend (GCP)

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "terraform/state"
  }
}
```

### Azure Blob Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### Terraform Cloud Backend

```hcl
terraform {
  cloud {
    organization = "my-org"

    workspaces {
      name = "my-workspace"
    }
  }
}
```

---

## State Operations

### List and Show Resources

```bash
# List resources in state
terraform state list

# Show specific resource
terraform state show aws_instance.web
```

### Move and Rename Resources

```bash
# Move resource in state
terraform state mv aws_instance.web aws_instance.app

# Remove resource from state (no destroy)
terraform state rm aws_instance.web
```

### Import Existing Resources

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

### Pull and Push State

```bash
# Pull remote state locally
terraform state pull > terraform.tfstate.backup

# Push local state to remote
terraform state push terraform.tfstate
```

### Replace Provider

```bash
# Replace provider in state
terraform state replace-provider hashicorp/aws registry.acme.corp/acme/aws
```

### Refresh State

```bash
# Refresh state (sync with actual infrastructure)
terraform refresh
```

### Mark Resource for Recreation

```bash
# Deprecated method
terraform taint aws_instance.web

# New method (recommended)
terraform apply -replace=aws_instance.web
```

---

## State Locking

### DynamoDB Lock Table (AWS)

```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "terraform-state-locks"
  }
}
```

---

## Remote State Data Source

### Access State from Another Configuration

```hcl
# Access state from another configuration
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from remote state
resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.vpc.outputs.public_subnet_ids[0]
  # ...
}
```

---

## Best Practices

### State File Security

1. Always enable encryption for remote state backends
2. Use state locking to prevent concurrent modifications
3. Never commit state files to version control
4. Restrict access to state storage using IAM policies
5. Enable versioning on state storage (S3, GCS)

### State Management

1. Use remote backends for team collaboration
2. Separate state files by environment (dev/staging/prod)
3. Use workspaces for environment isolation
4. Regularly backup state files
5. Use `terraform import` for existing resources

### State Operations Safety

1. Always backup state before manual operations
2. Use `terraform state rm` carefully (resource stays but removed from state)
3. Use `terraform import` to bring existing infrastructure under management
4. Avoid editing state files manually
5. Use `terraform plan` after state operations to verify changes

---

*Terraform State Management Reference*
*Part of faion-devops-engineer skill*

## Sources

- [Terraform State](https://www.terraform.io/language/state)
- [Remote State](https://www.terraform.io/language/state/remote)
- [State Locking](https://www.terraform.io/language/state/locking)
- [Workspaces](https://www.terraform.io/language/state/workspaces)
- [Sensitive Data in State](https://www.terraform.io/language/state/sensitive-data)
