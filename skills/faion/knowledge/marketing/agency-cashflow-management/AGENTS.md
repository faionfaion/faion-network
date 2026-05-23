# Agency Cashflow Management

## Summary

**One-sentence:** Micro-agency cashflow spec: deposit policy, milestone schedule, net-30 retainer terms, contractor-payable timing, and 30-60 day gap forecasting — a versioned operating artefact, not a spreadsheet that rots.

**One-paragraph:** Micro-agency cashflow spec: deposit policy, milestone schedule, net-30 retainer terms, contractor-payable timing, and 30-60 day gap forecasting — a versioned operating artefact, not a spreadsheet that rots. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Micro-agency (2-10 people) with mixed revenue: deposits + milestone + net-30 retainers.
- Founder has accountability for cashflow and can sign-off on the policy.
- Outflow profile includes contractor payments due on-receipt (not net-30).

## Skip If (ANY kills it)

- Solo freelancer with one cash inflow stream — a personal-finance template is enough.
- Enterprise agency with a CFO + treasury function — defer to existing finance policy.
- No named cashflow owner — defer until ownership is resolved.

**Ефективно для:**

- Мікро-агенції 2-10 людей з deposits + milestone + net-30 retainer mix-ом і постійним 30-60 day gap.
- Засновники-фрилансери що масштабуються в агенцію — потрібна перша cashflow-дисципліна.
- Команди де contractor payments йдуть on-receipt, а client receipts — net-30+: дрейф kills runway.
- Аудит-ready середовища: SOC2 / квартальний фінансовий огляд з вимогою repeatable forecast.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-cashflow-management.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
