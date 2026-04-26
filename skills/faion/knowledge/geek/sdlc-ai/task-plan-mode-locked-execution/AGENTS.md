# Plan Mode Then Locked Execution

## Summary

For any change that touches more than three files or runs longer than ~5 minutes of agent time, the agent must first enter Plan Mode (read-only — no Edit, no Write, no shell side-effects), produce an explicit plan with numbered steps, verification commands, and an `Out of scope` list, secure human approval, then execute the locked plan. The agent is forbidden from re-planning silently mid-execution; any deviation requires a new approved plan, not an in-flight pivot. Locking the plan before execution closes the prompt-injection window, because untrusted data the model encounters during execution cannot rewrite the agreed steps.

## Why

Anthropic's Claude Code research (Boris Cherny's published numbers) reports Plan Mode raises multi-file task success rates 2-3×; the broader plan-then-execute literature (agentic-patterns.com, kilo.ai) measures tool-use accuracy moving from 72% to 94% when planning is enforced as a separate phase. The mechanism is simple: tools that can do harm are disabled until the human sees the diff in advance. A read-only planning surface also lets the human catch scope creep ("you forgot the auth migration") before any file is touched, when the cost of a fix is one comment, not a revert. The same boundary stops a prompt-injected document from steering the agent off-script: by the time the agent reads it, the plan is frozen.

## When To Use

- Multi-file refactors and renames touching > 3 files.
- Schema migrations, framework upgrades, dependency major bumps with call-site rewrites.
- Anything with security or data implications (auth, secrets handling, PII flows, prod migrations).
- Long autonomous runs where the human will not review every diff line live.
- Cross-repo changes (worktree fan-out, multi-package monorepo edits).

## When NOT To Use

- Trivial single-line edits (typo, log-string change) — plan ceremony exceeds the change.
- Inline autocomplete in an IDE (no autonomous loop, human reviews each suggestion).
- Throwaway scratch sessions on a feature branch that will be force-deleted.
- Tasks already gated by `tasks.md` from spec-kit — that artifact is the plan; do not double-plan.

## Content

| File | What's inside |
|------|---------------|
| `content/01-plan-mode-contract.xml` | The read-only-during-planning rule and the four required plan sections (steps, verification, out-of-scope, rollback). |
| `content/02-no-silent-replan.xml` | Why mid-execution re-planning is forbidden and how the agent must surface deviations as a new plan request. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plan.md` | Skeleton plan document with the four required sections, ready to paste into the chat. |
