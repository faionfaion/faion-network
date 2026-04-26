# Agent Integration — PMBoK 8 Five Focus Areas

## When to use
- Structuring a project plan in PMBoK 8 vocabulary when sponsors expect process-group-style reporting (Initiating, Planning, Executing, Monitoring & Controlling, Closing) — focus areas reintroduce that flow without the rigidity of the legacy 49 processes.
- Mapping the 40 non-prescriptive processes onto a project: pick the subset that fits and drop the rest.
- Tailoring per delivery approach: same five focus areas, predictive vs agile artefacts (charter vs vision; WBS vs backlog; work packages vs sprints; EVM vs velocity; final report vs retro).
- Cross-walking a PMBoK 6 plan into PMBoK 8 vocabulary without losing artefacts.
- Building a per-focus-area gate checklist for stage reviews.

## When NOT to use
- Pure-Scrum teams whose entire universe is the Scrum Guide; focus areas add a meta-layer with no benefit.
- Single-team continuous delivery where Initiating and Closing collapse into a release note.
- Agile-coaching contexts where "process" is a four-letter word — the framing alienates the team.
- PMBoK 7 purist environments where focus areas have not yet been adopted; using them creates vocabulary drift.

## Where it fails / limitations
- Focus areas overlap with performance domains; the 5 × 7 grid is conceptually neat but operationally confusing — agents need explicit guidance on which axis owns what.
- Re-introducing process groups as "focus areas" was driven by ~80% practitioner support, but it can re-anchor teams in waterfall thinking.
- The 40 non-prescriptive processes are a menu, not a checklist; agents tend to apply them all, leading to overhead.
- Agile teams have to construct artefact mappings themselves (sprint review ≈ Monitoring + Closing), and there is no canonical mapping in PMI material.
- The Initiating focus area is often skipped on internal projects ("we already started"), leaving no charter / decision record.

## Agentic workflow
The agent uses focus areas as a *temporal* index (where in the lifecycle) and the seven domains as a *topical* index (what kind of work). A project plan is a 5 × 7 matrix; the agent fills only the cells that apply to this project and approach. Re-runs respect tailoring: if "Procurement under Stakeholders during Planning" was empty last time, do not invent it now.

### Recommended subagents
- `lifecycle-mapper` (define inline) — input: project context + chosen approach; output: filled 5 × 7 matrix of artefacts.
- `process-selector` (define inline) — input: filled matrix; output: subset of the 40 non-prescriptive processes that apply.
- `gate-checklist-builder` (define inline) — input: focus area + approach; output: stage-gate criteria.
- `faion-feature-executor` — for executing the cells that contain code work.
- `faion-brainstorm` — to populate empty cells when the project type is novel.

### Prompt pattern
```
Project: <name>; approach: <predictive|agile|hybrid>; pmbok_edition: 8.

For each (focus_area, performance_domain) cell, emit:
{ "focus": "Initiating|Planning|Executing|MnC|Closing",
  "domain": "Governance|Scope|Schedule|Finance|Stakeholders|Resources|Risk",
  "artefact": "name or null",
  "owner": "name or UNASSIGNED",
  "process_used": "PMBoK process name or null",
  "approach_specific_note": "..." }

Constraints:
- Only fill cells that this project needs; explicit nulls are OK.
- For agile, map sprint events to MnC + Closing as appropriate.
- Quote a process from the 40 non-prescriptive set or "tailored".
- Reject any cell where focus is "Closing" but approach is "agile"
  unless it ties to project-end retro.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Render the focus-area lifecycle diagram | https://github.com/mermaid-js/mermaid-cli |
| `yq` | Validate / mutate the lifecycle matrix YAML | https://github.com/mikefarah/yq |
| `pandoc` | Render the matrix as DOCX / PDF stage gate pack | https://pandoc.org/ |
| `gh project` | Map focus areas onto GitHub Project columns | https://cli.github.com/manual/gh_project |
| `jira-cli` | Mirror focus areas onto Jira workflow statuses | https://github.com/ankitpokhrel/jira-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MS Project / Project for the Web | SaaS | Yes — Graph API | Lifecycle phases ≈ focus areas |
| Smartsheet | SaaS | Yes — REST | Stage-gate templates for capital projects |
| Monday.com | SaaS | Yes — GraphQL | Phase-based boards |
| Asana Portfolios | SaaS | Yes — REST | Initiating + Closing = milestone columns |
| Confluence / Notion | SaaS | Yes — REST | Where the per-focus-area pack lives |
| Jira | SaaS | Yes — REST | Workflow statuses mapped to focus areas |
| Power BI | SaaS | Yes — SQL | Stage-gate KPI dashboards |

## Templates & scripts
See `templates.md` for the lifecycle pack. Inline matrix-to-checklist generator (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Convert a 5x7 lifecycle matrix YAML into a stage-gate checklist."""
import sys, yaml
FOCUS = ["Initiating", "Planning", "Executing", "MnC", "Closing"]
DOMAINS = ["Governance", "Scope", "Schedule", "Finance",
           "Stakeholders", "Resources", "Risk"]
def main(path):
    matrix = yaml.safe_load(open(path))["cells"]
    by_focus = {f: [] for f in FOCUS}
    for c in matrix:
        if c.get("artefact"):
            by_focus[c["focus"]].append(c)
    for f in FOCUS:
        print(f"\n## {f} — Stage Gate Checklist\n")
        for c in sorted(by_focus[f], key=lambda x: DOMAINS.index(x["domain"])):
            owner = c.get("owner") or "UNASSIGNED"
            proc  = c.get("process_used") or "tailored"
            print(f"- [ ] **{c['domain']}** — {c['artefact']}  "
                  f"(owner: {owner}; process: {proc})")
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Treat focus areas as time and domains as topic; do not collapse to a flat list.
- For agile projects, document the mapping (sprint planning = Planning + Executing slice; sprint review = MnC) in the charter so reviewers do not get lost.
- Do not adopt all 40 non-prescriptive processes — pick the ones with measurable inputs/outputs.
- Reuse focus-area gate checklists as steering-committee agenda templates.
- Closing is *not* optional; even an agile project needs a final retro / lessons-learned across all sprints.
- Solopreneur: keep Initiating + Closing tiny but real (a vision doc + a retro), drop Planning/Executing/MnC into a single weekly cadence.

## AI-agent gotchas
- LLMs use PMBoK 6 process group names ("Initiating Process Group") interchangeably with focus areas; pin "focus area" as the canonical term.
- The 40 non-prescriptive processes get listed in full when only 8-12 apply; cap with explicit constraint.
- Agents skip "Closing" on agile projects; require explicit non-null cell.
- "Monitoring and Controlling" gets abbreviated inconsistently (M&C, MnC, MC); pin one form.
- Agents conflate focus areas with phases — they are *aspects of work*, not sequential phases (work happens in many focus areas concurrently).
- Procurement, demoted to appendix, gets dropped from Executing; force inclusion when contractor count > 0.
- Sustainability is not a focus area; do not let agents promote it to one.

## References
- PMI — A Guide to the PMBOK 8th Edition (in development): https://www.pmi.org/standards/pmbok
- PMI — Process Groups: A Practice Guide: https://www.pmi.org/learning/library/process-groups-a-practice-guide
- PMI — A Guide to the PMBOK 7th Edition: https://www.pmi.org/standards/pmbok
- PMBOK 6 → 8 transition articles (PMI community / Mike Griffiths "Leading Answers")
- ISO 21500 — Guidance on Project Management: https://www.iso.org/standard/50003.html
- Praxis Framework process model (alternative): https://www.praxisframework.org/en/library/process-model
