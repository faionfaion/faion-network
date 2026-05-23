#!/usr/bin/env bash
# purpose: CI wrapper that parses Jacoco XML and enforces line/branch thresholds
# consumes: path to jacoco.xml + threshold args
# produces: pass/fail gate per jacoco-gate-in-ci rule
# depends-on: content/01-core-rules.xml rule jacoco-gate-in-ci
# token-budget-impact: ~250 tokens when loaded as context
# jacoco-gate.sh — fail CI if Jacoco coverage drops below thresholds.
# Usage: jacoco-gate.sh path/to/jacoco.xml [LINE_PCT] [BRANCH_PCT]
# Defaults: LINE=70, BRANCH=60
set -euo pipefail

XML="${1:?usage: jacoco-gate.sh JACOCO_XML [LINE] [BRANCH]}"
LINE="${2:-70}"
BRANCH="${3:-60}"

python3 - "$XML" "$LINE" "$BRANCH" <<'PY'
import sys, xml.etree.ElementTree as ET

xml_path, line_t, branch_t = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
tree = ET.parse(xml_path).getroot()

def pct(counter):
    miss = int(counter.attrib.get("missed", 0))
    cov  = int(counter.attrib.get("covered", 0))
    total = miss + cov
    return (cov / total * 100) if total else 100.0

line_cov   = next((pct(c) for c in tree.findall("counter") if c.attrib["type"] == "LINE"),   100.0)
branch_cov = next((pct(c) for c in tree.findall("counter") if c.attrib["type"] == "BRANCH"), 100.0)

print(f"line={line_cov:.1f}% branch={branch_cov:.1f}%")

fails = []
if line_cov   < line_t:   fails.append(f"line {line_cov:.1f}% < {line_t}%")
if branch_cov < branch_t: fails.append(f"branch {branch_cov:.1f}% < {branch_t}%")

if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("OK")
PY
