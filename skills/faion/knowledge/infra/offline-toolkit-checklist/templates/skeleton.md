<!-- purpose: Markdown skeleton for the pre-flight checklist with dated rows + verify commands. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Offline Toolkit Checklist — {trip_label}

## Trip window

From: YYYY-MM-DD HH:MM (TZ)
To:   YYYY-MM-DD HH:MM (TZ)

## Rows (every row carries verify_cmd + expected)

| id | category | row | verify_cmd | expected |
|----|----------|-----|------------|----------|
| r1 | dotfiles | chezmoi synced | `chezmoi status` | (no output) |
| r2 | secrets  | 1Password CLI | `op vault list` | Personal |
| r3 | repos    | active repos cloned | `git -C ~/work fetch --all --dry-run` | (no output) |

## Sign-off

**Operator:** @handle (role)  •  **Date:** YYYY-MM-DD  •  **Dry-run passed:** YES/NO
