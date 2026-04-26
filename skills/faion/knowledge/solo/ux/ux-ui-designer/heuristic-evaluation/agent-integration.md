# Agent Integration — Heuristic Evaluation

## When to use
- Before a usability test — eliminate obvious heuristic violations so testing resources go toward real user behavior, not expert-detectable issues
- When no user research budget is available — heuristic evaluation gives actionable findings at near-zero cost
- After a design sprint or major redesign — rapid expert review before handoff to development
- Code review for UI components — catching heuristic violations in PR review prevents regressions
- Competitive analysis: apply the same heuristics to competitor products to score relative quality systematically

## When NOT to use
- As a replacement for usability testing — heuristics find expert-visible violations, not real user struggles with domain-specific tasks
- After product launch as the sole quality gate — too late for design changes; use for iterative improvements
- When you need quantitative data to justify design decisions to stakeholders — heuristic evaluation produces qualitative expert opinions
- On a product used by domain experts who have learned to work around heuristic violations — their efficiency is in muscle memory, not heuristic compliance

## Where it fails / limitations
- Single-evaluator heuristic review finds only ~35% of issues; 3-5 evaluators finds ~75% — agents acting as a single evaluator have the same coverage limitation
- Heuristic evaluation has evaluator bias: what an agent classifies as "major" may be "cosmetic" to real users or vice versa
- Domain-specific mental models are hard to encode — an agent evaluating a medical device UI without clinical workflow knowledge will miss violations that matter most
- The method produces a list of problems, not solutions — recommendation quality depends on evaluator experience, which agents simulate but do not possess
- Inter-rater reliability is low even among human experts; agent severity ratings should be treated as first-pass triage, not final scores

## Agentic workflow
An agent can serve as a structured heuristic evaluator for digital interfaces — given access to screenshots, HTML/JSX, or design file exports, it can systematically apply Nielsen's 10 heuristics, log violations with location and severity, and produce a compiled report. Running the agent multiple times with different focus heuristics (one pass per heuristic) improves coverage better than a single omnibus pass. Human review of severity ratings and final prioritization is the required checkpoint — agents overrate cosmetic issues and underrate domain-specific violations.

### Recommended subagents
- `faion-usability-agent` — primary agent for heuristic evaluation; structured to apply all 10 heuristics with severity rating
- general code agent — extracts all interactive elements, states, labels, and flows from codebase before evaluation pass

### Prompt pattern
```
You are conducting a heuristic evaluation of the following interface using Nielsen's 10 heuristics.
Focus heuristic this pass: #[N] — [Heuristic name]

Interface description / screenshots: [input]
User scenario: [what task the user is trying to accomplish]

For each violation found:
- Location: [screen / component / element]
- Heuristic: #[N] — [name]
- Problem: [specific description of the violation]
- Severity: [0=not a problem, 1=cosmetic, 2=minor, 3=major, 4=catastrophic]
- Recommendation: [specific fix]

If no violations: "No violations found for this heuristic in the evaluated scope."
```

