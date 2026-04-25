# Agent Integration — Feature Prioritization (MoSCoW)

## When to use
- Fixed-timebox release (sprint, MVP, launch deadline) where the question is "what fits and what's cut".
- Stakeholder alignment workshop where the deliverable is a shared shortlist, not a numerical score.
- Pre-sales / contract-bound deliverables where Won't-Have must be documented to prevent scope creep.
- Pairing with MVP-scoping: MoSCoW gives the categorical lens, MVP-scoping gives the buildable cut.

## When NOT to use
- Continuous backlog ranking across many items — RICE / WSJF give finer-grained sequence.
- Strategic portfolio decisions across multiple products — MoSCoW lacks effort math.
- Fast iteration / shipping daily — the ceremony cost is too high for sub-week cycles.

## Where it fails / limitations
- "Must" inflation: stakeholders mark everything Must; only ~60% of capacity should be Must.
- Without an explicit timebox MoSCoW degrades into a wish list.
- No effort discipline — two Musts can each be a quarter long; check capacity before locking.
- Won't-Have is the most-skipped category and the most useful one. Agents and humans both forget it.
- Categories are coarse — within "Should" there's still ordering work that MoSCoW doesn't help with.

## Agentic workflow
Use a categorizer subagent to map each requirement to {M,S,C,W} with a rationale and a workaround field (required for S/C). A capacity-checker subagent sums effort by bucket and flags violations of the 60/20/20 split. A reviewer subagent challenges every Must by asking the methodology's three test questions and downgrades any item that fails. Lock the resulting matrix into the spec or release plan; changing a Must post-lock requires explicit human escalation.

### Recommended subagents
- `faion-mvp-scope-analyzer-agent` — MoSCoW-specific scope agent named in this methodology's metadata; also serves the MVP-scoping methodology.
- `faion-mlp-feature-proposer-agent` — proposes features that the categorizer then sorts.
- `faion-spec-reviewer-agent` — verifies each Must has acceptance criteria before lock.
- General-purpose `researcher` — pulls competitor / regulatory inputs for "is this really mandatory?".

### Prompt pattern
```
For each requirement, output JSON:
{
  "id": "<req-id>",
  "category": "M|S|C|W",
  "rationale": "<<= 200 chars>",
  "workaround": "<required if S or C, else null>",
  "effort_days": <int>,
  "must_test": {
    "fails_without": bool,
    "no_workaround": bool,
    "legal_or_contractual": bool
  }
}
Apply rule: category=="M" only if any must_test field is true.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` (ankitpokhrel) | Set MoSCoW via custom field on issues | https://github.com/ankitpokhrel/jira-cli |
| Linear GraphQL API | Custom MoSCoW field per issue | https://developers.linear.app |
| `gh` CLI + Projects v2 | Single-select MoSCoW field on Project items | https://cli.github.com |
| Notion API | MoSCoW database with category property | https://developers.notion.com |
| Airtable API | Spreadsheet matrix, easy capacity formulas | https://airtable.com/developers/web/api |
| `markdown-table-formatter` | Format MoSCoW matrices in specs | npm |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear / Jira | SaaS | Yes | Custom MoSCoW field; group views by category |
| Productboard | SaaS | Yes (REST) | Has prioritization views including MoSCoW |
| Aha! | SaaS | Yes (REST) | Prioritization scorecards incl. MoSCoW |
| Trello | SaaS | Yes (REST) | Cheap option: 4 lists for M/S/C/W |
| OpenProject | OSS | Yes (REST) | Self-hosted, custom fields |
| Miro / FigJam | SaaS | Limited (REST) | Workshop tool — mostly human; agents read board export |
| Notion / Airtable | SaaS | Yes (REST) | Easiest agent-writable backing store |

## Templates & scripts
See `templates.md` for the prioritization matrix and discussion guide. Capacity validator (≤ 30 lines):

```python
# moscow_check.py — validate 60/20/20 budget
import json, sys
TARGET = {"M": 0.60, "S": 0.20, "C": 0.20}

rows = json.load(sys.stdin)  # [{id, category, effort_days}]
total = sum(r["effort_days"] for r in rows if r["category"] != "W") or 1
by_cat = {"M": 0, "S": 0, "C": 0, "W": 0}
for r in rows:
    by_cat[r["category"]] += r["effort_days"]

violations = []
for cat, target in TARGET.items():
    actual = by_cat[cat] / total
    if cat == "M" and actual > target + 0.10:
        violations.append(f"Must over-allocated: {actual:.0%} (target {target:.0%})")
    if cat == "M" and actual < target - 0.10:
        violations.append(f"Must under-allocated: {actual:.0%} (target {target:.0%})")
print(json.dumps({"by_cat": by_cat, "violations": violations}, indent=2))
```

## Best practices
- Always pair MoSCoW with a fixed timebox + capacity number; without them the exercise is theatre.
- Force a non-empty Won't-Have list — at least 3 items, written before Must-Have is finalized.
- Apply the must-test (fails without, no workaround, legal/contractual) literally; if all three are false, it's not Must.
- Track per-stakeholder MoSCoW votes when groups disagree; the deltas themselves are useful signal.
- Re-baseline mid-release: if Must-Have effort grows > 10%, escalate before silently dropping Should items.
- When using with MVP-scoping, MoSCoW Must = MVP scope; Should = post-MVP fast-follow; Could = backlog; Won't = explicitly out of scope.

## AI-agent gotchas
- LLMs default to "Should" for ambiguous items; force a tie-break via the must-test booleans.
- Agents will silently drop Won't-Have. Make it a required, non-empty array in the output schema.
- Effort estimates from LLMs are unreliable; require T-shirt sizes that map to day ranges, not raw day counts.
- Watch for category-stuffing: an agent told "fit X requirements in capacity Y" will over-mark Should as Could. Validate with the capacity script.
- Human-in-loop checkpoints: Must lock-in, Won't-Have lock-in, any post-lock Must promotion.
- Do not let the same agent both propose and categorize — bias is severe. Use proposer → categorizer → reviewer triad.

## References
- DSDM Consortium — original MoSCoW source https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html
- Mike Cohn, "Agile Estimating and Planning" — chapter on prioritization techniques.
- Roman Pichler — "How to Prioritize Your Product Backlog" https://www.romanpichler.com/blog/
- ProductPlan glossary — MoSCoW https://www.productplan.com/glossary/moscow-prioritization/
