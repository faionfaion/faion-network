# Agency Risk Register Template

## Summary

**Ефективно для:**

- Micro-agency / consultancy з 3-25 людей.
- Weekly 30-min cadence з 8-column register.
- Revenue concentration, key-person, FX, contractor classification, pipeline.
- Auto-bumped score для будь-якого клієнта ≥40% trailing-90d revenue.

A weekly 30-minute risk-register cadence focused on agency-level risks (not just per-project): revenue concentration by client, key-person dependency, currency exposure, contractor classification, and pipeline thinness. Outcome: a one-page register the founder/PM can refresh every Monday in under 30 minutes, with each risk owned, scored, and given a trigger that escalates it from monitored to actioned.

## Applies If

- A micro-agency or consultancy of 3 to 25 people with a founder or PM who can hold a 30-minute slot every Monday for at least 8 weeks.
- A billing or invoicing export can give revenue by client over the trailing 90 days, and at least one client is above 20 percent or the agency bills or hires across borders.
- The CRM carries stage-weighted pipeline and the ledger gives revenue and costs by currency, so the pipeline and FX rows can be numbers.
- Every risk row can be given to a named person with an observable trigger, and the founder will sign acceptances for rows at 15 or more that are not mitigated.

## Skip If

- A solo freelancer with a single client: use freelancer-client-scorecard instead.
- An in-house product team: use the project-level risk register; this register holds agency classes only.
- The agency has a CFO or COO already running enterprise-risk reviews on a cadence.
- The 30-minute Monday slot cannot be held for 8 weeks; without the cadence the register decays into folklore.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing export | revenue by client for the trailing 90 days | invoicing or billing system, exported every Monday |
| Pipeline export | opportunities by stage with value and stage weight; monthly cost base | CRM; finance |
| Ledger by currency | share of revenue and share of costs per billing currency | accounting system |
| Contractor list | each cross-border contractor with jurisdiction and the classification test applied | contracts folder; legal or accountant |
| Credential and system inventory | single-point items with their holder | password manager, infrastructure docs |
| `templates/agency-risk-register-template.md.j2`, `templates/agency-risk-register-template.json` | register skeleton; the contract schema | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: six agency risk classes, 8-column rows, 90-day concentration auto-score, dated key-person remediation, quantified FX / contractor rows, pipeline months of coverage, 30-minute Monday, score-15 action or signed acceptance, closed tab never deleted | 1950 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the Monday register: agency headcount, 30-minute refresh with timed parts and overrun rule, concentration recomputed from the 90-day billing export with every client's share, 8-column rows across the six agency classes with quantified details (client share, dated key-person remediation, currency shares, contractor jurisdiction and test, pipeline months of coverage), mitigation or signed acceptance at 15 or more, closed tab with lessons; valid and invalid registers; 8 forbidden patterns | 5650 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with description + reason + repair | 1250 |
| `content/04-procedure.xml` | essential | 7 steps for the Monday refresh: recompute concentration from billing, update the six classes with numbers, walk the top five rows, decide every row at 15 or more, check owners and triggers, move resolved rows to the closed tab, write the action note and validate | 1550 |
| `content/05-examples.xml` | recommended | Complete Monday register for a six-person studio (28 minutes, Client A at 47 percent scored 20 and mitigated by Friday, seven rows across six classes, one closed row) with a note per value, plus a Wednesday hour of project rows and estimates and what the validator prints | 2600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule; read before drafting. | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-risk-register-template.md.j2` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/agency-risk-register-template.md` | Markdown skeleton (5-line header) for the artefact body. Generated from `templates/agency-risk-register-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/agency-risk-register-template.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-risk-register-template.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[client-health-scorecard-agency]]
- [[capacity-vs-ask-balancer]]
- [[regulatory-uncertainty-buffer]]
- [[vendor-risk-assessment-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.
