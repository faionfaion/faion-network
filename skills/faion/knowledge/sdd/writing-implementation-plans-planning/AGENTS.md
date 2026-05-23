# Writing Implementation Plans

## Summary

**One-sentence:** Generates implementation-plan.md from an Accepted design — WBS, dependency graph, wave shards, per-task token budgets, critical path, risk + test + rollout strategy.

**One-paragraph:** Bridges design.md (AD-X decisions + file table) and executor-ready TASK files. The 11-phase writing process: load SDD context → check prerequisites → WBS → dependency graph → wave analysis → phase definition → task format → critical path → risk assessment → testing strategy → rollout strategy. Output is implementation-plan.md (Accepted). The plan rows become the input to `template-task` for per-task file authoring.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'implementation-plan authoring' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Accepted design.md exists for the feature (status: Accepted).
- The feature has ≥3 interacting components OR sequencing matters.
- Multiple waves of parallel work are possible OR critical-path matters.
- The plan will be consumed by automated agents that need ordered, sharded inputs.

## Skip If (ANY kills it)

- Feature has fewer than 3 tasks — skip the plan, write TASK files directly.
- Spec or design doc is still Draft — writing the plan too early wastes tokens when requirements shift.
- Bug fixes — use a single TASK file.
- Exploratory spikes — plans assume known solutions; spikes discover the solution.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Accepted design.md | markdown | `.aidocs/features/<status>/<feature>/design.md` |
| Accepted spec.md (for FR-X back-trace) | markdown | `.aidocs/features/<status>/<feature>/spec.md` |
| Repo testing convention | markdown | repo testing guide |
| Existing implementation-plan template | shell | `templates/create-tasks.sh` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/workflow-design-phase` | Provides the Accepted design.md this plan consumes. |
| `solo/sdd/sdd-planning/template-task` | Downstream consumer that renders each plan row into a TASK file. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the implementation-plan.md + valid/invalid/forbidden examples | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 11-step procedure: load context → WBS → deps → waves → phases → tasks → critical path → risk → testing → rollout → review | ~1100 |
| `content/05-examples.xml` | medium | Worked example: implementation-plan.md for the JWT refresh feature | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposition` | sonnet | Mechanical mapping of file_table to atomic tasks. |
| `dependency-graph` | opus | Multi-task ordering + critical-path reasoning. |
| `wave-shard` | sonnet | Bin-pack tasks into waves respecting deps + token budgets. |
| `risk-and-rollout` | opus | Cross-task risk synthesis + rollout strategy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/create-tasks.sh` | Bash helper that stubs empty TASK_*.md files for a wave. |
| `templates/implementation-plan.md` | Canonical implementation-plan.md skeleton with WBS, dep graph, waves, critical path, risk, testing, rollout sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-writing-implementation-plans.py` | Validate the implementation-plan.md frontmatter against the schema in `content/02-output-contract.xml`. | After subagent returns the plan, before promoting to Accepted. |

## Related

- [[workflow-design-phase]]
- [[template-task]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (design Accepted, task count ≥3, sequencing matters) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether to run the full planning phase or shard tasks directly.
