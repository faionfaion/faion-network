#!/usr/bin/env python3
"""evm.py — minimal EVM calculator for a single work package.

Input:  WP dataclass with bac, pct_planned, pct_complete, ac
Output: dict with full EVM metric set (pv, ev, ac, sv, cv, spi, cpi,
        eac, etc, vac, tcpi)

Usage as library or script:
    python evm.py --bac 100000 --planned 0.50 --complete 0.40 --ac 55000
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass


@dataclass
class WP:
    bac: float           # budget at completion
    pct_planned: float   # fraction planned (0.0-1.0)
    pct_complete: float  # fraction complete (0.0-1.0), OBJECTIVE ONLY
    ac: float            # actual cost to date


def evm(wp: WP) -> dict:
    pv = wp.bac * wp.pct_planned
    ev = wp.bac * wp.pct_complete
    ac = wp.ac
    sv = ev - pv
    cv = ev - ac
    spi = ev / pv if pv else float("nan")
    cpi = ev / ac if ac else float("nan")
    eac = wp.bac / cpi if cpi else float("nan")
    etc = eac - ac
    vac = wp.bac - eac
    tcpi = (wp.bac - ev) / (wp.bac - ac) if (wp.bac - ac) else float("nan")
    return dict(
        pv=round(pv, 2), ev=round(ev, 2), ac=round(ac, 2),
        sv=round(sv, 2), cv=round(cv, 2),
        spi=round(spi, 3), cpi=round(cpi, 3),
        eac=round(eac, 0), etc=round(etc, 0),
        vac=round(vac, 0), tcpi=round(tcpi, 3),
    )


def color(idx: float) -> str:
    if 0.95 <= idx <= 1.05:
        return "GREEN"
    if 0.85 <= idx < 0.95:
        return "YELLOW"
    return "RED"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bac", type=float, required=True)
    p.add_argument("--planned", type=float, required=True)
    p.add_argument("--complete", type=float, required=True)
    p.add_argument("--ac", type=float, required=True)
    args = p.parse_args()
    m = evm(WP(args.bac, args.planned, args.complete, args.ac))
    for k, v in m.items():
        suffix = f"  [{color(v)}]" if k in ("spi", "cpi") else ""
        print(f"  {k.upper():5} = {v}{suffix}")
    if m["tcpi"] > 1.10:
        print("\n  TCPI > 1.10: project likely unrecoverable — escalate to sponsor.")
