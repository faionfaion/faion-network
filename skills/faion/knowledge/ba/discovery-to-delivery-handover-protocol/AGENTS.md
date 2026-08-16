# Discovery to Delivery Handover Protocol

## Summary

**One-sentence:** Formal handover protocol from pre-sales discovery BA to delivery BA: artefact bundle, walkthrough script, signed acknowledgement, and post-handover hot-line.

**One-paragraph:** Discovery to Delivery Handover Protocol pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Fixed-bid agency BA handing a sold engagement to a delivery squad.
- M&A / merger-induced personnel changes between contracts.
- Multi-region delivery model (discovery on-site, delivery offshore).
- Regulated industries (HealthTech, FinTech) where assumptions carry compliance risk.

## Applies If (ALL must hold)

- Pre-sales BA is different from delivery BA on this engagement.
- Engagement is fixed-price or fixed-scope where assumptions become contractual.
- Discovery surfaced material assumptions that must survive contact with the dev team.
- Project kickoff is within 30 days of discovery sign-off.

## Skip If (ANY kills it)

- Same person did discovery and runs delivery — handover is internal-memory only.
- Time-and-materials engagement where assumptions are renegotiable continuously.
- Discovery findings are trivial (single-feature engagement).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Discovery report | markdown / pdf | Pre-sales repo |
| Signed SoW | pdf | Legal / contracts |
| Assumption register | csv | Discovery output |
| Risk register | csv | Discovery output |
| Stakeholder map | yaml | Discovery output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-discovery-to-delivery-handover-protocol` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-to-delivery-handover-protocol.md.j2` | Markdown spec skeleton with required sections + placeholders |
| `templates/discovery-to-delivery-handover-protocol.md` | Markdown spec skeleton with required sections + placeholders Generated from `templates/discovery-to-delivery-handover-protocol.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/discovery-to-delivery-handover-protocol.schema.json` | JSON Schema for the structured spec output |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-discovery-to-delivery-handover-protocol.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/discovery-to-delivery-handover-protocol.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Discovery to Delivery Handover Protocol engagement",
  "rules_applied": [
    "REPLACE-WITH-RULE-ID"
  ],
  "evidence": [
    {
      "rule_id": "REPLACE-WITH-RULE-ID",
      "citation": "REPLACE-WITH-VERIFIABLE-CITATION",
      "source_type": "url"
    }
  ],
  "output_payload": {
    "status": "draft"
  },
  "consumer": "REPLACE-WITH-NAMED-CONSUMER",
  "owner": "REPLACE-WITH-NAMED-OWNER",
  "last_touched": "2026-05-23T10:00:00Z"
}
```
