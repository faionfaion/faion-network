# Multi-model gateway migration: lock-in to portability (2 months)

**Playbook slug:** `multi-model-gateway-migration-portability`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Vendor-locked agent → portable runtime where Anthropic / OpenAI / local LLM swap per-step or per-tenant with fallback, cost-aware routing, unchanged eval bar.

## Scope

Move a single-vendor agent (e.g. Anthropic-only) to a portable runtime where Anthropic / OpenAI / local LLM can be swapped per-step or per-tenant, with fallback chain, cost-aware routing, and unchanged eval bar.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Building a public LLM gateway product — out of scope
- Custom inference infra — use Ollama / vendor APIs

### Prerequisites

- Working vertical agent on one vendor
- Eval harness passing the playbook 1 bar

## Success criteria

The playbook is done when:
- All call sites go through gateway adapter
- Two vendors live + one local fallback
- Router policy documented + tested
- Eval suite passes on each backend
- Cost-aware routing reduces $/success

## Stages

### Stage 1: Adapter Layer

**Intent:** Centralize provider calls behind a single adapter.

**Tasks:**
- Wrap Claude API behind adapter
- Add OpenAI adapter
- Pick MCP-gateway composition if applicable

**Methodologies in chain:**
- `claude-api-integration` → `geek/ai/llm-integration/claude-api-integration`
- `openai-api-integration` → `geek/ai/llm-integration/openai-api-integration`
- `gemini-api-integration` → `geek/ai/llm-integration/gemini-api-integration`
- `mcp-gateway-composition` → `geek/ai/ai-agents/mcp-gateway-composition`
- `function-calling-patterns` → `geek/ai/llm-integration/function-calling-patterns`
- `tool-use-basics` → `geek/ai/llm-integration/tool-use-basics`
- `structured-output-basics` → `geek/ai/llm-integration/structured-output-basics`
- `structured-output-patterns` → `geek/ai/llm-integration/structured-output-patterns`
- `structured-output-mode-picker` → `geek/ai/ai-agents/structured-output-mode-picker`
- `semantic-xml-content` → `geek/ai/llm-integration/semantic-xml-content`

**Outputs:**
- Adapter module
- Call-site sweep diff

**Decision gate:**
> Advance only when all call sites route through adapter.

### Stage 2: Local Fallback

**Intent:** Ollama-backed local LLM as deterministic fallback.

**Tasks:**
- Stand up Ollama deployment
- Pick + tune local model
- Wire tool calling

**Methodologies in chain:**
- `local-llm-ollama` → `geek/ai/llm-integration/local-llm-ollama`
- `ollama-setup-models` → `geek/ai/ml-engineer/ollama-setup-models`
- `ollama-deployment` → `geek/ai/ml-engineer/ollama-deployment`
- `ollama-prompt-engineering` → `geek/ai/ml-engineer/ollama-prompt-engineering`
- `ollama-python-client` → `geek/ai/ml-engineer/ollama-python-client`
- `ollama-tool-calling` → `geek/ai/ml-engineer/ollama-tool-calling`
- `ollama-agent-integration` → `geek/ai/ml-engineer/ollama-agent-integration`

**Outputs:**
- Local LLM endpoint
- Cost+latency baseline

**Decision gate:**
> Advance when local backend passes ≥X% of eval set.

### Stage 3: Routing

**Intent:** Cost-aware + preference-trained routing across backends.

**Tasks:**
- Wire gateway fallback chain
- Add preference-trained router
- Reuse previous response ids where available

**Methodologies in chain:**
- `gateway-fallback-chain` → `geek/ai/ai-agents/gateway-fallback-chain`
- `preference-trained-router` → `geek/ai/ai-agents/preference-trained-router`
- `previous-response-id-reasoning-reuse` → `geek/ai/ai-agents/previous-response-id-reasoning-reuse`
- `weak-model-preselection` → `geek/ai/ai-agents/weak-model-preselection`

**Outputs:**
- Routing policy doc
- Shadow A/B fixture

**Decision gate:**
> Promote routing rule only after shadow A/B beats baseline.

### Stage 4: Eval Parity

**Intent:** Run eval suite on each backend; lock the bar.

**Tasks:**
- Run suite on each backend
- Replay traces with record-replay
- Lock schema versioning

**Methodologies in chain:**
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`
- `schema-version-pinning` (GAP — see below)
- `model-evaluation` → `geek/ai/ml-engineer/model-evaluation`
- `llm-observability-stack` → `geek/ai/ml-engineer/llm-observability-stack`
- `evaluation-benchmarks` (GAP — see below)
- `rag-eval-ab-testing` → `geek/ai/rag-engineer/rag-eval-ab-testing`

**Outputs:**
- Cross-backend eval table
- Schema pin manifest

**Decision gate:**
> Promote only when each backend meets minimum bar.

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
- **vendor-feature-portability-matrix** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **router-shadow-deploy-protocol** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **eu-sovereign-llm-deployment-bundle** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content multi-model-gateway-migration-portability --format md       # human-readable rendering
faion get-content multi-model-gateway-migration-portability --format context  # agent-optimised context bundle
faion get-content multi-model-gateway-migration-portability --format json     # raw structured form
```
