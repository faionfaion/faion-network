# Agent Integration — Project Integration Management

## When to use
- Multi-team / multi-vendor programs where decisions in one knowledge area routinely break another (scope ↔ schedule ↔ cost ↔ risk).
- Regulated programs where a Project Charter is a contractual artifact (gov contracts, FDA/EMA submissions, banking change boards).
- Hybrid agile + waterfall environments where component plans (scope, schedule, cost, quality, risk, comms, procurement) live in different tools and need a single integrated source of truth.
- Portfolio reporting where dozens of projects feed the same status rollup (PMO).
- Integrated Change Control across multiple workstreams when a change request affects more than one baseline.
- Partner with `change-control/`, `communications-management/`, `scope-management/`, `risk-management/`, `quality-management/`, `cost-estimation/`, `earned-value-management/`, `lessons-learned/`.

## When NOT to use
- Solo or duo teams — overhead exceeds value; a one-page README and a kanban board cover integration.
- Pure agile teams with one product backlog and one team — the Scrum framework already integrates work; bolting on PMBoK integration creates conflict.
- Pre-charter exploratory spikes / discovery sprints — formalizing integration too early kills learning.
- Projects with no formal sponsor or budget approval — integration without authorization is theatre.
- Portfolios where each project owner refuses to share artifacts in a common format — stop and fix governance first.

## Where it fails / limitations
- Charters drift from reality if not version-controlled; many orgs sign a PDF, file it, and never reconcile against the live plan.
- Integrated change control becomes a bottleneck when CAB / CCB meets infrequently — agile tempo collides with waterfall governance.
- LLMs producing status reports tend toward "GREEN washing" unless forced to compute RAG from quantitative inputs (variance thresholds).
- Component plans in heterogeneous tools (Jira for tasks, Smartsheet for schedule, Excel for budget, Confluence for risks) defeat integration unless a normalized export layer exists.
- The PM-as-integrator model assumes the PM has access; in matrix orgs functional managers gate visibility and the integration view is incomplete.
- Charter "success criteria" often degenerate into "on time, on budget, on scope" — meaningless without baselines and measurable outcomes.

## Agentic workflow
Treat each component plan as a typed YAML/JSON artifact in git: `charter.yaml`, `scope-baseline.yaml`, `schedule-baseline.yaml`, `cost-baseline.yaml`, `quality-plan.yaml`, `resource-plan.yaml`, `risk-register.yaml`, `comms-plan.yaml`, `procurement-plan.yaml`. An integration subagent reads all baselines, computes RAG status from variance thresholds, and emits the weekly Project Status Report deterministically. A change-control subagent intercepts every change request, runs cross-area impact analysis, and proposes baseline patches that humans approve. The agent never auto-approves changes touching cost or schedule baselines — those require sponsor sign-off recorded in git.

### Recommended subagents
- `faion-sdd-executor-agent` — drives integration as SDD tasks (TASK_charter, TASK_baseline_lock, TASK_status_report, TASK_change_request_NN).
- Custom `charter-author-agent` (opus) — drafts charter from intake form + business case; flags missing SMART objectives and acceptance criteria.
- Custom `status-aggregator-agent` (sonnet) — reads all baseline files, EVM metrics, risk register; emits Status Report with computed RAG (no opinion-based GREEN).
- Custom `change-impact-agent` (opus) — for each change request, walks scope/schedule/cost/quality/risk/resources and emits an impact matrix plus baseline patch proposal.
- Custom `plan-coherence-agent` (sonnet) — runs after every plan update; catches misalignments (schedule task not in WBS, cost line without WBS code, risk without owner).
- `password-scrubber-agent` — runs over charter / status reports before commit; charters often contain sponsor names, vendor pricing, customer NDAs.

### Prompt pattern
```
You are status-aggregator. Inputs: scope-baseline.yaml, schedule-baseline.yaml,
cost-baseline.yaml, evm-current.yaml, risk-register.yaml, last-status.yaml.
Compute Status Report. RAG rules:
  schedule: GREEN if SPI >= 0.95, YELLOW 0.85-0.95, RED < 0.85
  cost:     GREEN if CPI >= 0.95, YELLOW 0.85-0.95, RED < 0.85
  scope:    YELLOW if any unapproved CR open, RED if scope_change > 10%
  risk:     RED if any HIGH risk without mitigation owner
Emit STRICT JSON: { date, overall, dimensions[], accomplishments[],
planned[], issues[], metrics[]}.  Never invent numbers; mark missing as null.
```

