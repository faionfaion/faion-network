# Agent Integration — Architecture Decision Trees

## When to use
- Recurring architecture choices (style, stack, DB, cloud, build/buy) where consistency across projects matters more than bespoke analysis.
- Onboarding non-architect agents/contributors that need fast, defensible answers without deep ATAM cycles.
- Filtering options before a heavier trade-off analysis or ADR — turn 20 candidates into 3.
- Non-technical stakeholder communication — trees are far easier to discuss than utility matrices.

## When NOT to use
- Genuinely novel decisions where the tree's question set is the wrong frame.
- Decisions dominated by a single hard constraint (regulatory, contractual) — the tree obscures the gating factor.
- High-stakes irreversible decisions — use trees to shortlist, then full trade-off analysis to choose.

## Where it fails / limitations
- Trees encode the author's biases: a 2024 tree will route everyone to microservices at 50+ devs, even when 2025 evidence says otherwise. Re-validate inputs annually.
- Single-axis trees miss interaction effects (e.g., team size × DevOps maturity × revenue). Use multivariate matrices for those.
- LLMs follow the tree literally and skip the "industry data" caveats — must be prompted to challenge the recommendation.
- Trees can't represent strong-tradeoff choices well — the leaf says "Microservices" but doesn't surface "you must hire a platform team."

## Agentic workflow
Use the tree as a fast first-pass: a router agent answers each Q from inputs (team size, NFRs, budget), arrives at a leaf, and outputs the recommendation with the tree-justification. A second critic agent steel-mans the runner-up leaf and surfaces any preconditions (DevOps maturity, headcount, revenue). If the runner-up survives, escalate to a full trade-off analysis ADR. Keep a per-project decisions log so the same tree never re-runs from scratch.

### Recommended subagents
- `faion-brainstorm` — diverge over which tree applies, then converge on the leaf.
- `faion-sdd-execution` — turn leaf into a documented ADR with the tree path as evidence.
- `faion-improver` — re-validate decisions at 6 months against tree inputs that may have shifted.

### Prompt pattern
```
Use the architecture-style decision tree (see ../decision-trees/README.md).
INPUT: team_size=<n>, devops_maturity=<low|medium|high>, deployment_freq=<...>,
revenue=<...>.
TASK: Walk the tree. Output: leaf, full path, preconditions, three risks of
following the recommendation, and the runner-up leaf with its key trade.
```

```
ROLE: tree-skeptic
TASK: The tree recommends <X>. Argue for the runner-up using a different
weighting of NFRs. If your argument requires changing one input by 20%, say so
and identify which input is most fragile.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| jq | Walk JSON-encoded trees | bundled / package manager |
| yq | Walk YAML decision tables | https://github.com/mikefarah/yq |
| graphviz / d2 | Render decision trees as diagrams | `brew install graphviz` / https://d2lang.com/ |
| dialog / gum | Interactive CLI tree walkers | https://github.com/charmbracelet/gum |
| pandas / DuckDB | Score multivariate decision matrices | `pip install pandas duckdb` |
| WebSearch (Claude) | Refresh tree inputs against current industry data | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Confluence / Notion / GitHub wiki | SaaS | Partial | Host the canonical trees; agents render Markdown |
| Backstage TechRadar | OSS | Yes | Tech-radar-style trees with adoption stages |
| ThoughtWorks Tech Radar | SaaS | Read-only | Reference for "Adopt/Trial/Assess/Hold" rings |
| AWS / Azure / GCP Architecture Center | SaaS | Read-only | Vendor decision trees; biased toward each vendor |
| LikeC4 / Structurizr | OSS+SaaS | Yes | Embed trees alongside C4 models |
| Lovable / v0 | SaaS | Limited | Demo only; not for serious decisions |

## Templates & scripts
See `templates.md` for tree, matrix, ADR, and TCO templates. Inline tree walker that takes inputs and outputs a leaf:

```python
# walk_tree.py — walk a YAML-encoded decision tree against inputs.
import sys, yaml

def walk(node, inputs, path):
    if 'leaf' in node:
        return node['leaf'], path + [node.get('label', 'leaf')]
    q = node['question']
    val = inputs.get(node['var'])
    branches = node['branches']
    branch = branches.get(str(val), branches.get('default'))
    if branch is None:
        raise SystemExit(f"no branch for {node['var']}={val} at {q}")
    return walk(branch, inputs, path + [f"{q} -> {val}"])

if __name__ == "__main__":
    tree = yaml.safe_load(open(sys.argv[1]))
    inputs = dict(arg.split("=", 1) for arg in sys.argv[2:])
    leaf, path = walk(tree, inputs, [])
    print("LEAF:", leaf)
    for step in path:
        print("  ", step)
```

```yaml
# tree.yaml — example architecture-style tree.
question: "Team size?"
var: team_size
branches:
  "small": { leaf: "Monolith" }
  "medium": { leaf: "Modular Monolith" }
  "large":
    question: "DevOps maturity?"
    var: devops
    branches:
      "high": { leaf: "Microservices" }
      "default": { leaf: "Modular Monolith" }
```

## Best practices
- Version your trees in-repo and treat updates as ADRs themselves; "the tree changed" is itself an architectural decision.
- Annotate each leaf with preconditions and a known-good escape hatch (when the leaf no longer applies).
- Refresh industry-data citations at least annually; LLMs anchor on stale numbers.
- Use trees to filter, then a weighted matrix or ATAM to choose; never let a tree be the sole evidence for a major decision.
- Keep the input set small (≤7 questions per tree); deeper trees are unmaintainable and don't help.
- Force the agent to output the runner-up; eliminates rubber-stamp behavior.

## AI-agent gotchas
- Agents skip preconditions in the leaf and present the recommendation as unconditional. Bake preconditions into the leaf node and demand they be echoed.
- LLMs invent additional questions to "improve" the tree mid-walk; pin them to the version-controlled tree only.
- Tree outputs vary across runs unless inputs are fully specified; require explicit `null`/`unknown` handling.
- Stale 2023/2024 industry-data anchors persist; require WebSearch refresh on numbers older than 12 months.
- Human-in-loop gates: any leaf that triggers a non-reversible commitment (multi-year contract, hiring plan, public API) must escalate to a senior reviewer.

## References
- https://martinfowler.com/articles/microservices.html
- https://www.thoughtworks.com/radar
- https://aws.amazon.com/architecture/well-architected/
- https://learn.microsoft.com/azure/architecture/guide/technology-choices/
- https://cloud.google.com/architecture/framework
- https://shopify.engineering/shopify-monolith
- https://martinfowler.com/articles/break-monolith-into-microservices.html
