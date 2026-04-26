# Agent Integration — Use Case Modeling

## When to use

- Functional requirements need to be expressed as actor-system interactions before development starts (typical for transactional systems, line-of-business apps, regulated software).
- Test engineers need a deterministic, scenario-based source for end-to-end test design (each main/alternative/exception flow becomes a test path).
- A SaaS product has multiple actor types (customer, admin, billing, external API) and the team keeps shipping features that work for one role and break another — explicit actor-use-case mapping prevents that.
- Compliance / audit context (FDA 21 CFR Part 11, ISO 13485, SOX) where requirements traceability from actor goal → flow step → code → test must be defensible.
- Migrating a legacy system: reverse-engineering existing screens into use cases is a controlled way to converge on a complete spec without copy-pasting the old UI.
- Pre-development alignment when stakeholders speak in features ("export button") and developers need flows ("Generate Report → AF-1 large dataset → EX-1 export timeout").

## When NOT to use

- Pure exploratory / discovery phase — Opportunity Solution Trees and Jobs-to-be-Done give better signal than premature use case formalization.
- Highly emergent agile teams already operating well with user stories + acceptance criteria — adding UC specs duplicates work without traceability gain.
- Pure data / analytics platforms where the primary "interaction" is a query language; data flow / lineage models fit better than UC.
- ML/LLM-backed features where behavior is probabilistic — use cases assume deterministic system responses and break when the response is "best effort".
- Tiny CRUD apps with one actor and <10 screens — a one-page acceptance criteria sheet is faster and equally complete.
- Realtime / event-driven systems where the interesting structure is event topology, not actor goals; event storming or BPMN serves better.

## Where it fails / limitations

- Use case bloat: teams generate UC-001..UC-200 documents that nobody re-reads. Useful UCs cap at ~30 per release; beyond that, hierarchy collapses.
- LLMs over-include UI details ("user clicks blue button") which couple the spec to a specific design — agent prompts must explicitly forbid UI verbs and require system-behavior verbs.
- `<<include>>` and `<<extend>>` are misused ~80% of the time in human-authored UCs; LLMs amplify the confusion. Prefer flat UCs unless the include/extend genuinely de-duplicates 10+ steps.
- Step granularity drift: same diagram has 3-step UCs and 25-step UCs because authors lack a uniform rule. Without a fixed step-counting heuristic, LLM output is even more uneven.
- Exception flows are the highest-value section and the one humans skip; LLMs default to "Happy path looks great, please review" unless explicitly forced to enumerate failure modes.
- Use cases assume a closed system boundary. Microservices / mesh architectures with shifting boundaries make "the system" ambiguous and UCs misleading.

## Agentic workflow

Drive use case modeling as a four-stage pipeline (extract actors → enumerate goals → draft specs → validate completeness), each stage a discrete subagent invocation with structured I/O. Use Haiku for template-filling stages (actor extraction, main-flow drafting), Sonnet for review/validation/exception generation, Opus only for cross-UC relationship modeling (`<<include>>`, generalization). Persist artifacts as markdown UC specs under `.aidocs/<feature>/use-cases/UC-NNN-<slug>.md` with YAML front-matter for indexing, and emit a `use-case-index.md` at the feature level. The BA / PM stays human-in-the-loop on actor identification (cheapest place to fix mistakes) and on relationship modeling (highest cost of getting wrong).

### Recommended subagents

- `faion-sdd-executor-agent` — once UC specs stabilize, hand off as input to spec/design generation in `.aidocs/backlog/<feature>/`. UC-NNN IDs become traceability anchors in spec.md and test-plan.md.
- Custom `actor-extractor-agent` (Haiku) — input: project brief / existing screens / API surface. Output: JSON list of actors with type (primary/secondary/system) and one-line goal each.
- Custom `uc-drafter-agent` (Haiku) — input: one actor + one goal + system context. Output: UC spec markdown filling the template (`README.md` template). Forbid UI verbs in system prompt.
- Custom `uc-reviewer-agent` (Sonnet) — input: a draft UC. Output: gap report keyed to the 9-item quality checklist in `README.md`. Required to flag missing exception flows (default failure case in human-authored UCs).
- Custom `uc-relationship-agent` (Opus) — input: full UC set. Output: include / extend / generalization graph with rationale per edge. Run last; do not let drafter or reviewer invent relationships.
- `faion-brainstorm` skill — for the actor-discovery diverge step when the project brief is vague ("who else might use this?").

### Prompt pattern

