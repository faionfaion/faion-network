---
name: faion
description: "Retrieve relevant methodology context from the faion knowledge umbrella based on the current Claude Code session topic. Spawns a read-only Agent SDK subagent that searches knowledge/ and returns a curated bundle that fits a word budget."
tier: free
user-invocable: true
allowed-tools: Bash(python3:*)
---

# Faion knowledge retrieval

This skill spawns a read-only Agent SDK subagent (Sonnet) that:

1. reads the current session transcript (user + assistant text only — no tool calls, no system reminders)
2. searches `knowledge/` (cwd-scoped) for relevant methodology files
3. either:
   - calls `submit_selection` (validates word budget; retries if over) → returns `<faion_knowledge>` bundle, OR
   - calls `request_clarification` → returns `<faion_clarification>` with questions for the user

The output below is XML.
- If `<faion_knowledge>` — read each `<document>` as relevant context. Inlined `<faion-methodology slug="...">` blocks are pre-parsed methodology bodies (metadata stripped); treat them as the primary content.
- If `<faion_clarification>` — follow the `<instruction_to_main_agent>` block: ask the user via AskUserQuestion using the embedded questions, append their answers to the conversation, then re-invoke `/faion`.

```!
python3 ~/workspace/projects/faion-net/faion-network/skills/faion/scripts/retrieve.py "${CLAUDE_SESSION_ID:-}"
```

## Playbooks

Beyond knowledge methodologies, the faion umbrella also hosts **tier playbooks** at `playbooks/<tier>/<group>/<slug>/playbook.md`. Playbooks are standalone how-to guides (e.g., "Buy a domain on Namecheap", "Build an MCP server", "First hire developer") — one task, one tier, one folder.

Tier-gated on the same boundary as knowledge: free reads `playbooks/free/`; solo reads `free/ + solo/`; pro reads `free/ + solo/ + pro/`; geek reads all four. Each playbook MUST cite ≥1 methodology from `knowledge/<tier ≤ playbook tier>/`.

Spec: [`.aidocs/conventions/playbooks/playbook-spec.md`](../../.aidocs/conventions/playbooks/playbook-spec.md). Validator: `python3 scripts/validate-tier-playbook.py <path>`.

