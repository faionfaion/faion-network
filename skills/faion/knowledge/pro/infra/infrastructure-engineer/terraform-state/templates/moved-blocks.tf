# moved-blocks.tf — Terraform 1.1+ declarative refactoring
# Keep moved blocks until all users have applied, then remove them

# Rename a resource
moved {
  from = aws_instance.web
  to   = aws_instance.app_server
}

# Move resource to a module
moved {
  from = aws_instance.app_server
  to   = module.compute.aws_instance.main
}

# Rename a module
moved {
  from = module.old_compute
  to   = module.compute
}
