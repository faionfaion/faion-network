# purpose: Variant analyser with z-test, Wilson CI, and SRM chi-square check
# consumes: per-variant {exposures, conversions} dict
# produces: result block ready for the experiment-run artefact
# depends-on: content/02-output-contract.xml
# token-budget-impact: ~400 tokens when loaded
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
