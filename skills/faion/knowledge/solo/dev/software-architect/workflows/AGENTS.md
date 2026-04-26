# Architecture Workflows

## Summary

Seven repeatable workflow types for architecture activities: system design, architecture review, ADR creation, technology evaluation, ATAM/CBAM assessment, migration planning (Strangler Fig), and design-document review. Each workflow is a named pipeline of steps; agents run them as role-specialized subagent chains — clarifier, designer, critic, documenter — with state materialized to disk between steps.

## Why

Architecture decisions fail most often from skipped phases (no validate step, no after-action review) and from mixing design and review in the same prompt (rubber-stamp output). Naming the workflow type forces decomposition: the system-design workflow ends with a validate phase that is a separate adversarial call, not a closing paragraph.

## When To Use

- Standardizing repeated architecture activities across a team: pick one workflow per artifact type and stop inventing new review forms.
- Onboarding: gives a new architect a checklist instead of tribal knowledge.
- Multi-stakeholder decisions where the workflow ceremony (readouts, async review) is itself the deliverable.
- Audit-grade documentation where you must show "we followed an evaluation method."

## When NOT To Use

- One-person, one-decision contexts — workflow ceremony costs more than the decision value.
- Pure code-level refactors — use design-pattern methodologies instead.
- Tight time-boxed prototypes — the workflows assume room for review cycles.

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow-types.xml` | System design, ADR, technology evaluation, ATAM/CBAM, migration planning workflows with step sequences and key outputs. |
| `content/02-review-and-llm.xml` | Architecture review types (roadmap vs design), LLM usage patterns, decision trees for workflow selection, CI/CD quality gates. |

## Templates

none
