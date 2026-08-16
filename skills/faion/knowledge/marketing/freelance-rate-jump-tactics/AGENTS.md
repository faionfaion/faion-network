# Freelance Rate Jump Tactics

## Summary

**One-sentence:** Defensibly raise rates 30-50% inside a niche pivot — credential proof-building, anchor recalibration, case-study sequencing, graduated rollout split between existing clients + new leads.

**One-paragraph:** After a niche pivot, freelancers often leave rate increases on the table because the existing client list anchors them to old rates. This methodology defines the 4-tactic rate-jump: credential proof-building (3+ named outputs in the new niche); anchor recalibration (research the new niche's median + p75); case-study sequencing (3 case studies showing measurable outcome); graduated rollout (existing clients on 90-day notice; new leads at new rate immediately). Core rules: every rate target cites the new niche's market band; existing clients get written notice ≥60 days; case studies underlying the jump are published; no retroactive billing changes.

**Ефективно для:**

- Niche pivot complete — 3+ case studies in new niche.
- Solo consultant — annual rate review with directional jump.
- Agency owner — repositioning into higher-leverage offering.
- Freelancer with 5+ existing clients on legacy rates.

## Applies If (ALL must hold)

- Niche pivot delivered for ≥3 customers in the new niche.
- Existing client base on legacy rate &gt; 6 months.
- Authority to set rates unilaterally with new leads.
- Capacity to absorb potential client churn from the jump.

## Skip If (ANY kills it)

- &lt;3 case studies in new niche — credential proof-building incomplete.
- Single anchor client = 80%+ of revenue (cashflow risk).
- Niche pivot still in motion — wait until proof points exist.
- Existing contracts with locked rates for &gt;12 months.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| New niche market-rate research | report | Upwork / LinkedIn / network |
| Case studies in new niche (≥3) | docs | own portfolio |
| Existing client list with current rates | CSV | CRM |
| Cashflow runway projection | spreadsheet | own ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[freelancer-niche-positioning]] | Upstream — niche must be positioned first. |
| [[freelance-pilot-pricing]] | Pilots in the new niche produced the proof. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: market-band-citation, 60-day-notice-existing-clients, three-case-studies-required, graduated-rollout, no-retroactive-billing | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `research-market-band` | sonnet | Synthesis across sources. |
| `draft-notice` | sonnet | Light judgment on tone. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-jump-spec.json` | JSON example of rate-jump spec |
| `templates/client-notice.md.j2` | Markdown template for existing-client rate-change notice |
| `templates/client-notice.md` | Markdown template for existing-client rate-change notice Generated from `templates/client-notice.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-rate-jump-tactics.py` | Validate one spec JSON against the schema | After draft, before publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelancer-niche-positioning]]
- [[freelance-pilot-pricing]]
- [[fixed-vs-hourly-decision-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rate-jump-spec.json`

```json
{
  "jump_id": "rj-2026q2-saas-onboarding",
  "niche": "B2B SaaS onboarding rebuild",
  "current_rate": 100,
  "target_rate": 150,
  "market_band": {
    "median": 140,
    "p75": 175,
    "sources": [
      "upwork-q1-2026",
      "codementor-rate-card",
      "peer-survey-2026"
    ]
  },
  "case_studies": [
    {
      "customer": "Acme",
      "outcome": "+22% activation",
      "url": "https://example/acme"
    },
    {
      "customer": "Beta",
      "outcome": "-40% time-to-value",
      "url": "https://example/beta"
    },
    {
      "customer": "Gamma",
      "outcome": "+15 NPS",
      "url": "https://example/gamma"
    }
  ],
  "existing_client_notice": {
    "notice_days": 60,
    "wip_billing": "old-rate-until-complete"
  },
  "rollout_plan": {
    "new_leads_at": "2026-06-01",
    "existing_clients_at": "2026-08-01"
  },
  "owner": "@ruslan"
}
```
