# Agent Integration — Work Breakdown Structure (WBS)

## When to use
- Translating an approved scope statement / SOW into an estimable, assignable work-package tree before scheduling and costing.
- Bidding on fixed-scope work where every deliverable must be priced — bottom-up estimation needs leaves.
- Validating the 100% rule on a hand-drafted plan: have the agent diff the WBS against the scope statement and flag missing or over-counted deliverables.
- Generating a WBS dictionary (one card per leaf) at the same time as the tree, so context is captured once.
- Re-baselining after a change request: rerun the agent on the updated scope diff, only mutate the affected branch.

## When NOT to use
- Pure-Scrum or Kanban teams where the product backlog *is* the decomposition; an additional WBS layer creates two sources of truth.
- Discovery / research projects (< 30% of scope known) — the WBS will be hallucinated below level 2.
- Solo work on a feature ≤ 2 weeks: a checklist beats a WBS.
- Projects whose deliverables are emergent (innovation, R&D, platform exploration); rolling-wave planning fits better.

## Where it fails / limitations
- LLMs default to verb-based decomposition ("design", "build", "test") when the rule is noun-based deliverables; outputs need correction.
- The 8-80 hour rule is regularly violated by agents (1-hour or 200-hour leaves) — needs an explicit constraint and a post-check.
- Without a scope baseline the model fabricates branches that look plausible but are not in scope (silent scope creep).
- Numbering schemes drift across regenerations (1.2.3 vs 1.2.4) and break traceability if not pinned.
- Agents conflate WBS with schedule; they add dates / dependencies that belong elsewhere.
- A WBS for a hybrid project needs explicit predictive vs agile branches (e.g. "2.0 Sprint Increments" as a rolling node) — agents default to fully decomposed leaves and wreck the agile half.
- "Project Management" branch (1.0) is often forgotten by agents → no PM effort budgeted.

## Agentic workflow
Two-phase: (1) decomposition agent reads the scope statement + glossary and emits a tree YAML with leaves at work-package granularity (8-80h rule); (2) WBS-dictionary agent expands each leaf into a card (description, AC, owner, estimate, deps, deliverable). Human review between phases is mandatory — never let phase 2 run on an unvalidated tree. Re-runs only mutate the diff branch.

### Recommended subagents
- `wbs-decomposer` (define inline) — input: scope.md + glossary.yaml; output: wbs.yaml tree validated against 100% rule.
- `wbs-dictionary-writer` (define inline) — input: wbs.yaml leaf; output: wbs-dict-<id>.md card.
- `faion-sdd-executor` — once a leaf becomes a TASK, drives implementation through quality gates.
- `faion-brainstorm` — for the first level-1 decomposition when phase boundaries are not obvious.

### Prompt pattern
```
Decompose <project> into a noun-based deliverable tree.
Rules:
- Leaves obey the 8-80 hour rule.
- Each level represents 100% of its parent (no gaps, no overlap).
- Include "1.0 Project Management" as the first branch.
- Use stable IDs (1, 1.1, 1.1.1 …); re-runs MUST keep existing IDs and only append.
- Do NOT include dates, durations, or assignees — those are schedule/resource artefacts.
- If a deliverable is not in <scope.md>, do not invent it; emit "OUT_OF_SCOPE" instead.

Output: YAML
items:
  - id: "1"
    name: "Project Management"
    children: [...]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` (`mmdc`) | Render WBS as a tree diagram (mindmap or flowchart) | https://github.com/mermaid-js/mermaid-cli |
