# Creating or Updating Claude Code Agents

## Summary

**One-sentence:** Spec + config for Claude Code subagents: isolated context, whitelisted tools, designated role, decision rule when to use Agent vs Skill vs Command.

**One-paragraph:** Claude Code agents (subagents) are autonomous workers with dedicated context windows, whitelisted tools, and a designated role. Misusing the Task tool — wrapping a 1-step query in an agent, sharing mutable state with the parent, expecting interactive input mid-run — wastes 5-30K tokens per call. This methodology codifies the Agent / Skill / Command decision tree, the agent.md frontmatter, the tool-whitelisting rule, and the IPC-via-files pattern. Output is an agent definition file + a validator that checks the frontmatter shape.

**Ефективно для:**

- Параллельні незалежні задачі: 3+ модулі одночасно — Task tool fan-out.
- Context isolation: research subagent не отруює primary context window.
- Sequential pipeline stages: spec → design → impl → test — кожен у своєму context'і.
- Long-running background research / scraping / report-generation з orchestrator'а.

## Applies If (ALL must hold)

- Task has clear single-shot semantics (no interactive input needed).
- Subtask benefits from context isolation (research, code review, long synthesis).
- Tool surface for the subtask can be tightly whitelisted (≤ 5 tools typically).

## Skip If (ANY kills it)

- Single-step task that completes in one tool call — agent overhead unjustified.
- Subtask requires interactive user input mid-execution — agents run autonomously.
- Real-time streaming output required — Task tool is async; results return on completion.
- Subtask needs shared mutable in-memory state with the parent — agents are isolated; use files as IPC.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subtask spec | Markdown / prompt | task definition |
| Tool whitelist | list of allowed tools | from subtask spec |
| Output contract | JSON schema or Markdown | consumer of agent result |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: agent-vs-skill-vs-command, whitelist-tools-min, ipc-via-files-not-memory, output-contract-required, no-interactive-mid-run | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-agent-vs-alternative` | sonnet | Decision tree application. |
| `declare-frontmatter` | haiku | Template fill. |
| `write-agent-body` | sonnet | Prompt writing needs light judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent.md` | Agent definition template (frontmatter + role + inputs + steps + output contract) |
| `templates/agent-code-reviewer.md` | Worked example: code-reviewer subagent |
| `templates/agent-research.md` | Worked example: research subagent (Read+WebFetch only) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[commands]]
- [[skills]]
- [[hooks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
