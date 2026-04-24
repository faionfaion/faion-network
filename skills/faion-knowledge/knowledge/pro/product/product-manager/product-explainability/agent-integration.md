# Agent Integration — Product Explainability (PM Angle)

PM-specific lens: this methodology is a **communication discipline**, not a marketing artifact. The PM owns the bridge between what engineering shipped and how non-technical stakeholders (executives, sales, support, customers, AI assistants) understand it. Explainability fails when the PM lets feature lists, demo videos, and release notes substitute for an articulated, repeatable story of *purpose → behavior → limit → impact*.

The product-operations variant (`pro/product/product-operations/product-explainability/agent-integration.md`) covers the public-surface KB pipeline (`llms.txt`, JSON-LD, AEO probes). This file focuses on the upstream PM work: how a PM extracts, structures, and tells the product story to humans who don't read code.

## When to use
- Pre-roadmap-review: an exec asks "what does this product actually do?" and three PMs answer with three different framings — you need a single canonical explanation.
- Pre-launch story prep: enabling sales, support, customer success, and partner teams who must explain the feature without watching a Loom.
- Board / investor / all-hands narrative: distilling six months of work into a 90-second answer to "what shipped, what changed for users, what's next".
- Cross-team feature-to-impact mapping: every release should answer "which OKR / customer outcome moved, by how much, because of which capability".
- Post-mortem on miscommunication: customer expected X, got Y, churned — gap is in the story, not the product.
- Onboarding a new PM, designer, or engineer: the explainability artifact is the fastest path to shared mental model.
- Quarterly product review: forcing yourself to re-articulate purpose surfaces drift you can't see day-to-day.

## When NOT to use
- Inside the engineering loop: explainability framing slows iteration on technical specs; use ADRs and design docs there.
- For experiment-stage features behind a flag with <5% rollout — premature explainability hardens hypotheses you should still be testing.
- When the org already has rigorous PMM (product marketing) ownership and the PM is duplicating that artifact — collaborate, do not re-author.
- For deeply technical APIs whose only audience is engineers with the OpenAPI spec; story prose adds noise.
- Weekly tactical standups — it's a strategy and stakeholder artifact, not a status update.

## Where it fails / limitations
- **Feature-list trap.** PMs default to listing what shipped instead of explaining what changed for the user; stakeholders nod, retain nothing, mis-sell.
- **Translation collapse.** PM speaks PM-ese; sales translates to sales-ese; CS translates again to customer-ese. Each translation drops a limit or invents a capability.
- **Outcome-washing.** "We shipped X, NPS went from 42 to 44" — correlation passed off as causation, no isolation, no instrumentation. Stakeholders learn to distrust PM data.
- **Hero-narrative bias.** PM owns the story so the PM looks good in it; engineering and design contributions disappear, internal trust erodes.
- **Stale story.** The story is written at launch and never updated; six months later capabilities have changed but the deck hasn't, sales is selling vapor.
- **Audience collapse.** One artifact tries to serve exec, sales, support, customer, regulator at once; ends up serving none well.
- **Limit-omission.** Limits are perceived as "negative" and edited out before they reach sales; sales over-promises; CS absorbs the gap.
- **AI-readability blindness.** PMs write for humans only; the same LLM that just answered a customer's pre-sales question now misrepresents the product. PM owns this and most PMs don't realize it yet (2026 reality).
- **Storytelling vs. specification confusion.** PMs hide ambiguity behind narrative ("delights users", "boosts productivity"); engineers re-derive specs from the story and ship the wrong thing.

