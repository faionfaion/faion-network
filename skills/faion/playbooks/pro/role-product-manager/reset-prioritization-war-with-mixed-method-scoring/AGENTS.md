---
slug: reset-prioritization-war-with-mixed-method-scoring
tier: pro
group: role-product-manager
persona: role-product-manager
goal: govern-decide
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: PM walks into a contested backlog and exits with a defensible, stakeholder-bought-in ordered list anchored to outcomes, not opinions.
content_id: 423bc190598ea57f
methodology_refs:
  - stakeholder-management
  - opportunity-solution-trees
  - feature-prioritization-moscow
  - feature-prioritization-rice
---

# Reset prioritization war with mixed-method scoring

## Context

PM walks into a contested backlog and exits with a defensible, stakeholder-bought-in ordered list anchored to outcomes, not opinions. RICE alone is insufficient when the fight is about strategic value; this stacks Kano plus opportunity-tree plus RICE plus force-ranked OKR alignment.

Tier: **pro**. Complexity: **deep**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- OKR × item map exists for every contested ask.
- Every item has a Kano class.
- Top-N has RICE numbers, not opinions.
- Stakeholder-ratified list under version control.

## Steps

### 1. Surface contention

Catalogue what the fight is actually about.

Tasks:
- Pull every stakeholder's top-3 asks.
- Catalogue which items appear on multiple lists vs only one.
- Identify the items that drive the loudest disagreement.

Outputs:
- Stakeholder × ask matrix.

Decision gate: Advance when the contention pattern is visible on one page.

### 2. Anchor outcomes

Re-anchor on the quarter's OKRs.

Tasks:
- Map every contested item to the OKR it claims to serve.
- Reject items that do not map to any OKR.
- Surface items that map to multiple OKRs.

Outputs:
- OKR × item map.

Decision gate: Advance when every shortlisted item has at least one OKR mapping.

### 3. Apply Kano

Sort items by need-type, not feeling.

Tasks:
- Classify each item as Basic / Performance / Excitement / Indifferent / Reverse.
- Flag Indifferent + Reverse items for cut.
- Note Basic items as table-stakes.

Outputs:
- Kano classification.

Decision gate: Advance when every item has a Kano class.

### 4. Walk opportunity tree

Tie each ask to a user opportunity.

Tasks:
- Build an opportunity tree from the JTBDs.
- Map each contested item to a tree node.
- Surface items that are solutions in search of a problem.

Outputs:
- Opportunity tree with mapped items.

Decision gate: Advance when every shortlisted item has an opportunity-tree node.

### 5. Force-rank with RICE

Apply RICE only to the survivors.

Tasks:
- Run RICE on items that passed Kano + opportunity-tree filters.
- Compute reach × impact × confidence ÷ effort.
- Force-rank by RICE score.

Outputs:
- Force-ranked top list.

Decision gate: Advance when the top-N has explicit RICE numbers.

### 6. Stakeholder ratification

Walk the list with stakeholders to lock it.

Tasks:
- Run a single ratification meeting with all stakeholders.
- Use the four-filter rationale (OKR → Kano → tree → RICE).
- Lock the list under version control with the rationale.

Outputs:
- Ratified prioritized list + rationale doc.

Decision gate: Required: a signed-off list with rationale; no 'verbal agreement'.

## Decision points

- Kano Excitement vs Performance — only invest in Excitement when the Basic + Performance bar is already cleared.
- Re-rank by RICE alone vs full stack — full stack only when the prior process produced a fight; pure RICE for routine cycles.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/stakeholder-management`
- `pro/research/researcher/opportunity-solution-trees`
- `solo/product/product-manager/feature-prioritization-moscow`
- `solo/product/product-manager/feature-prioritization-rice`
