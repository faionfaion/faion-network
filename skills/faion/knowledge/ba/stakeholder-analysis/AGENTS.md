# Stakeholder Analysis

## Summary

**One-sentence:** A power-interest classification of named stakeholders that produces an engagement strategy, RACI matrix, and communications plan owned by a named BA.

**One-paragraph:** Projects fail when the wrong stakeholder is consulted too late or the right stakeholder is over-consulted into fatigue. Stakeholder analysis maps every named individual (no 'team X') onto a 2×2 (power × interest), defines a per-quadrant engagement strategy (manage closely / keep satisfied / keep informed / monitor), produces a RACI per major decision, and a communications plan with cadence + channel + owner. Output: a stakeholder register + RACI + comms plan reviewed at every milestone gate.

**Ефективно для:**

- Cross-functional programs with ≥3 departments + external vendors.
- Regulated initiatives with named legal / compliance reviewers.
- Pre-kickoff phase of any engagement ≥6 weeks.
- Re-engagement on a stalled project where ownership is unclear.

## Applies If (ALL must hold)

- the engagement has ≥3 distinct stakeholder organisations
- decisions require named approvers (not 'the team agrees')
- a BA or PM owns the artefact going forward
- the project has a known sponsor

## Skip If (ANY kills it)

- single-team internal tool with ≤5 users
- stakeholders refuse to be named individually — fix sponsorship first
- the engagement is fully open-scope T&M with no decision gates

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| org chart / contact list | PDF / CSV | sponsor / HR |
| project charter or business case | wiki / PDF | sponsor |
| prior project lessons (if rerun) | retrospective notes | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis-business-need]] | Defines why the project exists, which informs stakeholder relevance. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named individuals only, power × interest grid, per-quadrant strategy, RACI per major decision, owned comms cadence | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for stakeholder register + RACI + comms plan | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: anonymous teams, stale grid, RACI bloat, channel drift, sponsor invisible | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify → classify → strategize → RACI → comms plan | 700 |
| `content/05-examples.xml` | essential | Worked example: 6-stakeholder ERP rollout register + RACI excerpt | 600 |
| `content/06-decision-tree.xml` | essential | Tree on stakeholder count + decision gates + power skew | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify_individuals` | haiku | Mechanical extraction from org chart. |
| `classify_power_interest` | sonnet | Light judgment with rationale per row. |
| `draft_engagement_strategy` | sonnet | Bounded synthesis per quadrant. |
| `draft_raci` | sonnet | Mechanical mapping with reviewer cross-check. |
| `comms_plan_narrative` | sonnet | Cadence + channel + owner per stakeholder. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Markdown skeleton with rows for each stakeholder + power/interest + strategy. |
| `templates/raci.csv` | RACI matrix header: Decision, Responsible, Accountable, Consulted, Informed. |
| `templates/comms-plan.md` | Communications plan with cadence + channel + owner. |
| `templates/_smoke-test.md` | Minimum viable 3-stakeholder register. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-analysis.py` | Validates stakeholder register + RACI + comms plan against JSON Schema. | After register update; pre-commit. |

## Related

- [[strategy-analysis-business-need]]
- [[use-case-modeling]]
- [[scope-drift-early-warning-metrics]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
