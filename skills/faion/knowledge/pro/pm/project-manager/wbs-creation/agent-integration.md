# Agent Integration — Work Breakdown Structure (WBS)

## When to use
- Predictive/waterfall projects with fixed scope at kickoff: client agency contracts, ERP rollouts, hardware launches.
- Hybrid delivery: WBS at the program level, sprints/iterations underneath each work package.
- Cost-loaded schedules and EVM tracking: WBS is the spine for cost accounts.
- Migration projects (data, system, vendor) where every artefact must be enumerated.
- Compliance projects (SOC2, HIPAA, ISO 27001) where 100% rule maps to control coverage.

## When NOT to use
- Pure agile teams driven by a product backlog and continuously refined epics — WBS calcifies what should flex.
- Discovery / R&D where deliverables are emergent — use a hypothesis backlog, not a WBS.
- Fast-moving startup product work — WBS overhead exceeds value when scope changes weekly.

## Where it fails / limitations
- Activity-WBS confusion: teams list verbs (design, code, test) instead of nouns (auth module, dashboard); breaks the deliverable focus.
- 100% rule is asserted, rarely verified — overhead packages (PM, QA, deployment, training) get forgotten.
- 8/80 rule produces work packages too coarse for a 2-day sprint or too fine for a quarter — calibrate to your tracking unit.
- Decomposition depth becomes vanity: 5+ levels rarely improve estimate quality and waste hours.
- WBS without a Dictionary is just an outline; the value is the per-package definition (criteria, owner, predecessors).

## Agentic workflow
A subagent expands a charter or one-line goal into a hierarchical WBS, applies the 100% rule check, generates a WBS Dictionary entry per leaf, and emits both an outline and a structured YAML representation. Use a 2-pass model: pass 1 ideates major deliverables; pass 2 decomposes each. Keep depth and 8/80-rule enforcement in scripts so the LLM can't argue around them. Human-in-loop required after each level to confirm completeness — agents systematically miss PM/QA/deployment/training packages and "non-product" deliverables (training, comms, docs, runbooks).

### Recommended subagents
- `faion-pm-agent` — primary WBS draft and Dictionary entries.
- `faion-business-analyst` — cross-checks WBS against requirements (every requirement → at least one work package).
- `faion-software-architect` — validates that technical decomposition matches the architecture.
- `faion-sdd-executor-agent` — converts work packages → SDD `TASK_*.md` files.

### Prompt pattern
```
Input: charter.md (goals, scope, constraints), architecture.md (optional)
Output: wbs.yaml — hierarchy of {id, name, level, kind: deliverable|work_package,
parent}. Constraints: max_depth=4; leaf size 8-80h estimate; include
required overhead packages: project_management, qa, deployment,
documentation, training, transition.
After tree: produce dictionary entries for every leaf.
```

```
Validate wbs.yaml:
1. Every parent has children that cover its scope (state any gap).
2. Every requirement_id in requirements.yaml maps to at least one wbs id.
3. Leaf estimate within 8-80h; flag outliers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Render WBS tree → SVG/PNG | https://github.com/mermaid-js/mermaid-cli |
| `markmap-cli` | Markdown outline → mind map | https://markmap.js.org |
| `yq` | Query/transform wbs.yaml | https://github.com/mikefarah/yq |
| `pandoc` | Outline → DOCX/PDF deliverable | https://pandoc.org |
| `tree-cli` | Quick tree views from indented text | npm i -g tree-cli |
| `csvkit` | Pivot WBS CSV by owner/level | https://csvkit.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Project | Desktop/SaaS | Partial — XML import/export | Native WBS; agent can write `.mpp` via `python-mpxj` |
| Smartsheet | SaaS | Yes — REST API + hierarchy via parent_id | Ideal for WBS + EVM |
| MindMeister | SaaS | Yes — REST API | Mind-map style WBS for stakeholder review |
| Lucidchart | SaaS | Yes — REST API | Tree visualisation |
| Atlassian Confluence | SaaS | Yes — REST API | Host outline + Dictionary |
| Notion / Airtable | SaaS | Yes — REST API | Lightweight WBS DB |
| Jira (Advanced Roadmaps) | SaaS | Yes — REST API | Initiative→Epic→Story→Task mirrors WBS |
| MindManager / XMind | Desktop | Limited (file-format only) | Good for whiteboard-to-WBS |
| WBS Schedule Pro | Desktop | No API | Specialist; not for agents |

## Templates & scripts
See `templates.md` for outline and Dictionary entry. Inline 100% rule + 8/80 validator (≤50 lines):

```python
# wbs_validate.py — run after the agent emits wbs.yaml
import yaml, sys, collections

def main(path):
    nodes = yaml.safe_load(open(path))
    by_id = {n["id"]: n for n in nodes}
    children = collections.defaultdict(list)
    for n in nodes:
        if n.get("parent"):
            children[n["parent"]].append(n["id"])

    errors = []
    for n in nodes:
        kids = children.get(n["id"], [])
        is_leaf = not kids
        if is_leaf:
            est = n.get("estimate_hours")
            if est is None:
                errors.append((n["id"], "leaf has no estimate"))
            elif not (8 <= est <= 80):
                errors.append((n["id"], f"leaf estimate {est}h outside 8-80"))
            if "deliverable" not in n or not n["deliverable"]:
                errors.append((n["id"], "leaf missing deliverable"))
        else:
            if n.get("kind") == "work_package":
                errors.append((n["id"], "non-leaf marked work_package"))

    required = {"project_management", "qa", "deployment",
                "documentation", "training", "transition"}
    names = {n["name"].lower() for n in nodes}
    for r in required:
        if not any(r in nm for nm in names):
            errors.append(("WBS", f"missing required package: {r}"))

    for nid, msg in errors:
        print(f"[FAIL] {nid}: {msg}")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Deliverable-oriented (nouns), not activity-oriented (verbs). "User Authentication", not "Build user authentication".
- Always include the boring packages: PM, QA, Deployment, Documentation, Training, Transition. They are 15-25% of effort.
- Each leaf produces one verifiable artefact with explicit acceptance criteria — write it before estimating.
- Stop decomposing when 8/80 rule is satisfied; deeper is not better.
- Pair WBS with WBS Dictionary in the same source file (id keyed); never separate.
- Renumber rules: append-only IDs in long-running projects so links from CRs/risks/tasks remain stable.
- Convert leaves into SDD `TASK_*.md` 1:1 — the WBS is the source of truth, tasks are derived.

## AI-agent gotchas
- LLMs default to activity verbs; explicitly instruct "use noun phrases for deliverables".
- Agents skip overhead packages (PM, QA, deploy, train) — hard-code them in the prompt as required.
- Decomposition often has uneven depth: backend gets 4 levels, "Marketing" stays at level 2. Force the agent to balance.
- Dictionary entries get hallucinated owners and dates; force them to come from a stakeholder register and schedule input.
- Agents inflate estimates symmetrically (everything is 40h); inject a few known-good estimates as anchors.
- Do not let agents "consolidate" leaves to fit a target count — that breaks 8/80; reject and re-prompt.
- When converting WBS → tasks, beware ID drift: keep `wbs_id` field in every generated task for round-tripping.

## References
- PMBOK Guide 7th Edition — Planning Performance Domain.
- PMI Practice Standard for Work Breakdown Structures (3rd ed.).
- DoD Handbook MIL-STD-881 (WBS for defence systems).
- "Effective Work Breakdown Structures" — Gregory Haugan.
- ISO 21502 — Project work and decomposition guidance.
