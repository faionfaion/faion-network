# Agent Integration — Project Closure

## When to use
- End of any contracted / fixed-bid engagement where formal acceptance is required.
- Cancelled or descoped projects (closure must capture salvage value and lessons).
- Phase-gated programs at major milestone transitions (Phase 1 → Phase 2 closure).
- Internal projects transitioning from build to operate (handover to ops/support).

## When NOT to use
- Continuous-flow / product teams — there is no closure event, only release boundaries.
- Solo throwaway prototypes — a `DONE.md` line is enough.
- Projects still in execution; closure run too early loses incomplete deliverables.

## Where it fails / limitations
- Closure gets skipped under deadline pressure; missing acceptance signoff causes invoice disputes 6 months later.
- Lessons-learned sessions run after team disperses → low attendance, weak data.
- Document archive is "the shared drive" → unfindable in 12 months.
- Operations handover happens without runbooks; ops team inherits unsupportable system.
- Celebration step is the first to be cut, demoralizing the team.

## Agentic workflow
A subagent excels at the closure-administration grind: assemble the closure checklist from project artefacts, generate the deliverable acceptance form pre-filled per item, draft the final report from status reports + change register + EVM, package documents into a structured archive (with a `MANIFEST.json`), and produce a per-stakeholder closure communication. Humans drive acceptance signoffs, lessons-learned facilitation, and recognition. Run the agent at the end of execution, then again 30 days post-go-live for benefits-tracking handoff.

### Recommended subagents
- `faion-pm-agent` — owns closure checklist; drafts final report and handover doc.
- `faion-sdd-execution` quality gate — verifies acceptance criteria are met against the original specs.
- `faion-improver` agent (skill) — facilitates lessons-learned and writes follow-up actions.
- `faion-communicator` — drafts per-audience closure communications (sponsor, team, ops).

### Prompt pattern
```
Generate the project closure report. Inputs: charter, final WBS, schedule
baseline+actuals, budget baseline+actuals, change register, risk register,
last 5 status reports.
Output sections: executive summary, deliverables-vs-plan, schedule
performance (SPI), cost performance (CPI), top 5 lessons, outstanding
items, recommended follow-ups, acknowledgments. Cite sources for every
metric. Do NOT invent metrics.
```

```
Build the operations handover doc:
- system overview, architecture, dependencies, access, runbook links,
- known issues + workarounds, monitoring + alert thresholds,
- L1/L2/L3 contacts, escalation matrix, scheduled maintenance.
Flag missing-runbook sections as MUST-FILL.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git archive` + `tar` | Snapshot repo state at closure | git docs |
| `pandoc` | Convert closure report .md → DOCX/PDF for signoff | https://pandoc.org |
| `gh` CLI | Lock issues/milestones, archive repo at closure | https://cli.github.com |
| `aws s3 sync` / `rclone` | Push project archive to long-term storage | vendor docs |
| `7z` / `tar` | Bundle archive directory with checksums | system package |
| `sha256sum` | Manifest checksums for archive integrity | coreutils |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Confluence project space + archive | SaaS | Yes — REST API | Standard PMO archive target. |
| SharePoint Online | SaaS | Yes — Graph API | Enterprise default with retention policies. |
| Notion archive workspace | SaaS | Yes — REST API | Light, agent-friendly. |
| Jira release + archive | SaaS | Yes — REST API | Lock sprints, mark fixVersion released. |
| AWS S3 Glacier / Azure Blob Archive | Cloud | Yes — SDK/CLI | Long-term low-cost retention. |
| ServiceNow CMDB | Enterprise SaaS | Yes — REST API | For ops handover registration. |
| Linear cycles + projects | SaaS | Yes — GraphQL | Mark project complete with metrics. |

## Templates & scripts
See `templates.md` for closure checklist, acceptance form, handover template. Helper to bundle the archive with a manifest:

```bash
#!/usr/bin/env bash
# closeout-archive.sh — bundle a project closure archive with checksums.
set -euo pipefail
proj="${1:?usage: closeout-archive.sh <project-slug>}"
out="closeout-${proj}-$(date +%Y%m%d)"
mkdir -p "$out"/{planning,execution,technical,contracts,closure}
cp -r docs/charter*    "$out/planning/"     2>/dev/null || true
cp -r docs/wbs*        "$out/planning/"     2>/dev/null || true
cp -r status-reports/  "$out/execution/"    2>/dev/null || true
cp -r CHANGE-REGISTER* "$out/execution/"    2>/dev/null || true
cp -r RISK-REGISTER*   "$out/execution/"    2>/dev/null || true
cp -r contracts/       "$out/contracts/"    2>/dev/null || true
cp -r docs/runbook*    "$out/closure/"      2>/dev/null || true
( cd "$out" && find . -type f -exec sha256sum {} \; > MANIFEST.sha256 )
tar czf "${out}.tar.gz" "$out"
echo "archive: ${out}.tar.gz"
```

## Best practices
- Run lessons-learned BEFORE the team disperses, not after; resentment fades but so does memory.
- Get acceptance signoff in writing per deliverable — verbal "looks good" never holds up at invoice time.
- Capture both successes and failures; teams that only log failures stop contributing honestly.
- Hand operations a working runbook on day -7, not day 0; let them break it during shadow week.
- Schedule a 30-day and 90-day post-closure review to catch latent defects and benefits drift.
- Celebrate visibly — sponsor email, team lunch, named recognition; budget it before kickoff.

## AI-agent gotchas
- LLMs draft glowing closure reports by default; explicitly require "challenges" and "what failed" sections with cited examples.
- Agent-extracted metrics from inconsistent status reports drift; require source row references for every number.
- Don't let the agent draft acceptance signoffs as if signed; the form must be human-signed (digital signature ok).
- Lessons-learned summaries by LLMs sound generic; have the agent group quotes verbatim before paraphrasing.
- Token budget: closure reports across a multi-month project exceed context — chunk by phase, then synthesize.
- Human-in-loop checkpoints: (1) acceptance signoffs, (2) ops-team review of handover, (3) sponsor signoff on final report, (4) archival manifest verification.

## References
- PMI, *PMBOK Guide* 7th ed., Delivery Performance Domain — Project Closure.
- ISO 21500:2021 — Guidance on project management.
- PRINCE2 — Closing a Project process.
- A. Klein, *The Project Manager's Survival Guide* — closure chapter.
