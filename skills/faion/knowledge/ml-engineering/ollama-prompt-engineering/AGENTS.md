# Ollama Prompt Engineering

## Summary

**One-sentence:** Tunes prompts for small local Ollama models: model-card conventions, system-prompt headers, JSON mode, and few-shot density for 7B–70B class.

**One-paragraph:** Tunes prompts for small local Ollama models: model-card conventions, system-prompt headers, JSON mode, and few-shot density for 7B–70B class. The methodology assumes the inputs in Prerequisites and produces a `playbook-step` artefact validated by `scripts/validate-ollama-prompt-engineering.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Developers iterating on prompts against quantised local models where prompt sensitivity dominates output quality.

## Applies If (ALL must hold)

- Designing prompts for local Ollama deployments where output quality needs to match cloud models.
- Building prompt templates for NLP pipelines (extraction, classification, summarization).
- Optimizing temperature and context settings for specific task types.
- Implementing multi-turn conversation management with local models.

## Skip If (ANY kills it)

- Cloud model prompt engineering — technique overlap is high but cloud models tolerate vaguer prompts; over-constraining cloud models can reduce quality.
- Fine-tuning use cases — prompt engineering is a complement to fine-tuning, not a substitute when specialized behavior is required.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-fundamentals]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `expand-step` | sonnet | Inline judgment per step. |
| `integrate-with-upstream` | opus | Cross-step consistency. |
| `lint-output` | haiku | Format check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/playbook-step.md.tmpl` | Markdown playbook-step skeleton: trigger, action, verification, rollback. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ollama-prompt-engineering.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-engineering-fundamentals]]
- [[ollama-tool-calling]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-prompt-engineering` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/playbook-step.md.tmpl`

```markdown
-->

# ollama-prompt-engineering — playbook-step skeleton

> Replace every `TODO` block before handing off. The skeleton is wired to the schema in `content/02-output-contract.xml`; run `scripts/validate-ollama-prompt-engineering.py` after filling.

## Inputs

- Task brief: <link>
- Constraints: <link>

## Body

- TODO — section 1
- TODO — section 2
- TODO — section 3

## Acceptance

- All required keys present per the output contract.
- `forbidden_seen` is empty.
- Validator exits 0.

## Signature

- `signature: sha1(slug + version + date)[:16]`
```
