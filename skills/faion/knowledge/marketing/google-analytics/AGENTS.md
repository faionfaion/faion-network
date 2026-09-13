# Google Analytics 4 Setup

## Summary

**One-sentence:** Generates GA4 property config: data streams, enhanced measurement, custom dimensions, conversion events, BigQuery export, sampling guards.

**One-paragraph:** Generates GA4 property config: data streams, enhanced measurement, custom dimensions, conversion events, BigQuery export, sampling guards. Use it when новий проект потребує ga4 з нуля (ua вже sunset). The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Новий проект потребує GA4 з нуля (UA вже sunset).
- Потрібен BigQuery export для непідлеглих sampling-у звітів.
- Consent mode v2 обов'язковий для EU traffic.
- Server-side GTM доступний для resilient conversion tracking.

## Applies If (ALL must hold)

- A GA4 property is being created or reconfigured for a site the team controls, with admin access to the property and its data streams.
- A Google Cloud project is available to link the BigQuery export before the first production hit.
- The property's event list and the parameters reports will read are known, so custom dimensions can be registered before the first send.
- Consent regions, checkout and authentication domains, and office IP ranges are known for the consent, referral and internal-traffic settings.
- Where server-side events are planned, the server can read the browser's `_ga` cookie and keep the api_secret out of the client.

## Skip If (ANY kills it)

- No GA4 property is being created or reconfigured: for event taxonomy and tags use conversion-tracking; for reading numbers use a reporting methodology.
- The property has been live for months and the question is retroactive history: BigQuery does not backfill and registration is not retroactive; the fix is forward-only.
- The site uses only a third-party analytics vendor with no GA4 and no Google Ads: nothing here applies.
- The team cannot obtain admin access to the property: the settings this config records cannot be changed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Property and stream ids | numeric property id; `G-` measurement id per stream | GA4 admin, property settings and data streams |
| App architecture | whether each web stream is a SPA that pushes its own page_view | frontend team |
| Parameters and user properties to report | name, parameter, scope (event / user / item), kind | analytics requirements |
| Event list and conversions | exact event names; which are conversions and how they count | tracking plan (events.yml) |
| Order identifier | the order id available on the confirmation page | commerce backend |
| Consent regions and CMP | markets requiring consent; CMP capable of consent update calls | legal / CMP configuration |
| BigQuery project and location | project id, dataset location | Google Cloud admin |
| IP ranges, checkout and auth domains, journey domains | CIDR list; payment and SSO hosts; every domain in the funnel | IT, payments, product |
| `templates/gtag-snippet.html`, `templates/mp_track.py`, `templates/ga4_pull.py` | snippet with consent defaults, Measurement Protocol helper, Data API pull | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: property vs measurement id, enhanced measurement, custom-dimension cap, key events by name, purchase transaction_id dedup, consent mode v2 before config, BigQuery export and retention, Measurement Protocol client_id, internal traffic and referral exclusions | 2500 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the property config: numeric property id and G- streams with one page_view source, enhanced measurement toggles, registered custom dimensions with limits and used counts, key events by exact name, purchase with transaction_id, Consent Mode v2, BigQuery export with retention and sampling guard, Measurement Protocol on the _ga client_id, internal filter, unwanted referrals and cross-domain; valid and invalid configs; 8 forbidden patterns | ~5300 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 9 steps: create the property and record both ids, link BigQuery and set retention before launch, one page_view source, register dimensions within limits, snippet with consent defaults first, purchase event, key events by exact name, Measurement Protocol with the browser client_id, traffic filters and validate | ~1900 |
| `content/05-examples.xml` | recommended | Complete config for a SaaS SPA (property 123456789, G- stream with manual page_view, four registered dimensions, three key events, purchase on order id, advanced consent for EU/GB/CH, BigQuery linked before launch, PayPal, Stripe and auth excluded as referrers) with a note per value, plus the usual setup and what the validator prints | ~2500 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-google-analytics.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/google-analytics.config.yaml` | YAML config skeleton matching the contract: ids, streams, enhanced measurement, custom dimensions, key events, purchase, consent, BigQuery, Measurement Protocol, traffic filters |
| `templates/google-analytics.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-analytics.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
