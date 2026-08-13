# Seven Performance Domains (PMBOK 8)

## Summary

**One-sentence:** Spec for organising project oversight under the seven PMBOK 8 performance domains (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk) with one accountable owner per domain.

**One-paragraph:** Spec for organising project oversight under the seven PMBOK 8 performance domains (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk) with one accountable owner per domain. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-seven-performance-domains.py` enforces the output contract.

**Ефективно для:**

- Standing up PMBOK 8 governance for a new program.
- Migrating an existing program from PMBOK 6 Knowledge Areas to PMBOK 8 domains.
- Building a domain-health dashboard with one named owner per domain.
- Aligning portfolio-level reporting with domain-level project signal.

## Applies If (ALL must hold)

- Program is governed under PMBOK 8 (or transitioning to it).
- Each domain can be assigned one accountable owner (even if one person holds multiple).
- A value-realisation metric (outcomes / outputs) is required alongside delivery metrics.

## Skip If (ANY kills it)

- Pure agile team with no PMBOK governance requirement.
- Project size where seven-domain overhead exceeds steering value (typically <8 weeks, <$50k).
- Hardware-heavy waterfall with domain-irrelevant lifecycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter | Markdown | Sponsor |
| Stakeholder register | CSV/YAML | PM |
| Budget baseline | Currency total + cadence | Finance |
| Risk register seed | YAML/CSV | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-integration]] | integration discipline is the spine of all 7 domains |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assign-domain-owners` | sonnet | Judgement on owner fit + conflict-of-interest. |
| `score-domain-health` | haiku | Mechanical roll-up of per-domain colour to portfolio view. |
| `draft-value-realisation-metric` | sonnet | Light judgement converting outputs → outcomes formula. |

## Templates

| File | Purpose |
|------|---------|
| `templates/domains.yaml` | Seven-domain skeleton with owner, health colour, top-3 risks per domain |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[six-core-principles]]
- [[project-integration]]
- [[benefits-realization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/domains.yaml`

```yaml
# Per-project PMBOK 8 domain status manifest.
# Fill before each monthly review. Owner = accountable person.
# Status: G (green) | A (amber) | R (red)
# Evidence: path or quoted text from a real artifact.
# Gap: required for A and R; explain what is missing.

domains:
  governance:
    status: G
    owner: pm
    evidence: charter.md#authority-section
    gap: ""

  scope:
    status: A
    owner: po
    evidence: spec.md
    gap: "Acceptance criteria missing for 3 user stories in sprint 4"

  schedule:
    status: G
    owner: pm
    evidence: roadmap.md
    gap: ""

  finance:
    status: A
    owner: sponsor
    evidence: budget.xlsx
    gap: "Q3 forecast not updated since last month"

  stakeholders:
    status: G
    owner: pm
    evidence: stakeholder-register.md
    gap: ""

  resources:
    status: R
    owner: line_manager
    evidence: capacity.md
    gap: "Senior engineer departed; no backfill plan exists"

  risk:
    status: G
    owner: pm
    evidence: risk-register.md
    gap: ""

value_delivery:
  outputs_shipped: 0       # replace with actual count
  outcomes_realized: 0     # replace with actual count
  value_realization_rate: 0.0

sustainability_metrics:
  - co2_per_user_session_kg: null   # measure or "not applicable: <reason>"
  - inclusive_a11y_score: null      # WCAG level achieved
```
