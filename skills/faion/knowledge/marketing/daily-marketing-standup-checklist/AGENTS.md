# Daily Marketing Standup Checklist

## Summary

**One-sentence:** Produces a 15-minute morning checklist artefact: content queue status, social pulse (3 channels), pipeline anomalies, today's one-thing focus — written, dated, signed by owner.

**One-paragraph:** Codifies the recurring 15-minute morning marketing routine for in-house marketers and solo growth folks. Reduces tool-sprawl pain by forcing one consolidated screen per day. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (dated, owner-signed) that downstream tasks can consume without re-deriving the rationale.

**Ефективно для:** in-house marketers running content + social + paid in parallel; solo founders doing growth alongside dev; agencies handing off a daily report to clients.

## Applies If (ALL must hold)

- Marketer or founder runs ≥2 channels (e.g., LinkedIn + newsletter + paid)
- There is no shared daily ritual today (slack-driven chaos or silent drift)
- An owner exists and can sign off in 15 minutes
- Yesterday's data is queryable (analytics, ad dashboards, inbox)

## Skip If (ANY kills it)

- Solo marketer with one channel only — overhead exceeds signal
- Team already runs a tighter daily standup with same scope
- No analytics access — checklist would fail at step 1

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Yesterday's analytics screenshot | PNG or CSV | GA4 / Plausible / Posthog |
| Content queue status | Notion / Trello / Sheets | team tool |
| Paid campaign dashboard | Meta / Google / LinkedIn Ads | ads vendor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[content-marketing]]` | Content queue conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Fill standup template | sonnet | Data pull + summarisation. |
| Diagnose anomaly hypothesis | opus | Cross-channel reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/standup.md.tmpl` | Daily standup artefact skeleton with all sections. |
| `templates/anomaly-table.md.tmpl` | Anomaly table with metric, delta, hypothesis, owner columns. |
| `templates/_smoke-test.md` | Example filled standup. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-daily-marketing-standup-checklist.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/marketing/`
- `[[content-marketing]]`
- `[[growth-marketing]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether daily-marketing-standup-checklist applies: root question — "Does the marketer run ≥2 channels today?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
