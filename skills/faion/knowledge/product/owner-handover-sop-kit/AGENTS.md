# Owner Handover SOP Kit

## Summary

**One-sentence:** Generates a structured SOP kit (credentials, runbooks, financials, contracts, escalation) so an agency or product line can be handed to a new owner; output is a handover spec with completeness score.

**One-paragraph:** Generates a structured SOP kit (credentials, runbooks, financials, contracts, escalation) so an agency or product line can be handed to a new owner; output is a handover spec with completeness score. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Founder preparing acquisition: buyer needs explicit handover bundle pre-LOI.
- Founder graceful exit: no buyer, still want to shut down without burning customers.
- First-hire onboarding to COO level: SOP kit reduces founder transfer time.
- Continuity insurance: if founder is incapacitated, second-in-line can run ops.

## Applies If (ALL must hold)

- Business has active revenue + ≥3 critical SaaS / vendor accounts.
- Founder holds admin / billing on critical accounts.
- There is a plausible recipient (buyer, hire, second-in-line) in the next 12 months.
- Documentation can be written and stored in a single navigable location (Notion / GDrive / git).

## Skip If (ANY kills it)

- Pre-revenue stage — nothing to hand over.
- Solo product with no customers or vendors — overhead exceeds value.
- Recipient not yet identifiable — capture credentials only, full SOP can wait.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Account inventory | credentials manager export | founder's vault |
| Runbook list | Notion / GDrive index of ops runbooks | ops |
| Financial snapshot | P&L + AR/AP last 12 months | accounting |
| Contract list | active customer + vendor contracts | legal / drive |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-owner-handover-sop-kit` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-owner-handover-sop-kit.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[founder-dependency-audit]]
- [[post-launch-72h-watch-runbook]]
- [[portfolio-sunset-decision-frame]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
