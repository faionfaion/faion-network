# AI Feature Incident Runbook

## Summary

**One-sentence:** Playbook step for on-call response to AI feature incidents — triage matrix, kill-switch criteria, mitigation ladder, communication template, post-incident hand-off to post-mortem.

**One-paragraph:** Playbook step for on-call response to AI feature incidents — triage matrix, kill-switch criteria, mitigation ladder, communication template, post-incident hand-off to post-mortem. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a playbook-step produced by an agent applying ai feature incident runbook. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible playbook-step for ai feature incident runbook across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI feature is in GA / serving production traffic
- team has an on-call rotation responsible for this feature
- kill switch + rollback are technically possible (feature flag, model version pin, prompt SHA)

## Skip If (ANY kills it)

- feature is internal-only with low blast radius — runbook is overhead for now
- incident already handled by general ops on-call without AI-specific steps — fold lessons into general runbook
- feature is in beta with explicit user disclaimer — incidents handled via beta-feedback channel

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kill switch (feature flag or routing rule) | platform | ml-engineering |
| Observability dashboard with paging alerts | platform | ml-engineering |
| Comm channel + customer-comm template | trust & safety | ops |
| Post-mortem registry + intake flow | process | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-feature-observability-four-pillars]] | Observability for detection |
| [[ai-post-mortem-template]] | Hand-off target post-incident |

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
| `triage` | sonnet | Apply triage matrix from signals. |
| `mitigation` | sonnet | Walk mitigation ladder. |
| `communication` | sonnet | Compose customer + internal comm from template. |

## Templates

| File | Purpose |
|------|---------|
| `templates/incident-runbook.md` | Runbook playbook-step skeleton |
| `templates/incident-record.json` | Incident record JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in incident record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-incident-runbook.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-post-mortem-template]]
- [[ai-feature-observability-four-pillars]]
- [[ai-feature-progressive-rollout]]
- [[ai-feature-ga-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
