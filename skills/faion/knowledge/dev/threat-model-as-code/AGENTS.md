# Threat Model as Code

## Summary

**One-sentence:** Threat model encoded as a versioned YAML/Pytm/Threagile artefact in the repo: diff-able, CI-checkable, regenerated per architecture change — instead of a stale Confluence page.

**One-paragraph:** Threat model encoded as a versioned YAML/Pytm/Threagile artefact in the repo: diff-able, CI-checkable, regenerated per architecture change — instead of a stale Confluence page. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-threat-model-as-code.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Compliance-grade delivery (FinTech / HIPAA / PCI) потребує auditable TM artefact.
- Architecture changes часто (multiple per quarter) — Confluence TM завжди stale.
- Threat-model має consumer (compliance auditor, security review) що reads diffs.
- Team має заклад до as-code culture (infra-as-code, policy-as-code).

## Applies If (ALL must hold)

- Compliance context (FinTech / HIPAA / PCI / FedRAMP) requires auditable TM
- Architecture changes ≥1× per quarter — code-based TM stays in sync
- Repo CI can run a TM-validator (pytm, threagile, custom YAML schema)
- Existing as-code culture (infra-as-code, policy-as-code) — fits the patterns

## Skip If (ANY kills it)

- No compliance pressure and one-shot TM — Confluence + diagram fine
- Architecture is static — TM diff value is low; manual artefact is fine
- Team has no as-code muscle — adoption stalls
- No TM-consumer (no auditor, no security review) — TM-as-code becomes shelfware

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
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-threat-model-as-code` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | JSON instance matching the output contract |
| `templates/config.yaml` | YAML config skeleton matching the output contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threat-model-as-code.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[stride-threat-model-template]]
- [[trust-boundary-diff-helper]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
