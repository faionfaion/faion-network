# NDA / MSA Obligation Extractor

## Summary

**One-sentence:** Extracts obligations from NDAs and MSAs into a structured register: obligation, owner, trigger, deadline, evidence pointer, audit-ready.

**One-paragraph:** NDA / MSA Obligation Extractor pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Long-term outsource engagement with a multi-page MSA.
- M&A diligence work where every executed agreement carries obligations.
- Regulated client (defence, health, finance) with non-disclosure tripwires.
- Multi-vendor engagement where obligations differ per vendor.

## Applies If (ALL must hold)

- Engagement is governed by an NDA + MSA bundle.
- Contract length exceeds 5 pages with at least 10 obligations.
- Multiple team members must comply (not just legal).
- There is a recurring pattern of 'we did not realise we owed X' on prior engagements.

## Skip If (ANY kills it)

- Contract is a single-page click-through with no operational obligations.
- All obligations are handled by client legal team independently of BA.
- Engagement value too small to justify extraction overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signed NDA / MSA / SoW | pdf | Client / legal |
| Engagement role map | yaml | Stakeholder register |
| Obligation register template | yaml / csv | BA toolkit |
| Calendar / reminder system | url | Team ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-nda-msa-obligation-extractor` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nda-msa-obligation-extractor.md` | Markdown report skeleton with required sections + placeholders |
| `templates/nda-msa-obligation-extractor.schema.json` | JSON Schema for the structured report output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nda-msa-obligation-extractor.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
