# Stack Mandate Trade-off Frame

## Summary

**One-sentence:** ADR framing for an outsource senior dev writing inside a client-mandated stack: name the mandate, frame options within it, attach costed mitigations instead of stack-replacement language.

**One-paragraph:** ADR framing for an outsource senior dev writing inside a client-mandated stack: name the mandate, frame options within it, attach costed mitigations instead of stack-replacement language. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-stack-mandate-tradeoff-frame.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- P4 outsource senior dev пише ADR у client-mandated stack (EKS+Java21+PG16 чи аналогічно).
- Trade-off реальний (latency, cost, complexity), але stack-replacement не на столі.
- Client architect read ADR і політична tone matters більше за технічну зміну.
- Costed mitigation paths існують (більший instance, support tier) у procurement channel клієнта.

## Applies If (ALL must hold)

- Outsource engagement with explicit stack mandate (ENG standard, RFP requirement)
- Real trade-off in chosen stack worth documenting in an ADR
- Costed mitigation exists (vendor support, larger instance, infrastructure addition)
- Client architect reviews ADRs and decides procurement

## Skip If (ANY kills it)

- Greenfield project with no stack mandate — write a normal ADR
- Internal engagement (no client politics) — standard tradeoff-frame is enough
- Mandate change IS on the table — write a stack-replacement proposal, not this ADR
- Trade-off is trivial (<5% latency / cost delta) — ADR overhead not justified

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
| `draft-stack-mandate-tradeoff-frame` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stack-mandate-tradeoff-frame.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[technology-evaluation-rubric]]
- [[team-rfc-process-for-devs]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
