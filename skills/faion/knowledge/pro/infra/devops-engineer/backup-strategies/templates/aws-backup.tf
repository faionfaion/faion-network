# aws-backup.tf — AWS Backup vault + plan with vault lock + cross-region copy
variable "environment" { type = string }
variable "backup_retention_days" { type = number; default = 30 }
variable "dr_region" { type = string; default = "us-west-2" }

resource "aws_kms_key" "backup" {
  description             = "KMS key for backup encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  tags = { Environment = var.environment }
}

resource "aws_backup_vault" "primary" {
  name        = "${var.environment}-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn
  tags        = { Environment = var.environment }
}

# Immutable vault lock — min 7-day retention enforced
resource "aws_backup_vault_lock_configuration" "primary" {
  backup_vault_name   = aws_backup_vault.primary.name
  min_retention_days  = 7
  max_retention_days  = 365
  changeable_for_days = 3  # grace period to undo
}

resource "aws_backup_vault" "dr" {
  provider = aws.dr_region
  name     = "${var.environment}-backup-vault-dr"
  tags     = { Environment = var.environment; Purpose = "disaster-recovery" }
}

resource "aws_backup_plan" "main" {
  name = "${var.environment}-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.primary.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = var.backup_retention_days * 12
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr.arn
      lifecycle { cold_storage_after = 30; delete_after = var.backup_retention_days * 12 }
    }
  }

  rule {
    rule_name         = "monthly-backup"
    target_vault_name = aws_backup_vault.primary.name
    schedule          = "cron(0 4 1 * ? *)"
    lifecycle { cold_storage_after = 90; delete_after = 2555 }  # 7 years
  }
}

resource "aws_iam_role" "backup" {
  name               = "${var.environment}-backup-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole"; Effect = "Allow"; Principal = { Service = "backup.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_backup_selection" "tagged" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "${var.environment}-tagged-resources"
  plan_id      = aws_backup_plan.main.id

  selection_tag { type = "STRINGEQUALS"; key = "Backup"; value = "true" }
}
