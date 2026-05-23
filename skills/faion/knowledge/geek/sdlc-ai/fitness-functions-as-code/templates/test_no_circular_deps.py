# purpose: modularity fitness function — no circular import cycles
# consumes: repo source tree
# produces: pass/fail
# depends-on: ADR docs/adr/0007-layered-arch.md
# token-budget-impact: ~150 tokens
import subprocess
import json


def test_no_circular_deps() -> None:
    """ADR 0007 layered arch: no circular import cycles."""
    out = subprocess.check_output(["tach", "check", "--output", "json"]).decode()
    data = json.loads(out)
    cycles = [v for v in data.get("violations", []) if v.get("kind") == "cycle"]
    assert not cycles, f"Found {len(cycles)} cycles: {cycles[:3]}"
