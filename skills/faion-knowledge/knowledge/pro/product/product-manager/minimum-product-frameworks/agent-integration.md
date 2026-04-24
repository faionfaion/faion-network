# Agent Integration — 9 Minimum Product Frameworks

The methodology is a **selection matrix**, not a build playbook: it picks one of MVP / MLP / MMP / MAC / RAT / MDP / MVA / MFP / SLC for the next product cut. The agentic value is making the choice fast, defensible, and reversible — and then routing to the right downstream methodology (`mvp-scoping`, `mlp-planning`, `riskiest-assumption-test`, etc.) for actual scoping.

## When to use
- New product or major new module — before the first `spec.md` exists.
- The team is reflexively saying "let's ship an MVP" without checking if the market is crowded, the buyer is enterprise, or the differentiator is emotional.
- Pivot moment: the current build is failing on retention or conversion — re-pick the framework before re-scoping.
- Multiple stakeholders disagree on what "minimum" means (engineering says functional, marketing says lovable, sales says marketable) — use the matrix as a forcing function.
- Pre-investment / pre-board memo: justify the chosen framework against blue/red ocean and ICP positioning.
- Crowded category (many "good enough" alternatives) where MVP is the wrong default and MLP/SLC are likely correct.
- Technical infrastructure / dev-tool launches where MFP precedes any user-facing minimum.

## When NOT to use
- Methodology already chosen and validated — go straight to that framework's scoping doc, don't re-litigate.
- Pure feature work inside a shipped product (use `release-planning`, `feature-prioritization`, RICE/MoSCoW instead).
- Hard-deadline regulated launches where scope is dictated by compliance, not strategy.
- Tiny fix-it-fast tasks (<1 sprint); framework choice is overhead.
- Internal tools with one stakeholder — pick MFP and move on; the matrix is overkill.

## Where it fails / limitations
- **Acronym soup as theatre.** Teams pick "MLP" because it sounds nicer than "MVP" without changing scope. Without a written *exit criterion per framework*, the choice is decorative.
- **Single-axis market read.** "Crowded vs blue ocean" is the only matrix axis here; in practice you also need buyer (B2B/B2C), distribution (PLG/sales-led), regulatory load. The 9-framework table under-specifies.
- **No transition rule.** README says "MFP then expand" but doesn't define what triggers the transition (metric? time? validation event?). Agents will sit in MFP forever.
- **MAC ambiguity.** "Minimum Awesome Component" overlaps heavily with MLP and SLC; in red oceans a MAC often *is* the lovable hook, double-counting the same scope.
- **MVA vs MMP overlap.** Both target enterprise/ROI; the methodology doesn't disambiguate. In practice, MMP = sellable, MVA = measurable business value — agents conflate them.
- **No cost dimension.** All frameworks treated as equally cheap; in reality MLP and MDP cost 2-4x MVP for the polish budget. Without a cost column the recommendation is naive.
- **Framework lock-in.** Once "MLP" is in the deck, switching to RAT after a failed validation is socially expensive. Methodology offers no de-escalation path.
- **Survivorship-bias source.** "MVP is suicide in 2026" is a strong claim drawn from crowded-SaaS storytelling; doesn't generalise to vertical SaaS, B2B niches, or dev-tools where MVPs still win.

## Agentic workflow
Treat the matrix as a **routing decision**, not a build instruction. Drive it with a 3-pass subagent flow: (1) a research agent gathers market-condition evidence (competitor count, alternatives, ICP, buyer, switching cost) — emits a structured `market-context.yml`; (2) a PM agent applies the decision matrix to that file and emits a `framework-choice.md` with the chosen framework, the rejected ones, and the exit criterion; (3) the chosen framework's downstream methodology agent (e.g. `mvp-scoping`, `mlp-planning`) consumes that file as its input contract. Re-pick on every pivot (failed validation, missed activation target). The choice file is versioned in `.aidocs/product_docs/framework-choice.md` — diffing it across pivots is the audit trail.

