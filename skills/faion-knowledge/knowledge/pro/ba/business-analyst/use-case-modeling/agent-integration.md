# Agent Integration — Use Case Modeling (Business Analyst)

This page covers use case modeling from the **enterprise BA** angle — UML
use-case diagrams as a contractual deliverable, RUP / use-case-driven BA work,
vendor selection, RFP/RFI input, and regulated-industry traceability. For the
adjacent design-modeling angle (drafter → reviewer pipeline focused on `.aidocs`
spec generation) see
`../../ba-modeling/use-case-modeling/agent-integration.md`.

## When to use

- Enterprise kickoff where the BA must deliver a UML use-case diagram + UC specs as SoW deliverables (SAP/Salesforce/Dynamics rollouts, banking core upgrades, insurance claims platforms).
- RFP / RFI authoring — UC catalog is the apples-to-apples grid every vendor maps their product onto.
- RUP-style use-case-driven projects (still alive in regulated / government / telco) where iterations are scoped "implement UC-101..UC-110".
- Regulated industries (21 CFR Part 11, ISO 13485, IEC 62304, SOX, GxP, EU MDR): UCs anchor traceability actor goal → step → commit → test → audit evidence.
- Legacy migration (mainframe, Oracle Forms, Lotus Notes) — reverse-engineering screens into UCs is the safe path to a greenfield re-implementation spec.
- Outsourced delivery where the BA is the contractual interface; step-level UC specs replace ambient context the offshore team lacks.
- Stakeholder alignment workshops where executives speak outcomes ("approve loan") and engineers speak features ("decision rule engine"); UCs anchor at actor-goal level.

## When NOT to use

- Lean / startup contexts — JTBD, Opportunity Solution Trees, or story mapping deliver faster discovery without the SoW obligation to produce UML.
- Data / analytics platforms whose value is queries and dashboards; DFDs, dimensional models, lineage diagrams beat UCs.
- Internal tools with a single actor and <10 transactions — a one-page acceptance-criteria sheet is enough.
- ML / LLM-backed surfaces with probabilistic responses; UC main flows assume deterministic system responses and mislead.
- Event-sourced / reactive architectures — event storming or async message catalogs better expose the meaningful structure.
- Teams already running smoothly on user stories + acceptance criteria; layering UCs duplicates work with no traceability gain.

## Where it fails / limitations

- UML UC diagrams **cannot** show sequencing, timing, or data flow. BAs who encode "first A, then B" in arrows mislead developers — use activity / sequence / BPMN.
- `<<include>>` / `<<extend>>` are misused ~80% of the time in enterprise UCs; `<<extend>>` directionality (extension points to base UC) is consistently inverted. LLMs amplify the confusion.
- "Actor = role, not person" gets broken constantly — senior managers want their job title on the diagram. Without push-back the diagram becomes an org chart.
- UC bloat: enterprise programs spawn UC-001..UC-400 docs nobody re-reads. Useful UC count caps near ~30 per release; beyond that, hierarchy collapses.
- Step granularity drifts wildly across BAs and LLM calls (3-step vs. 25-step UCs in the same diagram). Without a fixed step-counting rule, estimation and test scaffolding break.
- Microservices / mesh architectures shift the system boundary; UCs assume a closed boundary and mislead when "the system" spans 12 services with their own SLAs.
- Agile sprints outdate UC specs from the first review. UC-driven BAs must budget for re-baselining, not spec freeze.

## Agentic workflow

Drive enterprise UC modeling as a four-stage chain (stakeholder mining →
actor + goal extraction → UC drafting → diagram + traceability rendering),
each stage a discrete subagent invocation with structured I/O. The BA stays
human-in-the-loop on actor identification (cheapest fix point) and on
include / extend / generalization (highest cost when wrong). Use Haiku for
extraction and template-filling, Sonnet for review, exception-flow generation,
and stakeholder paraphrasing, Opus only for cross-UC relationship modeling
and for distilling RFP-grade narrative from the UC catalog. Persist artifacts
under `.aidocs/<feature>/use-cases/UC-NNN-<slug>.md` with YAML front-matter
plus a `use-case-index.md` and a PlantUML `.puml` file rendered in CI to SVG
for the steering committee deck.

### Recommended subagents

- `faion-sdd-executor-agent` — once the UC catalog is locked, hand off as
  input for `.aidocs/backlog/<feature>/spec.md` and `test-plan.md`. UC-NNN IDs
  become traceability anchors and CI-checkable references.
