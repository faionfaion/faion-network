---
name: faion
description: "Faion umbrella for solopreneur dev work. AUTO-INVOKE on ANY of: (a) domain methodology lookup across 20 canonical knowledge domains (~2628 methodologies — dev, backend, frontend, infra, ai-core, ai-agents, ml-engineering, sdlc-ai, pm, product, ba, marketing, research, ux, sdd, architecture, security, comms, hr, claude-code); (b) tier-playbook how-to (~455 guides at playbooks/<tier>/<group>/<slug>/) organised by 11 goal-character categories; (c) multi-agent brainstorming / diverge-converge / 'give me 10 ideas' (MUST ASK USER FIRST if brainstorm wasn't explicitly requested); (d) single-feature or batch SDD execution (study → clarify → plan → wave-execute → verify → review → fix → close); (e) session-based improvement / system audit / 'що ми зробили' / 'find issues'; (f) AI media pipeline construction (TG channel + site + automation); (g) self-replenishing background agent pool for long task queues; (h) a task-shaped need that wants a *pipeline* rather than a document — 'build a research-first product', 'run an SDD feature end to end', 'write and translate an article', 'audit this tree and fix what the audit blocks' — routed to recipes/INDEX.xml (4 composable pipelines), with fragments/INDEX.xml (role prompts) and tools/INDEX.xml (runnable scripts) beneath it. Two-level retrieval: reads L1 (knowledge/domains.xml + playbooks/taxonomy.xml + recipes/INDEX.xml) first, picks ≤3 candidate buckets, then reads only those L2 INDEX.xml before opening any leaf methodology."
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
| Methodology question | L1: `knowledge/domains.xml` → pick ≤3 domains → L2: `knowledge/<domain>/INDEX.xml` → leaf: `knowledge/<tier>/<group>/<name>/AGENTS.md` |
| "How to do X" — concrete task with steps | L1: `playbooks/taxonomy.xml` (11 goal categories) → L2: `playbooks/by-goal/<goal>/INDEX.xml` → leaf: `playbooks/<tier>/<group>/<slug>/AGENTS.md` + `content/01-playbook.xml` |
| **Build / run it, not read about it** — "build a research-first product", "run this SDD feature", "write and translate an article", "audit and fix this tree" | L2: `recipes/INDEX.xml` → leaf: `recipes/<name>/<name>.card.md`. Supporting: `fragments/INDEX.xml` (the role prompts a recipe composes) · `tools/INDEX.xml` (scripts to run instead of writing one) |
| Workflow needed (brainstorm / SDD batch / improver / media pipeline / agent pool) | `workflows/AGENTS.md` to pick + load |

A task that names a **deliverable and a pipeline to produce it** routes to recipes, not into the methodology corpus: a methodology tells you what good looks like, a recipe is the thing that runs.

**Methodology layout (v3, post-F-066):**

```
knowledge/<tier>/<group>/<slug>/
├── AGENTS.md                       # envelope: frontmatter + 11 body sections incl. ## Decision tree
└── content/
    ├── 01-core-rules.xml           # ≥5 testable rules + rationale + source
    ├── 02-output-contract.xml      # JSON Schema + valid/invalid examples
    ├── 03-failure-modes.xml        # ≥3 antipatterns (symptom/root-cause/fix)
    ├── 04-procedure.xml            # step-by-step if complexity ≥ medium
    ├── 05-examples.xml             # worked example if produces ∈ {spec, report}
    └── 06-decision-tree.xml        # MANDATORY: root-question + branches → conclusion(ref=rule-id)
├── templates/                      # real working skeletons declared in AGENTS.md
└── scripts/validate-<slug>.py      # output-contract validator if schema present
```

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

## Recipes, fragments and tools

The composable layer: pipelines an agent runs, not prose it reads. Three L2 indexes, generated from `meta.json` by `scripts/regen-fragment-index.py`.

| Index | Holds | Read the leaf as |
|-------|-------|------------------|
| `recipes/INDEX.xml` | 4 workflow recipes — `sdd-feature` (free, 6 stages), `research-first-build` (free, 13), `article-pipeline` (free, 6), `audit-and-fix` (free, 4) | `<name>.card.md` — the card is the contract and is enough to invoke from; `recipe.json` is the compiler's input, never the agent's |
| `fragments/INDEX.xml` | 6 packs of role prompts a recipe composes, addressed `corpus:<name>` | the fragment body, or `faion frag get corpus:<name>` |
| `tools/INDEX.xml` | 3 packs of dependency-free scripts | `<name>.card.md` — read the card, never the script, and never re-implement a tool that already has one |

The whole layer ships at tier **free** — the pipeline is the mechanism that makes output correct, and what a tier buys is the content a pipeline consumes, not the pipeline. A fragment's tier is still always ≤ the tier of every recipe that composes it, so picking a recipe you can read never yields a stage you cannot. Compile a recipe with `faion workflow build <recipe.json> --var …`.

## Playbooks

Beyond knowledge methodologies, the faion umbrella also hosts **tier playbooks** at `playbooks/<tier>/<group>/<slug>/playbook.md`. Playbooks are standalone how-to guides (e.g., "Buy a domain on Namecheap", "Build an MCP server", "First hire developer") — one task, one tier, one folder.

Tier-gated on the same boundary as knowledge: free reads `playbooks/free/`; solo reads `free/ + solo/`; pro reads `free/ + solo/ + pro/`; geek reads all four. Each playbook MUST cite ≥1 methodology from `knowledge/<tier ≤ playbook tier>/`.

Spec: [`.aidocs/conventions/playbooks/playbook-spec.md`](../../.aidocs/conventions/playbooks/playbook-spec.md). Validator: `python3 scripts/validate-tier-playbook.py <path>`.
