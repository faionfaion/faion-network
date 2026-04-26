# Agent Integration — Decision Analysis

## When to use
- A reversible-but-expensive choice with ≥ 3 candidate options where the team is sliding toward gut feel (e.g. CRM platform, build-vs-buy, choosing a managed queue, picking an LLM provider). The matrix forces criteria onto the table.
- Stakeholders disagree because they secretly weight criteria differently — making the weights explicit (cost 25%, time 20%, ...) collapses argument-by-anecdote into argument-by-number.
- A decision will be re-litigated later (board review, audit, post-mortem) and you need a written rationale that survives staff turnover. The Decision Analysis Document is the artifact auditors / new hires read.
- Comparing N options against a current baseline (Pugh matrix mode): you want to know which alternatives strictly dominate "do nothing" and which only win on specific criteria.
- A decision has long-tail risk that only shows when you tabulate it (e.g. vendor lock-in, regulatory exposure). The "Risks" column in the matrix forces the question.
- Sequential / conditional decisions where outcomes depend on prior choices — switch from a flat matrix to a decision tree with probabilities and expected value.

## When NOT to use
- Two-option, low-cost, easily reversible decisions (one-way doors are rare; most of these are two-way doors). Use a 5-minute pros/cons list and ship.
- The decision is actually about strategy, not selection — no amount of weighted scoring fixes a wrong question. Run a brainstorm / strategy session first.
- You already know the answer and are trying to retrofit a matrix to "prove" it. This is the #1 failure mode (see Common Mistakes #1 in the README); reviewers will see through it and trust drops.
- Pure financial trade-offs with quantifiable cash flows — use NPV / discounted cash flow / cost-benefit analysis directly. A 1-5 score on "cost" throws away precision.
- Decisions under deep uncertainty (most numbers are guesses with > 1 order of magnitude error). Decision Analysis pretends to precision it does not have; prefer scenario planning or real-options analysis.
- Adversarial / political contexts where the "decision maker" will overrule any output. Document the decision instead of computing it.

## Where it fails / limitations
- **False precision**: a 3.85 vs 3.70 weighted total looks like a winner but is well within rater noise (typically ±0.5 on a 1-5 scale). Without sensitivity analysis the "winner" is often statistical noise.
- **Criteria collinearity**: "cost" and "TCO" and "subscription price" are often the same axis triple-counted, secretly inflating financial weight to 60%+ while the table shows 25%.
- **Inverse scaling errors**: cost is "lower is better" but features is "higher is better". Mixing direction silently breaks the math. Always normalize to "5 = best for this criterion".
- **Anchoring on first option**: the option scored first becomes the reference; later options drift toward 3 (regression to mean). Score one criterion across all options before moving to the next.
- **Missing options**: the matrix evaluates the options you brought; it cannot tell you the option you forgot. Pair with explicit divergence (brainstorm) before convergence (matrix).
- **Weight gaming**: stakeholders who want option B will lobby to raise the weight of criteria where B wins. Lock weights *before* scoring; record who set them and when.
- **No-uncertainty assumption**: the matrix treats each cell as a point estimate. Real options have wide ranges (cost ±50%, time ±100%); use Monte Carlo or ranges if stakes are high.

## Agentic workflow
Drive this with a three-pass structured pipeline. (1) **Frame pass** — a sonnet agent reads the decision context and emits the structured frame `{decision_statement, objectives[], constraints[], decision_maker, criteria[]}`; weights are NOT yet assigned. (2) **Score pass** — for each option × criterion cell, an agent retrieves evidence (vendor docs, pricing pages, GitHub issue counts, last-12-month uptime data) and emits `{option, criterion, raw_evidence_url[], normalized_score_1_5, confidence}`. Multiple agents in parallel reduce single-agent bias. (3) **Sensitivity / dissent pass** — an opus agent runs Monte Carlo over weights (±20%) and confidence intervals on cells, emits a recommendation with a "robustness score" and lists which cells, if flipped, would change the answer. Only the final memo is prose; everything else is JSON. The decision itself stays human — agents produce the matrix, the human signs.

