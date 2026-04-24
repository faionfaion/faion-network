# Agent Integration — Elicitation Techniques (ba-core)

This file is the ba-core fundamentals angle: catalog BABOK v3's 10+ techniques, give a deterministic "pick this one" rule per situation, and show how an agent should invoke each. The enterprise pipeline / PII / audit-trail story lives in the sibling `business-analyst/elicitation-techniques/agent-integration.md`; do not duplicate it here.

## When to use

- Early-discovery phase where the BA must choose a technique mix from BABOK's 10 elicitation techniques and justify each pick to a steering group.
- Training / onboarding a junior BA or an LLM agent that needs a deterministic decision tree, not a narrative essay.
- Mixed-method project where requirements quality depends on triangulation (e.g. interview + observation + document analysis on the same workflow).
- Renegotiating scope mid-project: re-elicit only the changed area with the cheapest technique that still answers the question.
- Budget / time pressure forcing the question "fewest sessions to reach acceptable confidence?" — a structured selector beats ad-hoc choice.

## When NOT to use

- The choice is already made by org policy (e.g. regulated industry mandates signed-off workshops). Skip selection, go straight to execution per `business-analyst/elicitation-techniques/`.
- Continuous-discovery shop on a stable product: weekly customer-interview cadence (Teresa Torres style) is its own pattern, not a per-project selector.
- One-stakeholder, one-sitting situation: just run the interview; a selector adds overhead.
- Pure UX research with users (not stakeholders) — use `ux-researcher/` techniques (usability tests, diary studies) instead.
- Hackathon / spike: time-box and prototype, do not run a BABOK ceremony.

## Where it fails / limitations

- The README lists 8 techniques. BABOK v3 names 10 elicitation techniques (interviews, workshops, focus groups, observation, surveys/questionnaires, document analysis, prototyping, brainstorming, interface analysis, collaborative games) — agents working only from this README will miss interface analysis and collaborative games.
- The "Technique Selection Guide" table is one-to-one; real situations need a *combination* (e.g. observation **then** interview, not OR). Agents tend to pick a single row and stop.
- Selection rule depends on hidden variables the README never asks for: number of stakeholders, geographic distribution, sensitivity, pre-existing artifacts, time budget, regulatory regime. Without those inputs the selector returns a default ("interview") regardless of context.
- "Best for similar users" (focus groups) ignores group-think — focus-group consensus is statistically biased toward extroverts; treat output as hypotheses, not requirements.
- Brainstorming alone produces volume, not quality. Always pair with a convergence step (`faion-brainstorm` does this; vanilla brainstorming does not).
- Document analysis on regulations/standards loses validity fast: the regulation version cited may be superseded. Selector must record `doc_version + retrieval_date`.
- Prototyping is treated as elicitation here, but BABOK also counts it in `requirements-analysis-and-design`. Without a clear scope flag agents double-count it.

## Agentic workflow

Drive ba-core elicitation as a two-step decision: **(1) classify the situation → (2) select techniques**. Inputs are concrete: stakeholder count, locale spread, time budget, sensitivity, evidence already on hand, regulatory regime. Output is a ranked technique mix with a justification per pick that cites the input variables. Execution is delegated to the sibling `business-analyst/elicitation-techniques/` workflow (artifacts, transcripts, redaction). Keep this skill focused on **fundamentals + selection logic** so an agent can answer "which technique, why, in what order?" without reading the heavier enterprise variant.

### Recommended subagents

