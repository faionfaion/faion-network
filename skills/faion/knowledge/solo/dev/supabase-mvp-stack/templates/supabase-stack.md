<!-- purpose: Markdown spec listing posture per Supabase surface. -->
<!-- consumes: see content/02-output-contract.xml inputs for supabase-mvp-stack -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Supabase MVP Stack Spec

- owner: REPLACE
- last_reviewed: REPLACE

## Tables (RLS + policies)
| Table | RLS | Policies |
|-------|-----|----------|
| orders | on | select_own / insert_own |
| tenants | on | select_by_role |

## Buckets
| Bucket | Private |
|--------|---------|
| avatars | no (signed URL writes) |
| invoices | yes |

## Migrations path
- supabase/migrations/

## Realtime channels
| Channel | Payload reviewed |
|---------|------------------|
| orders:by-tenant | yes |