## Agentic workflow
Drive PM-side explainability as a three-loop pipeline that turns engineering output into stakeholder-ready narratives. (1) **Extract loop** — a story-extractor agent reads PRDs, design docs, release notes, telemetry deltas, and user-research clips and emits a structured `feature-narrative.json` per release: `purpose`, `behavior_change`, `before/after_user_journey`, `measurable_outcome`, `limit`, `affected_personas`. (2) **Translate loop** — a render agent produces audience-specific renders from one source: exec memo (≤200 words, outcome + cost + risk), sales one-pager (job, pain, capability, limit, objection-handling), support runbook (symptoms → cause → fix → known-limit), customer changelog entry (plain-language, ≤80 words), AI-mediated KB delta (capability + status + since_version, feeds the operations-side `product-kb.json`). (3) **Validate loop** — a comprehension probe agent runs the renders past simulated stakeholder personas (exec, AE, CSM, churned-user, AI assistant) and scores recall + accuracy + limit-acknowledgment; failures route back to the PM. Run extract+translate on every feature flag flip from internal-only to GA; run validate weekly. Persist `feature-narrative.json` alongside the SDD feature folder so it travels with the spec, never as a separate marketing artifact.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — emits structured spec / design / test-plan; the story-extractor reads these as primary sources, enforcing that the narrative cannot diverge from what was built.
- `faion-research-agent` (`pro/research/researcher/`) — supplies persona vocabulary and runs the comprehension probe loop with stakeholder personas.
- `faion-business-analyst` (`pro/ba/ba-core/`, `pro/ba/ba-modeling/`) — converts behavior-change deltas into BPMN / journey diagrams that stakeholders read faster than prose.
- `faion-marketing-manager` methodologies (`free/marketing/marketing-manager/`) — owns the public-facing render; PM hands off `feature-narrative.json`, marketing produces site copy without re-interviewing engineers.
- `faion-communicator` (`solo/comms/communicator/`) — tightens the exec memo and customer changelog to active voice, no adjectives, no superlatives.
- `faion-stakeholder-management` methodology (sibling under product-manager) — defines audience matrix; story-extractor consumes this to know which renders are required.
- A purpose-built **stakeholder-comprehension probe agent** (worth creating): given the rendered artifact and a persona prompt, asks 5 canonical questions ("what changed?", "what does it cost me?", "what won't it do?", "who benefits?", "what's next?"), scores answers against the source narrative.

### Prompt pattern
Story extraction:
```
You extract a stakeholder-ready feature narrative. Inputs: <PRD path>,
<release notes>, <telemetry diff>, <user-research clips>. Output JSON:
purpose (one sentence, no marketing adjectives, names the user job),
behavior_change (before -> after, observable in product),
measurable_outcome (metric, baseline, current, isolation_method),
limit (what it intentionally does NOT do, why),
affected_personas[] (each: name, job, value_received),
risks[]. Refuse to invent outcomes; if a metric is unverified write
"unverified" — never optimistic-extrapolate.
```