- `faion-sdd-executor-agent` — wraps each elicitation session as an SDD task with a checklist tied to the technique chosen (interview-prep, workshop-agenda, observation-protocol, etc.).
- `faion-brainstorm` — used as the converge step after BABOK "brainstorming" elicitation; raw ideation is one prompt, ranked-merge is another, review pass kills duplicates.
- `faion-ba-agent` (per the README's `Agent` field) — owner of the technique-selection prompt; reads `stakeholder-analysis/` output and emits a technique mix.
- Custom `technique-selector-agent` (model: sonnet) — pure selector, no execution. Inputs: situation JSON. Output: ranked techniques + rationale + estimated session count.
- Custom `interview-guide-agent` (model: haiku) — fills the README interview-guide template from a topic + role + 3 prior artifacts; cheap because the template is fixed.
- Custom `workshop-agenda-agent` (model: sonnet) — drafts the workshop-agenda template, balances divergent vs. convergent slots, picks collaborative-game variants (e.g. Product Box, Speed Boat) when the goal is creative.
- Custom `interface-analysis-agent` (model: sonnet) — handles the missing-from-README technique: list inbound/outbound interfaces of the system under study, derive integration requirements.

### Prompt pattern

Two short prompts: classify situation, then select. Both return strict JSON so a wrapper can validate and route.

```
You are technique-selector-agent. Inputs: {stakeholder_count, locales, time_budget_days,
sensitivity in {low,med,high}, prior_artifacts[], regulated in {true,false},
goal in {discover_current_state, build_consensus, validate_design, generate_ideas,
quantify_demand, derive_integrations}}. Choose 1-3 techniques from BABOK v3:
[interview, workshop, focus_group, observation, survey, document_analysis,
prototyping, brainstorming, interface_analysis, collaborative_game]. Rank them
by expected info-yield-per-hour for THIS situation. Output:
{picks:[{technique, rationale_cites_inputs[], est_sessions, prerequisite}],
rejected:[{technique, why_not}], triangulation_pair_recommended}.
```

```
You are interview-guide-agent. Build a guide from elicitation-techniques/templates.md.
Inputs: {topic, interviewee_role, objectives[], prior_artifacts[]}. Constraints:
6 main questions max; ≥2 open + ≥2 probing + 1 closing; no leading phrasing;
each question must reference an objective by index. Output strict JSON matching
the template's sections.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` / `yq` | Parse situation JSON, manipulate technique-mix output in shell pipelines. | `apt install jq yq` |
| `pandoc` | Convert filled interview-guide / workshop-agenda Markdown to DOCX/PDF for stakeholder distribution. | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render technique-selection decision trees and observed processes from Mermaid into PNG. | `npm i -g @mermaid-js/mermaid-cli` |
| `gh issue` | One issue per planned elicitation session — agenda in body, transcript link in comments. | https://cli.github.com |
| `csvkit` | Pre-flight survey CSVs (`csvstat` for response rate, `csvsql` for cross-tabs). | `pip install csvkit` |
| `goose` / Sourcegraph search | Code/spec search step before document analysis — agents must read first, elicit second. | https://block.github.io/goose/ |
| `uv` / `pipx` | Run the technique-selector script (below) without polluting global Python. | https://docs.astral.sh/uv/ |
| `mustache` / `jinja2-cli` | Render per-stakeholder invites and consent blurbs from a single template. | `pip install jinja2-cli` |
| `whisper.cpp` | Local STT — referenced for execution, not selection; full pipeline lives in business-analyst variant. | https://github.com/ggerganov/whisper.cpp |
| `dot` (Graphviz) | Visualise interface-analysis maps (system → external system edges) cheaply. | `apt install graphviz` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Calendly / Cal.com | SaaS / OSS | REST API | Schedule interview/workshop slots; cron-driven invites from the selector output. |
| Google Forms / Tally.so / Typeform | SaaS | REST + webhooks | Channel for the "survey" technique; pick by N target and budget. |
| LimeSurvey | OSS | REST API | Self-host when a regulated regime forbids SaaS surveys. |
| Miro / FigJam / Mural | SaaS | REST API | Workshop boards with built-in collaborative-game templates (Product Box, Speed Boat, 6-3-5). |
| Loom / Tella | SaaS | REST API | Async observation: stakeholder records own workflow once; agent picks `observation` technique without scheduling. |
| Dovetail / EnjoyHQ | SaaS | REST API | Repository for tagged transcripts; agents query "which technique produced which insight". |
| Notion / Confluence | SaaS | REST API | Storage for filled templates and the selection-rationale doc; one page per session. |
| GitHub Issues / Projects | SaaS / OSS | REST API | Lightweight tracker for the elicitation backlog; one issue per chosen technique-instance. |
| Slido / Mentimeter | SaaS | REST API | Live polling inside workshops to surface dissent in real-time without the loudest-voice effect. |
| Stormboard | SaaS | REST API | Brainstorming-specific tool; agent-friendly export. |

## Templates & scripts

The README provides interview-guide and workshop-agenda templates — reuse those. Inline below: a deterministic technique-selector usable from `uv run` or as a CI step. It scores BABOK techniques against a situation JSON and prints a ranked mix.

```python
#!/usr/bin/env python3
"""technique_selector.py — BABOK v3 elicitation technique picker.
Usage: uv run technique_selector.py situation.json"""
from __future__ import annotations
import json, sys, pathlib

# (technique, base_score, multipliers keyed on situation features)
TECHS = [
    ("interview",        5, {"sensitivity:high":+2,"goal:discover_current_state":+2,"stakeholder_count<=10":+1}),
    ("workshop",         3, {"goal:build_consensus":+3,"stakeholder_count>=4":+1,"locales==1":+1}),
    ("focus_group",      2, {"goal:discover_current_state":+1,"stakeholder_count>=6":+1,"sensitivity:low":+1}),
    ("observation",      4, {"goal:discover_current_state":+3,"prior_artifacts<3":+1}),
    ("survey",           2, {"stakeholder_count>=30":+3,"locales>1":+2,"goal:quantify_demand":+3}),
    ("document_analysis",4, {"prior_artifacts>=3":+3,"regulated":+2}),
    ("prototyping",      3, {"goal:validate_design":+4,"prior_artifacts>=1":+1}),
    ("brainstorming",    2, {"goal:generate_ideas":+4,"stakeholder_count>=3":+1}),
    ("interface_analysis",3,{"goal:derive_integrations":+4,"prior_artifacts>=1":+1}),
    ("collaborative_game",2,{"goal:generate_ideas":+2,"goal:build_consensus":+1,"locales==1":+1}),
]

def feat(s: dict) -> set[str]:
    f = set()
    n = s["stakeholder_count"]; loc = s["locales"]; pa = len(s.get("prior_artifacts",[]))
    f.add(f"stakeholder_count{'<=' if n<=10 else '>='}{10 if n<=10 else 30 if n>=30 else n}")
    f |= {f"stakeholder_count<=10" for _ in [0] if n<=10}
    f |= {f"stakeholder_count>=4"  for _ in [0] if n>=4}
    f |= {f"stakeholder_count>=6"  for _ in [0] if n>=6}
    f |= {f"stakeholder_count>=30" for _ in [0] if n>=30}
    f.add(f"locales{'==1' if loc==1 else '>1'}")
    f |= {f"prior_artifacts{'<' if pa<3 else '>='}3" for _ in [0]}
    f |= {f"prior_artifacts>=1"} if pa>=1 else set()
    f.add(f"sensitivity:{s.get('sensitivity','low')}")
    f.add(f"goal:{s['goal']}")
    if s.get("regulated"): f.add("regulated")
    return f

def score(situation: dict) -> list[dict]:
    fs = feat(situation)
    out = []
    for name, base, mult in TECHS:
        s = base + sum(v for k,v in mult.items() if k in fs)
        out.append({"technique": name, "score": s})
    return sorted(out, key=lambda x: -x["score"])[:3]

if __name__ == "__main__":
    sit = json.loads(pathlib.Path(sys.argv[1]).read_text())
    print(json.dumps({"picks": score(sit), "triangulation": "pick technique #1 + technique #2"}, indent=2))
```

## Best practices

- Use the BABOK v3 *full* list of 10 techniques. Add interface analysis and collaborative games to the README's 8 — agents that only see 8 systematically miss integration requirements and creative-elicitation options.
- Never pick a single technique. Triangulate ≥2; the second technique is chosen to challenge the first (interview claim → observation reality, survey trend → focus-group nuance).
- Sequence cheap-then-expensive: document analysis → observation → interview → workshop → prototyping. Stop as soon as confidence target is met; the README's selector implies parallel choice and overspends.
- Tag each elicited statement as `stated`, `observed`, or `inferred`. Treat `observed` as gold, `stated` as silver, `inferred` as bronze; downstream prioritisation should respect the tier.
- Cap the technique-selector output at 3 picks per situation. More than 3 means the situation is under-specified — push back to `stakeholder-analysis/` and `ba-planning/`.
- Pre-read every interview / workshop with a 1-pager: objectives, prior artifacts, glossary. Skipping the pre-read is the most common quality leak per BABOK case studies.
- Distinguish brainstorming the *technique* from brainstorming the *meeting type*. The technique demands a structured divergence rule (6-3-5, Crazy Eights, Round-Robin) — generic "throw out ideas" is what fails.
- For surveys, design with N-target + confidence interval + pre-registered analysis plan. Otherwise the response is anecdote with statistics applied.
- Time-box: interview ≤60 min, workshop ≤90 min, observation ≤2 h per session. Past those bounds notes degrade and recall drops.
- Keep an "open questions" log per session. The next session's first job is to close items from the log; close-rate is a meaningful BA quality metric.
- Document the *rejected* techniques and why. Reviewers and auditors check the negative space; an "interview-only" plan with no rationale is a smell.

## AI-agent gotchas

- Single-row table fixation: the README's selection table is one situation → one technique. LLMs copy that and never combine. Force the prompt to return a *mix* with triangulation pair.
- Default-to-interview bias: when inputs are sparse, agents fall back to interviews because the example block is rich. Mitigate by requiring explicit input fields; reject selection if `stakeholder_count` or `goal` is null.
- Missing techniques: agents do not invent interface analysis or collaborative games unless prompted. Hardcode the 10-item BABOK list in the prompt.
- Leading questions: prep agents bias toward confirmation. Lint guides for "don't you", "wouldn't", "isn't it true" before sending to a stakeholder.
- Survey question type imbalance: agents over-use Likert; mix multiple-choice + ranking + 1 open per section. Validate against a known-good template.
- Workshop-agenda generation skews to talk slots, not activity slots. Require ≥40% of agenda time to be hands-on (sticky notes, dot-voting, mapping), not presentation.
- Document-analysis hallucination: agents cite "the spec says X" without a path + line range. Require `path:line-line` citation; reject claims without it.
- Brainstorming convergence skipped: agents return 30 ideas without ranking. Mandate a converge prompt (`faion-brainstorm` review pass) before the output is accepted.
- Observation translated to interview: agents propose "ask the user how they do X" instead of "watch the user do X". When `goal == discover_current_state`, force at least one observation slot.
- Collaborative-game selection: agents pick the most-mentioned game (Product Box) regardless of fit. Provide a small lookup `{goal: [games]}` and constrain.
- Human-in-the-loop checkpoints (mandatory for ba-core): the technique selection itself is signed off by a human BA before scheduling; the interview / workshop is run by humans (agents prepare, do not converse with stakeholders); the synthesis pass into requirements stubs is reviewed by humans before the stubs feed `requirements-lifecycle/`.
- Scope creep into business-analyst variant: agents pulled into elicitation tend to invent PII pipelines and consent forms. Keep ba-core narrow — selection + fundamentals — and route execution-heavy concerns to the sibling skill.

## References

- IIBA BABOK Guide v3, ch. 4 "Elicitation and Collaboration" + Part 10 technique catalog — https://www.iiba.org/standards-and-resources/babok/
- ISO/IEC/IEEE 29148:2018 §6.4 Elicitation — https://www.iso.org/standard/72089.html
- Steve Portigal, "Interviewing Users" 2nd ed. (Rosenfeld, 2023).
- Erika Hall, "Just Enough Research" 2nd ed. (Rosenfeld, 2019).
- Hohmann, "Innovation Games" (Addison-Wesley, 2006) — Product Box, Speed Boat, 20/20 Vision.
- Gause & Weinberg, "Exploring Requirements: Quality Before Design".
- Sibling: `business-analyst/elicitation-techniques/agent-integration.md` — execution pipeline, transcripts, PII, audit trail.
- Sibling ba-core methodologies: `stakeholder-analysis/`, `ba-planning/`, `requirements-lifecycle/`, `requirements-prioritization/`, `requirements-validation/`.
