# Naming and Domains

## Summary

**One-sentence:** Generate product names against trademark / pronounceability / SEO constraints, then validate domain + handle availability before launch.

**One-paragraph:** Names that are unsearchable, unpronounceable, or trademark-collided cost a relaunch later. This methodology produces a shortlist of 10 candidate names against fixed constraints (≤9 chars preferred / pronounceable in target locales / no trademark hits / not generic dictionary / two-word fallback allowed), then runs a domain + handle availability check (apex domain, .com / .net / .ai, plus the top 3 social handles), and outputs a report ranking the top 3 with rationale.

**Ефективно для:**

- Solo founder pre-launch picking a brandable name.
- Indie operator renaming after a pivot.
- Builder who has 'just one good idea' for a name and needs a sanity check.
- Operator deciding between .com vs .ai vs ccTLD before signup.

## Applies If (ALL must hold)

- Product or company name is being chosen pre-launch.
- Operator can register the chosen domain in the next 72 hours.
- Target locales (≥1) are known.
- Operator accepts that brandable > literal.

## Skip If (ANY kills it)

- Existing brand with traction — renaming costs > value.
- Name is a personal name (Sam Smith Consulting) — different rules.
- Trademark search is impossible (operator cannot afford counsel and the segment is heavily trademarked).
- Operator has emotional attachment to one name and won't accept the report — settle the attachment first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target locales | list | operator brief |
| Brand voice 1-pager (optional) | md | operator brief |
| Competing names in segment | csv / md | competitor scan |
| Domain registrar account | Cloudflare / Namecheap / Porkbun | operator setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/niche-evaluation` | niche definition feeds name semantics |
| `solo/marketing/marketing-manager` | brand-voice context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-naming-and-domains` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/naming-and-domains.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/naming-and-domains.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-naming-and-domains.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[niche-evaluation]]`
- `[[idea-generation-methods]]`
- `[[pricing-research]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
