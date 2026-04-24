# Changelog

## [Unreleased]

### Changed
- **Knowledge partitioned by tier: 52 domains now live under
  `faion-knowledge/knowledge/<tier>/<group>/<name>/`** (tiers: `free`, `solo`,
  `pro`, `geek`) matching the pricing manifest. Free tier gets 8 domains,
  solo adds 13, pro adds 24, geek adds 7. Tier gating becomes a directory
  boundary — a free-tier session reads only `knowledge/free/`, solo reads
  `free + solo`, pro reads `free + solo + pro`, geek reads all four.
  `tier-manifest.json` bumped to v3 with tier-prefixed `knowledge_paths`
  and new `knowledge_root` per tier. Top-level docs (`SKILL.md`,
  `CLAUDE.md`, `README.md`, `skills/CLAUDE.md`, `docs/directory-structure.md`,
  `GEMINI.md`) rewritten for the new layout. Applied-tool cross-refs in
  `faion-feature-executor`, `faion-improver`, `faion-sdd-execution`
  updated to tier-prefixed paths (e.g. `knowledge/solo/sdd/sdd/`,
  `knowledge/pro/infra/devops-engineer/`).
- **Knowledge consolidation: 52 domain skills merged into `faion-knowledge` umbrella.**
  Renamed orchestrator skill `faion-net` → `faion-knowledge`. All knowledge
  skills (dev, AI, infra, product, PM, BA, UX, marketing, research, comms, SDD)
  moved from `skills/faion-<name>/` to `skills/faion-knowledge/knowledge/<group>/<name>/`.
  Discovery break intentional — only umbrella + applied tools
  (brainstorm, feature-executor, sdd-execution, improver, media-ops) remain
  individually invocable. Knowledge loaded on-demand via `Read`, not `Skill()`.
  Dropped duplicate skills `ppc-manager`, `seo-manager`, `smm-manager` (superseded
  by faion-prefixed versions with finer-grained methodologies).
  Moved docs out of skill: `content-plan/`, `content-requirements/`,
  `product-research-2026/`, `decision-trees/` → `docs/*.md`.
- `tier-manifest.json` schema v2: split into `applied_skills` (invocable)
  and `knowledge_paths` (on-demand paths under `faion-knowledge/knowledge/`).
- Top-level indices (`skills/CLAUDE.md`, `faion-knowledge/SKILL.md`,
  `faion-knowledge/CLAUDE.md`, `README.md`, `GEMINI.md`,
  `docs/directory-structure.md`) rewritten to reflect umbrella structure.
- Entry-point references in knowledge-skill CLAUDE.md/SKILL.md/README.md
  updated from `/faion-net` routing claim to umbrella membership note.
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
