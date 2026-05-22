---
slug: design-system-v1-to-v2-migration-12-weeks
tier: pro
group: role-ux-ui-designer
persona: Design-system lead in a P6 product team
goal: migrate-rebuild
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Token + component library evolved to v2: semantic + modes taxonomy, versioned components, consumer apps migrated, drift dashboard live."
content_id: 44c127ad515be9fb
methodology_refs:
  - ai-enhanced-design-systems
  - figma-ai-ecosystem
  - accessibility-first-design
  - cross-platform-token-distribution
  - design-system-success-factors
  - semantic-tokens-and-modes
  - token-organization
  - w3c-design-tokens-standard
  - design-tokens-fundamentals
  - tailwind-design-tokens
  - consistency-standards
  - content-audit
  - design-critique
---

# Design system v1 to v2 migration (12 weeks)

## Context

Design-system lead migrates a multi-app system from v1 to v2 over 12 weeks. Includes taxonomy refactor, semantic + mode tokens, component versioning, consumer migration, Storybook + docs refresh, governance, and a drift dashboard. Done when all priority consumer apps are on v2, drift remains under threshold for 4 weeks, and governance ceremony is running.

## Outcome

v1 token/component library -> v2 with semantic tokens, modes, versioned components, migrated consumers, drift dashboard. Token + component library evolved to v2: semantic + modes taxonomy, versioned components, consumer apps migrated, drift dashboard live.

## Steps

1. **Audit v1.** Know what you are about to break. Tasks: Inventory tokens + components in v1; Run a content audit across consumer apps; List apps + their token versions.
2. **v2 taxonomy.** Design the semantic + mode token model. Tasks: Define semantic token tiers (core / alias / component); Add light/dark + density modes; Pick a W3C-compliant token format.
3. **v2 components.** Version components against new tokens. Tasks: Rebuild base components on v2 tokens; Version components (semver) with breaking change notes; Update Storybook + docs as source of truth.
4. **Token distribution.** Tokens land cleanly across iOS / Android / Web / Tailwind. Tasks: Wire token build to all platforms; Add Tailwind preset for web teams; Smoke-test on a sample app per platform.
5. **Consumer migration.** Roll consumer apps onto v2. Tasks: Migrate flagship app first; document patterns; Open PRs for remaining apps with codemods; Pair with each app team for cutover.
6. **Drift dashboard.** Detect regressions early. Tasks: Wire drift scan (visual + token coverage) on PRs; Publish a live dashboard with drift metrics; Define drift threshold + alert rules.
7. **Governance.** v2 stays healthy without you in the loop daily. Tasks: Stand up monthly design-system governance review; Define proposal -> review -> ship process for changes; Publish deprecation policy for v1.

## Decision points

- **After Audit v1:** Advance when every consumer app has a documented v1 footprint.
- **After v2 taxonomy:** Advance only when token tiers + modes are reviewed and signed off.
- **After v2 components:** Advance only when each base component has a versioned v2 release.
- **After Token distribution:** Advance only when sample apps render correctly on every platform.
- **After Consumer migration:** Advance when migration percentage hits >=90% of priority apps.
- **After Drift dashboard:** Advance only when dashboard runs on every PR and produces alerts.
- **After Governance:** Done when governance cycle has run twice without escalation.

## References

- `faion/knowledge/geek/ux/ui-designer/ai-enhanced-design-systems`
- `faion/knowledge/geek/ux/ui-designer/figma-ai-ecosystem`
- `faion/knowledge/pro/ux/accessibility-specialist/accessibility-first-design`
- `faion/knowledge/pro/ux/ui-designer/cross-platform-token-distribution`
- `faion/knowledge/pro/ux/ui-designer/design-system-success-factors`
- `faion/knowledge/pro/ux/ui-designer/semantic-tokens-and-modes`
- `faion/knowledge/pro/ux/ui-designer/token-organization`
- `faion/knowledge/pro/ux/ui-designer/w3c-design-tokens-standard`
- `faion/knowledge/solo/ux/ui-designer/design-tokens-fundamentals`
- `faion/knowledge/solo/ux/ui-designer/tailwind-design-tokens`
- `faion/knowledge/solo/ux/ux-ui-designer/consistency-standards`
- `faion/knowledge/solo/ux/ux-ui-designer/content-audit`
- `faion/knowledge/solo/ux/ux-ui-designer/design-critique`
- Related: `zero-to-one-product-design-brief-to-dev-handoff-8-weeks`, `design-system-as-code-lifecycle-tokens-storybook-figma-library-pr-governance`
