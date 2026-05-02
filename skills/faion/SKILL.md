---
name: faion
description: "Faion umbrella for solopreneur dev work. AUTO-INVOKE on ANY of: (a) domain methodology lookup across 52 knowledge bases (Python, JS, infra, AI, BA, PM, marketing, UX, etc.); (b) tier-playbook how-to (120 standalone guides — 'how to buy a domain', 'how to build an MCP server'); (c) multi-agent brainstorming / diverge-converge / 'give me 10 ideas' (MUST ASK USER FIRST if brainstorm wasn't explicitly requested); (d) single-feature or batch SDD execution (study → clarify → plan → wave-execute → verify → review → fix → close); (e) session-based improvement / system audit / 'що ми зробили' / 'find issues'; (f) AI media pipeline construction (TG channel + site + automation); (g) self-replenishing background agent pool for long task queues. Reads workflows/AGENTS.md to pick the right pattern, then loads the workflow's AGENTS.md and content."
tier: free
user-invocable: true
allowed-tools: Bash(python3:*)
---

# Faion umbrella

Single entry point for the entire faion knowledge + workflow stack. Auto-invokes on a wide range of triggers — see `description` above for the full routing surface.

## Routing

When invoked, decide what the user needs and read the right entry point:

| Signal | Read |
|--------|------|
| Methodology question (Python/JS/infra/AI/BA/PM/marketing/UX) | `knowledge/<tier>/<group>/<name>/` (start with this skill's retrieval pipeline below) |
| "How to do X" — concrete task with steps | `playbooks/<tier>/<group>/<slug>/playbook.md` |
| Workflow needed (brainstorm / SDD batch / improver / media pipeline / agent pool) | `workflows/AGENTS.md` to pick + load |

## Knowledge retrieval pipeline (default behaviour)

When the user has a domain question and no specific workflow trigger fired, spawn a read-only Agent SDK subagent that:

1. reads the current session transcript (user + assistant text only — no tool calls, no system reminders)
2. searches `knowledge/` (cwd-scoped) for relevant methodology files
3. either:
   - calls `submit_selection` (validates word budget; retries if over) → returns `<faion_knowledge>` bundle, OR
   - calls `request_clarification` → returns `<faion_clarification>` with questions for the user

The output is XML.
- If `<faion_knowledge>` — read each `<document>` as relevant context. Inlined `<faion-methodology slug="...">` blocks are pre-parsed methodology bodies (metadata stripped); treat them as the primary content.
- If `<faion_clarification>` — follow the `<instruction_to_main_agent>` block: ask the user via AskUserQuestion using the embedded questions, append their answers to the conversation, then re-invoke `/faion`.

```!
python3 ~/workspace/projects/faion-net/faion-network/skills/faion/scripts/retrieve.py "${CLAUDE_SESSION_ID:-}"
```

## Workflows (auto-routed)

| Trigger | Workflow folder |
|---------|-----------------|
| "brainstorm", "10 ideas", "audit X", "diverge-converge", "give me options" — and brainstorm is new in this session | `workflows/brainstorm/` (consent gate runs first if not user-initiated) |
| "виконай feature-NNN", batch of features in `.aidocs/<project>/todo/`, multi-feature SDD delivery | `workflows/sdd-batch-orchestrator/` |
| "що зробили в сесії", "audit my server", "find issues", "improve system", "what did we learn" | `workflows/improver/` |
| "новий медіа-пайплайн", "TG channel + сайт", "AI news pipeline", "media outlet" | `workflows/media-ops/` |
| "пул фонових агентів", "queue of N batches", "background pool dispatch" | `workflows/poll-agents/` |

To use a workflow: read its `AGENTS.md` (≤80 lines), then act per the phases described.

## Playbooks

Beyond knowledge methodologies, the faion umbrella also hosts **tier playbooks** at `playbooks/<tier>/<group>/<slug>/playbook.md`. Playbooks are standalone how-to guides (e.g., "Buy a domain on Namecheap", "Build an MCP server", "First hire developer") — one task, one tier, one folder.

Tier-gated on the same boundary as knowledge: free reads `playbooks/free/`; solo reads `free/ + solo/`; pro reads `free/ + solo/ + pro/`; geek reads all four. Each playbook MUST cite ≥1 methodology from `knowledge/<tier ≤ playbook tier>/`.

Spec: [`.aidocs/conventions/playbooks/playbook-spec.md`](../../.aidocs/conventions/playbooks/playbook-spec.md). Validator: `python3 scripts/validate-tier-playbook.py <path>`.
