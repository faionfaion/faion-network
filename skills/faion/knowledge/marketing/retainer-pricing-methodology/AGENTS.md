# Retainer Pricing Methodology

## Summary

**One-sentence:** Retainer Pricing Methodology — pinned method for the technical freelancer: fixed shape + named owner + evidence anchors + outcome review, so inbound-to-signed-retainer in one client cycle stops being folklore and starts being a reviewable operating tool.

**One-paragraph:** In growth and marketing, the technical freelancer runs inbound-to-signed-retainer in one client cycle on a recurring cadence — but the corpus only covers the upstream concepts, not the artefact that closes the loop. No coverage of retainer shapes (block-of-hours vs outcome-based vs availability), how to price them above-hourly-equivalent, and how to phase out hourly mid-relationship. Pro tier ops content covers contractor MANAGEMENT (hiring contractors) — not BEING the contractor selling time. `retainer-pricing-methodology` pins the artefact: a fixed shape, named owner, evidence anchors, and a published review cadence. It is loaded when the technical freelancer starts the block named in the trigger and produces a committed artefact reviewed against outcomes at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored method committed to the team's knowledge space.

**Ефективно для:**

- Переходу з hourly на retainer без втрати маржі.
- Розрахунку retainer rate ≥1.3× hourly-equivalent.
- Документації трьох форм retainer: block-of-hours, outcome-based, availability.
- Outcome-review: чи retainer тримається ≥6 місяців без переговорів.

## Applies If (ALL must hold)

- The client has recurring work in the same scope for at least 3 months ahead (maintenance, an ongoing feature stream, on-call availability), not a single bounded project.
- The freelancer's current hourly rate and, for an hourly client being converted, the last 3 months of billed hours and spend are known.
- The client's request pattern is clear enough to pick one shape: block-of-hours, outcome-based or availability.
- The freelancer can list every active retainer with its expected or maximum monthly hours next to available billable hours.
- The client will accept advance invoicing, a minimum term of 3 months and 30 days notice.

## Skip If (ANY kills it)

- The engagement is a single bounded project with no recurrence: price it fixed-scope and revisit when a second engagement appears.
- The client insists on month-to-month, cancel any time, billed in arrears; that is hourly billing with extra steps, not a retainer.
- Adding this retainer at its maximum load would push committed hours over available hours and no other retainer can end or be re-scoped.
- The client will only sign below 1.3x the hourly equivalent and offers no concession (12-month minimum term or full-term prepayment).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Client request pattern | last 3 months of tickets, deliverables or on-call asks, grouped by type | ticket system, email, invoices |
| Hourly history | billed hours and spend per month for the last 3 months, when converting an hourly client | invoicing tool |
| Rate card | current hourly rate and currency | freelancer's rate card |
| Capacity ledger | available billable hours per month; every active retainer with expected hours (maximum load for availability) | freelancer's planning sheet |
| Contract terms | acceptable minimum term, notice period, billing day and payment terms | client procurement / freelancer's standard terms |
| `templates/retainer-pricing-methodology.md.j2`, `templates/retainer-pricing-methodology.json` | spec skeleton; the contract schema | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream — the discovery-fed proposal that lists retainer as an option. |
| `pro/marketing/rate-raise-conversation-script` | Sibling — the live conversation when raising a retainer rate. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: retainer shape named, 1.3x hourly-equivalent floor, scope inclusions/exclusions and turnaround, term/notice/price review, invoiced in advance, hourly phase-out plan, capacity not oversold, 6-month outcome review | ~2450 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the retainer spec: one named shape with its terms (rollover and overage, deliverables, response time and max load, or hybrid invoicing and dispute clause), price as hours x rate x multiple at or above 1.3 or a named concession, inclusions, exclusions and turnaround, 3-month term, 30 days notice and 12-month price review, advance billing, hourly phase-out with 3-month average and cutover, capacity ledger within available hours, 6-month outcome review with the two-period actions; valid and invalid specs; 8 forbidden patterns | 4850 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~950 |
| `content/04-procedure.xml` | essential | 8 steps: confirm recurring scope and pick one shape, price at the 1.3x floor, write inclusions, exclusions and turnaround, set term, notice and price review, bill in advance, plan the hourly cutover, check the capacity ledger, schedule the 6-month review and validate | 1650 |
| `content/05-examples.xml` | recommended | Complete spec converting an hourly Django maintenance client (40-hour block at 120 EUR priced 6,240 EUR, one-period rollover, 2-business-day turnaround, 6-month term, cutover on the start date, 100 of 120 hours committed, review at 6 months) with a note per value, plus an availability retainer sold below the hourly rate and what the validator prints | 1650 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/retainer-pricing-methodology.md.j2` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/retainer-pricing-methodology.md` | Markdown skeleton (5-line header) for the artefact body. Generated from `templates/retainer-pricing-methodology.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/retainer-pricing-methodology.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retainer-pricing-methodology.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/`
- [[proposal-from-discovery-template]]
- [[rate-raise-conversation-script]]
- [[rate-increase-notice-template]]
- external: see Christensen, Gawande, Kahneman, Allspaw and the empirical sources cited in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.
