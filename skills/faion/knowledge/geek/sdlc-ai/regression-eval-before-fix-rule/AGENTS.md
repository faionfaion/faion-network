---
slug: regression-eval-before-fix-rule
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Every LLM-agent incident MUST produce a failing regression-eval case BEFORE the fix lands — the eval is the merge gate. Postmortem→eval→fix is non-skippable; eval-first is non-negotiable.
content_id: "a51ba9b7f087b305"
complexity: medium
produces: decision-record
est_tokens: 3300
tags: [llm-agents, regression-eval, postmortem, fix-discipline, ai-incident]
---
# Regression Eval Before Fix Rule

## Summary

**One-sentence:** Every LLM-agent incident MUST produce a failing regression-eval case BEFORE the fix lands — the eval is the merge gate. Postmortem→eval→fix is non-skippable; eval-first is non-negotiable.

**One-paragraph:** LLM-agent fixes regress silently: a prompt tweak that "obviously fixes" issue A re-introduces issue B that was fixed last month. Without a captured regression eval per incident, the team rediscovers the same bug every quarter. This methodology pins the rule: every postmortem on an agent incident MUST author a failing eval case that captures the bug deterministically; the fix PR cannot merge until that case flips from failing to passing AND no other eval cases regress. The output artefact is a decision-record linking incident → eval case path → fix PR.

**Ефективно для:**

- Repo з LLM agent (prompts, RAG, tools) що зазнає incidents.
- Команда, де "fix" без eval повертає старі баги через 2 місяці.
- Postmortem culture, що хоче перетворити incidents у permanent regression suite.
- Merge gate, де required check може блокувати на eval delta.

## Applies If (ALL must hold)

- Repo runs an LLM agent in production (chat, code, RAG, tools).
- An eval set exists (or can be created) with a deterministic replay harness.
- Incidents are reported (tracker, alert, user feedback) with reproducible inputs.
- CI can run the eval set as a required PR check.

## Skip If (ANY kills it)

- No LLM agent in scope.
- Incident is non-reproducible (one-off transient like vendor outage) — log it as "no-fix; vendor".
- Bug is a UX-only complaint with no model-output trigger — handle via UX backlog.
- Pre-prod prototype with no users — formal regression discipline is premature.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident report | tracker ticket with reproducible input | reporter |
| Eval-set repo | jsonl + replay harness | ml-engineer |
| CI required check | GitHub Actions workflow | platform |
| Decision-record template | Markdown | docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[postmortem-action-item-slo-tracking]] | Tracks action items including the eval case. |
| [[pr-time-cost-diff-tool]] | Same eval set powers cost-diff. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 700 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `reproduce-incident` | sonnet | Needs judgement to extract deterministic inputs. |
| `author-eval-case` | sonnet | Per-incident eval-case design. |
| `verify-fix-flip` | haiku | Mechanical: rerun eval before/after fix; check flip + no regressions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/regression-eval-record.md` | Decision-record skeleton (incident → eval case path → fix PR). |
| `templates/eval-case-jsonl.fixture` | Minimal failing eval-case JSONL fixture. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regression-eval-before-fix-rule.py` | Validate decision-record artefact + check eval case file exists. | Pre-merge of fix PR |

## Related

- [[postmortem-action-item-slo-tracking]]
- [[pr-time-cost-diff-tool]]
- [[task-agent-drafts-spec-before-coding]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (incident reproducible? eval-set available? CI check live?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether the rule should fire on a given incident — the tree terminates either on the active rule or on `skip-this-methodology`.
