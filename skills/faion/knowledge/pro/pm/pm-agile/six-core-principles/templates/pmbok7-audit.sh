#!/usr/bin/env bash
# pmbok7-audit.sh — Emit a PMBOK 7 six-principle audit form for a decision.
#
# Usage: ./pmbok7-audit.sh "ADR-005: Migrate to Linear"
# Output: Markdown audit table on stdout; fill PASS/WARN/FAIL + evidence in your editor.
set -euo pipefail

DECISION="${1:-<describe the decision here>}"

cat <<MD
# PMBOK 7 Audit: $DECISION

| Principle | PASS/WARN/FAIL | Evidence |
|-----------|----------------|----------|
| Adopt Holistic View | | |
| Focus on Value | | |
| Embed Quality | | |
| Lead Accountably | | |
| Integrate Sustainability | | |
| Build Empowered Teams | | |

## Constraints

- At least one WARN or FAIL required. If all pass, explain why with specific evidence.
- Separate audit from recommendation: do not write the recommendation in this document.

## Highest-Risk Violation

Principle: <name>
Evidence: <one sentence>
Mitigation: <one concrete action>
MD
