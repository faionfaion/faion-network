# AI Feedback Triage Protocol

## Summary

**One-sentence:** Routes inbound AI-product feedback (hallucination / refusal / wrong-tool / out-of-scope / cost-spike) into named lanes (ML eng vs product vs support) via 5-step explicit-signal protocol with owners + exit criteria.

**One-paragraph:** Routes inbound AI-product feedback (hallucination / refusal / wrong-tool / out-of-scope / cost-spike) into named lanes (ML eng vs product vs support) via 5-step explicit-signal protocol with owners + exit criteria. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Класифікація AI-фідбеку по 5 лейнах (hallucination / refusal / wrong-tool / out-of-scope / cost-spike).
- Маршрутизація: ML-команда vs product vs support — за explicit signals.
- AI-фічі з >5 фідбеків/тиждень — generic триаж занадто грубий.
- Постмортем-вхід: incidents → triage record → golden-set candidates.

## Applies If (ALL must hold)

- AI feature has user-visible feedback channel (in-app, email, support tickets).
- Feedback volume ≥5/week sustained for 4+ weeks.
- Distinct lanes exist: ML eng vs product vs support.
- Postmortem flow exists that can ingest triage records.

## Skip If (ANY kills it)

- Feedback volume <5/week — overhead exceeds value.
- No AI-specific failure surface — generic helpdesk triage suffices.
- Existing triage workflow already named-owner + exit-criterion compliant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feedback channel data | JSON / CSV / API export | Helpdesk / app telemetry |
| Lane definition | YAML / Markdown | Team — ML eng + product |
| Postmortem template | Markdown | SRE / ML eng team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-feedback-triage-protocol` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step.md` | Markdown playbook skeleton — named steps with owner + input + exit criterion + output location |
| `templates/step-checklist.md` | Per-step go/no-go checklist for operator runtime |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feedback-triage-protocol.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[ai-incident-triage-matrix]]
- [[golden-set-curation-and-maintenance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
