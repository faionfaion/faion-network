# A/B Testing Implementation

## Summary

**One-sentence:** Implements a deterministic A/B testing runtime — sticky bucketing via hash(user_id|experiment_id), exposure+conversion events, z-test for proportions with Wilson CI, and SRM detection.

**One-paragraph:** A/B testing runtime that survives device, session, and process changes. Core rule: assignment uses a 64-bit hash of (user_id || experiment_id) mod 100, never random.choice — this keeps the same user in the same arm across web, iOS, app, and email surfaces. The runtime emits typed exposure + conversion events to a stats engine and a periodic SRM (Sample Ratio Mismatch) check that fails the experiment if traffic split drifts more than the configured chi-square p-value.

**Ефективно для:**

- Solo dev wiring a feature flag into a real experiment instead of a kill switch.
- Multi-platform consistency — same user must get the same variant on web + iOS + email.
- Pricing or onboarding flow tests where mis-bucketing breaks trust + skews data.
- Adding statistical rigor (Wilson CI, z-test, SRM) instead of eyeballing event counts.

## Applies If (ALL must hold)

- Experiment design is complete (hypothesis + primary metric + MDE + sample size).
- Traffic is high enough to reach statistical power (>=1k weekly users on the surface).
- A stats engine (Snowflake / ClickHouse / BigQuery) is wired to receive events.
- Variants are independent (no network effects between users).

## Skip If (ANY kills it)

- Traffic too low for power — use qualitative methods.
- Change affects every user irreversibly (DB migrations, schema rewrites).
- Marketplace / pricing with strong network effects — use switchback or geo split.
- Compliance-bound flow (KYC / payments) where variant differences create audit problems.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment design | hypothesis + primary metric + MDE + sample size | PM / analyst |
| Feature flag | flag key + targeting rule | LaunchDarkly / Unleash / homegrown |
| Stats engine connection | event stream sink | data team |
| Salt / hash seed | per-experiment string | architect (do not reuse across experiments) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[feature-flag-cleanup-discipline]] | Flag cleanup gate after experiment ends. |
| [[deterministic-test-data-pattern]] | Same hashing discipline for offline test data. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules — runtime: deterministic hash, sticky across surfaces, SRM gate, exposure-before-conversion, Wilson CI; design + decision: pre-registered design, locked sample size, full business cycle, guardrails gate the ship, pre-specified segments, practical-significance floor, named human signs off | 2000 |
| `content/02-output-contract.xml` | essential | JSON Schema for experiment-run artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: random.choice, no-SRM, peeking, post-assignment changes, multi-variable variant, ignored guardrail | 950 |
| `content/04-procedure.xml` | essential | 6-step procedure (pre-register design → wire bucket → emit exposure → emit conversion → analyse → decide + sign off) | 950 |
| `content/05-examples.xml` | essential | Worked example: pricing-page A/B run with SRM-clean output | 600 |
| `content/06-decision-tree.xml` | essential | Routes by cycle length, power, SRM, significance, guardrails, practical floor | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ab_testing_implement_bucket` | sonnet | Hash impl + collision checks. |
| `ab_testing_analyse` | sonnet | Stats engine query + Wilson CI computation. |
| `ab_testing_srm_check` | haiku | Mechanical chi-square check. |
| `ab_testing_preregister` | sonnet | Draft the plan: metric choice, guardrail selection, sample-size computation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the experiment-run artefact |
| `templates/sample-size.py` | Sample-size calculator (proportions test, two-sided) |
| `templates/analyzer.py` | Variant analyser with z-test + Wilson CI + SRM check |
| `templates/_smoke-test.json` | Minimum viable filled-in experiment-run for validator round-trip |
| `templates/test-plan.md.j2` | Pre-registration plan frozen before launch: hypothesis, split, metrics, guardrails, sample size, timeline, risks |
| `templates/test-plan.md` | Pre-registration plan frozen before launch: hypothesis, split, metrics, guardrails, sample size, timeline, risks Generated from `templates/test-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/results-report.md.j2` | Human-readable results report: per-metric table, guardrail verdict, statistical detail, pre-specified segments, sign-off |
| `templates/results-report.md` | Human-readable results report: per-metric table, guardrail verdict, statistical detail, pre-specified segments, sign-off Generated from `templates/results-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing.py` | Validate experiment-run artefact against schema + SRM gate + power gate | Pre-commit; CI on each experiment close |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[feature-flag-cleanup-discipline]]
- [[deterministic-test-data-pattern]]
- [[caching-strategy]]
- [[api-rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) power — under-powered experiments never decide, (b) SRM — failing SRM invalidates the result regardless of significance, and (c) significance — only Wilson-CI-clean wins ship. Every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/ab-testing.json",
  "type": "object",
  "required": [
    "experiment_id",
    "hypothesis",
    "primary_metric",
    "design",
    "variants",
    "result",
    "decision"
  ],
  "properties": {
    "experiment_id": {
      "type": "string",
      "pattern": "^EXP-[0-9]{3,6}$"
    },
    "hypothesis": {
      "type": "string",
      "minLength": 16
    },
    "primary_metric": {
      "type": "string",
      "minLength": 3
    },
    "design": {
      "type": "object",
      "required": [
        "mde",
        "alpha",
        "power",
        "expected_split"
      ]
    },
    "variants": {
      "type": "object",
      "minProperties": 2
    },
    "result": {
      "type": "object",
      "required": [
        "lift",
        "wilson_ci_low",
        "wilson_ci_high",
        "z",
        "p_value",
        "srm_chi_square_p"
      ]
    },
    "decision": {
      "type": "string",
      "enum": [
        "ship",
        "kill",
        "extend",
        "invalid-srm",
        "invalid-underpowered"
      ]
    }
  }
}
```

