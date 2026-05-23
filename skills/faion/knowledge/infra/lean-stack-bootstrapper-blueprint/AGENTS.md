# Lean Stack Bootstrapper Blueprint

## Summary

**One-sentence:** Produces a free-tier reference architecture spec: Vercel + Supabase + Stripe + Cloudflare + one observability vendor, with cost ceiling, upgrade triggers, and vendor-lock acceptance note.

**One-paragraph:** faion infra knowledge skews to Docker / k8s / CI/CD heavy stacks (Pro). P2 reality: indie hackers use Vercel + Supabase + Stripe + Cloudflare. This methodology produces a tier-correct lean-stack reference at free tier: stack diagram, cost ceiling, upgrade triggers, vendor-lock acceptance note. ≤5 services, monthly ceiling alert at 80%, auto-pause at 100%, no premature Docker.

**Ефективно для:** indie hackers shipping their first 1-3 SaaS products; pre-PMF founders avoiding infra rabbit holes; teams that need a one-page architecture diagram to justify a free-tier deploy to a stakeholder.

## Applies If (ALL must hold)

- Indie hacker shipping first 1-3 SaaS products
- Pre-PMF revenue (<$2k MRR) where infra spend must stay under $50/mo
- Team has no DevOps engineer and won't hire one
- Stack must be deployable end-to-end in <1 day

## Skip If (ANY kills it)

- Compliance constraint (HIPAA / SOC2) requires self-hosted
- Already past PMF with $10k+ MRR and feature velocity is the bottleneck
- Team has a DevOps engineer and prefers k8s/IaC

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Product brief | Markdown, 1 page | founder |
| Domain name | registered domain | registrar |
| Stripe / Supabase / Vercel / Cloudflare accounts | free-tier accounts | vendor signup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[server-craft]]` | solo-tier server fundamentals if escalation needed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick vendor per role | sonnet | Rubric application. |
| Author stack diagram | sonnet | Composition from template. |
| Decide graduate-to-pro timing | opus | Trade-off across cost / latency / availability. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stack-diagram.md.tmpl` | 1-page architecture diagram with vendor / role / cost / ceiling table. |
| `templates/upgrade-triggers.md.tmpl` | Trigger table: metric, threshold, action. |
| `templates/cost-ceiling.md.tmpl` | Per-vendor ceiling + alert configuration recipe. |
| `templates/_smoke-test.md` | Filled example for a B2B SaaS founder. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lean-stack-bootstrapper-blueprint.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/infra/`
- `[[server-craft]]`
- `[[automation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether lean-stack-bootstrapper-blueprint applies: root question — "Is the project pre-PMF (<$2k MRR) and solo/duo founder?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
