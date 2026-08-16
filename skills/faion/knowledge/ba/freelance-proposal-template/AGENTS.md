# Freelance Proposal Template

## Summary

**One-sentence:** Solo / freelance proposal skeleton: scope envelope, assumptions, exclusions, payment milestones, change-request rate, anti-scope-creep language.

**One-paragraph:** Freelance Proposal Template pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Solopreneur / freelance BA bidding outsource work.
- Switching from W-2 to 1099 / FOP and needing reusable artefacts.
- First-time direct-to-client engagement (post-agency).
- Productised consultancy where every proposal is a near-clone.

## Applies If (ALL must hold)

- Solo or small-team BA / consultant pitching paid work to a new client.
- Engagement is fixed-bid or capped-T&M (not pure hourly).
- Client requires a written proposal before signing an MSA / SoW.
- Engagement value exceeds the threshold at which scope creep matters (≥ 5k USD).

## Skip If (ANY kills it)

- Pure hourly engagement with open scope.
- Internal-team work — no proposal needed.
- Engagement value too small to justify a structured proposal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Discovery call notes | markdown | Pre-sales calls |
| Hourly rate card | yaml | Your engagement model |
| Reference engagements | markdown | Portfolio / case studies |
| MSA template | pdf | Legal review |

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
| `draft-freelance-proposal-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelance-proposal-template.md.j2` | Markdown spec skeleton with required sections + placeholders |
| `templates/freelance-proposal-template.md` | Markdown spec skeleton with required sections + placeholders Generated from `templates/freelance-proposal-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/freelance-proposal-template.schema.json` | JSON Schema for the structured spec output |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-proposal-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

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

### `templates/freelance-proposal-template.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Freelance Proposal Template engagement",
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
