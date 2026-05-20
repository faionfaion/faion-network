# Make faion a programmatic context source for an agent

**Playbook slug:** `faion-as-programmatic-context-source`  
**Tier:** pro  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Agent builder wires faion CLI as structured methodology lookup → no markdown parsing, emits faion-citation tokens.

## Scope

Agent builder wires faion CLI as a structured methodology lookup inside their agent (RAG-as-a-service / SDR / code-review bot) without parsing human-readable markdown, and emits faion-citation tokens in agent output.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Building a public faion API wrapper SDK — out of scope
- End-user-facing search UI

### Prerequisites

- Faion CLI installed and authenticated
- Agent with tool-call support

## Success criteria

The playbook is done when:
- Faion exposed as a tool the agent can call
- Agent receives JSON, not markdown
- Citation tokens emitted with version + content_id
- Eval row asserting citation contract

## Stages

### Stage 1: Tool Wrap

**Intent:** Wrap faion CLI as an agent tool with strict schema.

**Tasks:**
- Discriminated-union output for tool result
- Strict required fields
- Structured errors

**Methodologies in chain:**
- `discriminated-union-output` → `geek/ai/ai-agents/discriminated-union-output`
- `strict-mode-required-fields` → `geek/ai/ai-agents/strict-mode-required-fields`
- `structured-tool-errors` → `geek/ai/ai-agents/structured-tool-errors`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`

**Outputs:**
- Tool wrapper module

**Decision gate:**
> Advance only when contract tests pass on the wrapper.

### Stage 2: Context Hygiene

**Intent:** Manifest-then-fetch + progressive disclosure to keep context lean.

**Tasks:**
- Manifest-then-fetch pattern
- Progressive disclosure of skills
- Auto-evict tool results
- Prompt-cache prefix order

**Methodologies in chain:**
- `manifest-then-fetch` → `geek/ai/ai-agents/manifest-then-fetch`
- `progressive-disclosure-skills` → `geek/ai/ai-agents/progressive-disclosure-skills`
- `auto-evict-tool-results` → `geek/ai/ai-agents/auto-evict-tool-results`
- `prompt-cache-prefix-order` → `geek/ai/ai-agents/prompt-cache-prefix-order`

**Outputs:**
- Context-pruning rules

**Decision gate:**
> Advance only when context budget holds on the longest trace.

### Stage 3: Citation Contract

**Intent:** Emit faion citation tokens with content_id + version.

**Tasks:**
- Define citation token schema
- Wire emission in agent output
- Eval that asserts citations are present + traceable

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Citation schema doc
- Eval row

**Decision gate:**
> Ship only when eval asserts every grounded answer has a citation.

## Common pitfalls

- Treating eval scores as ground truth without judge calibration
- Shipping prompt or model changes without a regression gate
- Skipping shadow rollout for routing or model swaps

## Quality checklist (self-review)

- Can I roll back this change in one step?
- Is the regression eval committed BEFORE the fix?
- Are tool / schema versions pinned in the manifest?

## Related playbooks

- `eval-harness-continuous-benchmark-suite`
- `agent-observability-drift-detection-rollout`
- `production-agent-eval-harness-week-1`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **methodology-as-json-feed** (tier `pro`) — required by playbook chain (see brainstorm-2026-05-17)
- **faion-cli-agent-adapter-pattern** (tier `pro`) — required by playbook chain (see brainstorm-2026-05-17)
- **citation-contract-back-to-source** (tier `pro`) — required by playbook chain (see brainstorm-2026-05-17)
- **methodology-versioning-and-changelog** (tier `pro`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content faion-as-programmatic-context-source --format md       # human-readable rendering
faion get-content faion-as-programmatic-context-source --format context  # agent-optimised context bundle
faion get-content faion-as-programmatic-context-source --format json     # raw structured form
```
