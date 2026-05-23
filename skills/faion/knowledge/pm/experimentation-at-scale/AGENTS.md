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
| `templates/readout.md` | Readout markdown skeleton with SRM check, primary result, decision. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-experimentation-at-scale.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[product-analytics]]
- [[release-planning]]
- [[product-led-growth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
