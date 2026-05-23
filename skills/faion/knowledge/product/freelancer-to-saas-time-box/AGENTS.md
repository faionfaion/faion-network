# Freelancer to SaaS Time-Box

## Summary

**One-sentence:** Pins an explicit weekly time-box + boundary contract that protects SaaS build slots from client work; produces a 90-day commitment spec with abort criteria.

**One-paragraph:** Pins an explicit weekly time-box + boundary contract that protects SaaS build slots from client work; produces a 90-day commitment spec with abort criteria. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Active freelancer with ≥3 paying clients trying to ship a SaaS on the side.
- Repeated SaaS attempts already died because client urgent eats build slot.
- Need explicit weekly hours commitment + boundary rules buyers and family can see.
- Want a pre-committed 90-day abort gate so the side build doesn't drift forever.

## Applies If (ALL must hold)

- Freelancer earns ≥80% income from billable client work today.
- SaaS idea has at least one paying-customer signal (LOI, pre-order, beta interest).
- Founder can commit ≥6 contiguous hours / week to SaaS for 90 days.
- Calendar control: founder owns own scheduling and can decline client requests.

## Skip If (ANY kills it)

- Founder cannot decline any client request — boundary contract is unenforceable.
- No paying-customer signal yet — apply pmf-rubric-for-solos first.
- Income runway < 90 days — survival > time-box; finish client work first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Weekly hour budget | JSON with day -> hours map | calendar audit (past 4 weeks) |
| Client backlog | list of contracts with deadline + revenue | CRM / Notion |
| SaaS hypothesis spec | one-page hypothesis: customer + problem + proof | founder |
| Runway | months of expenses covered by current cash | accounting |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-freelancer-to-saas-time-box` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-to-saas-time-box.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pmf-rubric-for-solos]]
- [[productized-service-design]]
- [[pivot-vs-quit-decision-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
