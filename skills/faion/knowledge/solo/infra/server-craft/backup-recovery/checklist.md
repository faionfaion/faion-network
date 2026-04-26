# Backup & Recovery Checklist

## Planning

- [ ] Inventory all data requiring backup (databases, configs, secrets, files)
- [ ] Define RPO (Recovery Point Objective) for each data type
- [ ] Define RTO (Recovery Time Objective) for full platform recovery
- [ ] Choose offsite storage provider (Backblaze B2, AWS S3, etc.)
- [ ] Plan backup schedule (daily, weekly, on-change)
- [ ] Calculate expected backup sizes and storage costs
- [ ] Create disaster recovery runbook

## Local Backup Setup

### PostgreSQL

- [ ] Create backup script with pg_dump (custom format `-Fc`)
- [ ] Test backup script manually
- [ ] Verify dump file is valid: `pg_restore --list backup.dump`
- [ ] Set backup directory with proper permissions
- [ ] Configure retention (delete backups older than N days)

### Redis

- [ ] Enable RDB snapshots in Redis config (`save` directives)
- [ ] Create backup script that copies dump.rdb
- [ ] Enable AOF if recovery precision matters (`appendonly yes`)
- [ ] Verify backup file is valid

### Configuration Files

- [ ] Create config backup script capturing:
  - [ ] /home/user/workspace/.env
  - [ ] /etc/nginx/sites-available/*
  - [ ] /etc/nginx/snippets/*
  - [ ] /etc/nginx/ssl/* (certificates and keys)
  - [ ] ~/.config/systemd/user/*.service
  - [ ] /etc/wireguard/*.conf
  - [ ] /etc/ssh/sshd_config
  - [ ] /etc/sysctl.d/*.conf
  - [ ] /etc/fail2ban/jail.d/*
  - [ ] crontab (via crontab -l)
  - [ ] Shell configs (.bashrc, .bash_aliases, .tmux.conf)
- [ ] Test config backup script

### Application Data

- [ ] Identify application-specific data directories (uploads, attachments)
- [ ] Include in backup script or restic backup paths

## Offsite Backup Setup

### Restic Repository

- [ ] Install restic: `sudo apt install restic`
- [ ] Create B2/S3 bucket for backups
- [ ] Generate and securely store API credentials
- [ ] Initialize restic repository: `restic init -r b2:bucket:path`
- [ ] Store repository password in password manager
- [ ] Create `.restic-password` file with chmod 600 (for automated scripts)
- [ ] Add restic credentials to .env or separate env file

### Backup Script

- [ ] Create comprehensive backup script (local + offsite)
- [ ] Script runs pg_dump, copies Redis, snapshots configs
- [ ] Script uploads to restic repository
- [ ] Script applies retention policy (forget + prune)
- [ ] Script logs results
- [ ] Script handles errors and reports failures

### Automation

- [ ] Add backup to cron (daily at off-peak time)
- [ ] Verify cron job runs successfully
- [ ] Set up failure notification (email, Telegram)

## Verification

### Backup Integrity

- [ ] Verify PostgreSQL dump is restorable: `pg_restore --list`
- [ ] Verify restic repository: `restic check`
- [ ] List restic snapshots: `restic snapshots`
- [ ] Check backup sizes are reasonable (not zero, not unexpectedly large)

### Restore Testing

- [ ] Test PostgreSQL restore to a test database
- [ ] Test Redis restore (stop, replace dump.rdb, start)
- [ ] Test config restore (copy to temp directory, verify contents)
- [ ] Test full restic restore to temporary directory
- [ ] Document restore time (contributes to RTO estimate)

### Monthly Restore Drill

- [ ] Pick a random backup snapshot
- [ ] Restore database to a test instance
- [ ] Verify data integrity (row counts, specific records)
- [ ] Restore configs and verify they are current
- [ ] Document any issues found
- [ ] Update runbook if procedures changed

## Disaster Recovery Readiness

### Runbook

- [ ] Document server provisioning steps (Hetzner, OS, specs)
- [ ] Document software installation steps (all packages)
- [ ] Document restore sequence (configs -> infra -> DB -> apps)
- [ ] Document DNS update procedure
- [ ] Document verification steps
- [ ] Store runbook in multiple locations (not just on the server)

### Access Requirements

- [ ] SSH keys backed up (or can generate new)
- [ ] Hetzner account credentials accessible
- [ ] Cloudflare account credentials accessible
- [ ] GitHub account accessible (for code repos)
- [ ] B2/S3 credentials accessible (for backup restore)
- [ ] Restic repository password accessible
- [ ] Domain registrar access (for DNS if needed)

## Monitoring

- [ ] Monitor backup cron job success/failure
- [ ] Monitor backup file sizes (detect anomalies)
- [ ] Monitor offsite storage usage and costs
- [ ] Alert on backup failure
- [ ] Calendar reminder for monthly restore drill
- [ ] Calendar reminder for annual runbook review
