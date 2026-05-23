# purpose: Terraform Aurora Serverless v2 in isolated DB subnets
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 9.0"
  name    = "${var.project}-db"
  engine  = "aurora-postgresql"
  engine_mode = "provisioned"
  serverlessv2_scaling_configuration = { min_capacity = 0.5, max_capacity = 8 }
  vpc_id                = module.vpc.vpc_id
  db_subnet_group_name  = module.vpc.database_subnet_group_name
  storage_encrypted     = true
  apply_immediately     = false
  skip_final_snapshot   = false
}
