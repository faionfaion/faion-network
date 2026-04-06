# Changelog

## [Unreleased]

### Changed
- Deep integrity check in `scripts/lib/integrity-check.sh`:
  case-mismatch detection (skill.md vs SKILL.md), frontmatter schema
  validation (name/description), Skill() cross-reference verification,
  hook executability check, per-category summary counts,
  INTEGRITY_VERBOSE=1 for detailed output

### Added
- Atomic update with snapshot rollback for `scripts/update.sh`
  - Pre-update snapshot creation (tarball in `~/.cache/faion-network/snapshots/`)
  - Post-update integrity check (SKILL.md, hooks, AGENTS.md)
  - `--rollback` flag to restore most recent snapshot
  - `--dry-run` flag to preview changes without modifying anything
  - Automatic snapshot rotation (keeps last 3)
  - Auto-rollback prompt on integrity check failure
- `scripts/lib/snapshot.sh` — snapshot create/restore/rotate library
- `scripts/lib/integrity-check.sh` — post-update integrity verification
