<!-- purpose: Markdown backup-and-recovery report with verified dumps + restic snapshots. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Backup Report — {window_label}

## Coverage

| target | tool | frequency | last_verified |
|--------|------|-----------|---------------|
| postgres:nero_db | pg_dump -Fc | daily 03:00 | YYYY-MM-DD |
| redis | docker cp RDB | daily 03:05 | YYYY-MM-DD |
| /etc + /srv/configs | restic | daily 03:30 | YYYY-MM-DD |

## Restic

- repository: b2:nero-backups:server
- last snapshot: <id>
- retention: --keep-daily 7 --keep-weekly 4 --keep-monthly 6

## RPO/RTO

- RPO: 24h
- RTO: 60-90min (drill on YYYY-MM-DD)

## Sign-off

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
