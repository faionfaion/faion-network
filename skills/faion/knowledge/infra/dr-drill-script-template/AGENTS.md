# DR Drill Script Template

## Summary

**One-sentence:** Per-drill script template covering declaration → runbook execution → restore validation → success criteria check → post-mortem within 7 days, scored against RTO/RPO targets.

**One-paragraph:** A DR drill is not 'failover and see what happens'. It's a scripted exercise with declaration, run, restore, validate, score, post-mortem. This methodology provides the per-drill script template: declaration step (read-only check that the scenario's criteria are met or simulated), run step (the runbook, executed verbatim), restore step (re-establish service), validation step (data integrity + smoke test), score (RTO/RPO achieved vs targets), post-mortem (gaps + tickets within 7 days). Output: drill-run.yaml capturing what happened + drill-report.md publishable to the team. Pairs with dr-drill-scenario-library which supplies the scenarios.

**Ефективно для:**

- Drill — це script, не improvisation; кожен крок документований.
- Score за RTO/RPO замість 'feels like it went ok'.
- Post-mortem обов'язковий + 7-day deadline.
- Pair з dr-drill-scenario-library: scenario → script execution.

## Applies If (ALL must hold)

- DR scenario library exists (use the library methodology first)
- Quarterly or more frequent drill cadence
- Team commits to producing a post-mortem within 7 days
- RTO/RPO targets exist (otherwise 'score' is undefined)

## Skip If (ANY kills it)

- No scenario library — author one first via dr-drill-scenario-library
- First-ever DR drill with no targets — pick targets first, then script

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| dr-drill-scenario-library output (scenarios.yaml) | library | platform team |
| RTO/RPO targets per service | SLO + DR policy | engineering leader |
| Post-mortem template | templates/postmortem.md | incident-mgmt |
| Drill calendar slot booked | team capacity | rotation owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[dr-drill-scenario-library]] | Supplies the scenario this script exercises |
| [[on-call-rotation-bootstrap]] | Provides the owner/escalation references |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `declaration_announce` | haiku | Template fill comms |
| `post_mortem_draft` | sonnet | Bounded structured writing from drill log |
| `gap_synthesis` | opus | Cross-step pattern detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dr-drill-script-template.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[dr-drill-scenario-library]]
- [[on-call-rotation-bootstrap]]
- [[alert-deduplication-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
