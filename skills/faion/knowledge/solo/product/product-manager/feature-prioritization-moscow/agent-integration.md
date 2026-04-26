# Agent Integration — Feature Prioritization (MoSCoW)

## When to use
- Fixed-timebox release (sprint, milestone, MVP, contractual deadline) where capacity is the constraint and a clear "won't" line is needed.
- Stakeholder workshop where the goal is shared vocabulary, not numerical optimization.
- Scoping a vendor or contractor engagement: M/S/C/W maps cleanly to contract obligations vs nice-to-haves.
- Compliance and legal-driven work where "Must" carries a non-negotiable definition.

## When NOT to use
- Cross-feature ROI comparison — MoSCoW does not encode effort or impact magnitude. Use RICE or WSJF.
- Long-horizon roadmaps (>1 quarter) — categories drift; rerun MoSCoW per release.
- Many candidates (>30 items) — categories collapse into "Must" by stakeholder pressure; you need a numeric framework.
- Strategic bets — MoSCoW cannot capture "this is a moat play, not viability."

## Where it fails / limitations
- "Must" inflation: without a strict capacity check, 80% of items end up Must.
- The "Won't" column is psychologically uncomfortable; teams omit it, which destroys the framework's main value.
- Effort allocation (60/20/20) is heuristic, not a law; mistaking it for one creates fake precision.
- Disagreements collapse to politics, not data — there is no tiebreaker mechanism inside the framework.
- Categories are binary-ish — no way to express "Must if customer X signs, Should otherwise."

## Agentic workflow
A scoping agent ingests the feature list plus a stated capacity (eng-weeks) and the release goal, and returns an initial M/S/C/W classification with a one-line "fail-test" per Must Have ("does product fail completely without this?"). A capacity agent sums the effort and warns if Must+Should >80% of capacity. A challenger agent attacks every Must by re-asking the fail-test from a contrarian persona ("a competitor ships without this and wins — still Must?"). Human approves; agent locks Must and Won't, leaves Should/Could editable.

### Recommended subagents
- `faion-mvp-scope-analyzer-agent` — initial classification, named in the README.
- A "must-challenger" agent — single job: re-ask the fail-test, force downgrades.
- A capacity-sentinel agent — runs on every backlog change, alerts when Must>60%.
- `faion-sdd-executor-agent` — picks up Must items first as SDD tasks.

### Prompt pattern
```
Release: <name>, capacity: <X eng-weeks>, goal: <one-line>.
Candidates: <list with effort estimate per item>.
Classify each as Must / Should / Could / Won't.
For each Must include a one-line fail-test: "without this, the product fails because ___".
For each Won't include a one-line "explicitly excluded because ___".
Flag if Must+Should sum exceeds 80% of capacity.
```

```
You are the must-challenger. For each item below currently classified Must,
state the strongest case for downgrading to Should. If you cannot construct
a credible case, leave it as Must. Output a diff, not a rewrite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh issue list --label moscow:must` | Filter GitHub issues by MoSCoW label | https://cli.github.com/manual/gh_issue_list |
| `linear-cli` / Linear GraphQL | Linear has a `priority` field; map MoSCoW to it via API | https://developers.linear.app |
| `jq` + project export | Sum effort per category to validate proportions | https://stedolan.github.io/jq/ |
| `mermaid-cli` | Render quadrant chart of MoSCoW classification | https://github.com/mermaid-js/mermaid-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (GraphQL) | Map MoSCoW to label or custom field; agents update via API. |
| GitHub Projects | SaaS | Yes (REST/GraphQL) | Free; use labels `moscow:must|should|could|wont`. |
| Notion | SaaS | Yes (REST API) | DIY board with `Category` select column; cheap. |
| Airfocus | SaaS | Yes (API) | Native MoSCoW board view. |
| Trello + Butler | SaaS | Limited | List-per-category; automation moves cards by rule. |
| OpenProject | OSS | Yes | Custom-field MoSCoW; self-hostable. |

## Templates & scripts
See `templates.md` for the matrix and discussion-guide formats. Inline capacity validator:

```bash
#!/usr/bin/env bash
# moscow-validate.sh items.csv capacity_weeks
# CSV: name,category,effort_weeks
set -euo pipefail
csv="${1:?items.csv required}"
cap="${2:?capacity in weeks required}"

awk -F',' -v cap="$cap" '
  NR==1 { next }
  { totals[$2] += $3 }
  END {
    must = totals["Must"]; should = totals["Should"]; could = totals["Could"]
    printf "Must: %.1fw (%.0f%%)\n", must, must/cap*100
    printf "Should: %.1fw (%.0f%%)\n", should, should/cap*100
    printf "Could: %.1fw (%.0f%%)\n", could, could/cap*100
    if ((must+should)/cap > 0.80) {
      printf "FAIL: Must+Should = %.0f%% of capacity (>80%%)\n", (must+should)/cap*100
      exit 1
    }
  }' "$csv"
```

## Best practices
- Always require a capacity number first. MoSCoW without a timebox is feature wishlisting.
- Force at least 1 item into Won't Have per session — the discomfort is the value.
- Apply the fail-test verbatim for every Must: "If we don't have this, does the product work?" If the answer is "it works worse," the item is Should, not Must.
- Lock Must + Won't after stakeholder sign-off. Should/Could remain editable; Must changes require explicit escalation.
- Re-run MoSCoW per release, not per quarter. Categories are release-scoped, not strategic.
- Pair MoSCoW with a numeric framework (RICE) for the Should/Could tier — MoSCoW says "yes-if-time," RICE says "in what order."

## AI-agent gotchas
- Agents over-classify as Must by default — being "comprehensive" reads as safer than being "ruthless." Add an explicit instruction: "default category is Could; promote with evidence."
- LLMs forget the capacity number mid-session and produce 200% allocations. Pin capacity in every system message.
- The Won't list is the one most often omitted; make it a required output field, not optional.
- Model produces vague Musts ("good UX", "fast performance"); enforce a fail-test sentence per Must.
- Human-in-loop checkpoint: every Must that exceeds 40% of capacity individually requires a co-sign — this is the most common scope-explosion vector.
- Human-in-loop checkpoint: Won't list before publication — agents frequently slip a real "Must" into Won't because it looks expensive.
- Don't let the agent silently reclassify items between sessions; it loses commitment context. Force a diff with rationale per change.

## References
- DSDM Consortium — original MoSCoW definition: https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html
- Atlassian MoSCoW guide: https://www.atlassian.com/agile/product-management/moscow-method
- Roman Pichler — comparing prioritization frameworks: https://www.romanpichler.com/blog/20-product-prioritization-techniques/
- "MoSCoW Method" in PMBOK 7th ed., Section on requirements prioritization.
