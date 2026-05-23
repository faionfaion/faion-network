# Google Ads Account Foundations

## Summary

**One-sentence:** Produces a Google Ads account-setup spec: campaign types selected, ad-group + keyword scaffold, conversion tracking + audiences + extensions enabled, billing + permissions sanity.

**One-paragraph:** Foundation spec for any new Google Ads account or major refactor. Locks campaign-type choice (Search / Display / Video / Shopping / Performance Max), the 1 ad group = 1 theme structure, match-type policy (broad with smart bidding OR exact/phrase without), conversion tracking + GA4 import, ad extensions (sitelinks, callouts, structured snippets), and billing + permission hygiene.

**Ефективно для:**

- New Google Ads account або major refactor.
- Selecting кампейн type — Search vs Display vs PMax.
- Ad-group structure: 1 group = 1 intent + 10-20 keywords.
- Conversion tracking + GA4 import + extensions setup.

## Applies If (ALL must hold)

- New Google Ads account onboarding.
- Major restructure: cleaning up legacy single-keyword-per-ad-group accounts.
- Audit before scaling spend ≥$5k/mo.
- Hand-off from agency / consultant to in-house team.

## Skip If (ANY kills it)

- Existing account already structured per these rules — minor tuning only.
- Awareness-only campaigns with no conversion — Display methodology fits better.
- Spend under $500/mo — overhead exceeds payoff.
- Single-product low-LTV ecom — Shopping methodology fits better.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Google Ads account access | OAuth | platform owner |
| GA4 linked + events defined | dashboard | ads-conversion-tracking |
| Keyword research | CSV | ads-google-keywords |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion events required before scaling. |
| `pro/marketing/ppc-manager/ads-google-keywords` | Keyword research feeds the ad-group scaffold. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-ads-basics | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-campaign-types` | sonnet | Intent-to-type mapping with judgement. |
| `ad-group-scaffold` | haiku | Mechanical 1-theme = 10-20 keyword grouping. |
| `extensions-set` | haiku | Apply standard 3-extension floor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/account-spec.md` | Google Ads account setup spec Markdown skeleton. |
| `templates/extensions-checklist.md` | Extensions checklist before launch. |
| `templates/account-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-ads-basics.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-google-keywords]]
- [[ads-google-creative]]
- [[ads-conversion-tracking]]
- [[google-ads-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
