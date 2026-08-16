# Ads Analytics Setup

## Summary

**One-sentence:** Three-layer (Collect / Analyze / Attribute) analytics config: GA4 property + event-spec + UTM standard + Consent Mode v2 + BigQuery link + ad-platform integrations.

**One-paragraph:** GA4 + ad-platform pixels are now table stakes; the failure mode is sequencing — pixel before event-spec, dataLayer before UTM standard, ad-link before consent-mode. This methodology specs the full three-layer setup: Collect (GA4 property + Consent Mode v2 + dataLayer), Analyze (custom events + conversions + funnels), Attribute (UTM standard + BigQuery link + ad-platform pixels). Output: analytics config spec + dataLayer schema + UTM convention doc + verification checklist.

**Ефективно для:**

- New launch: GA4 + Consent Mode v2 + dataLayer + BigQuery link from day one.
- UA → GA4 migration з event mapping без втрати historical comparability.
- Multi-channel rebuild: UTM standard + dataLayer schema + ad-platform integrations.
- Compliance refit: GDPR / CCPA / server-side tagging.

## Applies If (ALL must hold)

- New site/app launch needing GA4 + ad pixels from day one.
- UA → GA4 migration (UA sunset 2023) requiring event mapping.
- Multi-channel attribution rebuild (UTM standard + dataLayer schema).
- Compliance refit (Consent Mode v2, GDPR/CCPA, server-side tagging).

## Skip If (ANY kills it)

- Site lifespan < 90 days — analytics overhead exceeds learning value.
- Privacy-first audience (no consent expected) — server-side only stack, different methodology.
- B2B with named-account ABM-only strategy — pixel analytics not the lever.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-analytics-setup` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton with 5-line header |
| `templates/output.json` | JSON sidecar with __faion_header__ |
| `templates/_smoke-test.yaml` | Minimum viable filled config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/event-tracking-plan.md.j2` | legacy template for ads-analytics-setup — event-tracking-plan |
| `templates/event-tracking-plan.md` | legacy template for ads-analytics-setup — event-tracking-plan Generated from `templates/event-tracking-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/utm-conventions.md.j2` | legacy template for ads-analytics-setup — utm-conventions |
| `templates/utm-conventions.md` | legacy template for ads-analytics-setup — utm-conventions Generated from `templates/utm-conventions.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-analytics-setup.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.yaml`

```yaml
artefact_id: <SLUG-YYYY-Qx>
template_version: 1.1.0
owner: <named-owner@example>
platform: <ga4|google-ads|meta|linkedin>
settings:
  # platform-specific keys; reference 02-output-contract.xml for schema
  example_key: example_value
verification:
  verified_at: <ISO-8601>
  verified_by: <named>
  evidence: <DebugView screenshot path | CRM cross-check report path>
```

### `templates/output.json`

```json
{
  "artefact_id": "<SLUG-YYYY-Qx>",
  "template_version": "1.1.0",
  "owner": "<named-owner@example>",
  "platform": "<ga4|google-ads|meta|linkedin>",
  "settings": {
    "example_key": "example_value"
  },
  "verification": {
    "verified_at": "<ISO-8601>",
    "verified_by": "<named>",
    "evidence": "<DebugView screenshot path>"
  }
}
```

### `templates/_smoke-test.yaml`

```yaml
artefact_id: ads-config-2026-Q2
template_version: 1.1.0
owner: analytics-eng@faion.net
platform: ga4+google-ads+meta
settings:
  consent_mode_v2: true
  bq_link: true
  attribution_window_days: 30
  event_id_dedup: true
  utm_convention: lowercase-controlled-vocab
verification:
  verified_at: 2026-05-22T14:00Z
  verified_by: analytics-eng@faion.net
  evidence: evidence/ads-config-2026-Q2/debug.png
```
