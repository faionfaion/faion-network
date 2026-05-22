---
slug: agent-postmortem-template
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a blameless postmortem report where the agent itself is the defendant: pinned model id, byte-exact prompt diff, six-layer attribution (model/system-prompt/tool-schema/tool-result/retrieval..."
content_id: "371973b0699b2ba3"
complexity: medium
produces: report
est_tokens: 4500
tags: [postmortem, agent, incident, eval, layer-attribution, replay]
---

# Agent Postmortem Template (Agent-as-Defendant)

## Summary

**One-sentence:** Produces a blameless postmortem report where the agent itself is the defendant: pinned model id, byte-exact prompt diff, six-layer attribution (model/system-prompt/tool-schema/tool-result/retrieval...

**One-paragraph:** Generic incident postmortems treat the engineer as actor and agent as drafting tool. When the agent is the defendant — fabricated tool call, misread retrieval, jailbreak success, context overflow that dropped the system rule — the generic template hides the actual root cause. This methodology defines first-class fields for trace ID, model version, prompt diff, eval delta, and forced layer-attribution so the team converges on which layer to fix.

**Ефективно для:** agent-mediated incidents with user-visible harm; failed prod eval runs blocking deploy; jailbreak/prompt-injection investigations; context-window overflow root-causing.

## Applies If (ALL must hold)

- An agent-mediated action caused user-visible harm, customer escalation, or a failed eval in production
- A stored trace (request id, model id, rendered prompt, tool calls, tool results) exists and is replayable
- A named owner exists for at least one of the six layers
- The eval suite for this agent has a baseline score the incident can be compared against

## Skip If (ANY kills it)

- Incident is a pure infra outage (DB down, network split) with no agent decision involved
- Trace data was not captured — file Trace Gap action item instead
- Single-incident triage where label-only is enough; full postmortem is overhead

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Replayable trace | trace_id + artefacts | observability stack |
| Model pin | provider/name-YYYYMMDD | deploy log |
| System prompt snapshot at incident time | rendered string | trace store |
| Eval suite + baseline score | eval harness | eval owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[agent-observability-stack-blueprint]]` | Trace storage prerequisite |
| `[[agent-failure-taxonomy]]` | Labels for incident class |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Attribute layer | opus | Cross-layer reasoning. |
| Author prompt diff | sonnet | Mechanical. |
| Build regression case | sonnet | Pattern from incident. |

## Templates

| File | Purpose |
|------|---------|
| `templates/postmortem.md.tmpl` | Postmortem skeleton with all six fields. |
| `templates/layer-attribution.md.tmpl` | Six-layer decision rubric. |
| `templates/eval-delta.json.tmpl` | Eval-delta record schema example. |
| `templates/_smoke-test.md` | Filled example for a tool-schema regression. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-postmortem-template.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/ai/`
- `[[agent-failure-taxonomy]]`
- `[[agent-observability-stack-blueprint]]`
- `[[agent-drift-detection-statistical]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-postmortem-template applies: root question — "Did the incident involve an agent decision (not pure infra)?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
