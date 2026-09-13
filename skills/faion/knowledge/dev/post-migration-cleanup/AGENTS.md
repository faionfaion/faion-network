# Post Migration Cleanup

## Summary

**One-sentence:** Post-migration cleanup checklist: dual-write retirement, compat shims, doc refresh, dead-flag removal.

**One-paragraph:** Post-migration cleanup checklist: dual-write retirement, compat shims, doc refresh, dead-flag removal. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- 100% of production traffic has been served by the new path for at least one full weekly traffic cycle since a recorded cutover date.
- A reconciliation job can compare legacy and new stores (counts plus per-record checksum or field diff) and a request counter exists, or can be added, on the legacy read path.
- The migration's feature flags, shims, alerts, dashboards and infrastructure can be enumerated from the flag service, the codebase and the cloud inventory.
- Backup tooling can snapshot the legacy data, and code search plus the query log can be scanned across every repository in the organisation.
- A named human will read the snapshot URL and the scan result before any DROP or decommission runs.

## Skip If (ANY kills it)

- Cutover is not complete or has run for less than a weekly cycle; cleanup now deletes the rollback path.
- The legacy store is the contractual system of record for a retention period that has not elapsed; schedule the cleanup for after it, do not drop early.
- No reconciliation can be run (the two stores are not comparable) and no read counter can be added; the write and read paths cannot be safely retired.
- The migration is being rolled back rather than completed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cutover deploy record (first day at 100% on the new path) and the team's delivery cycle | deploy log + sprint calendar | release engineering |
| Reconciliation report: counts and per-record checksum or field diff, legacy vs new, per day | report URL | data engineering |
| Request counter on the legacy read path with caller labels, and the batch / month-end calendar | metric name + dashboard | observability |
| Flag service export listing every migration flag key | flag service | platform |
| Shim inventory: adapters, aliases, proxies, translators, redirects with known consumers | list from code review | owning team |
| Backup tooling and the snapshot's retention policy; code search across all repositories; slow-query or audit log | tool access | platform / DBA |
| Docs, runbooks, ADRs and diagrams, searchable by component name | repository | docs owners |
| Alert rules, dashboards, SLOs, synthetic checks and the cloud inventory tagged with the legacy service, with monthly cost | monitoring config + cloud billing export | SRE / FinOps |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: dual-write retired after parity, read path deleted at zero traffic, flags removed from code, shims with expiry, schema drop after backup + scan, docs/runbooks refreshed, alerts + infra decommissioned, cleanup deadline | 2150 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: cutover and parity window (>= 7 days, weekly cycle), deadline within one cycle (<= 30 days), reconciliation with zero mismatches for 7+ days and write removed by code deletion, read counter at zero 7+ days across the batch window, flags with key deleted and branches collapsed, shims deleted or dated with a named consumer, snapshot with retention and zero-hit cross-repo and query-log scan before a separate DROP, docs at zero hits outside the archive, alerts retargeted or deleted, infrastructure decommissioned with cost or running with reason and end date, deferred items with ticket and owner, human-executed drop; valid + invalid examples, forbidden patterns | ~5250 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | 1350 |
| `content/04-procedure.xml` | essential | 9 steps in safe order: fix cutover and deadline, reconcile and delete the legacy write, count reads to zero and delete the read path, delete every flag, list and date shims, snapshot and scan before the separate DROP, refresh docs, retarget alerts and decommission infra, record deferrals and hand to the reviewer | ~1850 |
| `content/05-examples.xml` | recommended | Complete cleanup checklist for an orders schema migration (three flags, one dated shim, snapshot and 41-repo scan, EUR 432/month removed, one deferred item), a note per non-obvious value, and a bad checklist with the validator output | ~2900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 850 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Checklist skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Checklist skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-post-migration-cleanup.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[framework-major-upgrade-inventory]]
- [[feature-flag-weekly-review-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
