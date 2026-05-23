# Terraform Modules — Prompts

## Summary

**One-sentence:** Prompts spec for AI agents authoring or refactoring Terraform modules: required context (state shape, provider versions, naming convention), output shape, gating questions.

**One-paragraph:** Prompts spec for AI agents authoring or refactoring Terraform modules: required context (state shape, provider versions, naming convention), output shape, gating questions. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Команда часто просить AI 'напиши модуль для X' і отримує різний стиль кожен раз — треба зафіксований шаблон prompt.
- Style-guide для модулів (snake_case, validation, sensitive flag) існує, але AI його забуває.
- Прескриптовані output_keys і required inputs мають бути в кожному модулі — це треба у prompt-у.
- Прескриптована послідовність fmt → validate → tflint → tfsec має виконуватися завжди.

## Applies If (ALL must hold)

- AI agent is being asked to scaffold or refactor a Terraform module
- Operator wants a prompt template that produces consistent module shape across requests
- Module style guide (snake_case names, validation blocks, required outputs) must be enforced
- Tool calling sequence (terraform fmt → validate → tflint → tfsec) needs to be embedded in the prompt

## Skip If (ANY kills it)

- Production module composition wiring — use terraform-modules-composition
- Module semver release process — use terraform-modules-versioning
- Module security review — use terraform-modules-security

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform-modules-prompts.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the task to design a reusable prompt template for AI-authored Terraform modules?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
