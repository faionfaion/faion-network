# AI Feature GA Checklist

## Summary

**One-sentence:** Pre-GA checklist for an AI feature — eval gate green, observability live, cost cap enforced, refusal policy tested, rollout plan + kill switch in place.

**One-paragraph:** Pre-GA checklist for an AI feature — eval gate green, observability live, cost cap enforced, refusal policy tested, rollout plan + kill switch in place. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a checklist produced by an agent applying ai feature ga checklist. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible checklist for ai feature ga checklist across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI feature is preparing to leave beta / EAP and serve general traffic
- the team owns prompt + model + retrieval + tool surfaces end-to-end
- the launch will be reviewed by leadership and tracked against KRs

## Skip If (ANY kills it)

- feature is staying in beta / EAP — use beta-readiness methodology instead
- feature is a non-AI ship-as-is move — use ordinary feature GA checklist
- feature is a hot-fix re-launch of an existing GA feature — use incident-runbook instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Eval suite + green run | ml-engineering | ml-engineering |
| Observability dashboard (quality + cost + latency + drift) | platform | ml-engineering |
| Cost cap + alert | finops | finance + ml-engineering |
| Refusal + safety policy + tests | trust & safety | trust & safety |
| Rollout plan + kill switch | rollout doc | ml-engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval gate |
| [[ai-feature-observability-four-pillars]] | Observability |
| [[ai-feature-progressive-rollout]] | Rollout plan |
| [[ai-feature-incident-runbook]] | Kill switch + runbook |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `checklist_walk` | sonnet | Walk each item with evidence pointer. |
| `evidence_audit` | sonnet | Verify cited evidence is real and dated. |
| `sign_off_routing` | sonnet | Route to required signers per org policy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ga-checklist.md` | Checklist artefact skeleton |
| `templates/evidence-table.json` | Evidence table JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in GA checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-ga-checklist.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-feature-observability-four-pillars]]
- [[ai-feature-progressive-rollout]]
- [[ai-feature-incident-runbook]]
- [[eval-driven-development-tdd-for-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
