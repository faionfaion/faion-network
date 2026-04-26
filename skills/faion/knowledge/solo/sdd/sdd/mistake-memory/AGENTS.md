# Mistake Memory

## Summary

Mistake Memory is the SDD practice of documenting failures in `.aidocs/memory/mistakes.md` immediately after they occur and injecting relevant warnings into agent context before similar tasks. Each entry requires: severity, what happened, root cause (Five Whys chain, min 3 levels), and one concrete prevention step. Generic preventions ("be more careful") are not acceptable.

## Why

LLM agents are stateless across sessions — they repeat the same error categories without a persistent record. Research confirms over-confidence and hallucination rates that make unguided retries ineffective. A keyword-indexed mistakes file gives the executor agent domain-specific warnings at task start, reducing recurrence. The second occurrence of a pattern triggers a mandatory CI rule, not just a doc update.

## When To Use

- Before starting any task: load `.aidocs/memory/mistakes.md` and filter entries matching the task's domain keywords
- After a task fails (CI failure, production bug, review rejection): append a new MIS-NNN entry within 24 hours
- When the same failure pattern occurs a second time: escalate to an automated prevention rule in CI
- When onboarding a new agent: include mistakes.md in the project context handoff

## When NOT To Use

- For tracking product bugs in a bug tracker — mistakes.md captures LLM/agent execution patterns, not feature defects
- When the project has fewer than 3 completed tasks — corpus too thin for useful patterns
- As a replacement for post-mortems on infrastructure incidents (mistakes.md is development-workflow scoped)

## Content

| File | What's inside |
|------|---------------|
| `content/01-capture-rules.xml` | When and how to capture a mistake; Five Whys requirement; entry quality rules |
| `content/02-error-categories.xml` | LLM-specific error taxonomy: hallucination, context loss, scope creep, missing validation |
| `content/03-prevention-layers.xml` | Four prevention layers: pre-task warnings, quality gates, CI rules, multi-model review |

## Templates

| File | Purpose |
|------|---------|
| `templates/mistake-entry.md` | MIS-NNN entry template with all required fields |
| `templates/inject-warnings.sh` | Bash script for keyword-based mistake injection before task start |
