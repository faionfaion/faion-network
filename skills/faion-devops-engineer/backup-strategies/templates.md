# Backup Strategies Templates

Reusable templates for backup configurations and documentation.

## Backup Policy Template

```markdown
# Backup Policy: [System Name]

## Overview

| Field | Value |
|-------|-------|
| System | [Name] |
| Owner | [Team/Person] |
| Classification | [Critical/Important/Standard/Archive] |
| Last Updated | [Date] |

## RPO/RTO Targets

| Metric | Target | Justification |
|--------|--------|---------------|
| RPO | [e.g., 1 hour] | [Business requirement] |
| RTO | [e.g., 4 hours] | [SLA commitment] |
| Max Data Loss | [e.g., 1 hour of transactions] | |

## Backup Schedule

| Type | Frequency | Retention | Storage |
|------|-----------|-----------|---------|
| Full | [e.g., Weekly] | [e.g., 90 days] | [Location] |
| Incremental | [e.g., Daily] | [e.g., 30 days] | [Location] |
| Transaction Log | [e.g., Every 15 min] | [e.g., 7 days] | [Location] |

## Storage Locations (3-2-1-1-0)

| Copy | Location | Type | Immutable |
|------|----------|------|-----------|
| 1 | [e.g., Local NAS] | Primary | No |
| 2 | [e.g., AWS S3] | Cloud | No |
| 3 | [e.g., S3 Object Lock] | Cloud | Yes |

## Verification

| Test | Frequency | Owner |
|------|-----------|-------|
| Automated integrity | Daily | [Automation] |
| Restore test | Monthly | [Team] |
| Full DR test | Quarterly | [Team] |

## Recovery Procedures

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Contacts

| Role | Name | Contact |
|------|------|---------|
| Primary | [Name] | [Email/Phone] |
| Secondary | [Name] | [Email/Phone] |
| Escalation | [Name] | [Email/Phone] |
```

## Disaster Recovery Plan Template

```markdown
# Disaster Recovery Plan: [System Name]

## Document Control

| Field | Value |
|-------|-------|
| Version | [1.0] |
| Last Updated | [Date] |
| Next Review | [Date] |
| Owner | [Name] |
| Approved By | [Name] |

## Scope

This DR plan covers:
- [Component 1]
- [Component 2]
- [Component 3]

## Recovery Objectives

| System | RPO | RTO | Priority |
|--------|-----|-----|----------|
| [Database] | 1 hour | 2 hours | P1 |
| [Application] | 4 hours | 4 hours | P2 |
| [Static Files] | 24 hours | 8 hours | P3 |

## Disaster Scenarios

### Scenario 1: [Data Center Failure]

**Trigger:** [Description]

**Response:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Recovery Time:** [Estimate]

### Scenario 2: [Ransomware Attack]

**Trigger:** [Description]

**Response:**
1. Isolate affected systems
2. Assess scope of encryption
3. Restore from immutable backups
4. Verify data integrity
5. Resume operations

**Recovery Time:** [Estimate]

### Scenario 3: [Database Corruption]

**Trigger:** [Description]

**Response:**
1. Stop application writes
2. Identify corruption point
3. Restore to point before corruption
4. Replay transaction logs
5. Verify data integrity
6. Resume operations

**Recovery Time:** [Estimate]

## Recovery Procedures

### Database Recovery

```bash
# 1. Stop application
kubectl scale deployment app --replicas=0

# 2. Restore database
./restore_database.sh /path/to/backup

# 3. Verify data
./verify_database.sh

# 4. Start application
kubectl scale deployment app --replicas=3
```

### Application Recovery

```bash
# 1. Deploy to DR region
./deploy_dr.sh

# 2. Update DNS
./update_dns.sh dr-region

# 3. Verify functionality
./smoke_test.sh
```

## Communication Plan

| Phase | Audience | Channel | Message |
|-------|----------|---------|---------|
| Detection | Ops Team | PagerDuty | Incident detected |
| Assessment | Management | Email/Slack | Scope assessment |
| Recovery | Stakeholders | Email | Recovery in progress |
| Resolution | All | Email | Service restored |

## Post-Incident

- [ ] Conduct post-mortem within 48 hours
- [ ] Document lessons learned
- [ ] Update DR plan if needed
- [ ] Schedule follow-up DR test
```