```
Compile the following heuristic evaluation findings from multiple evaluator passes.
Remove duplicates (same location + same heuristic). Where severity scores differ,
average them and note the range. Group by: (a) severity descending, (b) heuristic.
Output a prioritized action list: Severity 4 → 3 → 2 → 1.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` CLI | Automated accessibility-focused heuristic checks (heuristics #1, #5, #9 coverage) | `npm i -g @axe-core/cli` / github.com/dequelabs/axe-core |
| `lighthouse` CLI | Automated best-practice and accessibility scoring; maps to several heuristics | `npm i -g lighthouse` / github.com/GoogleChrome/lighthouse |
| `playwright` CLI | Capture screenshots of all states for visual heuristic review | `npm i -D @playwright/test` / playwright.dev |
| `pa11y` | Automated accessibility testing with WCAG mapping; complements heuristic #5, #9 | `npm i -g pa11y` / pa11y.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Maze | SaaS | Yes — API | Rapid remote usability testing; use after heuristic eval to validate severity ratings with real users |
| UserZoom (Qualtrics XM) | SaaS | Partial | Remote moderated/unmoderated testing; exports session data for analysis |
| Notion | SaaS | Yes — API | Agent writes structured heuristic evaluation report directly to Notion page |
| Airtable | SaaS | Yes — full API | Heuristic findings as a filterable database by severity, heuristic, and component |
| Zeplin | SaaS | Partial — plugin API | Design annotation tool; agent can add heuristic violation annotations to design files |
| UsabilityHub (Lyssna) | SaaS | Partial | First-click and preference tests; validates specific heuristic fixes |

## Templates & scripts
See `templates.md` for the Evaluation Template (per evaluator) and Compiled Report Template.

Inline script — run automated heuristic pre-check with axe + lighthouse:
```bash
#!/usr/bin/env bash
# Usage: ./heuristic-precheck.sh https://example.com
# Covers heuristics: #1 (system status), #4 (consistency), #5 (error prevention), #9 (error recovery)
URL=$1
echo "=== Accessibility (heuristics #5, #9) ==="
axe "$URL" --reporter=v2 2>/dev/null | \
  jq '[.violations[] | {rule: .id, impact: .impact, description: .description,
    count: (.nodes | length)}] | sort_by(.impact)' 2>/dev/null || \
  echo "axe not available, skipping"

echo ""
echo "=== Performance + Best Practices (heuristic #1) ==="
lighthouse "$URL" \
  --output=json \
  --chrome-flags="--headless" \
  --quiet 2>/dev/null | \
  jq '{
    performance: .categories.performance.score,
    accessibility: .categories.accessibility.score,
    best_practices: .categories["best-practices"].score,
    failed_audits: [.audits | to_entries[] |
      select(.value.score != null and .value.score < 0.5) |
      {id: .key, score: .value.score, title: .value.title}]
  }' 2>/dev/null || echo "lighthouse not available, skipping"
```

## Best practices
- Run one heuristic per evaluation pass — a single omnibus pass produces shallow findings for every heuristic; dedicated passes catch ~3x more issues per heuristic
- Severity 4 items block the release; severity 3 items are sprint-level fixes; severity 1-2 items go into the polish backlog — use this triage consistently
- Provide concrete location references (screen name, element name, user flow step) — "UI is confusing" is not an actionable finding
- Run evaluations against the same task scenarios your user research uses — this enables direct comparison between heuristic and usability test findings
- Use heuristic evaluation as a forcing function for design documentation — evaluators need to understand intended behavior to judge violations; gaps in that understanding reveal missing design specs
- Document what was evaluated (specific screens, flows, prototype version, date) — without this, findings cannot be reproduced or compared to later versions
- Combine with automated tools: axe-core covers ~30% of heuristic violations that can be detected programmatically, freeing evaluators to focus on judgment-heavy heuristics (#2, #6, #8)

## AI-agent gotchas
- An agent evaluating the same interface multiple times with the same prompt tends to reproduce the same findings — vary the user scenario and focus heuristic to increase coverage
- Agents inflate severity ratings for visually prominent issues and underrate violations in less conspicuous locations — severity calibration requires human judgment
- Heuristic #8 (aesthetic and minimalist design) is the most subjective; agent ratings for "excessive visual noise" depend heavily on the examples in its training and the prompt framing
- Agents cannot evaluate heuristic #7 (flexibility and efficiency of use) for keyboard shortcuts and power-user features without actually interacting with the product
- An agent declaring "no violations found" for a heuristic should prompt a follow-up — either the interface is genuinely excellent or the agent didn't look hard enough; ask it to explain its reasoning for each heuristic before accepting a clean bill

## References
- https://www.nngroup.com/articles/ten-usability-heuristics/
- https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- https://www.nngroup.com/articles/usability-inspection-methods/
- https://www.interaction-design.org/literature/article/heuristic-evaluation-how-to-conduct-a-heuristic-evaluation
- Usability Engineering — Jakob Nielsen (Morgan Kaufmann, 1994) — original severity scale definition
- https://jnd.org/heuristic-evaluation-considered-harmful/ — Don Norman on limitations