Audience render:
```
Render the feature-narrative for audience=<exec|sales|support|customer|ai>.
Constraints by audience:
- exec: <=200 words, lead with outcome and cost, single risk, no jargon.
- sales: job + pain + capability + limit + 2 objection-handlers; cite source line.
- support: symptom -> cause -> fix -> known-limit; runbook tone.
- customer: <=80 words, plain language, second-person, link to docs.
- ai: capability+status+since_version+limit triples, JSON, feeds product-kb.
Forbidden tokens across all renders: "best", "leading", "revolutionary",
"seamless", "powerful", "next-gen", "delight". Lint output, regenerate on hit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Anthropic CLI) | Headless story-extract + render passes against a PRD | https://docs.anthropic.com |
| `gh` CLI | Pull PR descriptions, release notes, linked issues for the extractor | https://cli.github.com |
| `pandoc` | Convert `feature-narrative.json` → exec memo (docx/pdf), customer changelog (md/html) | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render before/after journey diagrams from JSON for non-technical readers | `npm i -g @mermaid-js/mermaid-cli` |
| `quarto` | Single-source narrative → multiple stakeholder formats (slide, memo, web) | https://quarto.org |
| `jq` + `ajv-cli` | Lint `feature-narrative.json` against schema; block release if missing limit/outcome | `npm i -g ajv-cli` |
| `vale` | Style-lint renders; ban marketing adjectives via custom vocabulary | https://vale.sh |
| `loom` / `tella` CLI hooks | Auto-attach demo videos to extracted narrative; agent transcribes for accessibility | https://loom.com/ |
| Notion / Linear / Productboard CLIs | Push renders back into stakeholder tools where they actually live | vendor docs |
| `whisper.cpp` / `assemblyai` | Transcribe user-research clips → narrative inputs | https://github.com/ggerganov/whisper.cpp |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Productboard | SaaS PM platform | API yes | Native "feature → outcome → release" mapping; export to JSON, feed extractor. |
| Linear / Jira | Issue tracker | API yes | PRD + acceptance criteria source; renders attach back to issues for traceability. |
| Notion / Coda | KB / docs | API yes | Common home for PM narratives; push generated renders here as canonical. |
| Loom / Tella / Descript | Async video | API limited | Demo videos = supplementary, never the canonical narrative; transcribe to text. |
| Pendo / Userpilot / Appcues | In-product guidance | API yes | Customer-facing render lands here as tooltip / changelog modal. |
| Intercom / Zendesk / Front | Support tooling | API yes | Support runbook render imports here; tag with feature-id for closed-loop. |
| Gong / Chorus | Sales call analytics | API yes | Detect sales mis-statements vs. narrative; flag drift. |
| Sales enablement (Highspot, Seismic) | SaaS | API yes | Sales one-pager render lives here; expiration date matches `since_version`. |
| Slack / MS Teams | Distribution | API yes | Exec-memo render auto-posts to leadership channel on GA flip. |
| ChatGPT / Claude / Perplexity | AI surfaces | API yes | Customer-facing AI; the operations-side KB is the same narrative, structured. |
| Mintlify / GitBook | Docs | API yes | Customer changelog render publishes here with `lastmod`. |
| Figma | Design source | API yes | Pull before/after frames into the narrative as visual evidence. |

## Templates & scripts
The methodology files (`README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`) are nearly empty. The PM-side gap: no canonical narrative shape. Inline drop-in (≤50 lines) — JSON Schema for `feature-narrative.json` plus a release-gate validator:

```bash
#!/usr/bin/env bash
# feature-narrative-gate.sh — block release if narrative missing limit/outcome.
# Usage: feature-narrative-gate.sh path/to/feature-narrative.json
set -euo pipefail
fn="${1:?usage: feature-narrative-gate.sh NARRATIVE.json}"
schema="$(dirname "$0")/feature-narrative.schema.json"
cat > "$schema" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["purpose","behavior_change","measurable_outcome","limit","affected_personas"],
  "properties": {
    "purpose":{"type":"string","minLength":20,"maxLength":200},
    "behavior_change":{"type":"object",
      "required":["before","after"],
      "properties":{"before":{"type":"string"},"after":{"type":"string"}}},
    "measurable_outcome":{"type":"object",
      "required":["metric","baseline","current","isolation_method"],
      "properties":{"metric":{"type":"string"},"baseline":{"type":"string"},
                    "current":{"type":"string"},
                    "isolation_method":{"enum":["a/b","holdout","pre/post","unverified"]}}},
    "limit":{"type":"string","minLength":15},
    "affected_personas":{"type":"array","minItems":1,"items":{
      "type":"object","required":["name","job","value_received"]}},
    "risks":{"type":"array"}
  }
}
JSON
ajv validate -s "$schema" -d "$fn" --strict=true
banned='best|leading|revolutionary|seamless|powerful|next-gen|delight'
if grep -E -i "\"($banned)\"" "$fn" >/dev/null; then
  echo "FAIL: marketing adjective leaked into narrative"; exit 1