- `faion-brainstorm` skill — drives the actor-discovery diverge step when the
  client brief is vague (use the diverge → converge → review template; cap at
  3 rounds before forcing a decision).
- Custom `actor-extractor-agent` (Haiku) — input: SoW + interview transcripts
  + screenshots of the legacy system. Output: JSON list of `{name, type ∈
  {human, system, time}, goal_one_line, source_quote}`. Source quotes prevent
  hallucinated actors.
- Custom `uc-drafter-agent` (Haiku) — input: one actor, one goal, system
  context, business rules. Output: a single UC spec (markdown) following the
  template in this methodology's `README.md`. Forbid UI nouns in the prompt.
- Custom `uc-reviewer-agent` (Sonnet, adversarial framing) — input: a draft UC.
  Output: gap report scored against the 9-item quality checklist in `README.md`.
  Required to flag missing exception flows (the failure case humans skip most).
- Custom `uc-relationship-agent` (Opus) — input: full UC set. Output: include /
  extend / generalization graph with a one-line rationale per edge and a
  PlantUML rendering. Run last; do not let drafter or reviewer invent
  relationships.
- Custom `rfp-narrator-agent` (Opus) — input: UC catalog + actor list +
  business rules. Output: RFP / RFI narrative section grouping UCs by
  capability area, ready for vendor evaluation matrices.

### Prompt pattern

```
You are an enterprise BA producing UML-grade use cases for {client}, sector
{sector}, regulated under {regulation}. Output ONE use case spec per call,
following the template in
knowledge/pro/ba/business-analyst/use-case-modeling/README.md.

HARD RULES (reject if violated):
- Verb+Noun name. No UI nouns ("button", "screen", "modal", "popup").
- Actor.type in {human, system, time}; reject job titles as actors.
- System Response column = system behavior verbs (validates, persists, emits),
  never UI rendering.
- Main flow 5-9 steps. >9 → output {"error":"split_uc"}.
- >=1 alternative flow AND >=1 exception flow. If the goal is too thin to
  yield an exception, output {"error":"goal_too_thin"}.
- Postconditions must be observable (DB row, message, file, audit log).
- Cite the source artifact (interview line, SoW section, screenshot id) in
  the UC's "Source" front-matter field.

INPUT JSON:
  {actor:{name,type,goal}, system_context, business_rules:[...],
   sources:[{type,ref}], regulation_anchors:[...]}

OUTPUT: pure markdown, no prose framing.
```

