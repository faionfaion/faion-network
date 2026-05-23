# What You Don't Know About Launch Pre-Mortem

## Summary

**One-sentence:** Walk a solo SaaS launch through every category of unknown-unknown before pressing GO — produces a checklisted pre-mortem report with named owners and revisit triggers.

**One-paragraph:** Solo SaaS founders 'don't know what they don't know' about launch. This methodology walks a structured pre-mortem across the launch surface: billing edges, auth recovery, GDPR data paths, support SLAs, payment-processor edge cases, refund flows, abuse vectors, retention triggers. Each surface produces a row: what could fail / how we'd know / who owns the fix / kill criterion. Output: a one-page launch pre-mortem report signed by the founder, pinned at the canonical pre-launch path, refreshed on launch-week.

**Ефективно для:**

- Solo founder pushing a vibe-coded MVP to billing.
- Indie operator launching paid tier this quarter.
- Two-person team without a release engineer.
- Builder who skipped the staging-environment debate.

## Applies If (ALL must hold)

- Pre-launch hardening window is open (≥7 days before GO).
- Product has billing enabled or is about to.
- There is no formal launch checklist in place.
- Founder accepts that some launch outcomes are unrecoverable (refunds, data loss).

## Skip If (ANY kills it)

- Launch window already closed — run post-launch incident review instead.
- Product is pre-billing, fully reversible — defer pre-mortem to billing rollout.
- Team has an existing safe-launch checklist that already covers the surface.
- Regulated launch (HIPAA, PCI) where the regulator's launch protocol overrides.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Architecture sketch | diagram / md | founder notes |
| Billing-processor account state | Stripe / Lemon / Paddle dashboard | billing portal |
| Auth + recovery flows | screen list | product |
| Customer-support contact path | email / form / Intercom | support setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | operating context for solo PM tasks |
| `solo/product/gdpr-for-solo-saas` | the GDPR-specific row of the pre-mortem |

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
| `draft-what-you-dont-know-about-launch-pre-mortem` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/what-you-dont-know-about-launch-pre-mortem.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/what-you-dont-know-about-launch-pre-mortem.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-what-you-dont-know-about-launch-pre-mortem.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[gdpr-for-solo-saas]]`
- `[[beta-charter-template]]`
- `[[indie-portfolio-scorecard]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