Change-impact prompt: `Given change request CR-NN, walk all 8 component plans and emit matrix {area, impact, baseline_delta, approval_required}. Any cost or schedule delta requires sponsor approval; flag accordingly.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + git tags for baseline locks | Version-controlled charter, plans, baselines; tag `baseline-v1`, `baseline-v2` | preinstalled |
| `yq` / `jq` | Read/write component plan YAML/JSON | `apt install yq jq` |
| `pandoc` | Render charter and status reports to PDF/DOCX for sponsor sign-off | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Generate Gantt/dependency diagrams from schedule.yaml | `npm i -g @mermaid-js/mermaid-cli` |
| `pmcalc` (Python lib) / custom EVM script | Deterministic EVM, SPI, CPI, EAC computation | https://pypi.org/project/pmcalc |
| `pre-commit` | Block plan edits without baseline-version bump or change-request reference | https://pre-commit.com |
| `gh` / `glab` | Mirror change requests as PRs; CODEOWNERS = sponsor on baseline files | https://cli.github.com |
| `mkdocs` / `docusaurus` | Publish charter + status archive to internal portal | https://www.mkdocs.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Microsoft Project / Project for the Web | SaaS | REST (Project Online), Graph | Industry standard schedule baseline; Graph/Project APIs allow bidirectional sync. |
| Smartsheet | SaaS | REST | Common PMO host for plans, baselines, status; CSV/JSON export. |
| Jira + Advanced Roadmaps / Plans | SaaS | REST + JQL | Schedule integration via Plans API; weak baseline locking — must enforce externally. |
| Linear / Asana / ClickUp | SaaS | REST | Lighter alternative; export to canonical YAML for integration. |
| Wrike / Monday.com | SaaS | REST | Mid-market PPM with charter/status templates. |
| Planview / Clarizen / Sciforma | SaaS | REST | Enterprise PPM; deeper integration but slower change cadence. |
| ServiceNow SPM / PPM | SaaS | REST | Common in regulated enterprises; CAB integration built-in. |
| Confluence / Notion / SharePoint | SaaS | REST | Charter and status archive; weak schema — validate before commit. |
| Power BI / Tableau / Looker | SaaS | REST | Status dashboard rollup; pull from baselines, not from feelings. |
| GitHub Projects / GitLab Epics | SaaS | REST/GraphQL | Lightweight integrated view for engineering-led programs. |

## Templates & scripts
README provides Project Charter and Project Status Report templates. Inline below: a 30-line script that computes report-ready RAG status from baseline files.

```python
#!/usr/bin/env python3
"""status_rag.py — compute deterministic project RAG from baselines."""
import json, sys, yaml, pathlib

THR = {"green": 0.95, "yellow": 0.85}

def rag(idx: float) -> str:
    if idx >= THR["green"]: return "GREEN"
    if idx >= THR["yellow"]: return "YELLOW"
    return "RED"

def main(root: str = ".") -> int:
    p = pathlib.Path(root)
    evm = yaml.safe_load((p / "evm-current.yaml").read_text())
    risks = yaml.safe_load((p / "risk-register.yaml").read_text())
    open_high = sum(1 for r in risks["risks"]
                    if r["severity"] == "HIGH" and not r.get("mitigation_owner"))
    out = {
        "schedule": rag(evm["spi"]),
        "cost": rag(evm["cpi"]),
        "risk": "RED" if open_high else "GREEN",
        "spi": evm["spi"],
        "cpi": evm["cpi"],
        "eac": evm["bac"] / evm["cpi"] if evm["cpi"] else None,
    }
    out["overall"] = "RED" if "RED" in out.values() else (
        "YELLOW" if "YELLOW" in out.values() else "GREEN")
    json.dump(out, sys.stdout, indent=2)
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

## Best practices
- Charter is law — version it in git, sign it (digital sign or `Signed-off-by:`), and re-baseline only via approved change requests.
- One source of truth per artifact: schedule lives in one tool, exported to YAML for integration; banning duplicate plans prevents drift.
- Status RAG must be computed, never opinion-based. Define variance thresholds in `.integration.yaml` and have the agent enforce them.
- Integrated Change Control runs through PRs (or equivalent) — CR description, impact matrix, baseline patch, sponsor approval, merge tagged `baseline-vN+1`.
- Status reports go out on a calendar cadence; missed reports trigger automatic escalation, not silence.
- Component plan owners are named in `.CODEOWNERS` so PRs route correctly; PM owns integration, not every plan.
- Tie integration to lessons-learned — every approved CR generates a candidate lesson if it crossed >2 baselines.
- Charter success criteria must be SMART and measurable; reject "improve customer satisfaction" without metric, baseline, target, and date.
- Always pair scope changes with schedule and cost re-estimates in the same PR; refuse standalone scope edits.
- Re-baseline triggers: scope change > 10%, schedule slip > 15%, cost overrun > 10%, or sponsor change.

## AI-agent gotchas
- LLMs default to "GREEN" status when data is missing — force null on missing inputs and compute RAG only from non-null values; missing data → YELLOW with reason.
- Agents drafting charters fabricate stakeholders, dollar figures, and dates; require all numbers to come from explicit input fields, no inference.
- Integrated change control without an audit trail breaks regulator audits; every CR must have a unique ID, immutable diff, and approver signature in git history.
- Cross-baseline impact analysis hallucinates dependencies — feed the agent the actual dependency graph (WBS + schedule predecessors), do not let it infer.
- Status report generation can leak confidential info (vendor pricing, customer names, employee performance) when sourced from raw plans; run scrubber before publishing.
- Agents conflate "Project Manager authority" with "agent autonomy"; the agent has zero authority to approve baseline changes — it proposes, sponsor approves.
- Reading multiple component plan files into one prompt explodes context; use a summary index and pull individual files on demand.
- Charter freeze is a discipline gap: agents will happily edit a charter mid-flight; enforce with branch protection and CODEOWNERS.
- Human-in-the-loop checkpoints (mandatory): charter approval, baseline lock, baseline change, scope/cost/schedule deltas, change-request approval, project closure.

## References
- PMI PMBOK 7e — Project Integration Management; Performance Domain integration.
- PMI PMBOK 6e — Project Integration Management Knowledge Area (still richest source for charter / change control templates).
- ISO 21500 / 21502 — Project management — Guidance on project, programme and portfolio management.
- PRINCE2 7 — Directing and Managing a Project (analogous integration practices).
- Kerzner, H. — "Project Management: A Systems Approach" (deep integration treatment).
- Sibling methodologies: `change-control/`, `communications-management/`, `scope-management/`, `risk-management/`, `cost-estimation/`, `earned-value-management/`, `quality-management/`, `lessons-learned/`.
