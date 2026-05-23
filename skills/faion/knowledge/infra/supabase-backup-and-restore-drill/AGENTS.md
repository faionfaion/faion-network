# Supabase Backup and Restore Drill

## Summary

**One-sentence:** Generates a quarterly Supabase backup-and-restore drill plan + verified-restore evidence — provider snapshot + pg_dump + restore-to-clone — gated by an actual successful restore.

**One-paragraph:** Solo founders trust Supabase auto-backups without ever restoring from them. This methodology pins a quarterly drill: take a fresh pg_dump alongside the provider snapshot, restore into a clean Supabase project, run a row-count + checksum validation, record the restore time. Output: a DrillReport with restore_seconds + row_count_delta = 0.

**Ефективно для:**

- Solo SaaS storing customer data on Supabase / Neon / Render with no verified restore.
- Pre-launch hardening of a vibe-coded MVP before billing real users.
- SOC 2 / GDPR posture requiring documented restore drills.
- Audit of an existing 'we have backups' claim against actual restore proof.

## Applies If (ALL must hold)

- Production data lives on managed Postgres (Supabase / Neon / Render).
- Operator has never personally restored from backup OR last drill > 90 days ago.
- Customer data is non-trivial — billing, content, or identity.
- Compliance / customer trust requires evidence (not just provider claim).

## Skip If (ANY kills it)

- Self-managed Postgres on VPS — different methodology (backup-recovery).
- Zero-data app (purely stateless frontend).
- Drill performed within the last 90 days with documented evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Supabase service-role key | secret in 1Password | operator vault |
| Empty target Supabase project for restore | project ID | operator setup |
| Storage location for pg_dump | S3 / B2 / local | operator backup config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| secrets-management | Service-role key lives in the secrets plan. |
| monitoring-logging | Drill outcome reports via the alert path. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-quarterly-cadence, r2-restore-to-clone-not-prod, r3-checksum-validation, r4-named-owner, r5-evidence-recorded | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Supabase Backup and Restore Drill artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: trust-provider-no-verify, restore-into-prod, no-checksum-just-runs, drill-skipped | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-drill-plan` | sonnet | Per-project scoping with stakes. |
| `validate-restore-evidence` | sonnet | Row-count + checksum diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/supabase-backup-and-restore-drill.json` | DrillReport JSON skeleton. |
| `templates/supabase-backup-and-restore-drill.md` | Audit trail + restore-time evidence. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-supabase-backup-and-restore-drill.py` | Validate DrillReport JSON against the schema. | After each drill before closing the ticket. |

## Related

- [[secrets-management]]
- [[monitoring-logging]]
- [[supabase-rls-audit-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
