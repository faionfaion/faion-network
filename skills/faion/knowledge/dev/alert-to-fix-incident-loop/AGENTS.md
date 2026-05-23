# Alert-to-Fix Incident Loop

## Summary

**One-sentence:** Closed-loop run-of-play for solo on-call: from alert fired → triage → mitigate → fix → write postmortem → close alert quality gap, with each step's artefact named and validated.

**One-paragraph:** Solo devs lose 30+ minutes per page on rediscovery (where is the dashboard, which on-call rotation, what was the last similar incident). The methodology fixes the loop: alert → triage record → mitigation step → root-cause hypothesis → fix PR → postmortem → alert-quality patch. Each step's artefact is required; skipping the postmortem is the failure mode the loop exists to prevent. Output is the incident artefact conforming to the schema. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Alert-to-Fix Incident Loop — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `alert-to-fix-incident-loop` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Production system has triggered an alert (page, ticket, automatic rollback).
- Solo dev is the named on-call respondent OR is the only person reachable.
- Operator wants a recurring loop, not an ad-hoc response per incident.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Alert is a known false positive scheduled for muting — skip + ticket the mute, do not run the loop.
- Multi-team major incident — escalate to a coordinated incident commander, not a solo loop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[server-craft]] | Parent skill — infra & ops vocabulary |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-alert-to-fix-incident-loop-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-alert-to-fix-incident-loop.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-to-fix-incident-loop.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[ai-pairing-decision-tree]]
- [[api-monitoring]]
- [[api-contract-pattern-selection]]

## Decision tree

See `content/06-decision-tree.xml`. Routes the responder by severity + observable signal quality to one of {full loop, fast-mitigate-then-loop, escalate-to-coordinated-incident}. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
