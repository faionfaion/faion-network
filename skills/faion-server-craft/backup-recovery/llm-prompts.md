# Backup & Recovery LLM Prompts

## Backup Strategy

### Prompt: Design Backup Strategy for Solo VPS

```
Design a backup strategy for my solo developer VPS platform.

Server:
- Provider: [e.g., Hetzner CX53]
- OS: [e.g., Ubuntu 24.04]
- RAM/CPU: [e.g., 30GB/16 CPUs]

Services:
- Databases: [e.g., PostgreSQL 16, Redis 7 (both in Docker)]
- Applications: [e.g., FastAPI, Celery, React SPA]
- Message broker: [e.g., RabbitMQ]

Data characteristics:
- Database size: [e.g., 500MB]
- Growth rate: [e.g., ~10MB/day]
- File uploads: [Yes/No, size]
- Configuration files: [list critical ones]

Budget:
- Monthly backup storage: [e.g., under $5]

Requirements:
- RPO (max acceptable data loss): [e.g., 24 hours]
- RTO (max time to recover): [e.g., 2 hours]
- Offsite copy: [Yes/No]
- Encryption: [Yes/No]

Provide:
1. What to backup (and what NOT to backup)
2. Backup tools for each data type
3. Schedule (frequency for each type)
4. Retention policy
5. Offsite storage recommendation
6. Estimated monthly cost
7. Complete backup script
8. Cron configuration
9. Monitoring/alerting approach
10. Restore testing procedure
```

### Prompt: Audit Existing Backup Strategy

```
Audit my current backup setup and identify gaps.

Current backup approach:
[Describe what you currently do]

Backup script:
[Paste current backup script if any]

Crontab:
[Paste crontab entries]

What I'm backing up:
- [list items]

Where backups are stored:
- [local paths, cloud storage]

Retention:
- [how long you keep backups]

Questions to answer:
1. Am I backing up everything critical?
2. Is my retention policy adequate?
3. Are my backups actually restorable?
4. What's my current RPO/RTO?
5. What happens if the server is completely lost?
6. What's missing from my setup?
```

## Restore Operations

### Prompt: Restore Database from Backup

```
I need to restore my PostgreSQL database from a backup.

Situation:
- What happened: [e.g., bad migration, accidental DELETE, corruption]
- Recovery scope: [full database / specific table / specific rows]
- Latest good backup: [date/path of backup file]
- Current database status: [running normally / broken / empty]

Backup details:
- Backup format: [pg_dump custom (-Fc) / SQL / directory]
- Backup file: [path]
- Backup from PostgreSQL version: [version]
- Current PostgreSQL version: [version]
- Database name: [name]
- Database user: [user]
- Running in: [Docker / bare metal]

Provide:
1. Pre-restore safety steps (backup current state first)
2. Step-by-step restore commands
3. If partial restore: how to restore just what's needed
4. Post-restore verification
5. Application restart procedure
```

### Prompt: Disaster Recovery Execution

```
My server is gone and I need to recover to a new server.

What happened: [e.g., server crashed, provider issue, migration]
Available backups:
- Restic repository: [location, last verified date]
- Local backups: [available / lost with server]
- Git repos: [GitHub, all code safe]

New server:
- Provider: [same/different]
- OS: [e.g., Ubuntu 24.04]
- Specs: [same/different from old server]
- IP: [new IP address]

Old server details:
- Services running: [list all]
- Domain: [domain name]
- DNS: [Cloudflare / other]

Guide me through complete recovery:
1. Server setup and package installation
2. Restore backup data from restic
3. Restore configurations
4. Start infrastructure services
5. Restore databases
6. Deploy application code
7. DNS cutover
8. Verification and monitoring
9. Post-recovery hardening
```

## Troubleshooting

### Prompt: Debug Backup Failure

```
My backup script is failing. Help me debug.

Backup script:
[paste script]

Error output:
[paste error messages from log]

Cron entry:
[paste cron line]

Additional context:
- Last successful backup: [date]
- What changed recently: [package updates, config changes, etc.]
- Disk space: [df -h output]
- Docker status: [docker compose ps output]

Common things to check:
1. Disk space
2. Database connectivity
3. Restic repository access
4. Permissions
5. Environment variables in cron context
6. Docker container health
```

### Prompt: Fix Corrupt Backup

```
My backup appears to be corrupt. Help me investigate.

Backup type: [pg_dump / restic / redis RDB]
File path: [path]
File size: [size, and is it suspiciously small/large?]

Error when trying to restore:
[paste error]

What I've tried:
[list attempts]

Help me:
1. Verify if it's truly corrupt or if the error is something else
2. If corrupt, identify the cause
3. Find the most recent valid backup
4. Restore from the valid backup
5. Prevent this from happening again
```

### Prompt: Restic Repository Issues

```
I'm having issues with my restic repository.

Problem: [e.g., can't connect, check fails, restore fails, slow]

Repository location: [b2:bucket:path / s3:bucket/path]
Restic version: [restic version output]

Error message:
[paste error]

Repository stats (if accessible):
[restic stats output]
[restic check output]

Help me:
1. Diagnose the issue
2. Fix the repository if possible
3. If not fixable, start a new repository without losing existing data
4. Verify the fix works
```

## Planning

### Prompt: Create Disaster Recovery Runbook

```
Create a disaster recovery runbook for my platform.

Platform: [name]
Server: [provider, OS, specs]

Services:
[List all services with ports, dependencies, data stores]

Data stores:
[List databases, caches, file storage with sizes]

Backup locations:
[Where backups are stored]

DNS:
[DNS provider, domain, records]

Code repositories:
[Where code is hosted]

Access requirements:
[What accounts/credentials are needed to recover]

Create a step-by-step runbook with:
1. Prerequisites checklist (accounts, credentials)
2. Server provisioning steps
3. Software installation list
4. Backup restoration procedure
5. Service startup order
6. DNS cutover procedure
7. Verification checklist
8. Estimated time for each phase
9. Rollback procedures for each phase
10. Post-recovery checklist
```
