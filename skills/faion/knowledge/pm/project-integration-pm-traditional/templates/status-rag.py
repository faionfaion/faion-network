# purpose: Status RAG roll-up script: per-area signal → overall RAG
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""status_rag.py — compute deterministic project RAG from baseline YAML files.

Usage:
  python status_rag.py [project-root]

Expected files (YAML):
  evm-current.yaml  — keys: spi (float), cpi (float), bac (float)
  risk-register.yaml — keys: risks (list of {severity, mitigation_owner})

Output: JSON with RAG per dimension and overall.
"""

import json
import pathlib
import sys

import yaml

THRESHOLDS = {"green": 0.95, "yellow": 0.85}


def rag(value: float | None, higher_is_better: bool = True) -> str:
    if value is None:
        return "YELLOW"  # missing data is not GREEN
    v = value if higher_is_better else (1 / value if value else 0)
    if v >= THRESHOLDS["green"]:
        return "GREEN"
    if v >= THRESHOLDS["yellow"]:
        return "YELLOW"
    return "RED"


def main(root: str = ".") -> int:
    p = pathlib.Path(root)
    evm_path = p / "evm-current.yaml"
    risk_path = p / "risk-register.yaml"

    if not evm_path.exists():
        sys.stderr.write(f"Missing: {evm_path}\n")
        return 1

    evm = yaml.safe_load(evm_path.read_text())
    risks = yaml.safe_load(risk_path.read_text()) if risk_path.exists() else {}

    open_high = sum(
        1
        for r in risks.get("risks", [])
        if r.get("severity") == "HIGH" and not r.get("mitigation_owner")
    )

    spi = evm.get("spi")
    cpi = evm.get("cpi")
    bac = evm.get("bac")

    dims = {
        "schedule": rag(spi),
        "cost": rag(cpi),
        "risk": "RED" if open_high else "GREEN",
    }
    dims["overall"] = (
        "RED"
        if "RED" in dims.values()
        else ("YELLOW" if "YELLOW" in dims.values() else "GREEN")
    )

    result = {
        **dims,
        "spi": spi,
        "cpi": cpi,
        "eac": round(bac / cpi, 2) if bac and cpi else None,
        "open_high_risks": open_high,
    }
    sys.stdout.write(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
