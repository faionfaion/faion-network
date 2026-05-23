#!/usr/bin/env bash
# purpose: scaffold a per-project governance.md skeleton with named-owner placeholders
# consumes: project slug (and optional output path) supplied on the CLI
# produces: governance.md under .aidocs/in-progress/<slug>/ (decision-record artefact)
# depends-on: templates/governance.md sibling for full structure reference
# token-budget-impact: zero at runtime (bash script, no LLM in the loop)
#
# scaffold-governance.sh — generate governance.md skeleton under .aidocs/in-progress/.
# Usage: ./scaffold-governance.sh <project-slug> [output-path]
# Example: ./scaffold-governance.sh my-project
#          ./scaffold-governance.sh my-project .aidocs/in-progress/my-project/governance.md
set -euo pipefail

PROJECT="${1:?project slug required}"
OUT="${2:-.aidocs/in-progress/$PROJECT/governance.md}"
mkdir -p "$(dirname "$OUT")"

cat >"$OUT" <<EOF
# Governance — $PROJECT

_Last reviewed: $(date -I) — re-validate every 30 days._

## Decision Authority

| Decision Type | Authority (named person) | Escalation | Artifact |
|---------------|--------------------------|------------|----------|
| New requirement | BA Lead | PM | Jira REQ |
| Scope change | Steering | Sponsor | Jira CR |
| Priority change | PO | PM | Backlog |

## Change Control

1. Submit CR (Jira "CR" type)
2. Impact assessment (T-shirt: S/M/L/XL) — mandatory for all CRs
3. Review by authority from matrix above
4. Approve / Reject (with reason) / Defer (owner + date)
5. Update baseline; link CR → REQ

## Communication

| Audience | Info | Format | Frequency | Channel | Feedback |
|----------|------|--------|-----------|---------|---------|
| Sponsor | Status, risks | Summary | Weekly | Email | Review slot |
| Dev | Reqs detail | Full doc | Per sprint | Jira | Refinement log |
| Ops | Release plan | Checklist | Pre-release | Slack | Ack + blockers |

## Owners

- Artifact owner: <FILL: named individual + email>
- Decision-log owner: <FILL: named individual + email>
- Re-validation cadence: 30 days
- Stakeholder contacts: 1Password vault (NOT in this file)
EOF

echo "Wrote $OUT"
echo "REMINDER: replace <FILL: ...> placeholders with named individuals before sign-off."
