# Fixed-price vs T&M estimation with AI risk buffer

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** synthesis

## Why this playbook exists

Discovery brief → two defensible quotes (fixed-price and T&M) with explicit AI-leverage adjustment + regulatory-uncertainty buffer; post-mortem can replay assumptions.

Synthesis playbook for pre-sales pricing. Given a discovery brief, produces two defensible quotes — fixed-price and T&M — with explicit AI-leverage adjustment, regulatory-uncertainty buffer, internal margin model documented, and a post-mortem-replayable assumptions log.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Brief intake + WBS

**Intent:** Build the work breakdown both quotes will lean on.

**Tasks**
- Read brief; capture assumptions
- Apply scope-management to bound the work
- Build WBS to leaf level
- Identify deliverables vs activities

**Outputs**
- WBS to leaf level
- Assumptions log v1

**Decision gate**

Advance only when WBS leaves match deliverable nouns, not activities.

### Stage 2 — Risk + AI buffer

**Intent:** Quantify the variance that distinguishes FP from T&M.

**Tasks**
- Apply risk-management cycle
- Quantify AI-leverage adjustment per leaf (uplift vs unknown)
- Stack regulatory-uncertainty buffer where regime exposure exists
- Set change-control posture (sensitivity to scope drift)

**Outputs**
- Risk register
- AI-leverage adjustment table
- Regulatory buffer

**Decision gate**

Advance when each leaf has a quantified buffer.

### Stage 3 — Quote, defend, archive

**Intent:** Issue the two quotes; archive the margin model.

**Tasks**
- Compute fixed-price quote (with reserves)
- Compute T&M quote (with cap + rate card)
- Apply the FP-vs-T&M decision framework
- Build outsource margin calculator output
- Archive assumptions log + post-mortem replay pack

**Outputs**
- Fixed-price quote
- T&M quote
- Decision recommendation
- Margin model archive

**Decision gate**

Done when both quotes are issuable AND a post-mortem reviewer could replay the math.

## Common pitfalls

- Assuming AI uniformly speeds up — it speeds up the obvious, not the unknown
- Treating regulatory uncertainty as 'add 10%' instead of pricing the actual risk
- Burning the assumptions log after sending the quote — kills post-mortem learning

## Quality checklist

- Could a peer replay both quotes from my assumptions log?
- Did I price AI leverage per leaf, not as a blanket?
- Did I document the regulatory buffer separately?

## Related playbooks

- `fixed-price-bid-discovery-estimation`
- `tm-to-fixed-price-contract-conversion`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `ai-leverage-estimation-model` (blocks stage 2)
- `fixed-price-vs-tnm-decision-framework` (blocks stage 3)
- `regulatory-uncertainty-buffer` (blocks stage 2)
- `outsource-margin-calculator` (blocks stage 3)
