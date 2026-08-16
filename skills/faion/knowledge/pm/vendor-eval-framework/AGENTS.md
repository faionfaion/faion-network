# Vendor Evaluation Framework

## Summary

**One-sentence:** A 4-6 axis scoring rubric + 30-day trial protocol + explicit rollback gate for in-house teams buying $50-500/mo SaaS, replacing vibes-led vendor selection with a reviewable artefact.

**One-paragraph:** `build-vs-buy` exists at solo tier but assumes a single buyer. For an in-house team comparing Datadog vs Grafana, Linear vs Jira, or Vercel vs Netlify in the $50-500/mo band, there is no scoring matrix, no trial protocol, and no rollback gate. This methodology pins all three: 4-6 axis rubric (must include price + lock-in + ops-load + integration + DX + support), a minimum 30-day trial with at least one real workload migrated, multi-stakeholder scoring (eng + ops + finance), and an explicit rollback gate (criteria + responsible-owner) before the contract is signed. Annual revisit is built in to catch tool decay.

**Ефективно для:** tech lead, який втомився, що SaaS-вибір команди — це "хто крикнув голосніше на standup".

## Applies If (ALL must hold)

- Team is buying or replacing a SaaS vendor in the $50-500/mo band.
- There are ≥2 plausible candidates (single-vendor markets skip the rubric).
- A trial sandbox is technically feasible (not blocked by data residency or contract).
- A named decision-owner exists who can sign or veto.
- The team has at least 3 weeks of runway before the decision deadline.

## Skip If (ANY kills it)

- Trivial purchase under $50/month — over-engineered, just decide.
- Enterprise procurement with formal RFP — different process, defer to legal/procurement.
- Vendor mandated by parent company or regulator — selection is not the team's call.
- Single-vendor market — no comparison possible.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of 2-5 candidate vendors | CSV / YAML | team backlog or eng-ops channel |
| Scoring rubric (4-6 axes) | YAML | this methodology's `templates/` |
| Trial sandbox capability | infra | dev/staging env |
| Named decision-owner | role + person | team roster |
| Annual budget for the category | $ figure | finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm-agile` | Parent skill — provides operating context for this methodology. |
| `geek/product/vendor-evaluation-scorecard` | Peer geek-tier methodology with overlapping rubric; this one adds trial + rollback gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-6 axes, 30-day trial min, explicit rollback gate, multi-stakeholder scoring, annual revisit | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Trial-feasible gate + multi-stakeholder branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_rubric` | haiku | Template fill from category + axes list. |
| `score_trials` | sonnet | Per-axis judgment from trial evidence; cites scenarios. |
| `synthesize_decision` | opus | Cross-stakeholder synthesis; surfaces conflicts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.yaml` | 4-6 axis scoring rubric scaffold. |
| `templates/trial-protocol.md.j2` | 30-day trial plan with workload migration checklist. |
| `templates/trial-protocol.md` | 30-day trial plan with workload migration checklist. Generated from `templates/trial-protocol.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rollback-gate.yaml` | Rollback criteria + responsible-owner block. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-eval-framework.py` | Validate rubric + trial result + rollback gate output (axis count, stakeholder count, rollback criteria present). | Before vendor contract is signed. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[vendor-risk-assessment-template]] — sibling versioned-artefact methodology, runs in parallel for higher-risk vendors.
- [[vendor-evaluation-scorecard]] — product-tier peer; this geek-tier version adds trial + rollback.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether ≥2 candidates exist and a trial sandbox is feasible. If only one candidate → skip and document. If trial is blocked → escalate to procurement. If multi-stakeholder scoring is impossible (no finance representative) → defer until alignment is possible. Otherwise → emit the rubric.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rubric.yaml`

```yaml
version: "1.0.0"
category: "<saas-category>"      # e.g. apm, ticketing, ci-cd, hosting
candidates:
  - "<vendor-a>"
  - "<vendor-b>"
axes:
  - id: fit
    weight: 0.25
    scored_by: "eng-lead:<person>"
  - id: integrations
    weight: 0.15
    scored_by: "ops-lead:<person>"
  - id: pricing
    weight: 0.20
    scored_by: "finance:<person>"
  - id: support
    weight: 0.10
    scored_by: "ops-lead:<person>"
  - id: security
    weight: 0.15
    scored_by: "security:<person>"
  - id: exit_cost
    weight: 0.15
    scored_by: "eng-lead:<person>"
scoring_scale: "1-5 (1 worst, 5 best)"
```

### `templates/rollback-gate.yaml`

```yaml
version: "1.0.0"
candidate: "<vendor>"
criteria:
  - axis: "fit"
    threshold: 3        # minimum acceptable axis score on 1-5
  - axis: "pricing"
    threshold: 3
  - axis: "security"
    threshold: 4
day_60_check_date: "<ISO date>"
responsible_owner: "tech-lead:<person>"
switch_back_path:
  - "Re-enable previous vendor at <link>"
  - "Restore data from snapshot <id>"
  - "Communicate to team via #eng-ops"
```
