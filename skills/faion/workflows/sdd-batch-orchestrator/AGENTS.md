---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
content_id: 92296fb91a0883f3
success_criteria:
  - Every phase is fronted by a versioned prompt file under `prompts/`; the orchestrator never inlines long prompts.
  - Parallel waves run inside isolated `git worktree` checkouts; `flock` serializes merges into the default branch.
  - REVIEW → FIX loop respects the hard iteration cap defined in `content/07-verify-review-fix-loop.xml`.
  - Visual-delivery phase produces focused before/after evidence before the batch is declared done.
---

# SDD Batch Orchestrator

## Summary

Orchestration pattern for delivering a batch of related SDD features end-to-end inside one Claude Code session: study `.aidocs/` features → clarify → plan → wave-execute in worktrees → verify → review → fix → visual-deliver → close. The orchestrator never re-types long instructions; it spawns subagents via the `Agent` tool with a path to a versioned prompt file under `prompts/` plus a small parameter block. Per-phase prompts, per-surface playbooks, and shared reference docs live as files so behaviour is reproducible across runs.

## Why

Multi-feature batches drift when the orchestrator improvises long prompts each time: instructions evolve, drift becomes invisible, and parallelism collapses to "one feature at a time, manually narrated." Versioned prompt files turn each phase into a deterministic capability the orchestrator composes; isolated `git worktree` checkouts let unrelated features run in safe parallel waves; a final visual-delivery phase produces evidence the human reviewer can scan in seconds. The pattern is the explicit successor to the manual loop used in FEATURE-045.

## When To Use

- A batch of ≥3 SDD features in `.aidocs/<project>/todo/` that share a delivery surface (faion-net-fe, storybook, knowledge methodologies, mediamanager-fe, ETL).
- Bug-fix or small-feature work where SDD artifacts (spec, design, test plan, implementation plan) belong before code.
- Visual changes on a faion-network-hosted surface where before/after screenshots are the expected proof of done.
- Batches that span multiple nested repos under `faion-net/` and benefit from parallel waves.

## When NOT To Use

- Single one-off feature — the planning + wave overhead is not worth it.
- Pure exploratory research that produces no merge candidate.
- Cross-cutting refactor where every feature touches the same lines — wave parallelism gives nothing; run sequentially with `/faion` (sdd-batch-orchestrator workflow).
- Anything where the user has not authorized writes — this orchestrator commits, merges into `main` / `master` locally, and (only on confirmation) pushes.
- Pure data jobs that do not touch git — use `poll-agents` for queue-driven batch work that does not need SDD artifacts.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle, role split, language convention, neutrality of the SDD tracker shape. |
| `content/02-phases.xml` | The 12 phases and which prompt file fronts each. |
| `content/03-prompt-files.xml` | How a subagent prompt file is structured + dispatch shape. |
| `content/04-parallelism.xml` | Wave admission rules, worktree pattern, `flock` merge serialization, conflict handling. |
| `content/05-defaults-constraints.xml` | No-push / no-`--no-verify` / CHANGELOG / commit-format defaults. |
| `content/06-clarification-batching.xml` | Aggregating open questions into one batched `AskUserQuestion`. |
| `content/07-verify-review-fix-loop.xml` | Iterative quality gate with hard cap, faion-network verify commands. |
| `content/08-recapture-and-deliver.xml` | Focused before/after screenshots + delivery channels (`tg-send`, SDD `done/`). |
| `content/09-anti-patterns.xml` | What to avoid and why. |
| `content/10-playbook-adaptation.xml` | How to specialize the pattern per delivery surface (BE, FE, knowledge, storybook, ETL). |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-skeleton.md` | Skeleton for any subagent prompt file under `prompts/`. |
| `templates/playbook-skeleton.md` | Skeleton for a domain-specific playbook under `playbooks/`. |
| `templates/orchestrator-dispatch.txt` | Format of the `Agent` spawn message the orchestrator uses. |
| `templates/focused-screenshot.py` | Element-focused Playwright capture with CSS outline injection. |

## Related

- `docs/skill-authoring.md` — methodology folder shape, token budgets.
- `skills/faion/` — quality gates, reflexion, code review primitives.
- `skills/faion/` — sequential SDD task executor (counterpart for non-batch work).
- `skills/faion/` — self-replenishing background pool for queue-driven batches without SDD artifacts.
- `.aidocs/proposal/sdd-batch-orchestrator/` — original proposal text (kept for traceability).
