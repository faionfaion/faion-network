# Conversion Tracking

## Summary

**One-sentence:** Generates the conversion-tracking config: event taxonomy, pixel + server-side tags, validation script, QA fixtures across browsers.

**One-paragraph:** Generates the conversion-tracking config: event taxonomy, pixel + server-side tags, validation script, QA fixtures across browsers. Use it when кілька джерел трафіку, потрібен unified event taxonomy. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Кілька джерел трафіку, потрібен unified event taxonomy.
- Server-side tagging доступний (GTM Server / Cloudflare Worker).
- Privacy mode browsers + ad-blockers — потрібен CAPI / Conversions API.
- QA fixtures + validation script запускаються при кожній зміні tracking.

## Applies If (ALL must hold)

- The site sends conversion events to at least one of GA4, Google Ads, Meta or Plausible, and more than one traffic source needs one event taxonomy.
- The codebase has CI that can run `validate-events.py` against an `events.yml` registry before tag code merges.
- DNS for the site domain is under the team's control, so a server container can live on a first-party subdomain.
- A consent management platform can push Consent Mode v2 defaults before the config call and update on choice.
- Chrome, Safari, Firefox and an ad-blocker profile are available to run fixtures on every tracking change.

## Skip If (ANY kills it)

- No analytics or advertising destination exists yet: set one up first; there is nothing to track into.
- The site has a single traffic source and no revenue events, and one vendor snippet with default events covers it.
- Server-side tagging is required by the brief but the domain's DNS cannot be changed: a container on the vendor domain gains nothing under ITP.
- The change is a reporting question (which channel converts), not a tracking change: use the analytics reporting methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Business event list | event name, parameters, which destination treats it as a conversion | product and marketing leads |
| Destinations and ids | GA4 measurement id, Google Ads conversion actions, Meta pixel id | platform admin consoles |
| Order identifier | the per-order id finance reconciles against | order system |
| Consent regions | which markets require consent and the CMP in use | legal / CMP configuration |
| Server container endpoint | first-party subdomain with DNS record, e.g. `gtm.example.com` | DNS / GTM server or Cloudflare Worker |
| QA browsers | Chrome, Safari, Firefox and a Chrome profile with a mainstream ad blocker | QA environment |
| `templates/validate-events.py`, `templates/funnel-tracker.js` | CI registry check and funnel helper | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: event registry in CI, GA4 naming limits, transaction_id on revenue events, browser/server dedup, consent before tags, no PII, first-party server endpoint, cross-browser QA fixtures | 2300 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the tracking config: destinations, events.yml registry in CI, Consent Mode v2 defaults with regions, first-party server container forwarding browser ids, events inside GA4 limits with transaction_id dedup and conversion roles, QA fixtures per event across three browsers and an ad-blocker profile with PII-free payloads; valid and invalid configs; 8 forbidden patterns | ~5400 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 8 steps: register the taxonomy and CI validator, name events inside GA4 limits, transaction_id on monetary events, consent defaults before config, first-party server container, dual-send dedup, strip PII and hash identifiers, run fixtures and validate | ~1750 |
| `content/05-examples.xml` | recommended | Complete config for an e-commerce site (GA4 + Google Ads + Meta, EU/GB denied defaults, gtm.example.com, purchase with transaction_id dedup, hashed email on sign_up, fixtures in four profiles) with a note per value, plus the config as usually shipped and what the validator prints | ~3000 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-conversion-tracking.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/conversion-tracking.config.yaml` | YAML config skeleton matching the contract: destinations, registry, consent, server_side, events with dedup, QA fixtures |
| `templates/conversion-tracking.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-conversion-tracking.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
