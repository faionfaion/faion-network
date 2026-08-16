# Project Integration Management

## Summary

**One-sentence:** PM as integrator: ensures decisions in scope/schedule/cost/quality/risk/resources/comms/procurement are consistent and mutually reinforcing via charter, baseline, status RAG.

**One-paragraph:** PM as integrator: ensures decisions in scope/schedule/cost/quality/risk/resources/comms/procurement are consistent and mutually reinforcing via charter, baseline, status RAG. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-project-integration.py` enforces the output contract.

**Ефективно для:**

- Programs with ≥4 knowledge areas in scope.
- Multi-vendor programs needing integrator authority.
- Projects where charter is the contract between Sponsor and PM.
- Status reporting that rolls up area-level signal to portfolio.

## Applies If (ALL must hold)

- Project charter is authored or being authored.
- Each knowledge area has a baseline.
- Status cadence is agreed with Sponsor.

## Skip If (ANY kills it)

- Single-area project (e.g., pure dev sprint).
- Pre-charter discovery phase.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter | Markdown | Sponsor + PM |
| Per-area baselines | scope/schedule/cost/quality/risk/resources/comms/procurement | area leads |
| Status cadence | weekly/biweekly | Sponsor |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[change-control]] | integration tracks baseline integrity via change control |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-charter` | sonnet | Judgement on charter scope + authority. |
| `integrate-baselines` | sonnet | Cross-area consistency check. |
| `roll-up-rag` | haiku | Mechanical RAG roll-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-rag.py` | Status RAG roll-up script: per-area signal → overall RAG |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[change-control]]
- [[seven-performance-domains]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/status-rag.py`

```python
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
```
