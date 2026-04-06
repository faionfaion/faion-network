# scripts/lib — Shell Libraries

Reusable shell functions sourced by `update.sh`.

## Files

| File | Purpose |
|---|---|
| snapshot.sh | Create/restore/rotate pre-update snapshots (5MB limit) |
| integrity-check.sh | Post-update structural verification |

## Usage

These are not standalone scripts. Source them from a parent script:

```bash
source "${SCRIPT_DIR}/lib/snapshot.sh"
source "${SCRIPT_DIR}/lib/integrity-check.sh"
```

Requires `log_info`, `log_success`, `log_warning`, `log_error`, `log_file` functions defined by caller.
