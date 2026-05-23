# DR Drill Scenario Library

## Summary

**One-sentence:** Reusable catalogue of disaster-recovery scenarios (region loss, db corruption, secret-store loss, identity provider outage, vendor breach) with declaration, run, restore, and post-mortem steps.

**One-paragraph:** DR drills without a scenario library default to 'last quarter's region failover, run it again'. Real DR programs need a library — a catalogue of scenarios covering region loss, database corruption (logical not physical), secret-store loss, identity provider outage, vendor breach, ransomware. Each scenario has declaration criteria, runbook steps, restore validation, success criteria, and a post-mortem template. The library is exercised on a rotating cycle so the team practices uncommon scenarios before they need them. Output: dr-scenarios.yaml + per-scenario runbook + 4-week drill rotation calendar.

**Ефективно для:**

- DR drill вже не 'та сама regional failover'; rotate через library.
- Документована scenario для логічного db corruption (не lost-region).
- Identity provider outage — real scenario, real runbook.
- Drill rotation calendar: яка scenario наступного кварталу.

## Applies If (ALL must hold)

- Business depends on infra continuity (paying customers, SLA, regulated workload)
- DR drills are part of the compliance program (SOC2 CC7.5, ISO 22301)
- Team has 4+ engineers to participate in drills
- Multi-region or multi-vendor architecture (otherwise 'restore from backup' is the only scenario)

## Skip If (ANY kills it)

- Pre-revenue product — DR effort exceeds value
- Single-region single-vendor lock-in — write a single 'restore from backup' runbook instead
- Compliance not required and customers don't ask for DR evidence

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backup-verification-dr methodology | backup verification reports | platform team |
| Runbook authoring discipline | runbook style guide | SRE |
| Drill calendar slot (quarterly minimum) | team capacity | engineering leader |
| Post-mortem template | incident-mgmt repo | incident commander |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[dr-drill-script-template]] | Per-scenario script structure |
| [[on-call-rotation-bootstrap]] | Owners + escalation tree for drills |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scenario_authoring` | opus | Cross-vendor + cross-component synthesis |
| `runbook_draft` | sonnet | Bounded structured writing |
| `rotation_calendar` | haiku | Mechanical scheduling |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dr-drill-scenario-library.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[dr-drill-script-template]]
- [[on-call-rotation-bootstrap]]
- [[error-budget-policy-and-freeze-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
