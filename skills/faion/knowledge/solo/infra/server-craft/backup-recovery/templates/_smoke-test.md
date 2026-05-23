<!-- purpose: Minimum viable filled-in backup report. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Backup Report — 2026-05-W21

## Coverage

| target | tool | frequency | last_verified |
|--------|------|-----------|---------------|
| postgres:nero_db | pg_dump -Fc | daily 03:00 | 2026-05-23 |
| redis | docker cp RDB | daily 03:05 | 2026-05-23 |
| /etc + /srv/configs | restic | daily 03:30 | 2026-05-23 |

## Restic

- repository: b2:nero-backups:server
- last snapshot: abc12345
- retention: --keep-daily 7 --keep-weekly 4 --keep-monthly 6

## RPO/RTO

- RPO: 24h
- RTO: 70min (drill on 2026-05-01)

## Sign-off

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
