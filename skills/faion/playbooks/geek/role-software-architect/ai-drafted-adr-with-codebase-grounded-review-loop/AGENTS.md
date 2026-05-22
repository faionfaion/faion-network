---
slug: ai-drafted-adr-with-codebase-grounded-review-loop
tier: geek
group: role-software-architect
persona: role-software-architect
goal: plan-design
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Architect identifies a decision, runs a CLI flow that drafts an ADR from codebase context, validates each Consequence claim against the repo, and produces an ADR ready for team vote.
content_id: be5a2a991b469118
methodology_refs:
  - kb-codebase-rag-symbol-chunked
  - kb-symbol-index-fresh-tags
  - mr-codemod-refactor-agent
  - mr-graph-vs-diff-reviewer
  - quality-attributes-analysis
  - architecture-decision-records
  - system-design-process
  - trade-off-decision-matrix
---

# AI-drafted ADR with codebase-grounded review loop

**Slug:** `ai-drafted-adr-with-codebase-grounded-review-loop` · **Tier:** geek · **Complexity:** medium

## Context

Architect identifies a decision, runs a CLI flow that drafts an ADR from codebase context, validates each Consequence claim against the repo, and produces an ADR ready for team vote

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Prepare

Achieve the 'prepare' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Inventory

Achieve the 'inventory' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Decide approach

Achieve the 'decide approach' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Execute

Achieve the 'execute' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Verify

Achieve the 'verify' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 6: Document & decide

Achieve the 'document & decide' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/geek/sdlc-ai/kb-codebase-rag-symbol-chunked`
- `knowledge/geek/sdlc-ai/kb-symbol-index-fresh-tags`
- `knowledge/geek/sdlc-ai/mr-codemod-refactor-agent`
- `knowledge/geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `knowledge/pro/dev/software-architect/quality-attributes-analysis`
- `knowledge/solo/dev/software-architect/architecture-decision-records`
- `knowledge/solo/dev/software-architect/system-design-process`
- `knowledge/solo/dev/software-architect/trade-off-decision-matrix`
