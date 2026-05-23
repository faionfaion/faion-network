# STRIDE Threat Model Template

## Summary

**One-sentence:** Full STRIDE threat-model template: per-component data-flow diagram, threats per category, mitigation owner, residual-risk record — versioned + owner-signed.

**One-paragraph:** Full STRIDE threat-model template: per-component data-flow diagram, threats per category, mitigation owner, residual-risk record — versioned + owner-signed. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-stride-threat-model-template.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Security-by-design audit для нового service з нестандартним trust boundary.
- Compliance gate (SOC 2, ISO 27001, PCI-DSS) потребує threat-model artefact на review.
- Multi-team service-edge де STRIDE Lite не покриває cross-boundary threats.
- Архітектор веде full TM workshop і потрібен deterministic output shape.

## Applies If (ALL must hold)

- New or materially-changed service with data flow defined
- Multi-stakeholder review (security + arch + product) scheduled for the TM workshop
- Mitigation owners identifiable per threat row
- Versioned-artefact store exists (repo / wiki) for the TM output

## Skip If (ANY kills it)

- STRIDE Lite checklist sufficient — full template overkill
- Trust boundary unchanged from a previously-modeled service — re-use prior TM
- Team has no security-trained reviewer — output won't be acted on without one
- No mitigation budget — TM that surfaces 30 threats with no owner is shelfware

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | medium | One worked example end-to-end (filled artefact) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-stride-threat-model-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stride-threat-model-template.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[stride-lite-checklist-for-architects]]
- [[threat-model-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
