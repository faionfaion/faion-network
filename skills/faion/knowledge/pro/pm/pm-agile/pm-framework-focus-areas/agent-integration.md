# Agent Integration — PMBOK 8 Focus Areas

## When to use
- Replacing PMBOK 6 process groups in PMO documentation; the 5 focus areas (Initiating, Planning, Executing, Monitoring & Controlling, Closing) are method-agnostic.
- Mapping agile ceremonies onto a "process group equivalent" for stakeholders who learned PMBOK 6.
- Building a project audit rubric — each focus area becomes one section.
- Onboarding new PMs from PMP-aligned curricula since 2023.
- Tailoring conversations: "what's required at each focus area for this project size?"

## When NOT to use
- Pure agile teams that already operate with Scrum/Kanban events — overlaying focus areas adds bureaucracy.
- Highly regulated environments still mandating PMBOK 6 process groups verbatim — wait for org-level shift.
- Day-to-day execution detail — focus areas are framework-level, not task-level.
- Single-person solo work — overhead exceeds value.

## When NOT to use (cont'd)
- Replacement for actual deliverables; focus areas are organizing concepts, not artifacts you ship.

## Where it fails / limitations
- Section headings only — no prescriptive content; agents must pull substance from elsewhere (domain knowledge, PMBOK methodology cards).
- Boundaries between Planning ↔ Executing and Executing ↔ Monitoring & Controlling are fuzzy in agile/iterative work; teams either over-document or skip.
- "Closing" gets shortchanged in continuous-flow / product-mode work where there is no end; without explicit prompts, lessons-learned vanish.
- Without the 7 Performance Domains as the cross-axis, focus areas become a glorified TOC.
- 40 "non-prescriptive processes" sounds flexible but produces inconsistency across teams unless an org standardizes its own opinionated subset.

## Agentic workflow
A scaffolding agent generates a tailored project document tree (folders or wiki sections) from project metadata: type, size, regulatory regime → which focus areas need full treatment, which can be light. A coverage agent runs across an existing project corpus and reports which focus areas have artifacts and which are silently empty. A close-out agent fires when a project is marked done and forces a Closing-focus-area artifact (lessons learned, retrospective summary, formal acceptance) to be produced before archive.

### Recommended subagents
- `focus-area-scaffolder` — outputs a per-focus-area folder/section template based on project metadata.
- `focus-area-coverage-checker` — scans a corpus, reports completeness per focus area, flags gaps.
- `closing-enforcer` — blocks project archive until Closing artifacts exist; publishes lessons-learned to a shared repo.
- `phase-tagger` — auto-labels new docs / commits / tickets with their focus area for later analytics.

### Prompt pattern
```
You are focus-area-scaffolder. Inputs: project type (string), size (S/M/L), regulated (bool).
Output a Markdown directory tree under docs/ with one folder per focus area
(initiating, planning, executing, monitoring-controlling, closing). For each folder,
list 3-5 required documents tailored to the inputs. Mark optional with "(optional)".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mkdocs` | Render the focus-area folder tree as a project site | https://www.mkdocs.org |
| `tree` | Show generated scaffold for review | `apt install tree` |
| `pandoc` | Convert focus-area docs to PDF for governance audits | https://pandoc.org |
| `ripgrep` | Fast search for focus-area tags in commits / docs | https://github.com/BurntSushi/ripgrep |
| `yq` | Maintain a `focus-areas.yaml` manifest per project | https://github.com/mikefarah/yq |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Confluence | SaaS | Yes — REST | One space per project, one parent page per focus area. |
| Notion | SaaS | Yes — REST | Database-of-databases per focus area. |
| SharePoint + OneNote | SaaS | Yes — Graph API | Common in PMOs already on Microsoft. |
| Wiki.js / BookStack | OSS | Yes — REST | Self-hosted alternatives for compliance/sovereignty. |
| Project Online (MS) | SaaS | Yes — REST | Heavy PPM with focus-area / phase awareness. |

## Templates & scripts
The README is brief; useful inline scaffolder (`scripts/scaffold_focus_areas.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-docs}"; mkdir -p "$ROOT"
for fa in initiating planning executing monitoring-controlling closing; do
  d="$ROOT/$fa"; mkdir -p "$d"
  case "$fa" in
    initiating)            files=(charter.md vision.md stakeholder-register.md) ;;
    planning)              files=(spec.md design.md risk-register.md plan.md) ;;
    executing)             files=(decisions.md status-reports/.gitkeep) ;;
    monitoring-controlling)files=(metrics.md change-log.md burn-up.md) ;;
    closing)               files=(lessons-learned.md acceptance.md final-report.md) ;;
  esac
  for f in "${files[@]}"; do touch "$d/$f"; done
done
echo "scaffolded under $ROOT"
```

## Best practices
- Tag every commit and ticket with its focus area; later analytics show where the team actually spends effort vs. where they should.
- Pair focus areas with the 7 Performance Domains on the orthogonal axis — focus areas tell you "when", domains tell you "what".
- Keep focus-area boundaries intentionally fuzzy at the team level; codify them only at portfolio/audit level.
- Audit Closing every quarter for active long-running products; without forcing it, lessons-learned never happen.
- For agile teams, map: Sprint Planning → Planning, Sprint → Executing, Daily/Demo → Monitoring & Controlling, Retro → Closing-of-iteration.
- Don't double-document: if a sprint review covers Monitoring & Controlling, a separate "M&C report" is waste.

## AI-agent gotchas
- The README is sparse; agents will pad with PMBOK 6 process-group content and confuse focus areas with process groups. Pin terminology in the system prompt: "5 focus areas, NOT 5 process groups."
- "Non-prescriptive processes" prompt agents to invent 40 process names; constrain output to org-defined subset.
- Closing is the most forgotten focus area in agent outputs; force a check that Closing has at least one artifact before approval.
- Boundary-fuzziness causes agents to put the same artifact in multiple focus areas; require single-home tagging.
- Agents producing a scaffold tend to over-create files; cap at 3-5 docs per focus area as default.
- "Initiating" is over-equated to "kickoff meeting" — remind agents it includes business case, charter, sponsor sign-off.

## References
- PMBOK Guide, 8th edition (2025)
- PMI Standard for Project Management, 2nd edition
- https://www.pmi.org/pmbok-guide-standards
- PMP Examination Content Outline (current version)
- See sibling `seven-performance-domains` for the orthogonal axis