### Recommended subagents
- `faion-brainstorm` — diverge / converge / review to expand the option set before the matrix is locked. Skipping this is how you get a polished comparison of the 3 obvious options and miss option D.
- `faion-sdd-executor-agent` — once the recommended option is signed off, generate the implementation SDD task tree (constitution, spec, design) bounded by the choice.
- `faion-feature-executor` — execute discrete tasks that fall out of the decision (vendor onboarding, contract signing, migration plan).
- `faion-improver` — quarterly meta-loop: read decisions made 6-12 months ago, compare predicted scores to actual outcomes, log calibration errors as a recurring pattern.
- A custom `decision-evidence-gatherer` worth creating: input = `{option, criterion}`, output = `{evidence_urls[], extracted_facts[], normalized_score, confidence}`. Reuse across decisions; it caches vendor research.
- A custom `criteria-deduplicator`: input = criteria list, output = clusters of collinear criteria with merge recommendation. Catches the "cost / TCO / pricing" triple-count failure.

### Prompt pattern
```
You are a decision analyst. Inputs: decision_statement, options[], criteria[] with
weights summing to 100, score_evidence[] (one row per {option, criterion}). Output JSON:
{
  matrix: [{option, weighted_total, per_criterion: [{criterion, score, evidence_urls}]}],
  ranking: [{option, total, gap_to_next}],
  sensitivity: {weights_perturbed_pct: 20, recommendation_stable: bool, flip_threshold: {...}},
  collinearity_warnings: [{criteria_pair, correlation_estimate}],
  recommendation: {option, rationale_<= 80_words, top_3_risks, mitigation_per_risk}
}
Constraints:
- Do NOT invent scores; every cell must cite at least one evidence_url or be marked "low_confidence".
- If two criteria have correlation > 0.6, flag and recommend merging.
- If the gap between #1 and #2 is < 0.3, recommendation must be "tied — escalate to human".
- Never recommend "do nothing" without listing what we lose by stalling.
```

```
You are an evidence gatherer for ONE matrix cell. Input: {option, criterion}. Output JSON:
{
  evidence_urls: [<= 5 primary sources, vendor docs preferred over blog posts>],
  extracted_facts: [{fact, source_url, retrieved_at}],
  normalized_score_1_5: int,
  scoring_rubric_used: "<one sentence>",
  confidence: "high"|"medium"|"low",
  caveats: [<= 3 bullets>]
}
If you cannot find primary evidence, return confidence="low" with empty extracted_facts.
Never use marketing copy as the only source.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dakota` | Open-source decision analysis & uncertainty quantification (Sandia Labs) | https://dakota.sandia.gov |
| `pulp` (Python) | Linear programming for constrained selection (when criteria become hard constraints) | `pip install pulp` |
| `numpy` + `pandas` | Cell-level Monte Carlo over weights and scores; export sensitivity heatmap | `pip install numpy pandas` |
| `streamlit` | One-page interactive matrix the team can re-weight live during review | https://streamlit.io |
| `mermaid-cli` | Render decision trees from text (sequential decisions) | `npm i -g @mermaid-js/mermaid-cli` |
| `gh` + `jq` | Pull GitHub issue counts / commit cadence as evidence for "active maintenance" criterion | https://cli.github.com |
| `httpie` / `curl` | Hit vendor pricing/uptime APIs to populate cost & reliability cells | https://httpie.io |
| `claude` CLI | Drive the score & sensitivity passes on the JSON matrix | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Loomio | SaaS / OSS (AGPL) | Partial (REST) | Group decision deliberation; agent can post the matrix and harvest votes |
| Airtable | SaaS | Yes (REST API) | Cheap matrix store; agents read/write rows; non-tech stakeholders can re-weight |
| Notion | SaaS | Yes (REST API) | Agent posts the Decision Analysis Document as a draft, links the live matrix |
| Confluence | SaaS / Server | Yes (REST API) | Enterprise audit trail for the rationale doc |
| 1000minds | SaaS | Limited | Pairwise PAPRIKA method — strong for ranking criteria when stakeholders cannot agree on weights |
| TransparentChoice | SaaS | Limited | AHP (Analytic Hierarchy Process) for weight elicitation |
| SuperDecisions | OSS desktop | No | AHP / ANP reference impl; useful for one-off academic-grade analysis |
| Decision Lens | SaaS (gov) | API on enterprise tier | Heavyweight portfolio decision platform |
| Hugin / GeNIe | Commercial / academic | No | Bayesian network decision support — overkill for most product decisions |

## Templates & scripts
See `templates.md` (in this folder) for the Decision Analysis Document and Simple Decision Matrix shells. Inline a sensitivity-analysis helper to bolt onto the matrix:

