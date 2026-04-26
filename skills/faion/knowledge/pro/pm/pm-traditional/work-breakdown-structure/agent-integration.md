# Agent Integration — Work Breakdown Structure

## When to use
- Establishing a contractual scope baseline for fixed-bid or government-style work.
- Cost estimation for proposals where each work package needs an hours/$ line.
- Programs spanning multiple teams/vendors that need a single ID schema (1.2.3) for integration.
- Compliance / audit contexts where every deliverable must be traceable to a parent objective.

## When NOT to use
- Backlog-driven product teams; the product backlog plus epics already plays the WBS role.
- Discovery / R&D where deliverables are emergent.
- Sub-2-week tasks; a checklist or kanban swimlane suffices.
- Steady-state operations work — use service catalog, not WBS.

## Where it fails / limitations
- Drifts into a Gantt activity list when teams treat verbs as deliverables.
- 100% rule violations stay invisible without explicit coverage rationale per parent.
- Inconsistent depth between branches makes rollups misleading.
- WBS dictionary is the high-value, low-completion artefact; without it estimates are guesses.
- Locked baselines vs reality: WBS can become fiction when scope shifts but baseline is not refreshed.

## Agentic workflow
This methodology overlaps `wbs-creation`; the difference is emphasis on the WBS as a reusable scope-baseline artefact integrated with cost, schedule, and EVM. A subagent is effective at: drafting the hierarchy from charter+requirements, mirroring leaf packages into Jira/issue-tracker as `wbs-id` labelled items, validating coverage against the requirements traceability matrix, and detecting drift when PR diffs touch areas outside the baseline. Humans approve the baseline lock and any post-baseline changes (which become CRs).

### Recommended subagents
- `faion-pm-agent` — drafts WBS, owns dictionary, manages baseline.
- `faion-business-analyst` (ba-core / ba-modeling) — runs requirements-to-WBS traceability.
- `faion-sdd-execution` — gates that PR diffs mention a WBS ID in the commit/PR description.

### Prompt pattern
```
Decompose <scope statement>. Output WBS as YAML with id, name (noun),
deliverable, acceptance_criteria, owner, est_hours, predecessors[].
Enforce: leaf packages 8-80h; depth <= 5; include 1.0 Project Management.
For every parent emit a one-line "100% coverage rationale".
```

```
Cross-check this WBS against the requirements list. Output:
{wbs_id: [requirement_ids]} mapping. List orphans:
requirements_without_wbs[], wbs_without_requirements[].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Render WBS as `graph TD` or `mindmap` | https://mermaid.js.org |
| `markmap-cli` | Convert outline to interactive mindmap | https://markmap.js.org |
| `pandoc` | Outline → DOCX/PDF for sponsor review | https://pandoc.org |
| `jira-cli` | Bulk-create issues from WBS leaves with ID labels | https://github.com/ankitpokhrel/jira-cli |
| `gh` | GitHub equivalent: leaves as issues, parent label as milestone | https://cli.github.com |
| `dot` (Graphviz) | Tree visualizations from `wbs.dot` | https://graphviz.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Project / Project for the Web | SaaS | Yes — Graph API | Native WBS column with rollup. |
| Smartsheet | SaaS | Yes — REST API | Hierarchy + rollup formulas. |
| OpenProject | OSS / SaaS | Yes — REST API | Free-tier WBS + Gantt. |
| Asana with hierarchy | SaaS | Yes — REST API | Project → section → task as 3-level WBS. |
| Notion / Coda hierarchical DB | SaaS | Yes — REST API | Best for SDD repos and solo PMs. |
| Jira Advanced Roadmaps | SaaS | Yes — REST API | Initiative → Epic → Story as proxy WBS. |
| WBS Schedule Pro | Desktop | No | Strong graphical decomposition. |

## Templates & scripts
See `templates.md` for outline + dictionary entries. Lint script that enforces noun-leadership and depth bounds:

```python
# wbs_check.py
import sys, yaml
data = yaml.safe_load(open(sys.argv[1]))
errs = []
def walk(n, depth, pid):
    nid = f"{pid}.{n.get('seq','?')}".strip(".")
    name = n.get("name","")
    if name and name.split()[0].lower() in {"build","design","test","deploy","write","do"}:
        errs.append(f"verb-led {nid}: {name}")
    if depth >= 5 and n.get("children"):
        errs.append(f"too deep {nid}")
    if not n.get("children"):
        h = n.get("est_hours") or 0
        if h and not (8 <= h <= 80):
            errs.append(f"out of 8/80 rule {nid}: {h}h")
    for c in (n.get("children") or []):
        walk(c, depth+1, nid)
for i, root in enumerate(data if isinstance(data,list) else [data]):
    root.setdefault("seq", i+1)
    walk(root, 0, "")
print("\n".join(errs) or "ok"); sys.exit(1 if errs else 0)
```

## Best practices
- Number nodes with stable IDs (1.2.3); never reuse a removed number — mark deprecated.
- Pair every leaf with acceptance criteria so downstream Definition-of-Done is unambiguous.
- Validate the 100% rule explicitly at every parent; do not assume.
- Lock the WBS at level 3-4 for the baseline; finer detail evolves through schedule and CRs.
- Mirror the WBS in your tracker (Jira/Linear/GitHub) so team work always rolls up to a baseline ID.
- Refresh the WBS dictionary at every major change; entries dated >90 days are suspect.

## AI-agent gotchas
- Models default to verb-led names (activity-oriented). Pin "noun-led names only" in the system prompt.
- Estimates produced cold are ±100% — feed analogous-project data into the prompt.
- LLMs over-decompose; cap depth and leaf hours explicitly in the schema.
- Do not let the agent renumber after baseline; downstream artefacts (contracts, schedules, EVM) reference the IDs.
- Agent-generated dictionaries read generic; require the agent to extract acceptance criteria from source requirements verbatim.
- Human-in-loop checkpoints: (1) draft review, (2) 100%-rule validation per parent, (3) baseline lock with sponsor signoff, (4) any post-baseline change → goes through Change Control.

## References
- PMI, *PMBOK Guide* 7th ed., Planning Performance Domain.
- PMI, *Practice Standard for Work Breakdown Structures*, 3rd ed.
- DoD MIL-STD-881F (defense WBS taxonomy).
- G. Haugan, *Effective Work Breakdown Structures* (2002).
