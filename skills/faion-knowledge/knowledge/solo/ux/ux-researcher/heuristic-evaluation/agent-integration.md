# Agent Integration — Heuristic Evaluation

## When to use
- Before scheduling usability testing sessions — clear known issues first so sessions surface deeper problems
- When budget or timeline prevents full usability testing
- During rapid iteration cycles where expert review can gate each design sprint
- When evaluating a competitor's interface or an acquired product for UX debt
- As a quality gate before handoff from design to development

## When NOT to use
- As the sole validation method before launch — expert review does not substitute for real user testing
- When you need to understand "why" users struggle, not just "what" violates heuristics
- For novel interaction paradigms with no established heuristics (e.g., new VR interfaces) — existing heuristics are insufficient
- When the team has no UX expertise; untrained evaluators produce low-reliability findings

## Where it fails / limitations
- Single evaluator finds only ~35% of problems; three evaluators needed for ~60% coverage
- Evaluators bring their own mental models; problems obvious to experts may not match actual user struggles
- Severity ratings are subjective and vary widely between evaluators without calibration
- Heuristic evaluation catches violations of known principles but misses novel usability failures
- Digital prototypes with limited interactivity produce artificially low violation counts

## Agentic workflow
An agent can systematically apply Nielsen's 10 heuristics to a design artifact by working through a structured checklist: for each heuristic, examine specified screens, document violation/pass, rate severity 0-4, and produce a structured findings table. The agent operates best on static screenshots or recorded flows with timestamped notes; real-time interactive evaluation requires a human at the interface. A second agent pass can aggregate findings from multiple evaluator transcripts, deduplicate, and compute severity statistics.

### Recommended subagents
- `faion-sdd-executor-agent` — run a heuristic checklist across a defined scope and compile a structured findings table
- General Claude subagent with vision — analyze screenshots against each heuristic, note violations with location and severity

### Prompt pattern
```
You are a UX expert applying Nielsen's 10 usability heuristics to the attached screenshots of [product / flow name].

For each of the 10 heuristics, list:
- Violations found (location, description, severity 0-4)
- Passes (brief confirmation if no issues)

Output as a structured markdown table per heuristic.
```

```
Merge these two independent heuristic evaluation reports: [report A] [report B].
Deduplicate findings that describe the same issue. Where severity differs, take the higher rating.
Output: consolidated table sorted by severity descending.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pagespeed` (Lighthouse CLI) | Automated accessibility + performance heuristics | `npm i -g lighthouse` / developers.google.com/web/tools/lighthouse |
| `axe-cli` | Automated accessibility checks (partial overlap with heuristic #6, #9) | `npm i -g @axe-core/cli` / github.com/dequelabs/axe-core-npm |
| `playwright` | Capture screenshots of every screen in a flow for offline review | `npm i @playwright/test` / playwright.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Maze | SaaS | Partial (API) | Heuristic + usability testing; API for results extraction |
| UXCheck (Chrome extension) | OSS | No | Nielsen heuristics checklist overlay on live sites |
| Figma | SaaS | Partial (REST API) | Export frames for agent review; no built-in heuristic tooling |
| UserZoom | SaaS | No | Expert review modules; no programmatic evaluation |

## Templates & scripts
See `templates.md` for individual evaluator template and compiled report template.

Inline: severity aggregation helper for multiple evaluators:
```python
# Aggregate severity scores from multiple evaluators per issue
from statistics import mean, median

def aggregate_severities(evaluations: list[dict]) -> list[dict]:
    """
    evaluations: list of {issue_id, location, heuristic, severity, evaluator}
    Returns: list of {issue_id, location, heuristic, mean_severity, max_severity, count}
    """
    from collections import defaultdict
    grouped = defaultdict(list)
    for e in evaluations:
        grouped[e["issue_id"]].append(e["severity"])
    return [
        {
            "issue_id": iid,
            "mean_severity": round(mean(scores), 1),
            "max_severity": max(scores),
            "count": len(scores),
        }
        for iid, scores in grouped.items()
    ]
```

## Best practices
- Calibrate evaluators before the session: review 2-3 example findings together to align severity interpretation
- Evaluate independently first, aggregate second — this is the single most important rule; combined sessions suppress minority observations
- Keep each finding atomic: one violation per row, not "several issues on the checkout page"
- Assign location precisely: "checkout step 2, email field" not "form area"
- Pair heuristic evaluation with one round of tree testing or usability testing to cross-validate severity ratings
- Revisit heuristic #7 (flexibility/efficiency) specifically for power users; most evaluators focus on novice scenarios

## AI-agent gotchas
- Agents cannot interact with live interfaces — they can only analyze what's given to them (screenshots, recordings, design files)
- Vision models may miss low-contrast text violations that screen calibration would reveal; always specify to check WCAG contrast ratios explicitly
- Agent severity ratings will not match Nielsen's scale without explicit calibration prompts; always define the 0-4 scale in the prompt
- Do not use an agent as a replacement for the second or third human evaluator — diversity of mental models matters
- Structured output (JSON schema) for findings is critical; free-form prose findings from agents are difficult to aggregate

## References
- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design." https://www.nngroup.com/articles/ten-usability-heuristics/
- Nielsen, J. & Mack, R. (Eds.). "Usability Inspection Methods." Wiley, 1994.
- How to Conduct Heuristic Evaluation: https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- Beyond Nielsen's heuristics (Norman critique): https://jnd.org/heuristic-evaluation-considered-harmful/
- IDF guide: https://www.interaction-design.org/literature/article/heuristic-evaluation-how-to-conduct-a-heuristic-evaluation
