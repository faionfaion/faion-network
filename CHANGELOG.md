# Changelog

## [Unreleased]

### Added
- Research: requirements-validation (business-analyst) — agent-integration.md (162 lines).
- Research: user-story-mapping (business-analyst) — agent-integration.md (163 lines).
- Research: solution-assessment (business-analyst) — agent-integration.md (178 lines).
- Research: process-mining-automation — agent-integration.md (245 lines).
- Research: agile-ba-frameworks — agent-integration.md (188 lines).
- Research: data-analysis (ba-modeling) — agent-integration.md (186 lines).
- Research: ba-trends-summary — agent-integration.md (39 lines, too-thin note).
- Research: data-driven-requirements (business-analyst) — agent-integration.md (166 lines).
- Research: decision-analysis (ba-modeling) — agent-integration.md (159 lines).
- Research: use-case-modeling (ba-modeling) — agent-integration.md (182 lines).
- Research: requirements-lifecycle (business-analyst) — agent-integration.md (176 lines).
- Research: business-process-analysis (business-analyst) — agent-integration.md (196 lines).
- **Methodology research subsystem (`skills/faion-knowledge/.research/`):**
  per-methodology `agent-integration.md` enrichment loop. Subagent researches
  each methodology for agentic workflow, CLI tools, services, when-to-use /
  when-NOT-to-use, failure modes. Always-5-active dispatch policy (cron as
  safety net; completion notifications drive replacement).
- **Research round 1: 5 methodologies enriched with `agent-integration.md`**
  — risk-assessment, workflows, market-research-tam-sam-som,
  competitive-intelligence, trend-analysis (pro/research/researcher).
- Research: technical-debt-management (product-manager) — agent-integration.md (161 lines).
- Research: feedback-management (product-manager) — agent-integration.md (155 lines).
- Research: product-explainability (product-manager) — agent-integration.md (184 lines).
- Research: business-process-analysis — agent-integration.md (204 lines).
- Research: user-story-mapping (ba-modeling) — agent-integration.md (299 lines).
- Research: frameworks — agent-integration.md (167 lines).
- Research: user-research-at-scale — agent-integration.md (206 lines).
- Research: continuous-discovery — agent-integration.md (207 lines).
- Research: opportunity-solution-trees — agent-integration.md (159 lines).
- Research: business-model-research — agent-integration.md (178 lines).
- Research: business-model-research (market-researcher) — agent-integration.md (201 lines).
- Research: distribution-channel-research — agent-integration.md (145 lines).
- Research: distribution-channel-research (market-researcher) — agent-integration.md (191 lines).
- Research: agent-invocation — agent-integration.md (166 lines).
- Research: competitor-analysis (researcher) — agent-integration.md (162 lines).
- Research: competitive-intelligence (market-researcher) — agent-integration.md (187 lines).
- Research: persona-building — agent-integration.md (137 lines).
- Research: business-model-planning — agent-integration.md (159 lines).
- Research: market-research-tam-sam-som (market-researcher) — agent-integration.md (201 lines).
- Research: trend-analysis (market-researcher) — agent-integration.md (217 lines).
- Research: market-analysis — agent-integration.md (207 lines).
- Research: continuous-discovery (market-researcher) — agent-integration.md (252 lines).
- Research: competitor-analysis (market-researcher) — agent-integration.md (197 lines).
- Research: competitive-intelligence-methods — agent-integration.md (207 lines).
- Research: product-development-trends-2026 (market-researcher) — agent-integration.md (174 lines).
- Research: product-led-growth — agent-integration.md (146 lines).
- Research: product-development-trends (market-researcher) — agent-integration.md (142 lines).
- Research: product-analytics (product-manager) — agent-integration.md (165 lines).
- Research: stakeholder-management — agent-integration.md (156 lines).
- Research: stakeholder-management (product-manager) — agent-integration.md (182 lines).
- Research: interface-analysis (ba-modeling) — agent-integration.md (134 lines).
- Research: blurred-roles-team-evolution — agent-integration.md (131 lines).
- Research: portfolio-strategy (product-manager) — agent-integration.md (157 lines).
- Research: blurred-roles-team-evolution (product-manager) — agent-integration.md (148 lines).
- Research: product-operations (pro/product) — agent-integration.md (184 lines).
- Research: experimentation-at-scale — agent-integration.md (253 lines).
- Research: methodologies-summary (product-manager) — agent-integration.md (70 lines).
- Research: experimentation-at-scale (product-manager) — agent-integration.md (231 lines).
- Research: learning-speed-competitive-moat — agent-integration.md (189 lines).
- Research: product-explainability — agent-integration.md (168 lines).
- Research: continuous-discovery-habits (product-planning) — agent-integration.md (229 lines).
- Research: competitive-positioning (product-planning) — agent-integration.md (168 lines).
- Research: portfolio-strategy — agent-integration.md (146 lines).
- Research: product-led-growth (product-manager) — agent-integration.md (192 lines).
- Research: workflows (product-manager) — agent-integration.md (175 lines).
- Research: continuous-discovery-habits (product-manager) — agent-integration.md (278 lines).
- Research: product-operations (pro/product/product-manager) — agent-integration.md (297 lines).
- Research: competitive-positioning (product-manager) — agent-integration.md (193 lines).
- Research: product-lifecycle (product-manager) — agent-integration.md (157 lines).
- Research: mlp-planning (product-manager) — agent-integration.md (146 lines).
- Research: learning-speed-competitive-moat (product-manager) — agent-integration.md (207 lines).
- Research: acceptance-criteria (ba-modeling) — agent-integration.md (148 lines).
- **Worktree-dispatch policy for research**: each subagent now runs in its own
  git worktree and ships the full lifecycle (research → edit → commit → merge
  into main via flock-serialized ff-only merge). See `.research/BRIEF.md`.

