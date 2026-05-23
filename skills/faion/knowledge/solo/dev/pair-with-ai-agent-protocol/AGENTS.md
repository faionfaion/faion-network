---
slug: pair-with-ai-agent-protocol
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Runs an AI coding agent as a junior pair: scopes one task, names the artefact, sets explicit halt points for human review, and logs every command before commit.
content_id: "c041531f78c356bd"
complexity: medium
produces: checklist
est_tokens: 4300
tags: [ai-agent, pair-programming, protocol, human-in-the-loop, claude-code]
---
# Pair with AI Agent Protocol

## Summary

**One-sentence:** Runs an AI coding agent as a junior pair: scopes one task, names the artefact, sets explicit halt points for human review, and logs every command before commit.

**One-paragraph:** Runs an AI coding agent as a junior pair: scopes one task, names the artefact, sets explicit halt points for human review, and logs every command before commit. A bounded loop: human states intent + acceptance test, agent proposes plan, human ratifies, agent edits, human reviews diff, agent commits only after sign-off. Eliminates 'agent went off-script'. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Coding agent (Claude Code, Cursor, Aider) is doing 30%+ of the keystrokes on the change.
- Change touches a critical path (auth, payments, migrations) where silent agent drift is unsafe.
- Team has not yet codified how to bound an agent session and review its output.
- Output produces `checklist` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Coding agent (Claude Code, Cursor, Aider) is doing 30%+ of the keystrokes on the change.
- Change touches a critical path (auth, payments, migrations) where silent agent drift is unsafe.
- Team has not yet codified how to bound an agent session and review its output.

## Skip If (ANY kills it)

- Agent is only used for inline completions (Copilot ghost text) — no need for a session protocol.
- Greenfield throwaway prototype with no production users — overhead doesn't pay back.
- Pure documentation-only edits where the agent cannot create silent runtime bugs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task acceptance criteria | Markdown | Linked issue/spec |
| Agent transcript channel | file or chat log | Claude Code session log |
| Repo branch | git branch | feature branch off main |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[code-review-process]] | Human reviewer still applies the standard review bar. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | opus | Decompose the intent and propose changes plus tests; high-stakes step. |
| `edit-step` | sonnet | Mechanical edits inside the planned scope. |
| `review-step` | opus | Human-equivalent diff review; called only when human asks for second opinion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/session_protocol.md` | Markdown skeleton for the artefact. |
| `templates/halt_log.json` | JSON template scaffolding the artefact contract. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pair-with-ai-agent-protocol.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[code-review-process]]
- [[prompt-patterns-for-common-dev-tasks]]
- [[claude-code-skills-authoring]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the agent making non-trivial code or system changes (commits, migrations, deploys)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
