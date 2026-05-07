# AI Agents Skill

> **Entry Point:** Invoked via [/faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)

## When to Use

- Building autonomous AI agents
- Multi-agent system design
- LangChain agent implementation
- LlamaIndex agent patterns
- MCP (Model Context Protocol) integration
- Agent architectures (ReAct, plan-and-execute)
- EU AI Act compliance for agents

## Overview

Specializes in AI agent development and orchestration.

**Methodologies:** 84 | **Focus:** Agents, frameworks, MCP, structured-output, multi-model, planning, memory, eval, cost, prompts

## Quick Reference

| Area | Files |
|------|-------|
| Basics | ai-agent-patterns.md, agent-patterns.md, autonomous-agents.md |
| Multi-agent | multi-agent-basics.md, multi-agent-patterns.md |
| LangChain | langchain-basics.md, langchain-agents-architectures.md, langchain-chains.md |
| LlamaIndex | llamaindex-basics.md, llamaindex-agents-eval.md |
| MCP | mcp-model-context-protocol.md, mcp-ecosystem-2026.md |
| Governance | eu-ai-act-compliance-2026.md |
| Structured output (so-) | schema-field-order, weak-model-preselection, refusal-field-strict-schema, schema-version-pinning, structured-output-mode-picker, ... |
| Multi-model (mm-), tool-use (tu-), planning (pl-) | weak-model-preselection, file-reference-passing, ... (see folder index) |
| Long-running (lp-), memory (mem-), CLI (cli-) | (see folder index) |
| Eval (eval-), cost (cost-), MCP (mcp-) | cheap-guardrail-tripwire, ... (see folder index) |

## Methodology Count

- Legacy heavy-format (pre-2026-04): 31 methodologies
- New shape (2026-04 brainstorm batch): 53 methodologies in 10 categories (so/mm/tu/pl/lp/mem/cli/eval/cost/mcp)

**Total: 84**

The new-shape methodologies use `methodology.xml` (closed semantic XML vocabulary) instead of the 5-file legacy pattern. Public-reader articles for the 53 new entries are mapped at `faion-net-fe/content/knowledge/agents/MAP.md` (`AGT-A-001`..`AGT-A-053`).

## Agent Patterns

- **ReAct:** Reasoning + Acting loop
- **Plan-and-Execute:** Upfront planning, sequential execution
- **Reasoning-First:** Extended thinking before action
- **Multi-Agent:** Delegation, collaboration, specialization

## Related

- Parent: [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md)
- Uses: faion-llm-integration (tool calling)
- Peers: faion-rag-engineer (agentic RAG)

---

*AI Agents v1.0*