```
You are a use case drafter. Output ONE use case spec following this exact template
(see knowledge/pro/ba/ba-modeling/use-case-modeling/README.md for the template).

HARD RULES:
- Verb+Noun name. No UI nouns ("button", "screen", "modal").
- System Response column = system behavior, never UI rendering.
- Main flow: 5-9 steps. If >9, split the UC.
- MUST include >=1 alternative flow and >=1 exception flow. If you cannot
  invent a plausible exception, output {"error": "actor or goal too thin"}.
- Postconditions must be observable (DB state, message sent, file written).

INPUT:
  actor: {actor_name, type}
  goal: {one-sentence goal}
  system_context: {short paragraph}
  business_rules: [list]

OUTPUT: markdown UC spec, no prose before/after.
```

```
You are a use case reviewer. Input: one UC spec markdown. Score against the 9-item
quality checklist in README.md. Output JSON:
{"uc_id": "...", "score_0_9": N, "missing": ["exceptions","postconditions",...],
 "ui_leak": [step_numbers...], "step_count": N, "recommend": "ship|revise|split"}
Mark recommend="split" if step_count>9 or if >1 actor goal is bundled in main flow.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `plantuml` | Render `@startuml ... @enduml` UC diagrams to SVG/PNG from CLI | apt/brew `plantuml`; plantuml.com |
| `mermaid-cli` (`@mermaid-js/mermaid-cli`) | Render Mermaid `flowchart`/`sequenceDiagram` for UC flows in markdown CI | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert UC markdown specs to docx/pdf for stakeholder review packs | pandoc.org |
| `gherkin` / `cucumber` | Translate UC main+alt+exception flows into executable feature files | `npm i -g @cucumber/cucumber` |
| `gh` | Track UCs as issues with `uc-NNN` labels; link spec.md ↔ implementation PR | preinstalled |
| `jq` | Validate JSON schema of agent UC output (front-matter index, reviewer reports) | apt/brew |
| `yq` | Extract YAML front-matter from UC markdown for index generation | github.com/mikefarah/yq |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| draw.io / diagrams.net | OSS, SaaS, desktop | Partial (XML files) | UC diagrams as `.drawio` XML; agents can patch shapes but rendering needs UI or `drawio-export`. |
| PlantUML server | OSS, SaaS endpoint | Excellent (text-in, image-out HTTP API) | Best agent target: emit `@startuml` text, GET render URL. Self-hostable on faion-net. |
| Mermaid (mermaid.live) | OSS embed | Excellent (markdown-native) | Native render in GitHub/GitLab markdown; agents emit Mermaid in UC spec body. |
| Visual Paradigm | SaaS / desktop | Limited (proprietary `.vpp`) | Strong UC editor; weak API. Use only if team standardized on it. |
| Lucidchart | SaaS | Limited (REST API on Enterprise tier) | Good collaboration; locking down agent automation costs >$200/mo. |
| Modelio | OSS | Limited (Java GUI, no API) | Full UML; not agent-friendly. |
| Cucumber Studio (HipTest) | SaaS | Yes (REST API) | UC → BDD scenarios; useful when QA owns the artifact. |
| ReqView | Desktop | Limited (ReqIF export) | Strong if compliance demands ReqIF/DOORS interop. |
| IBM DOORS / DOORS Next | SaaS / on-prem | Limited (OSLC API, complex) | Only justified for regulated industries (medical, aerospace). |
| Notion / Confluence | SaaS | Yes (REST API) | Cheap UC store for <50 UCs; outgrows when traceability matters. |
| Linear / Jira | SaaS | Excellent (GraphQL/REST) | UC IDs as custom field on epics/stories; preferred backlog destination, not UC store. |
| Astah UML | Desktop | Limited (XMI export) | Educational pricing; agents can read XMI but not edit live. |

## Templates & scripts

The repo's `templates.md` for this methodology is currently empty; the UC spec and UC diagram templates live inline in `README.md` (sections "Use Case Specification Template" and "Use Case Diagram Template"). Agents should read those directly.

Inline UC index generator (≤50 lines, Bash + yq + jq). Walks `.aidocs/<feature>/use-cases/UC-*.md`, extracts YAML front-matter, emits a `use-case-index.md` and a JSON sidecar agents can consume.

```bash
#!/usr/bin/env bash
# uc-index.sh — build use-case-index.md from UC-NNN-*.md front-matter.
# Usage: ./uc-index.sh path/to/use-cases/
set -euo pipefail
DIR="${1:?usage: $0 <use-cases-dir>}"
cd "$DIR"

OUT_MD="use-case-index.md"
OUT_JSON="use-case-index.json"

{
  echo "# Use Case Index"
  echo
  echo "| ID | Name | Primary Actor | Status | Step Count |"
  echo "|----|------|---------------|--------|------------|"
} > "$OUT_MD"

echo "[]" > "$OUT_JSON"

