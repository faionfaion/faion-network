# import-blocks.tf — Terraform 1.5+ declarative imports
# Run: terraform plan -generate-config-out=generated.tf
# to auto-generate resource configuration for imported resources

import {
  to = aws_vpc.main
  id = "vpc-REPLACE_WITH_ID"
}

import {
  to = aws_subnet.public[0]
  id = "subnet-REPLACE_WITH_ID"
}

import {
  to = aws_security_group.app
  id = "sg-REPLACE_WITH_ID"
}
