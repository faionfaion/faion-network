# Blurred Roles and Team Evolution

## Summary

**One-sentence:** Modern AI-era product teams operate as overlapping Venn diagrams rather than relay-race handoffs.

**One-paragraph:** Modern AI-era product teams operate as overlapping Venn diagrams rather than relay-race handoffs. The methodology produces a `report` artefact gated by an explicit output contract (JSON Schema draft-07) + decision tree referencing core rules. Apply when the preconditions in `## Applies If` ALL hold and none of the `## Skip If` disqualifiers fires. Skip and reach for a sibling methodology otherwise.

**Ефективно для:**

- Repeatable cycles де треба явний report, не ad-hoc notes.
- Командна робота з named owner per artefact (audit trail).
- Pro-tier контекст: 3-20 retainer clients / mid-stage SaaS / agency-to-saas pivot.
- AI-augmented workflows, де LLM-агент виконує частину кроків процедури.

## Applies If (ALL must hold)

- Operating context matches the produces shape (`report`) — outcome can be inspected as a discrete artefact.
- Named human owner exists for the artefact + downstream actions (no orphan output).
- Inputs listed in `## Prerequisites` are available before the run.
- Cadence and time-box fit the cycle window the team actually operates.
- Output will be reviewed against the JSON Schema in `content/02-output-contract.xml` before acceptance.

## Skip If (ANY kills it)

- One-off task with no recurrence — value of the methodology is the rhythm.
- No named owner accountable for the produced artefact.
- Team already runs a more granular methodology that supersedes this one.
- Preconditions in `## Prerequisites` missing and no plan to source them this cycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs listed in `01-core-rules.xml` | system-of-record links (URL or path) | upstream owner |
| Prior cycle output (if any) | this methodology's own artefact | git history |
| Named owner for cycle | identity string | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output gates | ~800 |
| `content/05-examples.xml` | essential | End-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-inputs` | haiku | Mechanical mapping; no judgment. |
| `apply-procedure` | sonnet | Cross-section reasoning over the medium procedure. |
| `synthesize-report` | opus | Final cross-input judgment producing the report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/role-overlap.sh` | Emit per-author file-area distribution from git history |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blurred-roles-team-evolution.py` | Validate output artefact against JSON Schema | Pre-commit + CI on each artefact change |

## Related

- parent skill: `skills/faion/knowledge/pro/product/product-operations/`
- peer methodologies: siblings under the parent skill
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions satisfied, owner present, prior-cycle output available, cycle window fit) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology this cycle or defer.
