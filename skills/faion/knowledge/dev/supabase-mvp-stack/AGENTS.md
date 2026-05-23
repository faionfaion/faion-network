# Supabase MVP Stack

## Summary

**One-sentence:** Supabase MVP stack spec: RLS default-on, explicit non-permissive policies, versioned migrations, bucket policies private-by-default, Realtime payload review, edge-function audit.

**One-paragraph:** Solo SaaS on Supabase ships fast but leaks easily. RLS off by default leaks rows; permissive policies (`TO public USING (true)`) collapse access control; manual schema changes in the dashboard orphan dev environments; storage buckets default to public; Realtime over-broadcasts PII. This methodology produces a Supabase stack spec: per-table RLS posture, scoped policies, migration discipline, bucket privacy policy, Realtime payload review, and a per-edge-function permission audit, signed by a named owner.

**Ефективно для:**

- Перший Supabase проект - зафіксувати baseline (RLS-on + scoped policies + migrations).
- Audit після RLS-off table - перейти на default-on policy + ревью існуючих policies.
- Migration drift між dashboard і кодом - зафіксувати repo-only migrations.
- Storage bucket public-by-default leak - перейти на signed URLs + bucket policy.
- Realtime broadcast з PII - впровадити payload review + per-row policy.

## Applies If (ALL must hold)

- Backend uses Supabase (Postgres + Auth + Storage + Realtime + Edge Functions).
- Team controls the Supabase project (admin access for migrations + policy edits).
- At least one user-facing app reads/writes Supabase data.
- Project has user-scoped data (auth.uid()-keyed rows).

## Skip If (ANY kills it)

- Backend is plain Postgres or another BaaS (Firebase, Hasura) - use that stack's guide.
- Internal-only Supabase project with no public client - lighter guidance sufficient.
- Greenfield prototype with synthetic data - delay hardening to launch.
- Enterprise managed-Postgres alternative is already in flight - migrate instead of hardening.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Supabase project | URL + service role key in secret manager | platform |
| Migration tool | supabase CLI installed locally + in CI | engineering |
| Bucket inventory | list of buckets + intended privacy | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-testing]] | wider security context (auth + audit) the stack plugs into. |
| [[sql-optimization]] | Postgres performance methodology this stack relies on at scale. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: RLS-on, scoped policies, versioned migrations, bucket privacy, Realtime payload review, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: RLS audit, policy review, migrations, bucket policy, Realtime | ~800 |
| `content/05-examples.xml` | essential | Worked example: a 2-tenant SaaS on Supabase passing audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-rls-state` | haiku | Mechanical SELECT on pg_class + pg_policies. |
| `design-policies` | sonnet | Per-table scoping with auth.uid() / role. |
| `scope-migrations` | sonnet | Cadence + naming + review-gate per team. |
| `review-realtime-payloads` | opus | Stakes high; PII in Realtime is a public leak. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rls-audit.sql` | SQL query: list tables with RLS off + their owner. |
| `templates/policy-template.sql` | Policy templates scoped to auth.uid() and role. |
| `templates/supabase-stack.md` | Markdown spec listing posture per surface. |
| `templates/_smoke-test.json` | Filled-in minimum viable stack spec for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-supabase-mvp-stack.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[sql-optimization]]
- [[security-testing]]
- [[rest-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then RLS posture, then policy permissiveness, then migration discipline, then bucket / Realtime privacy. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default for non-Supabase stacks.
