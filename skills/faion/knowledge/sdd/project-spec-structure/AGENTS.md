# Project-Spec Structure

## Summary

**One-sentence:** `project-spec/` is the per-project source-of-truth folder (not a single file) that captures the durable shape of the system — domain, business rules, data model, deploy, invariants — and is updated in lockstep with every feature that lands.

**One-paragraph:** Where `spec.md` describes ONE feature (delta), `project-spec/` describes the whole project. Canonical location: `.aidocs/project-spec/` at the repo root (ONE spec per product for monorepos), committed to git, holding only the current revision of every file — history lives in git and `features/done/`, never in the tree. It is a directory tree, each subfolder carrying its own `AGENTS.md` + `CLAUDE.md` so agents can route into it without bulk-loading. The acceptance bar is the **rebuild test**: with only `project-spec/` + `ui-ux-design.md` + `constitution.md`, a mid-level dev should rebuild the project in two weeks. The test runs at end-of-feature (move to `done/`) and pre-deploy after any CR/BUG fix — not on a calendar cadence.

**Ефективно для:**

- Solo / small-team projects where institutional memory lives in one head.
- Multi-repo projects where `spec.md` per feature drifts from system-wide reality.
- LLM-driven dry-run audits (load only project-spec/ + ui-ux-design.md and probe for gaps).

## Applies If (ALL must hold)

- The project lives long enough that a per-feature spec is not enough context to onboard or rebuild.
- The team uses SDD lifecycle (features ship as deltas).
- The project repo carries a committed `.aidocs/` (SDD lifecycle), so the canonical `.aidocs/project-spec/` path is available.

## Skip If (ANY kills it)

- One-off script or throwaway prototype — overhead exceeds value.
- The project has no durable domain model (pure plumbing / glue code).

## Content

| File | What's inside |
|------|---------------|
| `content/01-folder-shape.xml` | Directory tree: subdirs `domain/`, `api/`, `integrations/`, `decisions/`; flat files `mission.md`, `glossary.md`, `business-rules.md`, `data-model.md`, `auth.md`, `deploy.md`, `config-secrets.md`, `non-functional.md`, `observability.md`, `invariants.md`. Each subdir has AGENTS.md+CLAUDE.md. |
| `content/02-rebuild-test.xml` | Definition of the rebuild test as acceptance gate. Run at end-of-feature transition to `done/` AND before each deploy following a CR/BUG fix. LLM dry-run protocol: read only project-spec + ui-ux-design.md + constitution.md; report gaps. |
| `content/03-delta-update.xml` | Per-feature delta lands in the same PR that ships the feature. Reviewer checks diff matches code. `readiness.md` carries a checkbox that blocks merge until delta is drafted or "no spec impact" is justified. |
| `content/04-location-decision.xml` | Canonical location: `.aidocs/project-spec/` at repo root, committed to git; ONE spec per product for multi-repo. Current-revision-only rule (history = git + `features/done/`). `constitution.md` declares deviations only. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sdd-workflow-overview]] — where project-spec slots in.
- [[readiness-checklist]] — `readiness.md` enforces the delta-update checkbox.
- [[cr-bug-tracking]] — BUG that exposes missing business rule MUST update `business-rules.md` in the same PR.
- [[plan-md-structure]] — per-feature `plan.md` carries feature-scoped contracts only.

## Decision tree

Apply this methodology when the project runs the SDD lifecycle and has crossed the "more than 3 features shipped" mark; the spec lives at the canonical `.aidocs/project-spec/` path unless constitution.md declares a deviation. Skip for prototypes and pure-CRUD scaffolds where the framework is the spec.
