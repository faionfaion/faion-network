# Agent Integration — Project Closure

## When to use
- Project objectives met and final deliverables accepted (normal closure).
- Project cancelled mid-flight: still close formally to recover value, release resources, capture lessons.
- Phase-end of multi-phase programs (each phase closes before the next funds).
- Agency engagement final invoice and warranty handover.
- M&A integration: closing legacy projects so absorbed teams can re-baseline.

## When NOT to use
- Project still has open scope, unresolved issues, or unsigned acceptance — closure first requires acceptance.
- Operational/run-rate work that has no defined endpoint — use service transition documents instead.
- Long-tail support work — that's run/operations, not project closure.

## Where it fails / limitations
- Closure is the most-skipped phase: teams roll onto the next project before formal handover.
- Lessons learned are captured in slides nobody reads; need a queryable retrospective DB.
- Resources stay allocated on paper while doing other work, distorting capacity planning.
- Contracts left open accrue costs (SaaS auto-renew, cloud reservations).
- Knowledge walks out: subject-matter experts leave teams without recording runbooks.
- Acceptance criteria written ambiguously make formal sign-off subjective.

## Agentic workflow
A subagent walks the closure checklist, audits current state of contracts, costs, accesses, and documentation, and produces a closure packet (final report, lessons summary, handover document, archive index). The agent never marks closure complete — it produces the artefacts and a checklist that the PM and sponsor sign off. Treat closure as data: each checklist item is a YAML record with status, owner, evidence link. Tie closure into the SDD lifecycle: feature folder moves `in-progress/ → done/` only after closure tasks are green. Pair with Lessons Learned methodology (separate methodology) for retrospective facilitation.

### Recommended subagents
- `faion-pm-agent` — drives checklist, drafts final report.
- `faion-improver` — runs lessons-learned facilitation prompts; mines patterns across closures.
- `faion-business-analyst` — verifies every requirement traces to an accepted deliverable.
- `faion-sdd-executor-agent` — moves SDD feature folder to `done/` after closure pass.

### Prompt pattern
```
Inputs: charter.md, scope_baseline.md, schedule_baseline.csv,
budget_baseline.csv, current_status.md, deliverables.yaml,
contracts.yaml, accesses.yaml.
Output: closure_packet/ — {final_report.md, acceptance_log.md,
handover.md, archive_index.md, closure_checklist.yaml}.
Each checklist item: {id, name, status: pending|done|na,
owner, evidence_url, blocker}.
```

```
Audit closure_checklist.yaml against today's state:
report items where status=done but no evidence_url, or pending with
no blocker reason. Output: critical-path open items only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh`, `glab`, `jira-cli` | Close issues, archive milestones, export ticket history | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `az devops`, `ado-rest` | Close iterations and work items in ADO | https://learn.microsoft.com/cli/azure/devops |
| `git archive` / `git bundle` | Archive code repository state at closure | https://git-scm.com |
| `pandoc` | Render final report → DOCX/PDF for sponsor sign-off | https://pandoc.org |
| `aws s3 sync` / `gsutil rsync` / `azcopy` | Move artefacts to long-term cold storage | cloud-vendor docs |
| `op` (1Password CLI) | Revoke project-scoped credentials | https://developer.1password.com/docs/cli |
| `terraform destroy` | Decommission temporary infra cleanly | https://www.terraform.io |
| `docusign-cli` | Collect electronic acceptance signatures | https://developers.docusign.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian Confluence | SaaS | Yes — REST API | Archive page tree; mark space read-only |
| Notion | SaaS | Yes — REST API | Project DB, change status to "Closed" |
| DocuSign / Adobe Sign | SaaS | Yes — REST API | Acceptance form signatures |
| ServiceNow | SaaS | Yes — Table API | Operations handover ticket; CMDB updates |
| Jira / ADO / GitHub Projects | SaaS | Yes — REST/GraphQL | Close epics, archive boards |
| 1Password | SaaS | Yes — `op` CLI | Revoke project vault access |
| AWS / GCP / Azure | SaaS | Yes — provider CLIs | Decommission infra; budget alerts |
| Sharepoint / Google Drive | SaaS | Yes — Graph / Drive API | Archive document library, set retention |

## Templates & scripts
See `templates.md` for closure checklist, deliverable acceptance, handover. Inline closure auditor (≤50 lines):

```python
# closure_audit.py — verify a closure_checklist.yaml is complete.
import yaml, sys

REQUIRED = {
    "deliverable_acceptance", "final_costs_recorded", "invoices_processed",
    "purchase_orders_closed", "contracts_terminated", "team_released",
    "equipment_returned", "access_revoked", "lessons_learned_session",
    "final_report", "documents_archived", "ops_handover", "stakeholders_notified",
}

def audit(path):
    items = yaml.safe_load(open(path))
    by_id = {i["id"]: i for i in items}
    missing = REQUIRED - set(by_id)
    bad = []
    for item in items:
        if item["status"] == "done" and not item.get("evidence_url"):
            bad.append((item["id"], "done without evidence"))
        if item["status"] == "pending" and not item.get("blocker"):
            bad.append((item["id"], "pending without blocker reason"))
        if item["status"] not in ("done", "pending", "na"):
            bad.append((item["id"], f"invalid status {item['status']}"))
    for m in missing:
        print(f"[FAIL] missing required item: {m}")
    for nid, msg in bad:
        print(f"[FAIL] {nid}: {msg}")
    sys.exit(1 if missing or bad else 0)

if __name__ == "__main__":
    audit(sys.argv[1])
```

## Best practices
- Schedule closure at kickoff: it's a deliverable, not an afterthought.
- Acceptance criteria must be observable and signed before closure starts; ambiguous "looks good" causes drift.
- Run lessons-learned before the team disperses; afterwards memories fade and the room scatters.
- Decommission infrastructure in stages: first read-only, then revoke writes, then deprovision; reverts are easier early.
- Archive code with a tagged release named `closure-<project>` for forensic recovery.
- Recover salvageable assets (designs, components, datasets) into a reusable library before deletion.
- Celebrate. Skipping recognition damages future engagement; budget a small line item from kickoff.
- For cancelled projects, document cancellation rationale formally — it prevents the same idea resurfacing without learning.

## AI-agent gotchas
- Agents over-rely on issue-tracker "Done" state as evidence of acceptance — actual acceptance requires a signed artefact, not a status flip.
- "Lessons learned" generated solely by the agent are platitudes; require quoted contributions per attendee.
- Auto-revoking access can break ongoing run/operations if handover isn't complete; sequence: handover ack → revoke.
- Final cost reconciliation often misses delayed invoices (vendor net-60); agent should flag "pending invoices" not auto-zero.
- Closure script that deletes cloud resources without a hold period risks data loss; default to 30-day soft-delete + retention policy.
- Don't let agents "summarise" the final report into bullet points — sponsors need narrative for stakeholder communication.
- Privacy: closure packets often contain salaries, vendor rates, customer data; restrict access before agents publish.

## References
- PMBOK Guide 7th Edition — Delivery Performance Domain (Closure).
- ISO 21502 — Project closure guidance.
- PRINCE2 — Closing a Project (CP) process.
- "Project Retrospectives" — Norman Kerth (lessons-learned facilitation).
- "Agile Retrospectives" — Esther Derby & Diana Larsen (alternative formats for closure-stage retros).
