---
slug: prep-the-agency-for-acquisition
tier: pro
group: business-analysis
persona: P5
goal: migrate-rebuild
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: 2-3 person agency to sellable to strategic / acqui-hire / manager-operator within 6-12 months; same prep removes founder dependency even if not selling.
content_id: eb9cb5889fb9ac5d
methodology_refs:
  - product-operations
  - ops-annual-planning-process
  - ops-financial-basics
  - ops-legal-basics
  - ops-legal-compliance-checklist
  - ops-partnership-strategy
---

# Prep the agency for acquisition (or graceful walk-away)

**Playbook slug:** `prep-the-agency-for-acquisition`
**Tier:** pro
**Complexity:** deep
**Persona:** P5 -- Micro-agency founder

## Intent

2-3 person agency to sellable to strategic / acqui-hire / manager-operator within 6-12 months; same prep removes founder dependency even if not selling.

## Scope

Get a 2-3 person agency to a state where it is sellable to a strategic buyer, an acqui-hirer, or transferable to a manager-operator within 6-12 months. Even if not selling, the same prep removes founder dependency. Exit artifact: due-diligence-ready data room + valuation rubric scorecard + handover SOP kit.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Investment banker representation - out of scope for micro-agency
- Public-market transactions - irrelevant to this size

### Prerequisites

- Steady revenue across 18+ months
- Bookkeeping + paperwork in functional state

## Success criteria

The playbook is done when:
- Founder-dependency audit complete
- Owner handover SOP kit produced
- Valuation rubric scorecard updated
- Data room with financial, legal, commercial assets
- Decision: sell / hold / handover written

## Stages

### Stage 1: Founder-dependency audit

**Intent:** Where the agency falls apart without the founder.

**Tasks:**
- Map every recurring decision
- Tag founder-only vs delegable
- Score concentration risk

**Methodologies in chain:**
- `product-operations` -> `pro/product/product-operations/product-operations`

**Outputs:**
- Dependency audit doc

**Decision gate:**
> Advance once founder-only decisions are tagged with a plan to delegate.

### Stage 2: Financial + legal pack

**Intent:** Numbers and paper sellable.

**Tasks:**
- Lock 24 months trailing financials
- Refresh legal + compliance pack
- Audit partnership + vendor commitments

**Methodologies in chain:**
- `ops-annual-planning-process` -> `pro/marketing/gtm-strategist/ops-annual-planning-process`
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`
- `ops-legal-basics` -> `pro/marketing/gtm-strategist/ops-legal-basics`
- `ops-legal-compliance-checklist` -> `pro/marketing/gtm-strategist/ops-legal-compliance-checklist`
- `ops-partnership-strategy` -> `pro/marketing/gtm-strategist/ops-partnership-strategy`

**Outputs:**
- Financial pack
- Legal + commercial pack

**Decision gate:**
> Advance once a stranger could read the packs and forecast next 12 months.

### Stage 3: Valuation + buyer fit

**Intent:** Run valuation rubric; identify buyer archetypes.

**Tasks:**
- Score against valuation rubric
- Profile 3 buyer archetypes
- Test soft conversations with 2

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Valuation scorecard
- Buyer profile doc

**Decision gate:**
> Advance with at least one buyer archetype showing live interest signal.

### Stage 4: Handover kit

**Intent:** Manager-operator can run agency end-to-end from kit.

**Tasks:**
- Document operating rhythm
- Produce SOPs per service line
- Stand up dashboard pack

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Handover SOP kit
- Dashboard pack

**Decision gate:**
> Required: an outsider can read the kit and run the agency for 30 days.

## Common pitfalls

- Selling before deciding - buyers smell desperation
- Skipping the dependency audit - sale collapses in due diligence
- Treating handover kit as optional - it is the asset

## Quality checklist (self-review)

- Could a manager-operator run this for 30 days using only the kit?
- Are the financials clean enough for due diligence?
- Did I price honestly, not aspirationally?

## Related playbooks

- `agency-to-recurring-revenue-transition`
- `annual-planning-and-financial-close`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-acquisition-prep** (tier `pro`, blocks stage 1) -- Founder-dependency stage needs a structured acquisition-prep canvas
- **founder-dependency-audit** (tier `pro`, blocks stage 1) -- Founder-dependency stage needs a tested audit template
- **agency-valuation-rubric** (tier `pro`, blocks stage 3) -- Valuation stage needs an explicit micro-agency valuation rubric
- **owner-handover-sop-kit** (tier `pro`, blocks stage 4) -- Handover-kit stage needs a default SOP kit template

## CLI usage

```
faion get-content prep-the-agency-for-acquisition --format md       # human-readable rendering
faion get-content prep-the-agency-for-acquisition --format context  # agent-optimised context bundle
faion get-content prep-the-agency-for-acquisition --format json     # raw structured form
```
