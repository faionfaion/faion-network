"""quality_gate.py — pass/fail a PR against quality-plan.yaml thresholds.

Usage:
  python quality_gate.py quality-plan.yaml ci-output.json
  exit 0 = PASS, exit 1 = FAIL

quality-plan.yaml shape:
  thresholds:
    test_coverage:     {op: ">=", value: 0.80}
    critical_bugs:     {op: "<=", value: 0}
    api_response_ms:   {op: "<=", value: 500}

ci-output.json shape:
  {"test_coverage": 0.85, "critical_bugs": 0, "api_response_ms": 320}
"""

import json
import pathlib
import sys

import yaml


def main(plan_path: str, ci_path: str) -> int:
    rules = yaml.safe_load(pathlib.Path(plan_path).read_text()).get("thresholds", {})
    actual = json.loads(pathlib.Path(ci_path).read_text())

    fails: list[str] = []
    for key, threshold in rules.items():
        value = actual.get(key)
        if value is None:
            fails.append(f"MISSING  {key} (required by quality-plan.yaml)")
            continue
        op = threshold.get("op", ">=")
        target = threshold["value"]
        ok = (value >= target) if op == ">=" else (value <= target)
        status = "PASS" if ok else "FAIL"
        line = f"{status}  {key}: {value} {op} {target}"
        sys.stdout.write(line + "\n")
        if not ok:
            fails.append(line)

    if fails:
        sys.stderr.write(f"\nQuality gate FAILED ({len(fails)} criterion/criteria)\n")
        return 1
    sys.stdout.write("\nQuality gate PASSED\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: quality_gate.py <quality-plan.yaml> <ci-output.json>\n")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
