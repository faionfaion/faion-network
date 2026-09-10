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

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules: directory not file, routing pair per subdir, rebuild test (two-week bar, delivery-event timing, blocking), same-PR delta + "no spec impact" + reviewer diff, canonical `.aidocs/project-spec/` path, current revision only, one spec per product, constitution deviation | ~1800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the project-spec/ tree + rebuild-test record; valid / invalid examples; 7 forbidden patterns | ~1800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: single giant file, subdir without routing pair, rebuild test on cron, "spec PR next week", spec in agent-home, git-ignored .aidocs | ~1150 |
| `content/04-procedure.xml` | essential | 6 steps: locate/create at canonical path, flat files, routing subdirs, same-PR delta, reviewer diff, rebuild test (LLM dry-run protocol) as blocking gate | ~1350 |
| `content/05-examples.xml` | recommended | The canonical tree with every file's purpose, subdirectory inventory, F0042 same-PR delta (good / bad) | ~1100 |
| `content/06-decision-tree.xml` | essential | Applicability gate, location check, then routing by delivery event (PR open / moving to done / post-fix deploy / cron / new project) | ~850 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-project-spec-structure.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sdd-workflow-overview]] — where project-spec slots in.
- [[readiness-checklist]] — `readiness.md` enforces the delta-update checkbox.
- [[cr-bug-tracking]] — BUG that exposes missing business rule MUST update `business-rules.md` in the same PR.
- [[plan-md-structure]] — per-feature `plan.md` carries feature-scoped contracts only.

## Decision tree

Apply this methodology when the project runs the SDD lifecycle and has crossed the "more than 3 features shipped" mark; the spec lives at the canonical `.aidocs/project-spec/` path unless constitution.md declares a deviation. Skip for prototypes and pure-CRUD scaffolds where the framework is the spec.
