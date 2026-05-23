# AI Feature Progressive Rollout

## Summary

**One-sentence:** Playbook step that scales AI feature traffic by ring (1% → 10% → 50% → 100%) gated on eval delta + observability pillars + customer-comm checkpoints.

**One-paragraph:** Playbook step that scales AI feature traffic by ring (1% → 10% → 50% → 100%) gated on eval delta + observability pillars + customer-comm checkpoints. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a playbook-step produced by an agent applying ai feature progressive rollout. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible playbook-step for ai feature progressive rollout across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI feature is launching new or rolling out a material change (prompt overhaul, model migration)
- the platform supports per-user / per-cohort feature flags
- observability pillars (quality / latency / cost / drift) are live for the feature

## Skip If (ANY kills it)

- change is a hot-fix to restore a green state — rollout-as-fast-as-safe-allows, not progressive
- platform cannot do per-cohort flagging — fix that first or use big-bang with explicit acceptance of risk
- feature is internal-only with <50 users — progressive rollout overhead exceeds value

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature flag platform with cohorts | platform | engineering |
| Observability pillars live | ml-engineering | ml-engineering |
| Eval gate green for current change | ml-engineering | ml-engineering |
| Customer comm template (if external) | trust & safety | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-feature-observability-four-pillars]] | Observability gates rollout |
| [[eval-driven-development-tdd-for-ai]] | Eval gates rollout |
| [[ai-feature-incident-runbook]] | Roll-back path |

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
| `ring_plan` | sonnet | Specify rings + traffic % + dwell time per ring. |
| `gate_check` | sonnet | Verify gates per ring transition. |
| `comm_handling` | sonnet | Customer comm at material transitions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollout-plan.md` | Rollout playbook-step skeleton |
| `templates/ring-config.json` | Ring config JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in rollout plan |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-progressive-rollout.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-feature-observability-four-pillars]]
- [[eval-driven-development-tdd-for-ai]]
- [[ai-feature-incident-runbook]]
- [[ai-feature-ga-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
