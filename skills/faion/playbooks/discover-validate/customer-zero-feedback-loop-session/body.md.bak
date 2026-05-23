# Customer-zero feedback loop session

**Playbook slug:** `customer-zero-feedback-loop-session`  
**Tier:** geek  
**Complexity:** light  
**Persona:** P7 — LLM Agent Developer

## Intent

30-90 min with one design partner → N failure modes captured, turned into eval rows + roadmap items before session ends.

## Scope

30-90 min sit with one design-partner customer, capture failure modes from their last week, turn N of them into eval rows + roadmap items before the session ends.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Generic discovery interviewing — see solo playbooks
- Pricing conversations

### Prerequisites

- A signed design-partner customer
- Eval harness reachable

## Success criteria

The playbook is done when:
- ≥5 failure modes captured verbatim
- Each turned into an eval row or roadmap item
- Trust signal: customer leaves with a citation back to the source

## Stages

### Stage 1: Listen

**Intent:** Capture failure modes from last week.

**Tasks:**
- Walk last 5 production trajectories together
- Ask 'what did you expect vs what happened'

**Methodologies in chain:**
- `trajectory-eval-otel` → `geek/ai/ai-agents/trajectory-eval-otel`
- `llm-observability` → `geek/ai/ml-engineer/llm-observability`

**Outputs:**
- Verbatim failure list

**Decision gate:**
> Advance only when at least 3 concrete failures captured.

### Stage 2: Convert

**Intent:** Verbatim → eval row + roadmap entry.

**Tasks:**
- Add eval row per failure
- Score with judge rubric
- Add roadmap entry if needed

**Methodologies in chain:**
- `llm-judge-rubric-evidence-first` → `geek/ai/ai-agents/llm-judge-rubric-evidence-first`
- `evaluation-framework` → `geek/ai/ml-ops/evaluation-framework`
- `rag-eval-production-monitoring` → `geek/ai/rag-engineer/rag-eval-production-monitoring`

**Outputs:**
- New eval rows committed

**Decision gate:**
> Advance only after each failure is mapped to an artefact.

### Stage 3: Close Loop

**Intent:** Show customer the eval rows landed.

**Tasks:**
- Send commit hashes
- Schedule next session

**Methodologies in chain:**
- (no methodology chain — stage is operator-only)

**Outputs:**
- Customer follow-up note

**Decision gate:**
> Close session only when customer sees their citation back to source.

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
- **design-partner-session-template** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **verbatim-to-eval-row-recipe** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## Operator notes

Time-boxed. 30 minutes minimum (one customer ready), 90 minutes maximum (do not let it sprawl). The point is to convert customer language into shipped artefacts in the same sitting, not to schedule follow-up calls.

Walk the actual trajectories together. Do not ask the customer 'what did you not like' — that produces generalities. Show them last week's traces and ask 'what did you expect to happen at turn 4?'. Specific traces produce specific failure modes; specific failure modes produce specific eval rows. Brainstorm flags the design-partner session template and verbatim-to-eval-row recipe as open gaps; until written, follow the trace-walk pattern.

Convert in the room. The cheapest failure mode is leaving with a list of 'things to look at'. The session is over only when the eval rows are committed (commit hash in hand) or the roadmap entries created (ticket number in hand). Show the customer the citation back to the source; trust is reciprocal.

Close the loop next week. The customer who sees their failure mode appear as a regression eval row becomes the highest-leverage source you have. The customer who sees nothing concrete after three sessions becomes the churn risk. Treat the close-loop email as a deliverable, not a courtesy.

## CLI usage

```
faion get-content customer-zero-feedback-loop-session --format md       # human-readable rendering
faion get-content customer-zero-feedback-loop-session --format context  # agent-optimised context bundle
faion get-content customer-zero-feedback-loop-session --format json     # raw structured form
```
