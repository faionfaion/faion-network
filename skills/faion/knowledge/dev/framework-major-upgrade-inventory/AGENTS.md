# Framework Major Upgrade Inventory

## Summary

**One-sentence:** Pre-upgrade forensics inventory: codemod surface, breaking-change map, risk matrix before any code touches.

**One-paragraph:** Pre-upgrade forensics inventory: codemod surface, breaking-change map, risk matrix before any code touches. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- The target is exactly one major version above the framework version deployed today (or the path has been split into one inventory per major step).
- The vendor publishes release notes or an upgrade guide for every minor between current and target.
- The full test suite runs green on the current version and the framework has a switch to elevate deprecation warnings to errors.
- The dependency manifest and each framework-dependent package's release notes are reachable.
- Deployed language, database and runtime versions are known for every environment.

## Skip If (ANY kills it)

- The bump is minor or patch (`major_gap` = 0); run the suite with warnings enabled and proceed without an inventory.
- No test suite exists to run with deprecation warnings as errors; write the characterisation tests first, the inventory has nothing to count.
- The framework is being replaced rather than upgraded; that is a migration plan, not an upgrade inventory.
- The vendor has no release notes for the target (unreleased or unsupported version); nothing can be cited.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Framework version deployed in every environment and the target version | version strings per environment | deployment config / lockfile |
| Vendor release notes for every minor between current and target, and the upgrade guide | URLs | vendor documentation site |
| CI run of the full suite on the current version with deprecation warnings elevated to errors | CI log URL | CI |
| Dependency manifest with every framework-dependent package and version | lockfile (`requirements.txt`, `package-lock.json`, `Gemfile.lock`, `pom.xml`) | repository |
| Release notes of each framework-dependent package stating its compatible framework versions | URLs | package repositories |
| Codemod tooling for the ecosystem and its documentation on partial or experimental transforms | tool docs | `django-upgrade`, `react-codemod`, `ng update`, `rector`, OpenRewrite, `pyupgrade` |
| Language, database, Node / JVM and base-image versions per environment | version strings | infrastructure inventory |
| Map of which modules serve production requests and which run jobs | code ownership doc or routing table | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: one major per inventory, vendor-cited map, deprecation warnings as errors, call-site counts, codemod classification, dependent-package compatibility, runtime prerequisites, two-axis risk | 2050 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for one major step: major_gap = 1, deprecation run with warnings as errors, release notes covered, breaking changes with vendor citation, reproducible call-site count, codemod / manual with dry run, two-axis risk and characterisation tests, dependent packages with blockers and plans, runtime prerequisites per environment, review state with no agent-opened branch; valid + invalid examples, forbidden patterns | ~5300 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | 900 |
| `content/04-procedure.xml` | essential | 8 steps: fix the single major step, deprecation run as errors, map from vendor release notes, reproducible call-site counts, codemod dry run, dependent packages and runtime prerequisites with blockers, two-axis risk and characterisation tests, hand to the human reviewer | ~1850 |
| `content/05-examples.xml` | recommended | Complete Django 4.2 to 5.0 inventory with three changes, a blocker plugin and a characterisation test, a note per non-obvious value, and a bad 3.2 to 5.0 inventory with the validator output | ~2750 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Report skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Report skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-framework-major-upgrade-inventory.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[post-migration-cleanup]]
- [[framework-decomposition-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
