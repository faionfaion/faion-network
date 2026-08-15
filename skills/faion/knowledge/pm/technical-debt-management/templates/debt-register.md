<!--
purpose: Debt register skeleton with type + interest + contagion + effort.
consumes: input from methodology
produces: artefact for downstream agent
depends-on: content/02-output-contract.xml
token-budget-impact: ~200-500 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: The product or codebase this register covers. One register per codebase - a company-wide debt list is something nobody feels responsible for and everybody cites in planning.
  - name: review_date
    type: string
    required: true
    description: Date the register was last reviewed, ISO. Registers rot faster than the debt in them, and a stale one becomes the argument for doing nothing about any of it.
  - name: first_item_id
    type: string
    required: true
    description: Id of the first entry (TD-001). Ids are permanent - a paid-off item keeps its number and is marked resolved, so the post-mortem that cited it still resolves to something.
  - name: first_item_name
    type: string
    required: true
    description: Short name for that entry, naming the thing and not the feeling - "Order service has no integration tests", never "legacy mess". Someone outside the team has to understand it.
  - name: debt_type
    type: enum
    required: true
    options: [deliberate, accidental, bit-rot, design, docs, test]
    description: Which kind this is. deliberate means somebody chose it with a reason - that reason belongs in the record, because it may still hold and the item may not be debt at all.
  - name: interest_evidence
    type: text
    required: true
    description: Evidence that this costs you continuously - the build-time chart, the post-mortem, the PR cycle-time graph. Without it this is a preference, and preferences lose to features every time.
  - name: fix_effort
    type: enum
    required: true
    options: [S, M, L, XL]
    description: T-shirt size, estimated by somebody who would actually do the work. An XL is usually three M items nobody has split yet, and it will sit in this register until they are split.
-->

## Technical Debt Register: {{product_name}}

### Summary
- **Total items:** [X]
- **High priority:** [X]
- **Est. fix time:** [X] days
- **Last reviewed:** {{review_date}}

### Debt Items

#### {{first_item_id}}: {{first_item_name}}
**Type:** {{debt_type}}
**Created:** [Date]
**Location:** [File/module/system]

**Description:** [What the debt is]

**Why it exists:** [How it was created]

**Impact:**
- Time tax: [Hours/sprint slowed]
- Risk: [What could happen]
- Affected areas: [What is impacted]

**Interest evidence:** {{interest_evidence}}
**Business evidence:** [Cost in currency or hours, named affected feature]

**Fix effort:** {{fix_effort}}
**Priority:** [High/Medium/Low]
**Related work:** [Upcoming features that touch this]

**Fix approach:** [How to address]

---

#### TD-002: [Name]
[repeat pattern]