fi
```

Wire this into the SDD release pipeline: a feature cannot move from `in-progress/` to `done/` without a passing narrative.

## Best practices
- **One source, many renders.** `feature-narrative.json` is canonical; exec memo, sales one-pager, support runbook, customer changelog, AI-KB delta are all generated. Hand-edits forbidden — they drift instantly.
- **Limit before benefit.** State what the feature does NOT do before what it does. Sales then can't accidentally over-sell because the limit is upstream of the pitch.
- **Outcome with isolation method.** Never report a metric move without the isolation method (`a/b`, `holdout`, `pre/post`, or honest `unverified`). Otherwise stakeholders discount all PM data.
- **Plain language, no adjectives.** Strip "best", "leading", "powerful", "seamless". Lint with `vale`. Stakeholders ignore adjectives; LLMs amplify them as marketing-tone signals.
- **Persona-anchored.** Every narrative names the persona, the job, and the value received. "Improves productivity" is not a value statement; "lets a CSM resolve a ticket without leaving Zendesk" is.
- **Before/after observable in product.** A PM should be able to demo the behavior change in <60s. If not, the story is too abstract.
- **Co-locate with spec.** `feature-narrative.json` lives in `.aidocs/.../in-progress/<feature>/feature-narrative.json` next to spec/design/test-plan. Story is part of the feature, not an afterthought.
- **Refresh on every status flip.** GA, deprecation, scope change → narrative re-extracted, renders regenerated, stakeholders re-notified.
- **Story is testable.** Comprehension probe with 5 canonical questions; ≥80% recall+accuracy across 5 personas before launch.
- **Author with engineering, not after.** PM drafts narrative during design phase; engineering reviews for accuracy of `behavior_change`. Catches scope drift early and prevents post-hoc invention.
- **Audit sales calls and support tickets.** Drift between narrative and field reality is the leading indicator of stakeholder-comprehension decay. Use Gong/Chorus + ticket sampling, weekly.

## AI-agent gotchas
- **Outcome inflation.** Render agents will round 2.1% to "double-digit improvement" or extrapolate one cohort to "all users". Hard rule: render agent must echo `measurable_outcome.metric` + `baseline` + `current` verbatim; no rephrasing of numbers.
- **Limit erosion across renders.** Translate-loop summarizes, summarization drops limits. Pass limits as a separate, verbatim, never-summarized field; lint each render to confirm the limit string is present.
- **Persona invention.** Extractor agents will invent personas to fill `affected_personas[]` when input is sparse. Anchor allowed personas to a registry (`personas.json`) and reject others.
- **Marketing-tone leakage.** Even with banned-tokens lists, LLMs route around (`top-tier`, `category-defining`). Maintain an evolving banned-token list; periodically have a second LLM lint for marketing tone.
- **Hero narrative bias.** Generator favors PM-as-protagonist framing. Force credit lines: "Designed by <name>, engineered by <team>"; remove first-person voice from exec memo.
- **Stale narrative re-publish.** Cron-driven render re-runs without an extract refresh produce confidently-wrong artifacts after capability changes. Always re-extract before re-rendering; never cache the narrative without a content hash check against PRD + telemetry.
- **Comprehension-probe gaming.** Probe agent and render agent share weights → probe scores artificially high. Use a different model family for probe vs. render (e.g. render with Claude, probe with GPT-4 or Gemini).
- **Confidentiality leak.** Narratives often expose unlaunched features, customer names, internal infra. Run `password-scrubber-agent` before any render leaves engineering's repo.
- **AI-readability skipped.** PM treats AI render as a marketing concern. Wrong: the AI render feeds the operations-side KB and the next pre-sales conversation. Make the AI render mandatory, not optional.
- **Cross-locale drift.** Translation agents helpfully soften limits ("doesn't support" → "is best for"). Localize structurally with per-locale render passes; never machine-translate limits.
- **Silent disagreement between extractor and engineering.** If extractor reads PRD only and never reads the implementation diff, narrative drifts from reality. Extractor must consume both PRD and recent commits; flag mismatches as agent-blocking.
- **Stakeholder feedback never closes the loop.** Renders ship one-way; comprehension failures don't update the narrative. Feed sales objections, support tickets, and AI-mis-answers back into the extractor as ground-truth signals; otherwise quality plateaus.

## References
- Roman Pichler, "Strategize: Product Strategy and Product Roadmap Practices for the Digital Age" — narrative-driven roadmaps.
- Teresa Torres, "Continuous Discovery Habits" — opportunity-solution trees as narrative scaffolding.
- Ryan Singer, "Shape Up" (Basecamp) — appetite + boundaries as a built-in story.
- Marty Cagan, "Inspired" / "Empowered" — narrative ownership inside product teams.
- Nancy Duarte, "Resonate" — story patterns for executive narrative.
- Chip & Dan Heath, "Made to Stick" — SUCCES framework, applies directly to feature narratives.
- Productboard, "Feature → Outcome → Release" reference — https://www.productboard.com/glossary/
- Reforge, "Communicating product strategy" — https://www.reforge.com/artifacts
- Lenny's Newsletter, "How great PMs communicate" — https://www.lennysnewsletter.com
- llms.txt proposal (for the AI render bridge to operations) — https://llmstxt.org/
- Sibling: `pro/product/product-operations/product-explainability/agent-integration.md` — public-surface KB pipeline.
- Sibling: `pro/product/product-manager/stakeholder-management/agent-integration.md` — audience matrix that drives render selection.
- Sibling: `solo/comms/communicator/` — render-tightening methodologies.