### Changed
- **Intra-domain tier reclassification round 1 (name heuristic): 90 methodology
  folders promoted to higher tier** — enterprise stacks
  (`java-spring*`, `php-laravel*`, `ruby-rails*`, `csharp-dotnet*`,
  `cqrs-pattern`, `event-sourcing*`, `microservices-design`) moved from
  `free/dev/` to `pro/dev/`; API design (`api-graphql`, `api-openapi-spec`,
  `api-rest-design`, `contract-first-development`, `pwa-development`,
  `nextjs-app-router`, `monorepo-turborepo`) moved `free/dev/` → `solo/dev/`;
  AI-adjacent topics (`claude-md-creation`, `llm-friendly-architecture`,
  `ai-*-pm-tools`, `ai-interview-analysis`, `ai-research-tool*`,
  `ai-assisted-specification-writing`, etc.) moved to `geek/`. Applied via
  `skills/faion-knowledge/.reclass/` (rules + scripts + audit log).
  Remaining 1009 ambiguous methodologies queued for content-review ticks.
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
- Research: methodologies-index — agent-integration.md (33 lines).
- Research: methodologies-detail — agent-integration.md (49 lines).
- Research: product-development-trends-2026 — agent-integration.md (152 lines).
- Research: audience-segmentation — agent-integration.md (141 lines).
- Research: product-development-trends — agent-integration.md (133 lines).
- Research: survey-design — agent-integration.md (158 lines).
- Research: market-researcher/risk-assessment — agent-integration.md (162 lines).
- Research: minimum-product-frameworks — agent-integration.md (194 lines).
- Research: release-planning (product-manager) — agent-integration.md (222 lines).
- Research: business-analyst/acceptance-criteria — agent-integration.md (215 lines).
- Atomic update with snapshot rollback for `scripts/update.sh`
  - Pre-update snapshot creation (tarball in `~/.cache/faion-network/snapshots/`)
  - Post-update integrity check (SKILL.md, hooks, AGENTS.md)
  - `--rollback` flag to restore most recent snapshot
  - `--dry-run` flag to preview changes without modifying anything
  - Automatic snapshot rotation (keeps last 3)
  - Auto-rollback prompt on integrity check failure
- `scripts/lib/snapshot.sh` — snapshot create/restore/rotate library
- `scripts/lib/integrity-check.sh` — post-update integrity verification
