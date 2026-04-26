# AI-Assisted Development

## Summary

Patterns for using AI coding assistants (Claude Code, Cursor, Copilot) effectively: match tool to task type, use structured prompts, always review AI output before accepting, and never auto-accept security-critical code. AI increases defect rate 4x when used without review discipline.

## Why

AI tools have different strengths: Claude Code for long-context planning and refactors, Cursor for flow-state implementation, Copilot for inline boilerplate. Mismatching tool to task produces inferior output. Structured prompts (context / task / requirements / output format) reduce vagueness that causes generic or incorrect code. Human review remains mandatory — AI-generated tests can certify their own incorrect output as passing.

## When To Use

- Setting up a project workflow where Claude Code, Cursor, or Copilot will be primary development tools.
- Deciding which AI tool to assign to which task type (planning vs. implementation vs. autocomplete).
- Building a CI step that uses AI for automated test generation or code review commentary.
- Onboarding a developer to AI coding tools — establishing safe review habits from the start.

## When NOT To Use

- Security-critical auth or payment logic where AI-suggested code must never be accepted without line-by-line human review.
- Compliance-sensitive environments (healthcare, finance) where AI tool output has not been approved by legal/compliance.
- Teams lacking the experience to review AI output critically — premature AI adoption creates hidden defect accumulation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-selection.xml` | Tool comparison matrix (Claude Code / Cursor / Copilot), when to use each, combination workflow. |
| `content/02-prompt-engineering.xml` | Structured prompt template, iteration strategy, security review requirements. |
| `content/03-test-generation.xml` | AI test generation workflow, self-certification risk, coverage gap analysis patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gen-tests.sh` | Bash script: calls Claude Code in --print mode to generate pytest test stubs for a source file. |
| `templates/prompt-code.txt` | Structured code-generation prompt template (context / task / requirements / output). |

## Scripts

none