## Backup Script Template

```bash
#!/bin/bash
# backup_template.sh - Template for backup scripts
# Usage: ./backup_template.sh [options]

set -euo pipefail

# ============================================
# Configuration
# ============================================
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Override these in environment or config file
: "${BACKUP_SOURCE:=/path/to/source}"
: "${BACKUP_DEST:=/path/to/destination}"
: "${BACKUP_RETENTION_DAYS:=30}"
: "${S3_BUCKET:=s3://backup-bucket}"
: "${IMMUTABLE_BUCKET:=s3://immutable-backup-bucket}"
: "${LOG_FILE:=/var/log/backup/${SCRIPT_NAME}.log}"
: "${ALERT_EMAIL:=ops@example.com}"
: "${SLACK_WEBHOOK:=}"

# ============================================
# Functions
# ============================================

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
  log "ERROR: $*" >&2
}

send_alert() {
  local message="$1"
  local severity="${2:-error}"

  # Email
  if [[ -n "$ALERT_EMAIL" ]]; then
    echo "$message" | mail -s "[$severity] Backup: $SCRIPT_NAME" "$ALERT_EMAIL" || true
  fi

  # Slack
  if [[ -n "$SLACK_WEBHOOK" ]]; then
    local color="danger"
    [[ "$severity" == "warning" ]] && color="warning"
    [[ "$severity" == "success" ]] && color="good"

    curl -s -X POST -H 'Content-type: application/json' \
      --data "{\"attachments\":[{\"color\":\"$color\",\"text\":\"$message\"}]}" \
      "$SLACK_WEBHOOK" || true
  fi
}

cleanup() {
  local exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    error "Backup failed with exit code $exit_code"
    send_alert "Backup failed: $SCRIPT_NAME on $(hostname)" "error"
  fi
  # Cleanup temporary files
  rm -rf "${TEMP_DIR:-/tmp/backup_$$}" 2>/dev/null || true
}
trap cleanup EXIT

usage() {
  cat << EOF
Usage: $SCRIPT_NAME [options]

Options:
  -s, --source PATH     Source directory to backup
  -d, --dest PATH       Destination directory
  -r, --retention DAYS  Retention period in days
  -n, --dry-run         Show what would be done
  -v, --verbose         Verbose output
  -h, --help            Show this help

Environment variables:
  BACKUP_SOURCE         Source directory
  BACKUP_DEST           Destination directory
  BACKUP_RETENTION_DAYS Retention period
  S3_BUCKET             S3 bucket for offsite backup
  ALERT_EMAIL           Email for alerts
  SLACK_WEBHOOK         Slack webhook URL
EOF
}

# ============================================
# Parse arguments
# ============================================

DRY_RUN=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    -s|--source)
      BACKUP_SOURCE="$2"
      shift 2
      ;;
    -d|--dest)
      BACKUP_DEST="$2"
      shift 2
      ;;
    -r|--retention)
      BACKUP_RETENTION_DAYS="$2"
      shift 2
      ;;
    -n|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

# ============================================
# Validation
# ============================================

[[ -d "$BACKUP_SOURCE" ]] || { error "Source not found: $BACKUP_SOURCE"; exit 1; }
mkdir -p "$BACKUP_DEST" || { error "Cannot create dest: $BACKUP_DEST"; exit 1; }
mkdir -p "$(dirname "$LOG_FILE")"

# ============================================
# Main backup logic
# ============================================

log "Starting backup: $BACKUP_SOURCE -> $BACKUP_DEST"

BACKUP_FILE="${BACKUP_DEST}/backup_${TIMESTAMP}.tar.gz"

# Create backup
tar -czf "$BACKUP_FILE" -C "$(dirname "$BACKUP_SOURCE")" "$(basename "$BACKUP_SOURCE")"

# Calculate checksum
sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"

log "Created backup: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"

# Upload to S3 (offsite)
if [[ -n "$S3_BUCKET" ]]; then
  log "Uploading to S3..."
  aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/" --storage-class STANDARD_IA
  aws s3 cp "${BACKUP_FILE}.sha256" "$S3_BUCKET/"
fi

# Upload to immutable storage
if [[ -n "$IMMUTABLE_BUCKET" ]]; then
  log "Uploading to immutable storage..."
  aws s3 cp "$BACKUP_FILE" "$IMMUTABLE_BUCKET/" \
    --object-lock-mode COMPLIANCE \
    --object-lock-retain-until-date "$(date -d "+${BACKUP_RETENTION_DAYS} days" --iso-8601=seconds)"
fi

# Cleanup old backups
log "Cleaning up backups older than $BACKUP_RETENTION_DAYS days..."
find "$BACKUP_DEST" -type f -name "backup_*.tar.gz" -mtime +"$BACKUP_RETENTION_DAYS" -delete
find "$BACKUP_DEST" -type f -name "backup_*.sha256" -mtime +"$BACKUP_RETENTION_DAYS" -delete

# Report success
log "Backup completed successfully"
send_alert "Backup completed: $SCRIPT_NAME on $(hostname)" "success"

# Push metrics (if Prometheus Pushgateway available)
if command -v curl &>/dev/null; then
  cat << EOF | curl -s --data-binary @- http://pushgateway:9091/metrics/job/backup/instance/$(hostname) 2>/dev/null || true
backup_last_success_timestamp $(date +%s)
backup_size_bytes $(stat -c%s "$BACKUP_FILE")
backup_duration_seconds $SECONDS
backup_last_status 1
EOF
fi
```

