# Freelance Referral Program Design

## Summary

**One-sentence:** Service-business referral mechanics — bounded incentive ($ or credit), NDA-safe testimonial framing, partner-swap pair design, ≤90-day attribution window, owner-named on every referral.

**One-paragraph:** growth-referral-programs targets B2C product loops; service businesses need their own mechanics. This methodology pins 4 elements: bounded incentive (flat $ amount or credit; never %); NDA-safe testimonial framing (logo + outcome without client-confidential numbers); partner-swap pair design (you refer them, they refer you, both consenting); attribution window ≤90 days (after that, the lead is organic). Core rules: incentive is documented in writing per referrer; testimonial framing pre-approved; partner pairs explicitly opted-in; attribution window enforced; conflict-of-interest disclosed.

**Ефективно для:**

- Solo consultant — formalize the warm-lead pipeline.
- Agency — partner network with non-competing peers.
- Productized service — referral incentive structure.
- Post-pivot pipeline — new niche referrers need a program.

## Applies If (ALL must hold)

- ≥3 closed customers willing to refer.
- Service offering with measurable customer outcome.
- Authority to pay flat incentives (legal + tax-compliant).
- Network of ≥3 non-competing peers for swap pairs.

## Skip If (ANY kills it)

- Pre-PMF — no referrers exist yet.
- Single anchor client = 80%+ revenue.
- Local-regulated business where referral fees are restricted.
- Enterprise sale where procurement forbids referrer comp.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer list with consent to refer | CRM | own ops |
| Peer / partner network list | spreadsheet | own ops |
| Standard offering price | spec | own ops |
| Tax handling for referral fees | guidance | accountant |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[freelance-pilot-pricing]] | Pilot completions are common referral sources. |
| [[freelancer-niche-positioning]] | Referrer pitch uses the niche positioning. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: flat-incentive-not-percent, written-incentive-per-referrer, nda-safe-testimonial-framing, attribution-window-90-days, partner-swap-opted-in | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-incentive` | sonnet | Light judgment with accountant input. |
| `draft-terms` | sonnet | Bounded template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/program-spec.json` | JSON example of referral program spec |
| `templates/referrer-terms.md` | Written terms template per referrer |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-referral-program-design.py` | Validate one spec JSON against the schema | After draft, before publish |

## Related

- [[freelance-pilot-pricing]]
- [[freelancer-niche-positioning]]
- [[partnership-co-marketing-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
