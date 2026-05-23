# Edge and CDN Strategy

## Summary

**One-sentence:** Edge compute + CDN strategy spec: pick Cloudflare Workers / Lambda@Edge / Fastly Compute, cache-key design, origin shielding, edge auth, fallback path, cost ceiling per request.

**One-paragraph:** Edge compute (Cloudflare Workers, Lambda@Edge, Fastly Compute) + CDN sits between the user and origin. Done well: 80% origin offload, p50 latency under 50ms globally, edge auth + WAF in one place. Done badly: wrong cache keys cause cache stampede + privacy leak; un-shielded origins still get hammered; auth done partially at edge + partially at origin = duplicated bugs; per-request cost balloons silently. This methodology picks the platform, designs cache keys, configures origin shielding, places auth + WAF, and sets a per-request cost ceiling that triggers a review.

**Ефективно для:**

- 80%+ origin offload через правильні cache keys + shielding.
- Edge auth + WAF в одному місці (не дублюй в origin).
- Per-request cost ceiling: alert до того, як bill сюрприз.
- Fallback path: edge down → origin straight (CDN-bypass DNS).

## Applies If (ALL must hold)

- Public-facing web/API with global user distribution
- p50 latency targets <100ms outside primary region
- Static assets + cacheable JSON API responses
- Edge platform available (Cloudflare / AWS / Fastly / Akamai)

## Skip If (ANY kills it)

- Single-region B2B SaaS where users sit near origin — CDN gains marginal
- 100% dynamic personalised content with no cacheable surfaces — Workers possible but heavy
- Compliance forbids data egress outside specific region — edge platforms may not match

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CDN/edge account (Cloudflare / AWS / Fastly) | credentials | platform team |
| DNS control (for edge bypass fallback) | DNS console | DNS owner |
| Origin endpoints + Auth scheme defined | API specs | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ssl-tls-setup]] | TLS terminated at edge + re-encrypted to origin |
| [[egress-cost-hidden-budget-guide]] | Egress cost accounting for shielded origin |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cache_key_design` | sonnet | Bounded judgment on vary headers |
| `platform_choice` | opus | Cross-tradeoff synthesis |
| `budget_calculation` | haiku | Arithmetic from forecasted volume |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-edge-and-cdn-strategy.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[egress-cost-hidden-budget-guide]]
- [[ssl-tls-setup]]
- [[headroom-cost-model]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
