#!/usr/bin/env python3
"""eac-montecarlo.py — three-point EAC Monte Carlo simulation.

Models CPI uncertainty as a PERT/triangular distribution to produce
p10/p50/p90 EAC estimates. Use when point-estimate CPI is volatile.

Usage:
    python eac-montecarlo.py --bac 100000 --cpi-min 0.65 --cpi-likely 0.75 --cpi-max 0.95
"""
import argparse
import numpy as np


def eac_mc(bac: float, cpi_min: float, cpi_likely: float,
           cpi_max: float, n: int = 10_000) -> dict:
    cpi_samples = np.random.triangular(cpi_min, cpi_likely, cpi_max, n)
    eac_samples = bac / cpi_samples
    return {
        "p10": round(float(np.percentile(eac_samples, 10)), 0),
        "p50": round(float(np.percentile(eac_samples, 50)), 0),
        "p90": round(float(np.percentile(eac_samples, 90)), 0),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bac", type=float, required=True, help="Budget at completion")
    p.add_argument("--cpi-min", type=float, required=True, help="Pessimistic CPI")
    p.add_argument("--cpi-likely", type=float, required=True, help="Most likely CPI")
    p.add_argument("--cpi-max", type=float, required=True, help="Optimistic CPI")
    p.add_argument("--n", type=int, default=10_000, help="Simulation runs")
    args = p.parse_args()

    result = eac_mc(args.bac, args.cpi_min, args.cpi_likely, args.cpi_max, args.n)
    print(f"EAC Monte Carlo ({args.n:,} runs, BAC={args.bac:,.0f}):")
    print(f"  P10 (optimistic) : ${result['p10']:>10,.0f}")
    print(f"  P50 (median)     : ${result['p50']:>10,.0f}")
    print(f"  P90 (pessimistic): ${result['p90']:>10,.0f}")
    print(f"\nRange: ${result['p10']:,.0f} – ${result['p90']:,.0f}")
