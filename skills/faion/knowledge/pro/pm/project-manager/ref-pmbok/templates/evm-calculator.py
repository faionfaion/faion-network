#!/usr/bin/env python3
"""EVM calculator: SV, CV, SPI, CPI, EAC, ETC, VAC, RAG.

Input JSON file:
  {"bac": 100000, "pv": 50000, "ev": 45000, "ac": 48000}

All values in the same currency unit.
RAG thresholds: green if SPI>=0.95 and CPI>=0.95; amber if both>=0.85; else red.

Usage: evm-calculator.py <inputs.json>
"""
import json
import math
import sys


def evm(bac: float, pv: float, ev: float, ac: float) -> dict:
    def safe_div(a: float, b: float):
        if b == 0 or math.isnan(b):
            return None
        return round(a / b, 3)

    sv = round(ev - pv, 2)
    cv = round(ev - ac, 2)
    spi = safe_div(ev, pv)
    cpi = safe_div(ev, ac)
    eac = round(bac / cpi, 2) if cpi else None
    etc = round(eac - ac, 2) if eac is not None else None
    vac = round(bac - eac, 2) if eac is not None else None

    if spi is not None and cpi is not None:
        if spi >= 0.95 and cpi >= 0.95:
            rag = "green"
        elif spi >= 0.85 and cpi >= 0.85:
            rag = "amber"
        else:
            rag = "red"
    else:
        rag = "unknown"

    return {
        "SV":  sv,   "formula_SV":  "EV - PV",
        "CV":  cv,   "formula_CV":  "EV - AC",
        "SPI": spi,  "formula_SPI": "EV / PV",
        "CPI": cpi,  "formula_CPI": "EV / AC",
        "EAC": eac,  "formula_EAC": "BAC / CPI",
        "ETC": etc,  "formula_ETC": "EAC - AC",
        "VAC": vac,  "formula_VAC": "BAC - EAC",
        "RAG": rag,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: evm-calculator.py <inputs.json>")
        sys.exit(2)
    inp = json.load(open(sys.argv[1]))
    result = evm(
        bac=float(inp["bac"]),
        pv=float(inp["pv"]),
        ev=float(inp["ev"]),
        ac=float(inp["ac"]),
    )
    print(json.dumps(result, indent=2))
