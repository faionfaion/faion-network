# purpose: Template fixture for fine-tune-vs-prompt-economic-model: economic-model.py
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
"""Fine-tune vs prompt economic kernel.

Usage: python3 economic-model.py [inputs.json] > economic-model.json
inputs.json holds the `inputs` block from content/02-output-contract.xml plus
workload / owner; with no argument the worked example from 05-examples.xml runs.
Pure stdlib, no network.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import sys

DAYS_PER_MONTH = 30
HORIZON_MONTHS = 12
NEVER_AFTER_MONTHS = 36  # rule r3: break-even beyond this is reported as "never"

EXAMPLE = {
    "workload": "support-classifier", "owner": "<owner-email>",
    "inputs": {
        "input_tokens_per_day": 8_000_000, "output_tokens_per_day": 1_000_000,   # r6: split, never blended
        "current_input_cost_per_k": 0.003, "current_output_cost_per_k": 0.015,  # 3.0 / 15.0 USD per M tokens
        "ft_input_cost_per_k": 0.00025, "ft_output_cost_per_k": 0.00125,        # 0.25 / 1.25 USD per M tokens
        "ft_training_cost": 800.0, "ops_overhead_per_month": 400.0,          # r1: must be > 0
        "vendor_risk_premium_pct": 15.0,                                     # r4: 10-20% default band
    },
}


def kernel(i: dict) -> dict:
    """One scenario: monthly costs, delta, 12-month sum, break-even month (r5)."""
    if i["ops_overhead_per_month"] <= 0:
        raise ValueError("ops_overhead_per_month must be > 0 (rule r1)")
    prompt = (i["input_tokens_per_day"] * i["current_input_cost_per_k"]
              + i["output_tokens_per_day"] * i["current_output_cost_per_k"]) / 1000 * DAYS_PER_MONTH
    ft_infer = (i["input_tokens_per_day"] * i["ft_input_cost_per_k"]
                + i["output_tokens_per_day"] * i["ft_output_cost_per_k"]) / 1000 * DAYS_PER_MONTH
    risk_carry = ft_infer * i["vendor_risk_premium_pct"] / 100
    ft = ft_infer + i["ops_overhead_per_month"] + risk_carry + i["ft_training_cost"] / HORIZON_MONTHS
    delta = prompt - ft
    if delta <= 0:
        break_even: int | str = "never"
    else:
        month = math.ceil(i["ft_training_cost"] / delta)
        break_even = max(month, 1) if month <= NEVER_AFTER_MONTHS else "never"
    return {
        "monthly_prompt_cost": round(prompt, 2), "monthly_ft_cost": round(ft, 2),
        "monthly_delta_usd": round(delta, 2), "npv_12mo_usd": round(delta * HORIZON_MONTHS, 2),
        "break_even_month": break_even,
    }


def perturb(i: dict, factors: dict[str, float]) -> dict:
    return {k: v * factors.get(k, 1.0) for k, v in i.items()}


def scenarios(i: dict) -> dict:
    """Rule r2: the four mandatory scenarios."""
    vol = {"input_tokens_per_day": 0.5, "output_tokens_per_day": 0.5}
    return {
        "base": kernel(i),
        "volume_minus_50": kernel(perturb(i, vol)),
        "volume_plus_50": kernel(perturb(i, {k: 1.5 for k in vol})),
        "prompt_cost_minus_30_eoy": kernel(perturb(i, {"current_input_cost_per_k": 0.7, "current_output_cost_per_k": 0.7})),
    }


def sensitivity(i: dict) -> list[dict]:
    """Rule r3: break-even under +-20% volume, +-20% $/k input, +-50% ops overhead."""
    sweeps = [
        ("volume", 20, ("input_tokens_per_day", "output_tokens_per_day")),
        ("$/k_input", 20, ("current_input_cost_per_k",)),
        ("ops_overhead", 50, ("ops_overhead_per_month",)),
    ]
    rows = []
    for dim, pct, keys in sweeps:
        for sign in (-1, 1):
            f = 1 + sign * pct / 100
            rows.append({"dimension": dim, "delta_pct": sign * pct,
                         "break_even_month": kernel(perturb(i, {k: f for k in keys}))["break_even_month"]})
    return rows


def recommend(sc: dict) -> str:
    """Procedure step 7 gate: break-even > 12 months in 3 of 4 scenarios overrides the base."""
    def late(s: dict) -> bool:
        return s["break_even_month"] == "never" or s["break_even_month"] > HORIZON_MONTHS
    if sum(late(s) for s in sc.values()) >= 3:
        return "prompt-or-other"
    return "borderline" if late(sc["base"]) else "fine-tune"


def build(spec: dict) -> dict:
    i = spec["inputs"]
    sc = scenarios(i)
    return {
        "workload": spec["workload"], "owner": spec["owner"],
        "created_at": dt.date.today().isoformat(),
        "inputs": i, "scenarios": {k: {f: v[f] for f in ("monthly_delta_usd", "npv_12mo_usd", "break_even_month")} for k, v in sc.items()},
        "sensitivity": sensitivity(i),
        "outputs_base": {"monthly_prompt_cost": sc["base"]["monthly_prompt_cost"], "monthly_ft_cost": sc["base"]["monthly_ft_cost"]},
        "recommendation": recommend(sc),
    }


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else EXAMPLE
    json.dump(build(spec), sys.stdout, indent=2)
    sys.stdout.write("\n")
