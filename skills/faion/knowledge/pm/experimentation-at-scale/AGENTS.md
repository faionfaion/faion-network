# Experimentation at Scale

## Summary

**One-sentence:** Hypothesis-driven A/B experimentation program (>=100 experiments/year) with pre-registered metrics, guardrails, statistical rigor, and an agent-assisted triage -> readout -> archive loop.

**One-paragraph:** Mature experimentation discipline: every experiment ships with a pre-registered hypothesis (primary metric, secondary, guardrails, MDE, stop conditions); SRM check is mandatory before readout; readouts end in binary ship/kill/iterate; an agent triages proposals and dedups against historic experiments. Output: experiment-doc YAML + readout markdown + archive record.

**Ефективно для:**

- Високотрафіковий продукт із MDE detectable у <=4 тижні.
- Quarterly planning, де roadmap-bets потребують experimental triage.
- Pricing/packaging зміни, що вимагають quantified lift перед commit.
- Stakeholder dispute resolution через pre-registered metric, а не політику.

## Applies If (ALL must hold)

- Product has stable instrumentation + bucketing infrastructure (GrowthBook / Statsig / Eppo / in-house).
- Roadmap bet is reversible and has a clear behavioural prediction measurable within 4 weeks at current traffic.
- Quarterly planning where roadmap candidates outnumber conviction — turn opinions into a ranked experiment slate.
- Pricing or packaging change where finance wants quantified lift before commit.
- Stakeholder disputes (design vs eng vs growth) where pre-registering a metric is faster than politics.

## Skip If (ANY kills it)

- Low-traffic product where MDE detection is infeasible in 4 weeks — use qualitative methods.
- Irreversible high-risk change (security, M&A, brand re-positioning) — experiment is the wrong instrument.
- Legal / compliance blocks variant exposure (bait pricing, regulated UI).
- Team lacks a real analytics platform — instrument first, then experiment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tracking plan | YAML/JSON under version control | product-analytics methodology |
| Experimentation platform | GrowthBook / Statsig / Eppo / in-house | platform team |
| Hypothesis backlog | list of {hypothesis, primary, secondary, guardrails, MDE} | PM |
| Decision-rights map | table | stakeholder-management output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides the tracking plan + bucketing the experiments consume. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology: pre-registration, guardrails, MDE, SRM, binary readout, triage | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for experiment doc + readout | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: peeking, primary-swap, SRM-ignored, zombie-hold | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: triage -> author -> launch -> readout -> archive | 800 |
| `content/05-examples.xml` | medium | Worked end-to-end experiment + readout | 800 |
| `content/06-decision-tree.xml` | essential | Routing on traffic, reversibility, MDE feasibility | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `idea-triage` | haiku | Bulk dedup + ev/effort ranking. |
| `hypothesis-author` | sonnet | Structured authoring of primary/guardrails/MDE. |
| `post-experiment-readout` | opus | Cross-segment Simpson's-paradox detection + decision synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hypothesis-doc.yaml` | Experiment hypothesis YAML skeleton with primary/secondary/guardrails/MDE. |
| `templates/triage-idea.py` | Triage script: rank ideas by ev/effort, dedup against historic experiments. |
| `templates/readout.md.j2` | Readout markdown skeleton with SRM check, primary result, decision. |
| `templates/readout.md` | Readout markdown skeleton with SRM check, primary result, decision. Generated from `templates/readout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-experimentation-at-scale.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[product-analytics]]
- [[release-planning]]
- [[product-led-growth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/hypothesis-doc.yaml`

```yaml
id: exp_2026-04-onboarding-checklist
opportunity_tree_node: opp.activation.first-value
hypothesis: |
  If we replace the static onboarding video with a 3-step interactive checklist,
  then day-7 activation rate will increase by >= 4% (relative)
  because users self-direct to first-value tasks faster (evidence: 12 interviews, 3 prototype tests).
primary_metric: d7_activation_rate
guardrail_metrics:
  - signup_to_login_latency_p95
  - support_tickets_per_signup
mde_relative: 0.04
power: 0.8
alpha: 0.05
runtime_min_days: 14
segment_cuts: [device, plan, signup_source]
decision_rule: |
  SHIP if primary_lift >= 4% AND ci_low > 0 AND no guardrail breach AND no SRM.
  ITERATE if 0 < primary_lift < 4% AND no guardrail breach.
  KILL if primary_lift <= 0 OR guardrail breach.
  EXTEND if power_achieved < 0.7 AND no guardrail breach.
stop_conditions:
  - support_tickets_per_signup spike > 25% week-over-week
  - p95 signup latency > 1.5x baseline for >24h
sponsor: vp-product@team
prior_evidence:
  - dovetail/study-2026-03-onboarding-pain
  - maze/proto-2026-04-checklist-v3
  - exp_2025-Q4-onboarding-video (null result)
```

### `templates/triage-idea.py`

```python
"""

"""
triage-idea.py — score an idea's testability and route to experiment tier.
Input:  JSON via stdin: {reversible, min_traffic_ok, behavioral_prediction, notes}
Output: JSON: {score, tier, rationale}
Tiers: A/B (score 3), prototype-or-A/B (score 2), qual-first (score 1), irreversible-strategic (score 0)
"""
import json, sys

TIER = {
    3: "A/B",
    2: "prototype-or-A/B",
    1: "qual-first",
    0: "irreversible-strategic",
}


def triage(idea: dict) -> dict:
    score = 0
    score += 1 if idea.get("reversible") else 0
    score += 1 if idea.get("min_traffic_ok") else 0
    score += 1 if idea.get("behavioral_prediction") else 0
    return {
        "score": score,
        "tier": TIER[score],
        "rationale": idea.get("notes", ""),
    }


if __name__ == "__main__":
    idea = json.load(sys.stdin)
    json.dump(triage(idea), sys.stdout)
    print()
```