## Terraform AWS Backup Template

```hcl
# backup.tf - AWS Backup configuration template

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "backup_retention_days" {
  description = "Backup retention in days"
  type        = number
  default     = 30
}

variable "cold_storage_after_days" {
  description = "Move to cold storage after days"
  type        = number
  default     = 90
}

variable "dr_region" {
  description = "DR region for cross-region copy"
  type        = string
  default     = "us-west-2"
}

# KMS key for backup encryption
resource "aws_kms_key" "backup" {
  description             = "KMS key for backup encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name        = "${var.environment}-backup-key"
    Environment = var.environment
  }
}

# Primary backup vault
resource "aws_backup_vault" "primary" {
  name        = "${var.environment}-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn

  tags = {
    Environment = var.environment
  }
}

# Vault lock for immutability
resource "aws_backup_vault_lock_configuration" "primary" {
  backup_vault_name   = aws_backup_vault.primary.name
  min_retention_days  = 7
  max_retention_days  = 365
  changeable_for_days = 3
}

# DR region vault
resource "aws_backup_vault" "dr" {
  provider = aws.dr_region
  name     = "${var.environment}-backup-vault-dr"

  tags = {
    Environment = var.environment
    Purpose     = "disaster-recovery"
  }
}

# Backup plan
resource "aws_backup_plan" "main" {
  name = "${var.environment}-backup-plan"

  # Daily backups
  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.primary.name
    schedule          = "cron(0 2 * * ? *)"
    start_window      = 60
    completion_window = 180

    lifecycle {
      cold_storage_after = var.cold_storage_after_days
      delete_after       = var.backup_retention_days * 12
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr.arn
      lifecycle {
        cold_storage_after = var.cold_storage_after_days
        delete_after       = var.backup_retention_days * 12
      }
    }

    recovery_point_tags = {
      Type        = "daily"
      Environment = var.environment
    }
  }

  # Weekly backups (longer retention)
  rule {
    rule_name         = "weekly-backup"
    target_vault_name = aws_backup_vault.primary.name
    schedule          = "cron(0 3 ? * SUN *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 730
    }

    recovery_point_tags = {
      Type        = "weekly"
      Environment = var.environment
    }
  }

  # Monthly backups (compliance)
  rule {
    rule_name         = "monthly-backup"
    target_vault_name = aws_backup_vault.primary.name
    schedule          = "cron(0 4 1 * ? *)"

    lifecycle {
      cold_storage_after = 90
      delete_after       = 2555  # 7 years
    }

    recovery_point_tags = {
      Type        = "monthly"
      Environment = var.environment
    }
  }

  tags = {
    Environment = var.environment
  }
}

# IAM role for AWS Backup
resource "aws_iam_role" "backup" {
  name = "${var.environment}-backup-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "backup.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_iam_role_policy_attachment" "restore" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}

# Resource selection by tag
resource "aws_backup_selection" "tagged" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "${var.environment}-tagged-resources"
  plan_id      = aws_backup_plan.main.id

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}

# Specific resource selection (RDS, EBS)
resource "aws_backup_selection" "databases" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "${var.environment}-databases"
  plan_id      = aws_backup_plan.main.id

  resources = [
    "arn:aws:rds:*:*:db:${var.environment}-*",
    "arn:aws:dynamodb:*:*:table/${var.environment}-*"
  ]
}

output "backup_vault_arn" {
  value = aws_backup_vault.primary.arn
}

output "backup_plan_id" {
  value = aws_backup_plan.main.id
}
```

