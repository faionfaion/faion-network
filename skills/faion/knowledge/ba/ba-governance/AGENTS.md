# BA Governance

## Summary

**One-sentence:** Establishes decision rights (RACI), change-control workflow, and stakeholder communication plan for a requirements stream before requirements work starts.

**One-paragraph:** Establishes decision rights (RACI), change-control workflow, and stakeholder communication plan for a requirements stream before requirements work starts. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- New product / squad — governance set-up before requirements work begins.
- Cross-stakeholder project (sponsor + dev + ops + legal) — communication plan mandatory.
- Existing process audit: rework, scope drift, sign-off ambiguity observed.
- Regulated build (SOX / HIPAA / GDPR) — decision audit trail required.

## Applies If (ALL must hold)

- Setting up decision rights, change-control, and approval workflow before requirements work starts.
- Project crosses three or more stakeholder groups (sponsor, dev, ops, legal).
- Elicitation logistics and technique selection prepared before interviews / workshops.
- Regulated build (SOX / HIPAA / GDPR) requiring a decision audit trail.

## Skip If (ANY kills it)

- Solo founder / single-team early MVP — formal governance burns time.
- Pure engineering refactor with no external stakeholders — PR review suffices.
- Research spike / discovery sprint where goal is learning, not committing scope.
- Crisis incident — use incident command, not governance workflow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project / squad charter | Markdown / Confluence | Sponsor / PMO |
| Stakeholder roster | Markdown / org chart | PM |
| RACI template | Markdown / spreadsheet | BA core team |
| Change-control system | Jira / Linear issue type | Eng tooling |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ba/ba-core/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ba-governance` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md.j2` | Markdown decision record — context + options + decision + owner + last_reviewed |
| `templates/decision-record.md` | Markdown decision record — context + options + decision + owner + last_reviewed Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-instance.json` | JSON instance of a filled decision record |
| `templates/governance.md.j2` | Full governance skeleton — decision-authority + change-control + comms-plan + owners |
| `templates/governance.md` | Full governance skeleton — decision-authority + change-control + comms-plan + owners Generated from `templates/governance.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/scaffold-governance.sh` | Bash scaffold that writes `governance.md` into `.aidocs/in-progress/<project>/` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-governance.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ba/ba-core/AGENTS.md`
- [[agile-ba-frameworks]]
- [[ambiguity-contradiction-detector]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-instance.json`

```json
{
  "project_id": "proj-2026-checkout",
  "decision_rights": [
    {
      "decision_type": "new requirement",
      "authority": "BA Lead",
      "escalation": "PM",
      "artefact": "Jira REQ"
    },
    {
      "decision_type": "scope change",
      "authority": "Steering Chair",
      "escalation": "Sponsor",
      "artefact": "Jira CR"
    },
    {
      "decision_type": "priority change",
      "authority": "Product Owner",
      "escalation": "PM",
      "artefact": "Backlog"
    },
    {
      "decision_type": "baseline update",
      "authority": "BA Lead + PO",
      "escalation": "PM",
      "artefact": "Confluence page"
    }
  ],
  "change_control": {
    "steps": [
      "submit_cr",
      "impact_assess",
      "authority_review",
      "decide",
      "baseline_update"
    ],
    "decision_sla_days": 5
  },
  "comms_plan": [
    {
      "audience": "Sponsor",
      "info": "status + risks",
      "format": "summary",
      "frequency": "weekly",
      "channel": "email",
      "feedback": "standing review slot"
    },
    {
      "audience": "Dev team",
      "info": "detailed reqs",
      "format": "full doc",
      "frequency": "per sprint",
      "channel": "Jira",
      "feedback": "refinement questions log"
    },
    {
      "audience": "Ops",
      "info": "release plan",
      "format": "checklist",
      "frequency": "pre-release",
      "channel": "Slack",
      "feedback": "ack + blockers thread"
    }
  ],
  "owner": "jane@team.io",
  "last_reviewed": "2026-05-23"
}
```

### `templates/scaffold-governance.sh`

```bash
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
```
