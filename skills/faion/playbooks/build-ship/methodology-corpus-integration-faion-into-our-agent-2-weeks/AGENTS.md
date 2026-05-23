# Methodology corpus integration: faion-into-our-agent (2 weeks)

**Persona:** P7 - **Tier:** geek - **Complexity:** medium - **Angle:** global

## Context

Embed the faion knowledge base as a reasoning prior for an in-house vertical agent: ingestion, chunking, retrieval, reranking, eval, plus governance / licence / drift hygiene.

Most operators improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step.

## Outcome

By the final stage, the operator holds a written artifact for every step, every decision-gate passed in writing, and a documented go / no-go (or kill) trail another person can audit without asking a question.

## Steps

### 1. Frame

*Intent:* State the outcome, constraints, and exit-condition in one paragraph.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/auto-evict-tool-results`
- `geek/ai/ai-agents/terse-default-tool-output`
- `geek/ai/rag-engineer/chunking-semantic`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/sdlc-ai/kb-codebase-rag-symbol-chunked`

Outputs:
- Written artifact for stage 1 (Frame) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 1 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 2. Discover

*Intent:* Pull evidence and prior art before any design decision.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/compaction-preserve-refs`
- `geek/ai/ml-engineer/embeddings-batch-and-cache`
- `geek/ai/rag-engineer/embedding-caching`
- `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `geek/sdlc-ai/kb-versioned-agent-memory-files`

Outputs:
- Written artifact for stage 2 (Discover) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 2 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 3. Design

*Intent:* Sketch target structure with explicit cuts and trade-offs.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/file-reference-passing`
- `geek/ai/ml-engineer/embeddings-evaluation`
- `geek/ai/rag-engineer/embedding-model-selection`
- `geek/ai/rag-engineer/reranking-diversity-mmr`

Outputs:
- Written artifact for stage 3 (Design) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 3 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 4. Build

*Intent:* Implement the smallest version that proves the chain works.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/manifest-then-fetch`
- `geek/ai/ml-engineer/eu-ai-act-compliance`
- `geek/ai/rag-engineer/hybrid-search-implementation`
- `geek/ai/rag-engineer/reranking-pipeline-integration`

Outputs:
- Written artifact for stage 4 (Build) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 4 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 5. Validate

*Intent:* Test against the rubric or real data before broad rollout.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/progressive-disclosure-skills`
- `geek/ai/rag-engineer/chunking-document-structure`
- `geek/ai/rag-engineer/rag-architecture`
- `geek/ai/rag-engineer/reranking-two-stage`

Outputs:
- Written artifact for stage 5 (Validate) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 5 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

### 6. Close

*Intent:* Apply decision gate, document outcome, archive for re-use.

Tasks:
- Read the assigned methodology references and reconcile them with this stage's goal.
- Produce the stage artifact named in 'outputs' and store it where the next stage can read it.
- Re-check the decision gate before advancing; loop within this stage if it fails.

Methodologies in scope:
- `geek/ai/ai-agents/rerank-before-reasoning`
- `geek/ai/rag-engineer/chunking-production-service`
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/sdlc-ai/gov-license-compliance-scan`

Outputs:
- Written artifact for stage 6 (Close) named per the project's docs convention
- Decision-gate note (advance / iterate / kill) appended to the playbook log

*Decision gate:* Advance when the stage 6 artifact exists in writing AND the methodology chain assigned to this stage has been applied. Iterate or escalate otherwise.

## Decision points

Each stage carries a decision-gate. Do not advance until the gate condition is met in writing. If a gate fails twice in a row, escalate to the playbook's review owner rather than looping a third time.

## References

Methodology chain (resolved unless marked gap):

- `geek/ai/ai-agents/auto-evict-tool-results`
- `geek/ai/ai-agents/compaction-preserve-refs`
- `geek/ai/ai-agents/file-reference-passing`
- `geek/ai/ai-agents/manifest-then-fetch`
- `geek/ai/ai-agents/progressive-disclosure-skills`
- `geek/ai/ai-agents/rerank-before-reasoning`
- `geek/ai/ai-agents/terse-default-tool-output`
- `geek/ai/ml-engineer/embeddings-batch-and-cache`
- `geek/ai/ml-engineer/embeddings-evaluation`
- `geek/ai/ml-engineer/eu-ai-act-compliance`
- `geek/ai/rag-engineer/chunking-document-structure`
- `geek/ai/rag-engineer/chunking-production-service`
- `geek/ai/rag-engineer/chunking-semantic`
- `geek/ai/rag-engineer/embedding-caching`
- `geek/ai/rag-engineer/embedding-model-selection`
- `geek/ai/rag-engineer/hybrid-search-implementation`
- `geek/ai/rag-engineer/rag-architecture`
- `geek/ai/rag-engineer/rag-eval-pipeline`
- `geek/ai/rag-engineer/rag-eval-production-monitoring`
- `geek/ai/rag-engineer/rag-eval-retrieval-metrics`
- `geek/ai/rag-engineer/reranking-diversity-mmr`
- `geek/ai/rag-engineer/reranking-pipeline-integration`
- `geek/ai/rag-engineer/reranking-two-stage`
- `geek/sdlc-ai/gov-license-compliance-scan`
- `geek/sdlc-ai/kb-codebase-rag-symbol-chunked`
- `geek/sdlc-ai/kb-versioned-agent-memory-files`

Gaps in the methodology chain (see `playbook.yaml` `gaps[]`):

- `faion-cli-as-agent-skill`
- `methodology-corpus-licence-bundle`
- `retrieval-drift-alerting-recipe`

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

Run `faion get-content methodology-corpus-integration-faion-into-our-agent-2-weeks --format context` to pull the full chain into an agent-readable payload.