```
You are a UC reviewer with adversarial framing. Score the input UC spec
against the 9-item checklist in README.md. Output JSON:
  {"uc_id":"...","score_0_9":N,"missing":[...],"ui_leak":[step_numbers...],
   "actor_leak":[role_phrases...],"step_count":N,
   "regulation_gaps":[...],"recommend":"ship|revise|split"}
recommend="split" if step_count>9 OR >1 actor goal is bundled in main flow.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `plantuml` | Render `@startuml ... @enduml` UC diagrams to SVG/PNG/PDF from CLI | apt/brew `plantuml`; plantuml.com/use-case-diagram |
| `mermaid-cli` (`mmdc`) | Render Mermaid use-case-as-flowchart in markdown CI | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert UC markdown specs to docx / PDF / ReqIF for deliverable packs | pandoc.org |
| `staruml-cli` | Headless export of StarUML `.mdj` to image / XMI for CI | staruml.io |
| `gherkin` / `cucumber` | Translate UC main + alt + exception flows into BDD `.feature` files | `npm i -g @cucumber/cucumber` |
| `gh` | Track UCs as labeled issues / project board cards (`uc-NNN`) | preinstalled |
| `jq` / `yq` | Validate JSON schemas of agent UC output and parse YAML front-matter | apt/brew |
| `reqif-tools` | Convert UC catalog ↔ ReqIF for DOORS / Polarion / ReqView | github.com/eclipse-rmf |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PlantUML server | OSS, SaaS endpoint | Excellent (text-in, image-out HTTP) | Best agent target. Self-hostable; emit `@startuml` text and GET render URL. |
| Mermaid (mermaid.live) | OSS embed | Excellent (markdown-native) | No native UC notation — agents emit `flowchart LR` workaround inside UC body. |
| draw.io / diagrams.net | OSS / SaaS / desktop | Partial (XML files) | UC diagrams as `.drawio` XML; agents can patch shapes, render needs `drawio-export`. |
| Visual Paradigm | SaaS / desktop | Limited (proprietary `.vpp`) | Strong UC editor; weak API. Use only if team standardized on it. |
| StarUML | Desktop | Partial (`.mdj` JSON, CLI export) | Common in regulated EU programs; agents can edit `.mdj` then headless export. |
| Sparx Enterprise Architect | Desktop / on-prem | Limited (COM / OSLC) | Dominant in defense / aerospace / large telco. Automation needs Windows COM. |
| IBM Engineering Requirements Mgmt DOORS Next | SaaS / on-prem | Limited (OSLC API) | Only justified for regulated industries; requires OSLC RM client. |
| Polarion ALM | SaaS / on-prem | Yes (REST API) | UC-as-workitem with reqs traceability; common in medical / automotive (ASPICE, IEC 62304). |
| Jama Connect | SaaS | Yes (REST API) | UC-as-item with relationship matrix; common alternative to DOORS. |
| ReqView | Desktop | Limited (ReqIF export) | Light alternative; pairs with `reqif-tools` for agent ingestion. |
| Cucumber Studio (HipTest) | SaaS | Yes (REST API) | UC → BDD scenarios; good when QA owns the artifact. |
| Lucidchart | SaaS | Limited (REST on Enterprise tier) | Common collaboration tool; agent automation cost ramps fast. |
| Modelio | OSS | Limited (Java GUI, no API) | Full UML; not agent-friendly but accepted in EU public-sector tenders. |
| Notion / Confluence | SaaS | Yes (REST API) | Cheap UC store for <50 UCs; outgrows when traceability and ReqIF demands kick in. |
| Jira / Linear | SaaS | Excellent (REST / GraphQL) | UC-NNN as custom field on epics / stories; preferred backlog destination, not the UC store itself. |

## Templates & scripts

The methodology's `templates.md` is empty in this repo; the UC spec and UC
diagram templates are inline in `README.md` (sections "Use Case Specification
Template" and "Use Case Diagram Template"). Agents should read those directly.

Inline PlantUML emitter (≤50 lines, Bash + jq) — produces a UC diagram
`.puml` file from the JSON UC index built by the sibling `uc-index.sh`
script (in the ba-modeling agent-integration). Render with
`plantuml diagram.puml`.

```bash
#!/usr/bin/env bash
# uc-to-plantuml.sh — emit @startuml UC diagram from use-case-index.json
# Usage: ./uc-to-plantuml.sh path/to/use-case-index.json "System Name"
set -euo pipefail
JSON="${1:?usage: $0 <use-case-index.json> <system-name>}"
SYS="${2:-System}"

declare -A ACTORS
echo "@startuml"
echo "left to right direction"
echo "skinparam packageStyle rectangle"

# Collect distinct actors
while read -r a; do ACTORS["$a"]=1; done < <(jq -r '.[].actor' "$JSON" | sort -u)
for a in "${!ACTORS[@]}"; do
  printf 'actor "%s" as A_%s\n' "$a" "$(echo "$a" | tr -c '[:alnum:]' '_')"
done

echo "rectangle \"$SYS\" {"
jq -r '.[] | "  usecase \"\(.name)\\n[\(.id)]\" as \(.id|gsub("-";"_"))"' "$JSON"
echo "}"

# Edges actor -> uc
jq -r '.[] | "\(.actor)\t\(.id)"' "$JSON" | \
while IFS=$'\t' read -r actor uc; do
  printf 'A_%s --> %s\n' \
    "$(echo "$actor" | tr -c '[:alnum:]' '_')" \
    "$(echo "$uc" | tr '-' '_')"
done