```python
# sensitivity.py — usage: python sensitivity.py matrix.json
# matrix.json: {"weights":{"cost":0.25,...}, "scores":{"opt_a":{"cost":4,...}, ...}}
import json, sys, random, statistics

def weighted_total(weights, scores):
    return sum(weights[c] * scores[c] for c in weights)

def perturb(weights, sigma=0.2):
    p = {c: max(0.01, w * random.gauss(1, sigma)) for c, w in weights.items()}
    s = sum(p.values())
    return {c: w / s for c, w in p.items()}

m = json.load(open(sys.argv[1]))
N = 2000
wins = {opt: 0 for opt in m["scores"]}
totals = {opt: [] for opt in m["scores"]}
for _ in range(N):
    w = perturb(m["weights"])
    scored = {opt: weighted_total(w, m["scores"][opt]) for opt in m["scores"]}
    winner = max(scored, key=scored.get)
    wins[winner] += 1
    for opt, t in scored.items():
        totals[opt].append(t)

print("robustness (% Monte Carlo wins under +/-20% weight noise):")
for opt, w in sorted(wins.items(), key=lambda x: -x[1]):
    print(f"  {opt}: {100*w/N:.1f}%  mean={statistics.mean(totals[opt]):.2f}  sd={statistics.stdev(totals[opt]):.2f}")
```
If the top option wins < 70% of Monte Carlo trials, the recommendation is fragile — escalate to human or gather more evidence.

## Best practices
- Lock weights *before* scoring options; record the weight-setter and timestamp. Otherwise weights drift to support a preferred answer.
- Score one criterion across all options at once, not one option fully then the next — kills anchoring bias on the first option scored.
- Always include a "do nothing" / status-quo option, even when it feels silly. It calibrates the rest of the matrix.
- Force evidence URLs on every cell. A score with no source is a vote, not data.
- Publish raters' individual scores before averaging — disagreement is signal; collapsing it into a mean hides it.
- Run sensitivity analysis (±20% on weights, ±1 on scores) automatically. If the top changes, the decision is fragile, not robust.
- Keep the matrix to ≤ 7 criteria. More than 7 and stakeholders cannot hold them in working memory; weights become arbitrary.
- Pre-mortem the recommended option ("assume in 12 months this was the wrong call — why?"). The output goes into the Risks section, not as an afterthought.
- Archive the final matrix + rationale in the project's `.aidocs/` (or equivalent) so the next team can audit and learn calibration.

## AI-agent gotchas
- Agents will hallucinate vendor capabilities and pricing. Force evidence URLs on every cell and reject cells without primary sources (vendor docs, pricing pages, GitHub repos), not blog posts.
- LLMs cluster in the middle of 1-5 scales (regression to median). Calibrate by asking for percentile rank instead, or by anchoring with two extreme reference options.
- A single agent doing all scoring inherits its own biases across the whole matrix. Use parallel scoring agents (one per criterion or one per option) and compare; large disagreement = low confidence cells.
- Agents will silently mix scoring directions ("cost: 5 = expensive" in one row, "5 = cheap" in another). Fix at the schema level: every criterion has an explicit `direction: "higher_better"|"lower_better"`.
- Date drift: pricing and uptime data goes stale fast. Stamp `retrieved_at` on every fact; agents must refuse to reuse evidence > 90 days old without re-fetching.
- LLMs love to recommend the option you mentioned first or last. Randomize option order in the prompt before the score pass.
- Agent-only decisions are an anti-pattern. The matrix is decision *support*, not decision *making*. Human-in-the-loop checkpoints: weights (before scoring), final rec (before commitment), post-implementation calibration review.
- Watch for prompt-injected criteria: if option descriptions come from vendor websites, vendors can plant criteria favoring themselves. Strip suspicious instructions; never let vendor copy define weights.

## References
- Hammond, Keeney, Raiffa — *Smart Choices: A Practical Guide to Making Better Decisions* (the canonical decision-analysis text).
- Howard & Abbas — *Foundations of Decision Analysis* (the theory: utility, value of information, decision trees).
- BABOK Guide v3 — Requirements Analysis and Design Definition, §10.18 Decision Analysis (industry-standard reference for the BA role).
- Saaty — *Decision Making for Leaders* (Analytic Hierarchy Process for weight elicitation).
- Tetlock & Gardner — *Superforecasting* (calibration and sensitivity to noise; relevant to scoring quality).
- Kahneman, Sibony, Sunstein — *Noise* (why structured decision processes outperform expert gut feel).
- https://dakota.sandia.gov/ — open-source quantitative decision-analysis toolkit.
- https://www.lesswrong.com/posts/cTthrcKgvD3kkH3nJ/how-to-have-good-research-taste — relevant on calibration when evidence is thin.
