# Feedback Management

## Summary

**One-sentence:** Pipeline turning scattered inbound feedback (support, NPS, app-store, sales, social) into ranked product themes via fixed taxonomy, segment-weighted scoring, and close-loop tracking.

**One-paragraph:** A canonical feedback store + fixed taxonomy + segment-weighted theme ranking + close-loop tracking. Items flow from multi-channel sources into a normalized record; an agent classifies and clusters; monthly review surfaces top themes with verbatim citations; PM dispositions each (will-do / under-consideration / won't-do) and triggers close-loop comms.

**Ефективно для:**

- Inbound volume >20 items/день із кількох каналів.
- Recurring monthly review із потребою top-N themes + verbatim citations.
- Pre-roadmap або pre-OKR session із quantified themes за 90 днів.
- Solopreneur agency з кількома продуктами і обмеженим людським triage.

## Applies If (ALL must hold)

- Inbound feedback volume exceeds human triage capacity (>20 items/day across channels).
- Multiple disconnected sources (support tickets, app store, in-app widget, social, sales) need a single canonical store.
- Recurring monthly review cycle must surface patterns, rank by segment and revenue, and link to backlog items.
- Close-loop emails to specific requesters are repetitive but high-leverage.
- Pre-roadmap sessions where PM needs 'top 10 themes from last 90 days with verbatim citations'.

## Skip If (ANY kills it)

- Pre-PMF with <5 feedback items/week — direct human reading is faster.
- High-stakes strategic decisions (pivot, kill) where verbatim nuance dominates count.
- Compliance-bound feedback (HIPAA / GDPR DSAR text) where LLM ingestion needs DPA review.
- Sentiment-only loop with no commitment to act — automation amplifies noise without close-loop.
- Single-channel product where the channel tool's native AI already handles categorization.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel inventory | list of sources + auth | support / marketing / sales |
| Taxonomy v1 | YAML <=30 leaves | product / research |
| Customer attributes | table {user_id, segment, plan_tier, ARR, churn_risk} | CRM / billing |
| Canonical store | Postgres / SQLite / Airtable | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides segment/retention attributes used for weighting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology: canonical store, fixed taxonomy, segment-weighted ranking, close-loop, monthly review, daily triage SLA, volume threshold before escalation | 1300 |
| `content/01-feedback-pipeline.xml` | medium | Source inventory, categorization taxonomy, 6-step pipeline, agent workflow (triage / aggregator / close-loop) | 1100 |
| `content/02-feedback-patterns.xml` | medium | Monthly review example, app-store response strategy, embedding dedup, LLM-drift audit, PII gotchas, human-in-loop checkpoints | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for feedback-record + monthly-theme-report | 850 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: noise-overload, vote-only ranking, lost close-loop, taxonomy drift, anecdote-driven escalation, inbox rot | 1050 |
| `content/04-procedure.xml` | essential | 6-step procedure: ingest -> normalize -> classify -> deduplicate -> rank -> dispose | 950 |
| `content/05-examples.xml` | medium | Worked monthly review producing top-10 themes + dispositions | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on volume + multi-channel + commitment | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage` | haiku | Bulk taxonomy classification at high volume. |
| `theme-synthesis` | sonnet | Cross-source clustering with verbatim citations. |
| `close-loop-email-draft` | haiku | Templated reply per requester. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feedback-log.md.j2` | Monthly feedback-log skeleton with theme rows + citations. |
| `templates/feedback-log.md` | Monthly feedback-log skeleton with theme rows + citations. Generated from `templates/feedback-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/response-templates.md.j2` | Close-loop email templates per disposition. |
| `templates/response-templates.md` | Close-loop email templates per disposition. Generated from `templates/response-templates.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feedback-management.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |
| `scripts/triage.py` | Triage one feedback item via LLM with strict JSON-schema output; normalises text, computes the dedup hash, validates topic against the taxonomy | Per item, at the classify step; PII must be stripped first |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[product-analytics]]
- [[continuous-discovery-habits]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
