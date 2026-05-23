# Supabase RLS Audit Checklist

## Summary

**One-sentence:** Generates a per-table Supabase RLS audit — enable flag, SELECT/INSERT/UPDATE/DELETE policy presence, anon/auth role coverage — gated by row-level test fixtures.

**One-paragraph:** RLS misconfiguration on Supabase is the leading data-leak pattern for vibe-coded MVPs. This methodology audits every public-schema table: enable flag, presence of SELECT/INSERT/UPDATE/DELETE policies, anon-vs-authenticated coverage, and a fixture-driven test that proves anon CANNOT read another tenant's row. Output: an RlsAuditReport with per-table verdicts.

**Ефективно для:**

- Pre-launch MVP on Supabase that has 'shipped fast' without an RLS review.
- Audit of a freshly-AI-generated schema where policies were skipped.
- Compliance prep (SOC 2, GDPR) requiring documented tenant isolation.
- Routine quarterly check of an existing production schema.

## Applies If (ALL must hold)

- Production data on Supabase (or any Postgres with RLS).
- Multi-tenant or multi-user app where rows belong to specific principals.
- Anon role has any access to public schema tables.
- No documented RLS audit within the last 90 days.

## Skip If (ANY kills it)

- Single-tenant app where every authenticated user can see everything.
- Tables explicitly designed for public read (CMS content, blog posts).
- Audit performed within the last 90 days with documented evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Supabase service-role key | secret | operator vault |
| Schema dump | pg_dump --schema-only | supabase CLI |
| Test fixtures (≥2 tenants) | SQL inserts | test repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| secrets-management | Service-role key handling from secrets plan. |
| supabase-backup-and-restore-drill | Audit runs against a restored clone, never prod. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-rls-enabled-every-public-table, r2-policy-per-verb, r3-anon-cannot-read-other-tenant, r4-named-owner, r5-fixture-driven-tests | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Supabase RLS Audit Checklist artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: rls-disabled-public-table, missing-update-policy, anon-can-read-all, no-test-fixtures | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-audit-plan` | sonnet | Per-table risk assessment. |
| `render-test-fixtures` | sonnet | Per-table fixture generation with tenant boundaries. |
| `diff-against-prev` | haiku | Schema diff between audits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/supabase-rls-audit-checklist.json` | RlsAuditReport JSON skeleton. |
| `templates/supabase-rls-audit-checklist.md` | Audit trail + per-table verdict table. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-supabase-rls-audit-checklist.py` | Validate RlsAuditReport JSON against the schema. | After each audit before closing. |

## Related

- [[secrets-management]]
- [[supabase-backup-and-restore-drill]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
