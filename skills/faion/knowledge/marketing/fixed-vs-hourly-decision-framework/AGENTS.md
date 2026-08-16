# Fixed Vs Hourly Decision Framework

## Summary

**One-sentence:** Decision framework for fixed-price vs hourly engagement — 4 signals (scope clarity, change-rate, client maturity, domain familiarity) score to one shape; recorded with kill-criteria + named decider.

**One-paragraph:** Freelancers daily face "do I quote this fixed or hourly?" with no decision aid. SOW playbooks assume fixed-price. This framework scores 4 signals and routes to fixed / hourly / hybrid (fixed scope + time-and-materials change-budget). Core rules: every signal carries a numeric or 3-band score; the decision logs option chosen + options rejected + evidence + reversal trigger; kill-criteria are numeric per option; the decision is signed by a single named decider; reassessment at 25% of project elapsed. Output: a decision-record artefact filed in the SOW workflow.

**Ефективно для:**

- Inbound proposal — quick fixed-vs-hourly call before SOW draft.
- Existing retainer re-shape — quarterly review.
- Multi-engagement portfolio — same client, multiple shapes.
- Agency / freelance handoff — successor sees the rationale, not just the price.

## Applies If (ALL must hold)

- Service engagement &gt; 20 hours (below that, hourly default is fine).
- Authority to set engagement shape with the client.
- ≥3 of the 4 signals are observable (scope, change-rate, maturity, familiarity).
- Named decider available (you, the freelancer, or designated agency lead).

## Skip If (ANY kills it)

- Engagement &lt; 20 hours — overhead exceeds value.
- Client has rigid procurement that forbids the chosen shape.
- Tiny experimental project where pricing matters less than learning.
- No SOW infrastructure — fix invoicing + change-order workflow first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope document or rough brief | doc | client |
| Prior projects with this client (if any) | report / notes | own CRM |
| Domain-familiarity self-assessment | score | own portfolio |
| SOW + change-order templates | files | own ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[freelance-pilot-pricing]] | Pilot-pricing fits the hybrid bucket here. |
| [[freelance-rate-jump-tactics]] | Hourly rate target feeds the score. |
| [[proposal-from-discovery-template]] | Downstream proposal artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: signal-scored, kill-criteria-numeric, decision-logged-with-reversal, single-named-decider, mid-project-reassessment | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: gather scope → score 4 signals → pick shape → record decision → reassess at 25% | 600 |
| `content/06-decision-tree.xml` | essential | Tree mapping signal scores to fixed / hourly / hybrid | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-signals` | sonnet | Per-signal judgment. |
| `record-decision` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.json` | JSON example of the decision record |
| `templates/decision-record.md.j2` | Markdown skeleton for the SOW appendix |
| `templates/decision-record.md` | Markdown skeleton for the SOW appendix Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-vs-hourly-decision-framework.py` | Validate the decision-record JSON | After scoring, before SOW finalization |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelance-pilot-pricing]]
- [[freelance-rate-jump-tactics]]
- [[proposal-from-discovery-template]]
- [[retainer-pricing-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes signal scores to one of three engagement shapes (fixed / hourly / hybrid) and pins the rule from `01-core-rules.xml`. Use it before drafting the SOW — picking the wrong shape costs 10-30% of margin.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-record.json`

```json
{
  "decision_id": "fvh-acme-onboarding-rebuild",
  "engagement": {
    "client": "Acme",
    "scope_summary": "Rebuild onboarding flow over 6 weeks; deliver A/B framework + 3 variants."
  },
  "signals": {
    "scope_clarity": "high",
    "change_rate": "low",
    "client_maturity": "high",
    "domain_familiarity": "high"
  },
  "options_considered": [
    "fixed",
    "hourly",
    "hybrid"
  ],
  "chosen": "fixed",
  "kill_criteria": {
    "fixed": "If change requests >3/week sustained 2 weeks, reopen as hybrid",
    "hourly": "n/a (rejected): client maturity high supports fixed",
    "hybrid": "n/a (rejected): scope clarity high reduces need for T&M buffer"
  },
  "reversal_trigger": "Change-request rate exceeding 3/week sustained for 2 weeks AND total change-effort > 15% of fixed scope",
  "decider": "@ruslan",
  "decided_at": "2026-05-23",
  "reassessment_at_25pct": "2026-06-04"
}
```