### Recommended subagents
- `faion-product-manager` (this directory's parent skill) — orchestrator. Reads the matrix, calls research agent, emits the choice file.
- `faion-market-researcher-agent` (`pro/research/market-researcher/`) — produces market-context inputs: competitor density, ICP, buyer type, switching cost. Required before the matrix can be applied.
- `faion-research-agent` (`pro/research/researcher/`) modes `validate`, `personas`, `pains` — confirms the chosen framework's assumption (e.g. "users will pay for lovable" or "buyer cares about ROI").
- `mvp-scoping` / `mlp-planning` / sibling methodology agents (under `pro/product/product-manager/`) — downstream consumers of the choice; one fires depending on the matrix output.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts the chosen framework's scope into a `spec.md` → `design.md` → tasks chain.
- `faion-brainstorm` skill — diverge/converge when the matrix is genuinely tied between two frameworks (e.g. MLP vs MDP); avoids single-LLM lock-in.
- A purpose-built **framework-pivot-detector agent** (worth creating): re-runs the matrix when an activation/retention/win-rate metric crosses a threshold; emits a "re-pick recommended" alert with rationale.

### Prompt pattern
Framework selection pass:
```
You are a product manager applying the 9 minimum product frameworks
matrix. Inputs: <market-context.yml> and <icp.yml>.

For each of MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC:
- score 0-3 on fit with market_condition + buyer + differentiator
- list the single strongest reason for and against
Pick the top-1 with a 1-sentence rationale and write 2 explicit
exit criteria (metric + threshold). Output framework-choice.md.
Refuse to pick if any of: market_condition is missing, buyer is
"unknown", or two frameworks tie above score 2 — return
"need-discovery" and list the gap.
```

Framework re-pick (post-pivot):
```
You are a PM auditor. Inputs: framework-choice.md (current),
last-30-days metrics snapshot, post-mortem of the failed validation.

Decide: stay (state why), pivot to <framework> (state why and what
changes), or escalate (matrix can't decide — name the missing data).
No prose unless one of the three. Append decision to
framework-choice.md as a new dated section; never rewrite history.
```

Framework hand-off to scoping:
```
You are <chosen-framework>-scoping agent (e.g. mlp-planning).
Input: framework-choice.md. Constraint: do not re-litigate the
choice. Produce: scope.md with in/out lists, the one assumption
this framework is built to test, the kill-criterion. If the input
file is older than 14 days or refers to a different framework,
abort and request a re-pick.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI | PR-review the framework-choice.md so PM + founder co-sign. | https://cli.github.com |
| `claude` (Anthropic CLI) | Run the 3-pass selection flow headlessly via cron / makefile target. | https://docs.anthropic.com |
| `dbt` / `metabase` | Encode framework exit criteria as SQL models so "did we hit MVP exit?" is auditable. | https://docs.getdbt.com |
| `growthbook` / `statsig` | Encode the RAT (riskiest assumption test) as a feature flag + experiment with a stop condition. | https://docs.growthbook.io |
| `posthog` (HogQL) | Pull activation / retention / NPS for MLP and MDP exit-criterion verification. | https://posthog.com/docs |
| `typeform` / `tally` API | Cheap qualitative validation for MLP "lovable" claim before any code. | https://www.typeform.com/developers |
| `productboard` API | If used, sync the chosen framework + exit criteria to roadmap items. | https://developer.productboard.com |
| `linear` / `jira` API | Tag every initiative with the framework label; agents use it to filter. | https://developers.linear.app |
| `notion` API | Versioned framework-choice doc with comment-thread history. | https://developers.notion.com |
| `pmf-survey` (Sean Ellis) tooling | "How would you feel if you couldn't use this product?" — exit-criterion proxy for MVP→MLP transition. | https://pmfsurvey.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Productboard | SaaS | API yes | Tag features by framework; agents filter MVP-vs-MLP scope. |
| Aha! | SaaS | API yes | Roadmap layer; encode framework as a custom field. |
| Linear / Jira | SaaS | API yes | Initiative-level framework tag; sprint planning respects it. |
| Notion / Confluence | SaaS | API yes | `framework-choice.md` lives here when not in repo. |
| Mixpanel / Amplitude / PostHog | SaaS / OSS | API yes | Exit-criterion measurement; agents pull cohorts for re-pick decisions. |
| Hotjar / FullStory / LogRocket | SaaS | API limited | Qualitative signal for MLP/MDP "lovable / delightful" claims. |
| Sprig / Survicate / Maze | SaaS | API yes | In-product surveys; cheap MLP validation without code changes. |
| LaunchDarkly / GrowthBook / Statsig | SaaS / OSS | API yes | Encode RAT as a flag with a stop rule; agents control rollout. |
| Userpilot / Appcues / Pendo | SaaS | API yes | MDP onboarding polish layer without engineering churn. |
| ProductPlan | SaaS | API yes | Roadmap visualisation per framework type. |
| Gainsight | SaaS | API yes | MMP / MVA buyers — track ROI-style adoption metrics. |
| Reforge / Lenny's library | content | n/a | Framework selection essays; LLM context for prompt grounding. |

## Templates & scripts

The README ships only the matrix table. The missing artefact is a machine-readable framework-choice file the downstream agents can consume. Drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# pick-framework.sh — apply the 9-framework matrix to a market-context file.
# Inputs: .aidocs/product_docs/market-context.yml
# Output: .aidocs/product_docs/framework-choice.md (versioned via git)
set -euo pipefail
ctx=".aidocs/product_docs/market-context.yml"
out=".aidocs/product_docs/framework-choice.md"
[ -f "$ctx" ] || { echo "missing $ctx — run market-researcher agent first" >&2; exit 2; }
mkdir -p "$(dirname "$out")"
python3 - "$ctx" "$out" <<'PY'
import sys, yaml, datetime
ctx = yaml.safe_load(open(sys.argv[1])); out = sys.argv[2]
m = ctx.get("market_condition", "").lower(); b = ctx.get("buyer", "").lower()
diff = ctx.get("differentiator", "").lower(); tech = ctx.get("tech_uncertainty", False)
rules = [
    (lambda: tech, "MFP", "Technical feasibility unknown — prove infra first."),
    (lambda: "enterprise" in b or "b2b" in b, "MMP", "Enterprise buyer needs sellable surface."),
    (lambda: "crowded" in m or "red ocean" in m, "MLP", "Crowded market — emotional differentiation required."),
    (lambda: "premium" in diff or "luxury" in diff, "MDP", "Premium positioning needs delight."),
    (lambda: "high uncertainty" in ctx.get("risk_profile", "").lower(), "RAT", "Validate riskiest assumption before scope."),
    (lambda: "consumer" in b and "simple" in diff, "SLC", "Consumer + simplicity — Simple/Lovable/Complete."),
    (lambda: True, "MVP", "Default: blue ocean, low cost, fast learning."),
]
chosen, why = next((f, w) for cond, f, w in rules if cond())
with open(out, "w") as f:
    f.write(f"# Framework choice — {datetime.date.today().isoformat()}\n\n")
    f.write(f"**Chosen:** {chosen}\n\n**Rationale:** {why}\n\n")
    f.write("## Inputs\n```yaml\n" + yaml.safe_dump(ctx) + "```\n\n")
    f.write("## Exit criteria\n- TODO: define metric + threshold\n- TODO: define kill-criterion\n")
    f.write("\n## History\n- " + datetime.date.today().isoformat() + f": initial pick = {chosen}\n")
print(out, chosen)
PY
git add "$out"
```

The script is intentionally rule-based (not LLM) so the choice is auditable; the LLM agent fills the exit-criteria stubs and reviews the rationale.

## Best practices
- **Pair every framework choice with two exit criteria** — one quantitative (metric + threshold) and one disqualifying (kill-criterion). Without exit criteria the framework is theatre.
- **Version the choice file in git, not Notion.** `framework-choice.md` belongs next to the spec; pivots show as commits.
- **Default to MVP only when market is genuinely uncontested.** If 3+ "good enough" competitors exist, the default flips to MLP or SLC; "we'll iterate to lovable later" rarely happens.
- **Pick exactly one framework per scope cycle.** "MVP+MLP hybrid" is a hedge; force a single choice and let the next cycle re-pick.
- **MFP is a stepping stone, not a destination.** Pre-commit to the trigger (e.g. "first internal demo passes") that ends MFP and enters MVP/MLP.
- **MMP / MVA need a sales letter before code.** Write the buyer's purchase-justification memo first; if it doesn't read as compelling, the framework is wrong.
- **Run a "framework retro" 30 days post-launch.** Did the chosen framework's exit criteria fire? Was the rejected alternative actually better in hindsight? Feed back into selection heuristics.
- **Keep MAC use rare.** A killer feature without a product is a demo, not a business; require explicit founder sign-off before picking MAC.
- **Score every framework, not just the winner.** Forces honest disagreement rationale; hides nothing in the prompt log.
- **In red oceans, lead with the differentiator type, not the framework.** "Lovable, marketable, or delightful" is the real choice; MLP/MMP/MDP are wrappers.

## AI-agent gotchas
- **Acronym hallucination.** LLMs invent extra frameworks (MUP, MEP, MWP) under prompt pressure. Constrain to the exact 9-row enum; reject any output naming a framework outside the list.
- **Default-to-MVP drift.** Any LLM trained on 2010s startup canon will pick MVP unless explicitly told to consider crowded-market evidence. Force the agent to print the matrix score per framework before naming the winner.
- **Crowded-market over-claim.** Without competitor evidence, agents will declare every market "crowded" to justify MLP. Require `competitor_count` + named competitors in `market-context.yml`; refuse to pick if missing.
- **Exit-criterion vagueness.** Agents emit "good user feedback" or "high adoption" as exit criteria. Validate that each criterion has a metric, a threshold, and a measurement window.
- **Framework-then-justify failure.** Agent picks first, rationalises second. Mitigate by structured output: scores per framework BEFORE the chosen one, in a JSON schema the prompt enforces.
- **Confounding with mvp-scoping methodology.** Agent jumps straight into in/out scope before picking the framework. Pipeline must enforce: choice file exists → only then scoping methodology runs.
- **Pivot inertia.** Agent re-confirms the original framework even when metrics scream pivot. Force a structured "stay vs pivot" decision with rejection-reason for the rejected option.
- **No human checkpoint on enterprise commitments.** MMP/MVA implies sales contracts and SLAs — agents must not autonomously promote to these without a founder/PM sign-off step.
- **Hand-off contract drift.** Downstream methodology agents read the choice file; if framework changes mid-cycle without re-running the downstream agent, scope and framework drift apart. CI: hash the choice file in the spec front-matter; mismatch fails the build.
- **2026-claim staleness.** README says "in 2026 MVP is suicide in crowded markets" — agents will quote this verbatim in pitches; phrase it as a heuristic, not a law, to avoid over-confident decks.

## Hand-off contracts (framework choice ↔ downstream)
| Artifact | Owner | Reader | Format | Cadence |
|----------|-------|--------|--------|---------|
| `market-context.yml` | market-researcher agent | PM agent | YAML in `.aidocs/product_docs/` | Per scope cycle |
| `framework-choice.md` | PM agent | mvp-scoping / mlp-planning / RAT agents | Markdown, dated history | Per scope cycle, append-only |
| Exit-criteria block (inside choice file) | PM | analytics agent | YAML inside markdown | Reviewed weekly |
| Re-pick decision | framework-pivot-detector | PM, founder | New section in choice file | Triggered by metric breach |
| Framework retro | PM | team | `.aidocs/product_docs/retros/<date>.md` | 30 days post-launch |

## References
- Eric Ries (2011). *The Lean Startup*. Crown Business. (MVP origin.)
- Frank Robinson — coined MVP (2001). https://www.syncdev.com/minimum-viable-product/
- Henrik Kniberg — "Spotify squad MVP / MLP cake metaphor". https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp
- Brian de Haaff (Aha!) — MLP advocacy. https://www.aha.io/blog/the-minimum-lovable-product
- David J. Bland — *Testing Business Ideas* (RAT, riskiest-assumption tests). Wiley, 2019.
- Marty Cagan — *Inspired* and *Empowered* (product-discovery alternatives to MVP). SVPG.
- Teresa Torres — *Continuous Discovery Habits*. (Sibling methodology in this folder.)
- Jason Cohen — "Simple, Lovable, Complete" essay. https://longform.asmartbear.com/slc/
- Sibling methodologies: `mvp-scoping`, `mlp-planning`, `riskiest-assumption-test`, `product-led-growth`, `release-planning` (all under `pro/product/product-manager/`).
