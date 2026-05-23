# Harden an agent against prompt injection and jailbreak across tool boundaries

**Playbook slug:** `agent-prompt-injection-jailbreak-hardening`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Agent with file-read / web-fetch / MCP tools → survives indirect-prompt-injection red-team without exfiltrating data, escalating permissions, or breaking refusal policy.

## Scope

Agent with file-read / web-fetch / MCP tools survives an indirect-prompt-injection red-team suite without exfiltrating data, escalating permissions, or violating refusal policy.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Building a security product — out of scope
- Full red-team consulting engagement

### Prerequisites

- Agent with tools that ingest external content
- Eval harness reachable

## Success criteria

The playbook is done when:
- Indirect-injection eval suite committed
- Trust boundary documented per tool
- Refusal policy holds across boundary
- Canary exfiltration tokens deployed
- Adversarial eval gates merges

## Stages

### Stage 1: Boundary Model

**Intent:** Document trust boundaries per tool.

**Tasks:**
- Bundle-vs-split tools with trust in mind
- Idempotent writes with auth checks
- Cheap guardrail tripwires on ingested content

**Methodologies in chain:**
- `bundle-vs-split-tools` → `geek/ai/ai-agents/bundle-vs-split-tools`
- `idempotent-write-tools` → `geek/ai/ai-agents/idempotent-write-tools`
- `cheap-guardrail-tripwire` → `geek/ai/ai-agents/cheap-guardrail-tripwire`

**Outputs:**
- Trust boundary table

**Decision gate:**
> Advance only when every tool has a documented boundary.

### Stage 2: Refusal & Output

**Intent:** Strict refusal field + discriminated union.

**Tasks:**
- Strict refusal schema
- Discriminated union output

**Methodologies in chain:**
- `refusal-field-strict-schema` → `geek/ai/ai-agents/refusal-field-strict-schema`
- `discriminated-union-output` → `geek/ai/ai-agents/discriminated-union-output`

**Outputs:**
- Hardened output schema

**Decision gate:**
> Advance only when schema enforces refusal explicitly.

### Stage 3: Red-Team

**Intent:** Run injection + jailbreak suite via chaos eval.

**Tasks:**
- Chaos-eval with injection payloads
- Wire canary tokens for exfil detection

**Methodologies in chain:**
- `chaos-eval-fault-injection` → `geek/ai/ai-agents/chaos-eval-fault-injection`

**Outputs:**
- Red-team eval results

**Decision gate:**
> Advance only when suite catches at least one planted attack.

### Stage 4: Gate

**Intent:** Make adversarial eval block merges.

**Tasks:**
- Wire CI to fail on suite regression
- Document rollback for guardrails

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- CI gate active

**Decision gate:**
> Ship only after a known-bad PR is correctly blocked.

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
- **indirect-prompt-injection-defense** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **tool-trust-boundary-model** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **jailbreak-eval-suite-bootstrap** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **data-exfiltration-canary-tokens** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Trust boundary modelling first. Without explicit trust boundaries per tool, every guardrail is a patch on a flawed mental model. File-read of user-uploaded content, web-fetch of arbitrary URLs, and MCP tools that consume external messages are all untrusted; the agent must treat their outputs as input to be inspected, not instructions to be followed.

Refusal field strict schema is the second layer. A refusal must be a first-class structured output, not a model-style apology paragraph. The discriminated-union output type forces the agent to declare 'I am refusing' rather than emitting plausible-sounding compliance text.

Red-team with chaos-eval. Inject prompt-injection payloads into the same harness that runs other adversarial cases; without this, you ship a hardening that nobody tests next week. Plant canary tokens that the agent must never emit; if the canary appears in any response, you have an exfiltration leak.

Idempotent writes with auth checks block escalation. A tool that performs destructive actions must require an explicit confirm token in the same tool call; an injected prompt cannot manufacture a confirm token from a user input. Cheap guardrail tripwires inspect ingested content for common injection patterns before the LLM sees them; they fail open by design, but they catch the cheap attacks for free.

Brainstorm flags indirect-prompt-injection defense, tool-trust-boundary model, jailbreak eval-suite bootstrap, and data-exfiltration canary tokens as the four open gaps. Pin the CI gate so the suite blocks merges.

## CLI usage

```
faion get-content agent-prompt-injection-jailbreak-hardening --format md       # human-readable rendering
faion get-content agent-prompt-injection-jailbreak-hardening --format context  # agent-optimised context bundle
faion get-content agent-prompt-injection-jailbreak-hardening --format json     # raw structured form
```