echo "@enduml"
```

## Best practices

- Lock the system boundary in writing (one paragraph, signed off) before
  drafting any UC. Every drafter prompt includes that paragraph verbatim.
- Cap main flow at 5-9 steps; <5 = system function, >9 = split. CI fails the
  PR on violation.
- Forbid UI nouns in System Response. Replace with system-behavior verbs
  ("validates", "persists", "emits event"). Enforce with a regex check
  (`button|modal|popup|screen|click|tab|dropdown`) in CI.
- Mandate >=1 alternative flow and >=1 exception flow per UC; LLMs and humans
  both default to "happy path only".
- Use a single step-counting heuristic across all UCs: one actor action +
  one system response = one step. Without it estimation and test scaffolding
  collapse.
- Store UCs as markdown with YAML front-matter (`id`, `name`, `primary_actor`,
  `status`, `version`, `regulation_anchors`, `source`). Front-matter feeds
  ReqIF export, the index script, and CI checks.
- Treat the UC index as the source of truth for test scaffolding: each main
  flow → 1 happy-path test, each AF / EX → 1 negative-path test. Generate
  test stubs from the index, not by hand.
- Validate UC names with a regex (`^[A-Z][a-z]+ [A-Z][a-z]+`) — verb + noun
  only. CI fails the PR on violation.
- Re-run the relationship agent on the full UC set whenever a new UC lands;
  include / extend / generalization needs the global view.
- Keep UI mockups out of UC files. Link from front-matter (`mockup_url:`).
  The UC outlives the design system; the design system does not outlive
  the UC.
- For regulated programs, embed the regulation anchor (e.g.,
  `21CFR11.10(e)`, `IEC62304-5.2.2`) in front-matter and let CI fail when a
  UC referenced by the safety case has no anchor.
- For RFP / RFI work, freeze the actor list and UC catalog before issuing the
  RFP. Vendor responses must map to the frozen catalog one-for-one or be
  rejected as non-comparable.

## AI-agent gotchas

- LLMs default to writing the happy path and stopping. Force >=1 AF and
  >=1 EX in the schema; reject outputs that omit them.
- Drafters invent UI details ("displays popup confirmation") even when told
  not to. Add a post-generation regex check and bounce drafts that match.
- Step granularity drifts across calls. Pin the heuristic in the system
  prompt AND validate step count post-hoc.
- Relationship inference (`<<include>>`, `<<extend>>`, generalization) is
  the highest-error part. Run only Opus, only after all UCs are drafted, and
  require rationale per edge. The directionality of `<<extend>>` is
  consistently inverted by both humans and LLMs — assert it explicitly in
  the prompt and check in code review.
- LLMs hallucinate actors from UI elements ("Header", "Sidebar") or org-chart
  job titles ("VP Sales"). Force `type ∈ {human, system, time}` in the JSON
  schema and reject anything else.
- Long context tempts "draft 30 UCs in one call" — accuracy collapses past
  ~5 UCs per call due to template repetition errors. Chunk one UC per call.
- Drafter and reviewer using the same model and prompt yields self-congratulatory
  reviews. Use a different model family or at minimum an adversarial system
  prompt for review.
- "Generate test cases from this UC" produces redundant tests when
  `<<include>>` is used. Resolve includes inline before test generation.
- Regulated-industry agents must NEVER auto-merge UC changes; require human
  sign-off recorded in the audit log even when CI is green.
- Pre-commit hook in this repo blocks commits without a CHANGELOG entry.
  Agents producing UC specs that touch CHANGELOG must follow the
  `## [Unreleased]` convention.
- LLMs translate "use case" loosely as "feature" or "user story"; pin the
  Cockburn / RUP definition (sequence of actor-system interactions yielding
  observable value) in the system prompt to prevent drift.

## References

- Alistair Cockburn, *Writing Effective Use Cases* (2000) — canonical
  goal-level taxonomy (cloud, kite, sea, fish, clam) and the original
  fully-dressed UC template.
- Ivar Jacobson, Ian Spence, Kurt Bittner, *Use-Case 2.0* (2011) — slim,
  agile-friendly use cases; the practical update.
- Karl Wiegers and Joy Beatty, *Software Requirements* 3rd ed. — UC vs.
  user story trade-offs and elicitation patterns.
- IIBA, BABOK Guide v3 — "Requirements Analysis and Design Definition" →
  "Specify and Model Requirements" → Use Cases technique.
- Rational Unified Process (RUP) — use-case-driven, architecture-centric,
  iterative methodology; foundational reference for enterprise UC work.
- OMG UML 2.5.1 — Use Case Diagrams notation reference (omg.org/spec/UML).
- PlantUML use case syntax — plantuml.com/use-case-diagram.
- Polarion ALM API docs — polarion.plm.automation.siemens.com.
- IBM DOORS Next OSLC RM v2.0 — open-services.net/specifications/rm.
- Anthropic, *Building effective agents* (2024) — chained vs. orchestrated
  agents pattern (drafter → reviewer → relationship modeler).
- Faion Network — sibling methodology
  `../../ba-modeling/use-case-modeling/agent-integration.md` for the
  design-modeling-focused variant.
