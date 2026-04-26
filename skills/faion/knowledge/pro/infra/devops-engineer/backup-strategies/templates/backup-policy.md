# Backup Policy: {{System Name}}

## Overview

| Field | Value |
|-------|-------|
| System | {{Name}} |
| Owner | {{Team/Person}} |
| Classification | {{Critical/Important/Standard/Archive}} |
| Last Updated | {{Date}} |

## RPO/RTO Targets

| Metric | Target | Justification |
|--------|--------|---------------|
| RPO | {{e.g., 1 hour}} | {{Business requirement}} |
| RTO | {{e.g., 4 hours}} | {{SLA commitment}} |

## Backup Schedule (3-2-1-1-0)

| Copy | Type | Location | Immutable | Retention |
|------|------|----------|-----------|-----------|
| 1 | Production | Live database | No | n/a |
| 2 | Primary backup | {{Local NAS / S3 Standard-IA}} | No | {{30 days}} |
| 3 | Immutable | {{S3 Object Lock COMPLIANCE / Azure WORM}} | Yes | {{90 days}} |

| Schedule | Frequency | Tool |
|----------|-----------|------|
| Full | {{Daily at 02:00}} | {{pg_dump / restic}} |
| WAL/Log | {{Continuous / every 5 min}} | {{WAL archive / binlog}} |

## Verification

| Test | Frequency | Owner |
|------|-----------|-------|
| Automated restore integrity | Daily | Automation |
| Manual restore test | Monthly | {{Team}} |
| Full DR drill | Quarterly | {{Team}} |

## Contacts

| Role | Name | Contact |
|------|------|---------|
| Primary | {{Name}} | {{Email}} |
| Escalation | {{Name}} | {{Email}} |
