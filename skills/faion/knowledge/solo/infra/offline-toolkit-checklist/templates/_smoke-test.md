<!-- purpose: Minimum viable filled-in checklist for one travel day. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Offline Toolkit Checklist — 2026-05-23 lisbon-conf

## Trip window

From: 2026-05-23 06:00 (UTC+1)
To:   2026-05-25 22:00 (UTC+1)

## Rows

| id | category | row | verify_cmd | expected |
|----|----------|-----|------------|----------|
| r1 | dotfiles | chezmoi synced | `chezmoi status` | (no output) |
| r2 | secrets  | 1Password CLI signed in | `op vault list` | Personal |
| r3 | repos    | nero-core fetched | `git -C ~/work/nero-core fetch --dry-run` | (no output) |

## Sign-off

**Operator:** @ruslan (founder)  •  **Date:** 2026-05-22  •  **Dry-run passed:** YES
