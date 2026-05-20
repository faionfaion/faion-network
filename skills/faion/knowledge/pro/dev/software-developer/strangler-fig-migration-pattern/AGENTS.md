---
slug: strangler-fig-migration-pattern
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "d424428bec41642f"
summary: Named, stepped-out incremental-migration pattern for framework upgrades (Vue 2→3, Next pages→app router, Rails major, Django major) that avoids the big-bang branch.
tags: [strangler-fig, migration, framework-upgrade, refactor, pro, dev]
---
# Strangler Fig Migration Pattern

## Summary

**One-sentence:** The canonical incremental-migration pattern, named and stepped out for common framework-upgrade scenarios (Vue 2→3, Next pages→app router, Rails major, Django major), to survive a major upgrade without a big-bang branch.

**One-paragraph:** Trunk-based content references the pattern obliquely ("don't fork main"). This methodology names it and gives the developer a recipe: wrap the legacy boundary with a router or adapter, build new functionality in the target framework BESIDE the legacy code, redirect routes one-by-one to the new implementation, and delete the legacy code only when all routes have been redirected. The result: main stays releasable every day, no long-running branch, no all-or-nothing cutover, no team blocked by a single mega-PR. Four scenario-specific recipes are included: Vue 2→3 (vue-demi compatibility layer), Next.js pages→app router (route-by-route move), Rails major (engine isolation), Django major (URL-include split).

## Applies If (ALL must hold)

- Codebase is on a framework version with a known major upgrade path AND continued business need.
- Team has &gt;1 person (the pattern relies on parallel work on legacy + new).
- The build system can serve both old and new code paths simultaneously (router-level routing, feature-flag system, or framework support).
- The deprecated version has an OS / security window of at least 6 months (less → emergency upgrade methodology applies instead).

## Skip If (ANY kills it)

- Codebase is small enough that a big-bang upgrade in a week is cheaper than the pattern overhead (rule of thumb: ≤30 files, ≤200 commits).
- Framework upgrade is incompatible with parallel operation (rare; e.g. monolithic global runtime change with no isolation primitive).
- Business cannot tolerate ANY mixed state (regulated compliance contexts where dual-stack is a control failure).
- The "upgrade" is actually a full rewrite — different methodology (`microservice-extraction-decision-tree` or full rewrite playbook).

## Prerequisites

- A migration backlog: list of routes / modules / components in legacy, each tagged with size + risk.
- An "outermost router" or boundary that can dispatch between legacy and new (e.g. nginx, Next.js middleware, Rails Rack stack, Django URLconf).
- A feature-flag or environment-variable mechanism to gate per-route routing.
- CI capable of running both stacks side-by-side on the same PR.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/codemod-recipe-library` | Codemods automate the mechanical portion of each move. |
| `pro/dev/software-developer/contract-testing-consumer-driven` | Contract tests verify the new implementation matches legacy at the boundary. |
| `geek/dev/software-developer/dual-write-shadow-read-template` | Useful when the migration includes a backend store. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: boundary first, new code beside legacy, route-by-route cutover, legacy frozen post-cutover, completion-by-deletion | ~1300 |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodologies: `codemod-recipe-library`, `contract-testing-consumer-driven`, `microservice-extraction-decision-tree`
- external: [Martin Fowler — StranglerFigApplication](https://martinfowler.com/bliki/StranglerFigApplication.html) · [Next.js App Router Migration Guide](https://nextjs.org/docs/app) · [Vue 3 Migration Guide](https://v3-migration.vuejs.org/)
