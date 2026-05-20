# Fine-tune vs prompt-engineer decision flow (4 weeks worst case)

**Playbook slug:** `fine-tune-vs-prompt-decision-flow`  
**Tier:** geek  
**Complexity:** deep  
**Persona:** P7 — LLM Agent Developer

## Intent

Stuck on prompt iteration → clear go/no-go on fine-tuning with LoRA SFT/DPO data prep, training, eval, or documented stay on prompt+retrieval.

## Scope

Structured decision and execution path: from baseline scorecard to a clear go/no-go on fine-tuning, including LoRA SFT/DPO data prep, training, eval, and deployment — or staying with prompt+retrieval if economics don't beat the floor.

### What this playbook covers

This is a chain of existing faion methodologies tailored for an LLM-agent developer building production agent systems. Each stage ends in an explicit decision gate; the chain assumes a small team with at least one engineer responsible for the agent end-to-end. Brainstorm intent angle and full methodology list are preserved in the manifest.

### Non-goals

- Full RLHF pipeline from scratch — out of scope
- Pretraining new base models — out of scope

### Prerequisites

- Baseline prompt agent in production with logs
- Sandbox account with fine-tuning quota

## Success criteria

The playbook is done when:
- Written decision (tune / stay) with cost+quality table
- If tune: SFT/DPO dataset prepared, trained, evaluated, shadow-deployed
- Regression eval gate held throughout
- Cost-per-success better OR documented why we accepted parity

## Stages

### Stage 1: Baseline

**Intent:** Record current cost+quality baseline on golden set.

**Tasks:**
- Run cost+quality baseline
- Score against decision framework
- Mine production traces for candidate training data

**Methodologies in chain:**
- `llm-decision-framework` → `geek/ai/ml-engineer/llm-decision-framework`
- `decision-framework` → `geek/ai/ml-engineer/decision-framework`
- `cost-optimization` → `geek/ai/ml-engineer/cost-optimization`
- `cost-reduction-strategies` → `geek/ai/ml-ops/cost-reduction-strategies`
- `prompt-engineering-evaluation` → `geek/ai/ml-engineer/prompt-engineering-evaluation`
- `record-replay-debugging` → `geek/ai/ai-agents/record-replay-debugging`

**Outputs:**
- Baseline scorecard
- Training-candidate trace set

**Decision gate:**
> Advance to Decide if a tune candidate beats the floor in projection.

### Stage 2: Decide Tune-Or-Not

**Intent:** Apply tune-vs-prompt rubric on projected ROI.

**Tasks:**
- Estimate fine-tune cost
- Estimate quality lift on eval
- Write decision doc with rubric

**Methodologies in chain:**
- `finetuning` → `geek/ai/ml-engineer/finetuning`
- `fine-tuning-openai-basics` → `geek/ai/ml-ops/fine-tuning-openai-basics`
- `finetuning-basics` → `geek/ai/ml-ops/finetuning-basics`
- `role-specialized-models` → `geek/ai/ai-agents/role-specialized-models`
- `confidence-thresholded-cascade` → `geek/ai/ai-agents/confidence-thresholded-cascade`

**Outputs:**
- Tune-vs-prompt decision doc

**Decision gate:**
> If tune doesn't beat floor by ≥X% projected, exit playbook with decision logged.

### Stage 3: Data Prep

**Intent:** SFT and DPO dataset hygiene.

**Tasks:**
- Build SFT dataset from traces
- Add DPO pairs for preference signal
- Document dataset provenance

**Methodologies in chain:**
- `fine-tuning-openai-data-prep` → `geek/ai/ml-engineer/fine-tuning-openai-data-prep`
- `fine-tuning-openai-sft` → `geek/ai/ml-engineer/fine-tuning-openai-sft`
- `fine-tuning-openai-dpo` → `geek/ai/ml-engineer/fine-tuning-openai-dpo`
- `finetuning-datasets` → `geek/ai/ml-ops/finetuning-datasets`

**Outputs:**
- SFT corpus
- DPO pair file
- Provenance log

**Decision gate:**
> Advance only after data audit and dedup pass.

### Stage 4: Train

**Intent:** LoRA or full SFT/DPO training run with eval gating.

**Tasks:**
- Pick LoRA vs full tune
- Train + checkpoint
- Score against held-out eval

**Methodologies in chain:**
- `fine-tuning-lora` → `geek/ai/ml-engineer/fine-tuning-lora`
- `lora-qlora` → `geek/ai/ml-ops/lora-qlora`
- `fine-tuning-openai-production` → `geek/ai/ml-ops/fine-tuning-openai-production`

**Outputs:**
- Trained checkpoint
- Eval report

**Decision gate:**
> Promote only checkpoints beating baseline on golden + adversarial.

### Stage 5: Deploy

**Intent:** Shadow-deploy, then promote if eval-in-prod holds.

**Tasks:**
- Shadow-deploy tuned model
- Compare on live traffic in-shadow
- Promote and pin schema

**Methodologies in chain:**
- `fine-tuning-openai-eval` → `geek/ai/ml-engineer/fine-tuning-openai-eval`
- `fine-tuning-openai-deployment` → `geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `schema-version-pinning` → `geek/ai/ai-agents/schema-version-pinning`

**Outputs:**
- Shadow report
- Promotion decision

**Decision gate:**
> Promote only after shadow holds for ≥1 release cycle.

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
- **fine-tune-vs-prompt-economic-model** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **production-trace-mining-for-training-data** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)
- **tuned-model-shadow-deploy-protocol** (tier `geek`) — required by playbook chain (see brainstorm-2026-05-17)

## CLI usage

```
faion get-content fine-tune-vs-prompt-decision-flow --format md       # human-readable rendering
faion get-content fine-tune-vs-prompt-decision-flow --format context  # agent-optimised context bundle
faion get-content fine-tune-vs-prompt-decision-flow --format json     # raw structured form
```
