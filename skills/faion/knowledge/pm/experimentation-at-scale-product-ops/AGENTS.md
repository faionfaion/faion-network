# Experimentation at Scale

## Summary

**One-sentence:** Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction step.

**One-paragraph:** Enterprise experimentation is a disciplined platform — not ad-hoc A/B testing — with defined hypothesis intake, pre-registered metrics, guardrails, SRM checks, and a learning-extraction step. The methodology produces a `spec` artefact gated by an explicit output contract (JSON Schema draft-07) + decision tree referencing core rules. Apply when the preconditions in `## Applies If` ALL hold and none of the `## Skip If` disqualifiers fires. Skip and reach for a sibling methodology otherwise.

**Ефективно для:**

- Repeatable cycles де треба явний spec, не ad-hoc notes.
- Командна робота з named owner per artefact (audit trail).
- Pro-tier контекст: 3-20 retainer clients / mid-stage SaaS / agency-to-saas pivot.
- AI-augmented workflows, де LLM-агент виконує частину кроків процедури.

## Applies If (ALL must hold)

- Operating context matches the produces shape (`spec`) — outcome can be inspected as a discrete artefact.
- Named human owner exists for the artefact + downstream actions (no orphan output).
- Inputs listed in `## Prerequisites` are available before the run.
- Cadence and time-box fit the cycle window the team actually operates.
- Output will be reviewed against the JSON Schema in `content/02-output-contract.xml` before acceptance.

## Skip If (ANY kills it)

- One-off task with no recurrence — value of the methodology is the rhythm.
- No named owner accountable for the produced artefact.
- Team already runs a more granular methodology that supersedes this one.
- Preconditions in `## Prerequisites` missing and no plan to source them this cycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs listed in `01-core-rules.xml` | system-of-record links (URL or path) | upstream owner |
| Prior cycle output (if any) | this methodology's own artefact | git history |
| Named owner for cycle | identity string | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output gates | ~800 |
| `content/05-examples.xml` | essential | End-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-inputs` | haiku | Mechanical mapping; no judgment. |
| `apply-procedure` | sonnet | Cross-section reasoning over the deep procedure. |
| `synthesize-spec` | opus | Final cross-input judgment producing the spec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-doc.yaml` | Pre-registration template for hypothesis, metrics, guardrails |
| `templates/sample_size.py` | Sample-size + MDE calculator (stdlib only) |
| `templates/srm_check.py` | Sample Ratio Mismatch detector |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- parent skill: `skills/faion/knowledge/pro/product/product-operations/`
- peer methodologies: siblings under the parent skill
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions satisfied, owner present, prior-cycle output available, cycle window fit) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology this cycle or defer.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/experiment-doc.yaml`

```yaml
experiment_id: exp-2026-XXX
title: ""
hypothesis: |
  ""
primary_metric: ""
mde: 0.0
sample_size: 0
guardrails:
  - metric: p95_latency_ms
    threshold: 350
  - metric: error_rate
    threshold: 0.01
pre_registered_at: ""
srm_passed: null
sequential_design: none  # one of: none, mSPRT, group-sequential
owner: ""
review_decision_date: ""
```

### `templates/sample_size.py`

```python
import argparse, math, sys

def z(p):
    # cheap inverse-normal for common levels
    table = {0.5: 0.0, 0.6: 0.2533, 0.7: 0.5244, 0.8: 0.8416, 0.9: 1.2816, 0.95: 1.6449, 0.975: 1.96, 0.99: 2.3263}
    if p in table: return table[p]
    # crude linear fallback
    keys = sorted(table)
    for i in range(len(keys)-1):
        if keys[i] <= p <= keys[i+1]:
            a, b = keys[i], keys[i+1]
            return table[a] + (p - a) * (table[b] - table[a]) / (b - a)
    return table[0.975]

def size(baseline, mde, alpha, power):
    p1, p2 = baseline, baseline + mde
    pbar = (p1 + p2) / 2
    za = z(1 - alpha / 2)
    zb = z(power)
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1*(1-p1) + p2*(1-p2))) ** 2
    return math.ceil(num / (mde ** 2))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=float, default=0.1)
    p.add_argument("--mde", type=float, default=0.02)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.8)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        n = size(0.1, 0.02, 0.05, 0.8)
        sys.stdout.write(f"self-test n={n}\n")
        sys.exit(0 if n > 100 else 1)
    n = size(a.baseline, a.mde, a.alpha, a.power)
    sys.stdout.write(f"per-arm sample size: {n}\n")

if __name__ == "__main__":
    main()
```

### `templates/srm_check.py`

```python
import argparse, math, sys

def chi2_p(c, t, ratio):
    n = c + t
    exp_c = n * ratio
    exp_t = n * (1 - ratio)
    chi2 = (c - exp_c) ** 2 / exp_c + (t - exp_t) ** 2 / exp_t
    # 1 dof, survival function via series approx
    # Use Q-function approx for chi2(1) which equals 2 * Phi(-sqrt(chi2))
    z = math.sqrt(chi2)
    p = math.erfc(z / math.sqrt(2))
    return chi2, p

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--control-n", type=int, required=False)
    p.add_argument("--treatment-n", type=int, required=False)
    p.add_argument("--expected-ratio", type=float, default=0.5)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        chi2, pv = chi2_p(5000, 5000, 0.5)
        ok = pv > 0.001
        sys.stdout.write(f"self-test chi2={chi2:.3f} p={pv:.4f} pass={ok}\n")
        sys.exit(0 if ok else 1)
    if a.control_n is None or a.treatment_n is None:
        sys.stderr.write("--control-n and --treatment-n required\n"); sys.exit(2)
    chi2, pv = chi2_p(a.control_n, a.treatment_n, a.expected_ratio)
    if pv < 0.001:
        sys.stderr.write(f"SRM FAIL chi2={chi2:.3f} p={pv:.4f}\n"); sys.exit(1)
    sys.stdout.write(f"SRM ok chi2={chi2:.3f} p={pv:.4f}\n")

if __name__ == "__main__":
    main()
```