### `templates/sample-size.py`

```python
"""Sample-size calculator (proportions test, two-sided).

Pure stdlib implementation of the z-test for two proportions sample-size
formula. Equivalent to statsmodels.NormalIndPower.solve_power but with no
external dependency.

Usage:
    python sample-size.py                 # runs example
    python sample-size.py --self-test     # validates against known fixture
"""
from __future__ import annotations

import argparse
import math
import sys


def _phi_inv(p: float) -> float:
    """Inverse of the standard normal CDF (Beasley-Springer-Moro approx)."""
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0, 1)")
    a = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00)
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5]) * q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
           ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def sample_size_per_arm(p_baseline: float, mde_relative: float,
                        alpha: float = 0.05, power: float = 0.8) -> int:
    """Return required sample size per arm for a two-sided z-test on proportions."""
    if not (0 < p_baseline < 1):
        raise ValueError("p_baseline must be in (0, 1)")
    p2 = p_baseline * (1 + mde_relative)
    if not (0 < p2 < 1):
        raise ValueError(f"effective p2={p2:.4f} out of range")
    z_alpha = _phi_inv(1 - alpha / 2)
    z_beta = _phi_inv(power)
    p_avg = (p_baseline + p2) / 2
    num = (z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) +
           z_beta * math.sqrt(p_baseline * (1 - p_baseline) + p2 * (1 - p2))) ** 2
    den = (p2 - p_baseline) ** 2
    return math.ceil(num / den)


def main() -> int:
    ap = argparse.ArgumentParser(description="Sample-size calculator")
    ap.add_argument("--p-baseline", type=float, default=0.05)
    ap.add_argument("--mde-relative", type=float, default=0.10)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        # known reference: p=0.05, mde=0.10, alpha=0.05, power=0.8 -> ~31000-32000/arm
        n = sample_size_per_arm(0.05, 0.10)
        if not (29000 <= n <= 36000):
            sys.stderr.write(f"self-test failed: n={n}\n")
            return 1
        sys.stdout.write(f"self-test OK (n={n})\n")
        return 0
    n = sample_size_per_arm(args.p_baseline, args.mde_relative, args.alpha, args.power)
    sys.stdout.write(f"Required sample size per arm: {n}\n")
    sys.stdout.write(f"Total experiment size: {n * 2}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### `templates/analyzer.py`

```python
"""Pure-stdlib analyser for A/B experiments.

z-test for two proportions, Wilson 95% CI on the lift, and a chi-square
Sample Ratio Mismatch (SRM) check. No external dependency — uses
math.erf for the normal CDF and a closed-form chi-square (df=1) tail.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def _chi2_sf_df1(x: float) -> float:
    """Survival function of chi-square distribution with df=1."""
    if x <= 0:
        return 1.0
    return 2.0 * (1.0 - _norm_cdf(math.sqrt(x)))


@dataclass
class AnalysisResult:
    lift: float
    wilson_ci_low: float
    wilson_ci_high: float
    z: float
    p_value: float
    srm_chi_square_p: float


def wilson_ci(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 0.0)
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def srm_check(observed: dict[str, int], expected_split: dict[str, float]) -> float:
    total = sum(observed.values())
    chi = 0.0
    for k, frac in expected_split.items():
        e = total * frac
        if e <= 0:
            continue
        o = observed.get(k, 0)
        chi += (o - e) * (o - e) / e
    return _chi2_sf_df1(chi)


def analyse(variants: dict[str, dict[str, int]], expected_split: dict[str, float]) -> AnalysisResult:
    keys = list(variants.keys())
    if len(keys) != 2:
        raise ValueError("analyser expects exactly 2 variants")
    a, b = variants[keys[0]], variants[keys[1]]
    n1, c1 = a["exposures"], a["conversions"]
    n2, c2 = b["exposures"], b["conversions"]
    p1 = c1 / n1 if n1 else 0.0
    p2 = c2 / n2 if n2 else 0.0
    lift = (p2 - p1) / p1 if p1 > 0 else 0.0
    pooled = (c1 + c2) / (n1 + n2) if (n1 + n2) else 0.0
    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2)) if n1 and n2 and pooled and pooled < 1 else 0.0
    z = (p2 - p1) / se if se > 0 else 0.0
    p_value = 2 * (1 - _norm_cdf(abs(z)))

    # Wilson CI on the lift via difference of CIs (conservative)
    lo1, hi1 = wilson_ci(c1, n1)
    lo2, hi2 = wilson_ci(c2, n2)
    diff_low = lo2 - hi1
    diff_high = hi2 - lo1
    lift_low = diff_low / p1 if p1 > 0 else 0.0
    lift_high = diff_high / p1 if p1 > 0 else 0.0

    observed = {keys[0]: n1, keys[1]: n2}
    srm_p = srm_check(observed, expected_split)
    return AnalysisResult(lift, lift_low, lift_high, z, p_value, srm_p)


def main() -> int:
    ap = argparse.ArgumentParser(description="A/B analyser")
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        r = analyse(
            {"control": {"exposures": 12450, "conversions": 380},
             "variant_a": {"exposures": 12490, "conversions": 442}},
            {"control": 0.5, "variant_a": 0.5},
        )
        if not (r.srm_chi_square_p > 0.001 and r.wilson_ci_low > -1):
            sys.stderr.write(f"self-test failed: {r}\n")
            return 1
        sys.stdout.write(f"self-test OK: {r}\n")
        return 0
    if not args.file:
        ap.print_help()
        return 2
    obj = json.loads(Path(args.file).read_text())
    r = analyse(obj["variants"], obj["design"]["expected_split"])
    sys.stdout.write(json.dumps(r.__dict__, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### `templates/_smoke-test.json`

```json
{
  "experiment_id": "EXP-0142",
  "hypothesis": "Replacing pricing-page hero copy lifts trial-start CR by >= 5% relative",
  "primary_metric": "trial_started",
  "design": {
    "mde": 0.05,
    "alpha": 0.05,
    "power": 0.8,
    "expected_split": {
      "control": 0.5,
      "variant_a": 0.5
    }
  },
  "variants": {
    "control": {
      "exposures": 12450,
      "conversions": 380
    },
    "variant_a": {
      "exposures": 12490,
      "conversions": 442
    }
  },
  "result": {
    "lift": 0.165,
    "wilson_ci_low": 0.041,
    "wilson_ci_high": 0.292,
    "z": 2.61,
    "p_value": 0.009,
    "srm_chi_square_p": 0.78
  },
  "decision": "ship"
}
```
