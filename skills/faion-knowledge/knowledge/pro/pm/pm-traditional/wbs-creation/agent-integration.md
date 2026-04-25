# Agent Integration — WBS Creation

## When to use
- New project where scope is fixed enough to decompose into deliverables (>4 weeks of work).
- Fixed-bid proposal estimation where each work package needs an hours/cost line.
- Programs requiring a contractual scope baseline with WBS IDs (1.2.3) for traceability.
- Migration / cutover projects where missing a deliverable is expensive.

## When NOT to use
- Pure-Scrum backlog work where the product backlog plays the same role.
- Exploratory R&D — you do not know the deliverables yet.
- Single-week tasks; a checklist is faster.
- Operations / continuous-flow work (use service catalog instead).

## Where it fails / limitations
- Activity-oriented WBSs (verbs everywhere) silently drift toward Gantt charts and lose deliverable focus.
- Inconsistent depth across branches — one branch detailed to level 5, another stays at level 2.
- 100% rule violations are invisible without explicit verification.
- WBS Dictionary is the part everyone skips, then estimates become hand-waving.
- For multi-team programs, naming collisions (two "API" branches) break traceability.

## Agentic workflow
A subagent is highly effective for the mechanical decomposition: take a charter / scope statement and produce a candidate WBS, validate the 100% rule, generate WBS Dictionary stubs, and lint for verb-vs-noun violations. Humans validate completeness and own the final dictionary. Pair the agent with the project sponsor for one calibration round before going wide.

### Recommended subagents
- `faion-pm-agent` — owns WBS authoring; drafts hierarchy from scope statement.
- `faion-sdd-planning` agent (knowledge/solo/sdd) — connects WBS work packages to SDD task breakdown.
- `faion-business-analyst` agent — useful for requirements-to-WBS traceability matrix.

### Prompt pattern
```
Decompose this scope statement into a WBS following the 100% rule.
Output YAML:
- id: "1"
  name: "<deliverable>"
  type: deliverable|workpackage
  children: [...]
Constraints:
- Names are nouns (deliverables), not verbs.
- Leaf work packages: 8-80 hours estimable.
- Include a "Project Management" branch (1.X) for planning/control/closure.
- Flag any branch where you cannot confirm 100% coverage as needs_review.
```

```
Lint this WBS:
- Verb-led names: list violations.
- Branches with depth < 3: list as "underspecified".
- Branches with depth > 5: list as "over-decomposed".
- Missing PM branch: error.
- Suspected duplicates by stem similarity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `wbstool` (Open Source by Critical Tools) | Visual WBS authoring | https://www.criticaltools.com |
| `mermaid-cli` (`mmdc`) | Render Mermaid `mindmap`/`graph` to SVG/PNG | https://github.com/mermaid-js/mermaid-cli |
| `markmap-cli` | Markdown outline → interactive mindmap | https://markmap.js.org |
| `tree` | Verify nested folder representation of WBS | system package |
| `pandoc` | Outline → DOCX/PDF for stakeholder approval | https://pandoc.org |
| `gh` / `jira-cli` | Push leaf work packages as issues with WBS-ID label | vendor docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MS Project / Project for the Web | SaaS | Yes — Graph API | Native WBS column, schedule integration. |
| Smartsheet | SaaS | Yes — REST API | Hierarchy + parent-rollup formulas. |
| Lucidchart / Miro WBS templates | SaaS | Limited — REST API | Visualization only; no estimation rollup. |
| WBS Schedule Pro | Desktop | No | Strong graphical decomposition. |
| OpenProject | OSS / SaaS | Yes — REST API | Free WBS + Gantt, agent-friendly. |
| ProjectLibre | OSS | No | Desktop-only MS Project clone. |
| Notion / Coda hierarchical DB | SaaS | Yes — REST API | Best for solo/SDD repos. |

## Templates & scripts
See `templates.md` for outline and dictionary entry. Lint helper:

```python
# wbs_lint.py — usage: python wbs_lint.py wbs.yaml
import sys, yaml
VERBS = {"design","build","implement","test","deploy","write","create","develop"}
errs = []
def walk(n, depth, path):
    name = n.get("name","").strip().lower()
    first = name.split()[0] if name else ""
    if first in VERBS:
        errs.append(f"verb-led: {path} '{n['name']}'")
    if depth >= 5 and n.get("children"):
        errs.append(f"over-deep: {path}")
    for i,c in enumerate(n.get("children") or []):
        walk(c, depth+1, f"{path}.{i+1}")
tree = yaml.safe_load(open(sys.argv[1]))
for i,root in enumerate(tree if isinstance(tree,list) else [tree]):
    walk(root, 0, str(i+1))
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
```

## Best practices
- Use nouns at every level; activities belong in the schedule, not the WBS.
- Always include a "1.0 Project Management" branch — captures planning, status, closure work.
- Number every node (1.2.3 style) and never reuse numbers when refactoring; mark removed nodes as deprecated.
- Lock the WBS at the work-package level for the baseline; deeper detail can evolve via the schedule.
- Cross-reference each work package to (a) requirements, (b) acceptance criteria, (c) responsible owner.
- For SDD repos, mirror leaf work packages as files in `.aidocs/` so the structure is grep-able.

## AI-agent gotchas
- LLMs love to write activity-oriented WBSs; system prompt must enforce noun-led naming.
- Agents over-decompose ("Login button color" as a leaf) — cap depth at 5 in the prompt.
- 100% rule is hard to verify automatically; require the agent to emit a coverage rationale per parent.
- Never let the agent renumber the WBS after baseline — IDs are referenced by contracts, schedules, and registers.
- WBS dictionaries written by LLMs read generic; seed each entry with the parent's acceptance criteria text, not just the name.
- Human-in-loop checkpoints: (1) initial draft review, (2) 100%-rule validation, (3) baseline lock with sponsor sign-off.

## References
- PMI, *PMBOK Guide* 7th ed., Planning Performance Domain.
- PMI, *Practice Standard for Work Breakdown Structures*, 3rd ed.
- G. Haugan, *Effective Work Breakdown Structures* (2002).
- DoD MIL-STD-881F — WBS for defense programs.
