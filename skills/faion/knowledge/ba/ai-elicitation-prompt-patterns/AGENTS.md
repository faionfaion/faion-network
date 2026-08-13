# AI Elicitation Prompt Patterns

## Summary

**One-sentence:** Reusable prompt-skeleton + slot library for BA elicitation tasks (interview prep, follow-up probes, paraphrase-back validation) with structural validation per call.

**One-paragraph:** Modern BAs run elicitation through a shared LLM (Copilot, Claude, internal RAG). Without a versioned prompt library, every BA reinvents prompts and outputs drift. This methodology codifies a closed pattern set: interview-prep prompts, follow-up question generators, paraphrase-back validators, and persona-driven probes. Each pattern has named slots, a schema for its output, and an eval harness. Output is a `playbook-step` that drops into the elicitation workflow.

**Ефективно для:**

- Stakeholder-interview prep (LLM drafts questions від project brief).
- Follow-up question generation (LLM пропонує наступні probes після initial answers).
- Paraphrase-back validation (LLM перефразовує requirement → BA confirms with stakeholder).
- Persona-driven probing (LLM генерує запитання з точки зору specific persona).

## Applies If (ALL must hold)

- You build, refine, or hand off an LLM workflow used by ≥2 BAs.
- The pattern's output is structurally validated (schema, regex, or downstream parser).
- Cost and latency budget per call are known before authoring.
- Versioning rule for the prompt is in place (Git, registry, or prompt-eval harness).

## Skip If (ANY kills it)

- One-off prompts used once and discarded.
- Output consumed by humans only, with no downstream parser.
- Provider-specific quirks change weekly — register the prompt, do not encode it here.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target model + provider | config (YAML) | infra team |
| Eval harness fixture set | JSONL | BA lead |
| Versioning convention | repo policy doc | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-assisted-requirements-elicitation]] | Upstream BABOK-grounded methodology this implements |
| [[ai-acceptance-criteria-generator-reviewer]] | Downstream rubric that scores the output of these prompts |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: slot discipline, schema gate, version tag, cost cap | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for a prompt pattern + valid/invalid examples | 750 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: slot bleed, schema-less, version-orphan, cost runaway, prompt-injection | 850 |
| `content/04-procedure.xml` | essential | 5-step authoring procedure | 700 |
| `content/06-decision-tree.xml` | essential | Pattern selection by elicitation phase | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prompt_compile` | haiku | Mechanical slot-fill from inputs. |
| `eval_run` | sonnet | Run prompt against ground-truth fixture set. |
| `pattern_refactor` | opus | Identify drift and rewrite skeleton. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-pattern.yaml` | Prompt-pattern skeleton with slots + schema reference |
| `templates/_smoke-test.yaml` | Minimum viable filled pattern for interview-prep |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-elicitation-prompt-patterns.py` | Validate emitted pattern against output-contract schema | CI on each pattern change; pre-commit |

## Related

- [[ai-assisted-requirements-elicitation]]
- [[ai-acceptance-criteria-generator-reviewer]]
- [[acceptance-criteria]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes the BA from elicitation-phase observable (interview-prep vs follow-up vs paraphrase-back vs persona-probe) to a specific pattern + rule from `01-core-rules.xml`. Use when picking which pattern to instantiate for a given stakeholder session.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-pattern.yaml`

```yaml
pattern_id: REPLACE-with-kebab-case-id
phase: interview-prep        # one of: interview-prep | follow-up | paraphrase-back | persona-probe
slots:
  - name: stakeholder_role
    type: string
    required: true
  - name: project_brief
    type: string
    required: true
skeleton: |
  You are preparing an elicitation interview for {{stakeholder_role}}.
  Project brief: {{project_brief}}
  Draft 8 open questions; cite the brief paragraph each question is grounded in.
output_schema_ref: templates/output-schema.json#/interview_questions
eval_reference: evals/interview-prep-v1.jsonl
budget:
  tokens_in: 800
  tokens_out: 400
  cost_usd_cap: 0.05
version_tag: v1.0.0
```

### `templates/_smoke-test.yaml`

```yaml
pattern_id: interview-prep-smoke
phase: interview-prep
slots:
  - {name: stakeholder_role, type: string, required: true}
  - {name: project_brief, type: string, required: true}
skeleton: "Prepare 5 questions for {{stakeholder_role}}. Brief: {{project_brief}}."
output_schema_ref: "templates/output-schema.json#/interview_questions"
eval_reference: "evals/smoke.jsonl"
budget:
  tokens_in: 400
  tokens_out: 200
  cost_usd_cap: 0.01
version_tag: v0.1.0
```