| `graphviz` (`dot`) | Render WBS as a hierarchical diagram | https://graphviz.org/ |
| `yq` | Validate / mutate WBS YAML in CI | https://github.com/mikefarah/yq |
| `xmlstarlet` | Edit WBS in PMI-standard `WBS-XML` format | http://xmlstar.sourceforge.net/ |
| `pandoc` | WBS markdown → DOCX / PDF for sponsor packs | https://pandoc.org/ |
| `gh` / `jira-cli` | Sync WBS leaves into issues / epics | https://cli.github.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MS Project / Project for the Web | SaaS | Yes — Graph API + MPP/XML import | Native WBS support, dictionary as task notes |
| Smartsheet | SaaS | Yes — REST | WBS as hierarchical sheet |
| Asana / ClickUp / Monday | SaaS | Yes — REST | Tasks + subtasks ≈ WBS branches |
| MindMeister / Whimsical | SaaS | Partial — REST + export | WBS as mindmap, export OPML |
| WBS Schedule Pro | Desktop | No — file format | Industry-standard WBS app, MPP I/O |
| Lucidspark / Miro | SaaS | Yes — REST | Collaborative WBS workshops |
| Jira (Advanced Roadmaps / Plans) | SaaS | Yes — REST + JQL | Initiative → epic → story ≈ WBS levels 1-3 |
| Notion / Confluence | SaaS | Yes — REST | WBS dictionary cards live here |

## Templates & scripts
See `templates.md` for the markdown WBS + dictionary skeleton. Inline 100%-rule validator (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Validate a WBS YAML for 100% rule + 8-80h leaf rule."""
import sys, yaml
ERR = []
def walk(node, parent_id=""):
    items = node.get("children", [])
    if items:
        weights = [c.get("weight_pct", 0) for c in items]
        if abs(sum(weights) - 100) > 0.5:
            ERR.append(f"{node['id']}: children sum to {sum(weights)}%, expect 100")
        for c in items:
            walk(c, node["id"])
    else:
        h = node.get("effort_hours")
        if h is None or not (8 <= h <= 80):
            ERR.append(f"{node['id']}: leaf effort {h}h violates 8-80 rule")
def main(path):
    doc = yaml.safe_load(open(path))
    for top in doc["items"]:
        walk(top)
    if ERR:
        print("\n".join(ERR)); sys.exit(1)
    print("WBS valid"); sys.exit(0)
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Lock the scope baseline before decomposing; a moving scope makes WBS regeneration meaningless.
- Always include the "Project Management" branch (charter, status, risk, change control) — usually 8-15% of total effort.
- Numbering: 1, 1.1, 1.1.1; never go past four levels for human readability — go deeper only in the dictionary.
- Pair WBS with the responsibility matrix (RACI) so each leaf has exactly one A.
- Tag leaves with development-approach (predictive vs agile) — drives downstream estimation method.
- Keep WBS dictionary cards in version control alongside the tree; treat as code, review via PR.
- Do not put dates in the WBS — schedule lives in the schedule artefact; mixing them creates churn.
- Re-baseline triggers: scope change, sponsor change, > 10% effort variance per branch.

## AI-agent gotchas
- LLMs love verbs ("Design dashboard"); enforce noun phrasing in the prompt and post-validate via regex (`^[A-Z][a-z]+ [A-Z]?` is a smell).
- Agents skip the 100% rule because it sounds tautological; require explicit `weight_pct` per child and validate sum.
- ID stability across regenerations is broken by default; pass the previous WBS in context and instruct "keep IDs, append only".
- Agents inflate level depth on confident topics and under-decompose on unfamiliar ones; cap depth at 4 and require justification for any sibling > 5.
- Cross-cutting work (security, documentation) gets duplicated across branches; name a single owning branch and reference from others.
- Agents emit fake estimates ("4 hours") to satisfy the 8-80 rule; force them to mark `effort_hours: TBD` when unknown.
- For very large projects (> 200 leaves), an LLM context window cannot hold the full tree; decompose level-by-level with separate calls and stitch.

## References
- PMI — Practice Standard for Work Breakdown Structures (3rd ed.): https://www.pmi.org/standards/work-breakdown-structures
- PMI — A Guide to the PMBOK 7th Edition, Planning Performance Domain: https://www.pmi.org/standards/pmbok
- DoD MIL-STD-881F — WBS for defense materiel items (industry reference): https://www.acq.osd.mil/asda/dpc/cp/policy/mil-std-881.html
- "Effective Work Breakdown Structures", Gregory T. Haugan
- WBS Schedule Pro tutorials: https://www.criticaltools.com/wbs-schedule-pro-tutorials.html
- PMI Knowledge Shelf — "How to Build a WBS"