## Velero Schedule Template

```yaml
# velero-schedule-template.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: {{ .Name }}-daily
  namespace: velero
  labels:
    app: velero
    schedule: daily
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces:
      {{- range .Namespaces }}
      - {{ . }}
      {{- end }}
    excludedResources:
      - events
      - events.events.k8s.io
    includedResources: []
    labelSelector:
      matchLabels:
        backup: "true"
    storageLocation: default
    volumeSnapshotLocations:
      - default
    ttl: 720h  # 30 days
    snapshotVolumes: true
    defaultVolumesToFsBackup: true
    metadata:
      labels:
        velero.io/schedule-name: {{ .Name }}-daily
---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: {{ .Name }}-weekly
  namespace: velero
spec:
  schedule: "0 3 * * 0"
  template:
    includedNamespaces:
      {{- range .Namespaces }}
      - {{ . }}
      {{- end }}
    ttl: 2160h  # 90 days
    snapshotVolumes: true
---
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: {{ .S3Bucket }}
    prefix: velero
  config:
    region: {{ .Region }}
    s3ForcePathStyle: "false"
---
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  config:
    region: {{ .Region }}
```

## Prometheus Alert Template

```yaml
# backup-alerts-template.yaml
groups:
  - name: backup-alerts
    rules:
      - alert: BackupJobFailed
        expr: backup_last_status{job="{{ .JobName }}"} == 0
        for: 5m
        labels:
          severity: critical
          team: {{ .Team }}
        annotations:
          summary: "Backup job {{ .JobName }} failed"
          description: "Backup job {{ "{{ $labels.job }}" }} on {{ "{{ $labels.instance }}" }} failed"
          runbook_url: "https://wiki.example.com/runbooks/backup-failure"

      - alert: BackupNotRecent
        expr: time() - backup_last_success_timestamp{job="{{ .JobName }}"} > {{ .MaxAgeSeconds }}
        for: 1h
        labels:
          severity: critical
          team: {{ .Team }}
        annotations:
          summary: "Backup for {{ .JobName }} is stale"
          description: "Last successful backup was {{ "{{ humanizeTimestamp $value }}" }}"

      - alert: BackupSizeAnomaly
        expr: |
          abs(
            backup_size_bytes{job="{{ .JobName }}"} -
            backup_size_bytes{job="{{ .JobName }}"} offset 1d
          ) / backup_size_bytes{job="{{ .JobName }}"} offset 1d > 0.5
        for: 1h
        labels:
          severity: warning
          team: {{ .Team }}
        annotations:
          summary: "Backup size anomaly detected for {{ .JobName }}"
          description: "Backup size changed by more than 50%"

      - alert: BackupStorageLow
        expr: |
          backup_storage_free_bytes{job="{{ .JobName }}"} /
          backup_storage_total_bytes{job="{{ .JobName }}"} < 0.2
        for: 6h
        labels:
          severity: warning
          team: {{ .Team }}
        annotations:
          summary: "Backup storage running low for {{ .JobName }}"
          description: "Only {{ "{{ humanizePercentage $value }}" }} storage remaining"
```
