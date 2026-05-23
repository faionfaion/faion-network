# Research Workflows

## Summary

**One-sentence:** Workflow router that picks the correct end-to-end research workflow (market / competitors / pricing / personas / validation / pricing-research / names / pains) and emits a workflow plan with checkpoints.

**One-paragraph:** Workflow-routing methodology for the research domain. Given a research mode (market | competitors | pricing | personas | validation | names | pains | niche), this picks the right end-to-end pipeline, names the artefacts produced at each checkpoint, and emits a workflow plan. Output is a workflow-plan.md that downstream subagents execute.

**Ефективно для:**

- Orchestrator-mode скрипт обирає workflow перед запуском subagents.
- Дослідницький запит надто широкий ('зроби research') - треба звузити до конкретного workflow.
- Композитна задача (market + personas + pricing) - треба послідовний план.
- SDD spec.md потребує research дзвінків - workflow plan входом для виконавця.
- Quarterly retro: чи правильно ми обирали workflows.

## Applies If (ALL must hold)

- Orchestrator picks a workflow before spawning research subagents.
- Research request is broad ('do research') and must be narrowed to a concrete workflow.
- Composite task (market + personas + pricing) requires a sequenced plan.
- SDD spec.md needs research inputs; the workflow plan is what the executor consumes.
- Quarterly retro: were we picking workflows correctly?

## Skip If (ANY kills it)

- Single-methodology task (call the methodology directly).
- Out-of-domain task (not research).
- Pure mechanical fetch (no workflow needed).
- When the user explicitly named a workflow.
- Pre-research framework selection (use frameworks methodology first).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research goal | 1-3 sentences | user / orchestrator |
| Stage tag | ideation / pre-pmf / post-pmf / scale | founder |
| Output consumer | spec.md / pitch deck / GTM doc | downstream |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[frameworks]] | supplies the framework selection that constrains workflow choice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-mode` | haiku | Map research goal to one of 8 canonical workflow modes. |
| `compose-plan` | sonnet | Sequence the methodologies + artefacts + checkpoints. |
| `name-checkpoints` | haiku | Mechanical checkpoint naming + acceptance criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/workflow-plan.md` | Workflow plan skeleton (mode + steps + artefacts + checkpoints) |
| `templates/check-names.sh` | Bash helper to validate workflow-mode names against the canonical set |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-workflows.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[frameworks]]
- [[methodologies-index]]
- [[methodologies-detail]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
