# Solo Change Order Mini Contract

## Summary

**One-sentence:** A one-page change-order email template that converts "just one more thing" into a signed, dated, priced amendment to the existing engagement — sent and signed within 60 minutes, legally sufficient under E-SIGN / eIDAS / UK ECA.

**One-paragraph:** Scope management methodologies define the conversation; ops-legal-basics covers the master agreement. Neither bridges "we are on day 14 of a fixed-bid project and the client just asked for a feature." The freelancer needs a one-page pack: subject anchoring to master SOW + three-paragraph body + four explicit deltas (scope, price, schedule, payment terms) + a "reply YES to authorize" close. Output is a typed `ChangeOrder` record that references master_sow_id and stores the immutable artefact + invoice line link. Anchored to the technical freelancer's scope-change conversation pattern.

**Ефективно для:**

- Scope-change conversation when client says "just one more thing" (sub-$10k).
- Within-hour amendment to an existing signed master SOW.
- Audit trail linking invoice line → change order → master SOW.
- Capping verbal-authorisation risk at 8 hours.

## Applies If (ALL must hold)

- Existing signed master agreement / SOW covers the engagement.
- New ask is sub-$10k (or sub-MSA threshold).
- Jurisdiction enforces e-signature ("reply YES") for modifications (US E-SIGN, EU eIDAS, UK ECA).
- Client reachable by email or chat.

## Skip If (ANY kills it)

- No master agreement in place — write a fresh SOW, not a change order.
- Ask large enough to renegotiate retainer / rate — go full SOW.
- Enterprise procurement requiring PO + paper signature — follow their process.
- Jurisdiction lacks reliable e-signature enforceability — escalate to real signature.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Master SOW (signed, dated, identifier) | PDF / signed doc | client |
| Rate card / hourly figure | YAML | freelancer |
| Email or chat thread | per channel | client |
| Invoice numbering scheme | per finance | freelancer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vendor-margin-defense-checklist]] | Bleed alert triggers CR via this template. |
| [[solo-late-fee-and-pause-clause-template]] | Sibling — payment-terms clause referenced here. |
| [[proposal-red-team-checklist]] | Change-control clause reviewed in red-team pause-point. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: anchor to MSA, four explicit deltas, reply-YES acceptance, verbal cap 8h, immutable storage | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `ChangeOrder` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: unanchored, ambiguous deltas, weak acceptance, parallel work without signature, lost artefact, hand-off chain | ~900 |
| `content/04-procedure.xml` | medium | 5-step: draft email → send → capture YES → store immutable → invoice with reference | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: master_sow? sub-threshold? jurisdiction? signature? → send / escalate / pause | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-co-email` | sonnet | Diplomatic + concrete numbers. |
| `extract-deltas` | haiku | Mechanical fill from scope diff. |
| `capture-acceptance` | haiku | Verbatim transcription. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | ChangeOrder email skeleton with subject + body + 4-delta table + reply-YES |
| `templates/skeleton.md` | ChangeOrder email skeleton with subject + body + 4-delta table + reply-YES Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `ChangeOrder` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-change-order-mini-contract.py` | Validate `ChangeOrder`: master_sow_ref + 4 deltas + reply-YES + invoice link | Pre-merge |
| `scripts/staleness-check.py` | Flag records past archive retention | Weekly cron |

## Related

- [[vendor-margin-defense-checklist]]
- [[solo-late-fee-and-pause-clause-template]]
- [[proposal-red-team-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps master-SOW presence, threshold size, jurisdiction enforceability, and signature capture to send / escalate / pause. Every leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/header.yaml`

```yaml
owner:
  role: ""
  person: ""
last_reviewed: ""
version: ""
```

### `templates/_smoke-test.json`

```json
{
  "co_id": "CO-002",
  "master_sow": {
    "name": "Acme Web Portal SOW",
    "date": "2026-04-12",
    "identifier": "acme-2026-q2-001"
  },
  "header": {
    "owner": {
      "role": "freelancer",
      "person": "alex"
    },
    "last_reviewed": "2026-05-10",
    "version": "1.0"
  },
  "scope_delta": "Add CSV export endpoint + UI button on /clients page.",
  "price_delta": "+$1,200 flat (fixed)",
  "schedule_delta": "New end date 2026-05-29 (+5 business days)",
  "payment_terms_delta": "Net-14, same as SOW",
  "acceptance": {
    "reply_yes_captured": true,
    "captured_at": "2026-05-10T14:00:00Z",
    "channel": "email"
  },
  "artefact": {
    "immutable_link": "drive://co/CO-002.pdf",
    "invoice_line_ref": "INV-2026-05-12-L3"
  },
  "verbal_authorization_hours": 0
}
```
