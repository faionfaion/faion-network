---
slug: frontline-validation-protocol
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Operator-grounded as-is validation: ≥2 frontline operators per variant via shadowing/gemba/listening-session, closed observation taxonomy, reconcile-not-replace synthesis blocking sponsor-pleasing model edits.
content_id: "268c713a0f213153"
complexity: deep
produces: report
est_tokens: 5200
tags: [ba, process-improvement, gemba, shadowing, frontline, elicitation]
---
# Frontline Validation Protocol

## Summary

**One-sentence:** Operator-grounded as-is validation: ≥2 frontline operators per variant via shadowing/gemba/listening-session, closed observation taxonomy, reconcile-not-replace synthesis blocking sponsor-pleasing model edits.

**One-paragraph:** Process-improvement initiatives fail when frontline operators are skipped, because sponsors describe the process they wish existed and SMEs describe the process documented two years ago. This methodology defines three engagement methods — direct shadowing, gemba walk, structured listening session — and the gating rule: no as-is model is signed off until ≥2 frontline engagements with 2 different operators per process variant are completed. Mechanism: per-variant validation matrix, time-boxed observation slots, closed observation taxonomy (workaround, deviation, blocker, tribal-knowledge), and synthesis that reconciles documented vs observed process.

**Ефективно для:**

- Process-improvement, де sponsor розповідає про процес, який він хоче, а SME — про процес з документу 2-річної давнини.
- RPA / automation design — щоб автоматизувати реальний процес, а не задокументований.
- Audit remediation з compliance theater ризиком — performative compliance детектор спрацьовує.
- System replacement, де workarounds — це і є справжній процес.

## Applies If (ALL must hold)

- engagement type ∈ {process_improvement, system_replacement, RPA/automation_design, audit_remediation}
- ≥1 frontline operator role exists in the process scope
- duration of the initiative ≥4 weeks (frontline overhead not worth it for sprints)
- sponsor sign-off authority exists separately from the operator level
- access to operator workspace (physical or screen-shared) is granted

## Skip If (ANY kills it)

- Pure greenfield design (no current process to observe).
- Automation of a single API call between two systems (no operator involvement).
- Regulatory work where direct observation is prohibited.
- Single-operator process where operator == sponsor — collapse to standard elicitation.
- Distributed-workforce process with no consistent operator role.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Documented sponsor-supplied as-is process | Markdown / BPMN | sponsor |
| Frontline role list with headcount | JSON / CSV | HR / Ops |
| Access agreement signed | PDF | manager + HR + union if applicable |
| Observation slot calendar | ics / Google Cal | scheduling |
| Safety / confidentiality briefing | Markdown | compliance |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/elicitation-techniques` | SME-side elicitation complements frontline. |
| `pro/ba/business-analyst/business-process-analysis` | Consumes the validated as-is model. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `observation_log_normalizer` | haiku | Tag each note with closed taxonomy enum. |
| `workaround_pattern_synthesis` | sonnet | Cluster observations across operators. |
| `as_is_reconciliation` | opus | Reconcile documented vs observed; high-consequence. |
| `listening_session_question_draft` | sonnet | Non-leading question templates per step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observation-log.md` | Per-shift observation capture with closed taxonomy tags. |
| `templates/listening-session-guide.md` | 60-minute structured guide with non-leading prompts. |
| `templates/validation-matrix.md` | Per-variant coverage table (operator × method × completed). |
| `templates/access-agreement.md` | Manager / HR sign-off template. |
| `templates/_smoke-test.md` | Minimum viable filled-in report. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-frontline-validation-protocol.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[elicitation-techniques]]
- [[business-process-analysis]]
- [[process-mining-automation]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