for f in UC-*.md; do
  [ -f "$f" ] || continue
  fm=$(yq -f extract '.' "$f" 2>/dev/null || true)
  id=$(echo "$fm"      | yq '.id // ""')
  name=$(echo "$fm"    | yq '.name // ""')
  actor=$(echo "$fm"   | yq '.primary_actor // ""')
  status=$(echo "$fm"  | yq '.status // "draft"')
  steps=$(grep -cE '^\| [0-9]+ \|' "$f" || true)
  echo "| $id | $name | $actor | $status | $steps |" >> "$OUT_MD"
  jq --arg i "$id" --arg n "$name" --arg a "$actor" --arg s "$status" --argjson c "$steps" \
    '. + [{id:$i, name:$n, actor:$a, status:$s, steps:$c}]' \
    "$OUT_JSON" > "$OUT_JSON.tmp" && mv "$OUT_JSON.tmp" "$OUT_JSON"
done

echo "wrote $OUT_MD and $OUT_JSON ($(jq length "$OUT_JSON") use cases)"
```

## Best practices

- Pin the system boundary in the system prompt before every drafting call. "The System" must resolve to a concrete service / app / API surface, not a vague "the platform".
- Cap main flow at 5-9 steps. Fewer than 5 → likely a system function, not a UC. More than 9 → split or delegate via `<<include>>`.
- Forbid UI nouns in System Response column ("renders modal", "shows blue button"). Replace with system-behavior verbs ("validates", "persists", "emits event"). Enforce in the LLM prompt as a hard rule.
- Always require at least one alternative flow and one exception flow before accepting a UC as "complete". Agents skip these by default.
- Use the same step-counting heuristic across all UCs (one actor action + one system response = one step). Without it, comparison and traceability collapse.
- Store UCs as markdown with YAML front-matter (`id`, `name`, `primary_actor`, `status`, `version`). The front-matter feeds index/traceability scripts and CI checks.
- Treat the UC index as the source of truth for test scaffolding: each UC main flow → 1 happy-path test, each AF/EX → 1 negative-path test. Generate test stubs from the index.
- Validate UC names with a regex (`^[A-Z][a-z]+ [A-Z][a-z]+`) — verb + noun only. CI fails the PR if a UC violates the convention.
- Re-run the reviewer agent on the full UC set whenever a new UC lands; relationship inference (`<<include>>`) is fragile and needs the global view.
- Keep UI mockups out of UC files. Link from front-matter (`mockup_url:`) instead. The UC outlives the design system; the design system does not outlive the UC.

## AI-agent gotchas

- LLMs default to writing the happy path and stopping. Always force ≥1 alternative + ≥1 exception flow in the schema; reject outputs that omit them.
- Drafter agents invent UI details ("displays popup confirmation") even when told not to. Add a post-generation regex check (`button|modal|popup|screen|click`) and bounce drafts that match.
- Step granularity drifts across calls. Pin the heuristic in the system prompt ("one step = one actor action + one system response") AND validate step count post-hoc.
- Relationship inference (`<<include>>`, `<<extend>>`, generalization) is the highest-error part. Run only Opus, only after all UCs are drafted, and require rationale per edge.
- LLMs hallucinate actors that are really UI elements ("Header", "Sidebar"). Force actor `type ∈ {human, system, time}` in the JSON schema; reject anything else.
- Long context tempts "draft 30 UCs in one call" — accuracy collapses past ~5 UCs per call due to template repetition errors. Chunk one UC per call.
- Agents conflate primary and secondary actors. Make `actor_type` required and validate that exactly one primary actor is set per UC.
- Reviewer agents grade their own drafts too generously. Use a different model family (or at minimum a different system prompt with adversarial framing) for review than for drafting.
- "Generate test cases from this UC" produces redundant tests when `<<include>>` is used. Resolve includes inline before test generation, or de-duplicate by step ID.
- Pre-commit hook in this repo blocks commits without a CHANGELOG entry. Agents producing UC specs that touch CHANGELOG must follow the `## [Unreleased]` convention.

## References

- BABOK v3, "Requirements Analysis and Design Definition" → "Specify and Model Requirements" → Use Cases technique.
- Alistair Cockburn, *Writing Effective Use Cases* (2000) — canonical structure (goal levels: cloud, kite, sea, fish, clam).
- Ivar Jacobson et al., *Use-Case 2.0* (2011) — slim use cases for agile teams.
- OMG UML 2.5.1 — Use Case Diagrams notation reference (omg.org/spec/UML).
- Karl Wiegers, *Software Requirements* 3rd ed. — UC vs. user story trade-offs.
- PlantUML use case syntax — plantuml.com/use-case-diagram.
- Mermaid use-case via flowchart workaround — mermaid.js.org (no native UC; use `flowchart LR`).
- Anthropic, *Building effective agents* (2024) — chained vs. orchestrated agents pattern (drafter → reviewer → relationship modeler).
- Faion Network — sibling methodology `user-story-mapping/README.md` for hand-off after UC modeling.
