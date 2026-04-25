# Agent Integration — Roadmap Design

## When to use
- Communicating a 1–4 quarter plan to internal team, investors, or customers.
- Multiple stakeholders need a single source of truth that links strategy → themes → initiatives.
- Decision moment between roadmap formats (timeline / Now-Next-Later / outcome / kanban) — methodology contains a selection matrix.
- Onboarding a new contractor or PM and you need a one-page document describing direction.

## When NOT to use
- Less than 4 weeks of work — roadmap overhead exceeds value; use a sprint plan or release notes.
- Pure exploration phase before PMF; an explicit roadmap creates anchors and biases discovery.
- Highly volatile environments (hackathon, week-by-week pivots) — Now-Next-Later collapses to "Now"; just keep a backlog.
- When the goal is a feature commitment to a single customer; that is a contract, not a roadmap.

## Where it fails / limitations
- Roadmaps treated as commitments instead of intent — slip dates blow trust.
- Confidence levels missing or applied uniformly ("everything is High") strip the signal that makes Now-Next-Later useful.
- "Later" column becomes graveyard; nothing moves out of it and stakeholders stop reading.
- One-size-fits-all roadmap shared with engineering, exec, and customers — each audience needs a different abstraction.
- LLM-generated roadmaps default to listing every backlog item under "Next", which defeats the prioritisation purpose.

## Agentic workflow
Pipeline: an analyst agent ingests strategy doc + backlog + OKRs and proposes themes; a strategist agent allocates initiatives across Now/Next/Later with confidence scores and links each to an objective; a writer agent produces audience-specific renders (internal vs external). Use the format-selection matrix from `README.md` as a deterministic first step (do not let the LLM pick randomly). Human checkpoints: theme approval, "not doing" list, external publication.

### Recommended subagents
- `faion-mlp-impl-planner-agent` — referenced in `README.md`; turns themes into initiative slates.
- `faion-task-creator-agent` — explodes a Now initiative into ready backlog items.
- `faion-spec-reviewer-agent` — validates each initiative has an objective + confidence + measure.
- `faion-idea-generator-agent` — populates the "exploring" list under Later without committing.

### Prompt pattern
```
System: You are a roadmap designer. Output ONLY a JSON document with keys:
  vision, objectives[], themes[], horizons{now, next, later}, not_doing[], risks[].
  Each initiative: {id, theme, objective_id, confidence: high|medium|low,
  effort: s|m|l, owner, measure, status}.
  Forbid dates per initiative outside "now". Forbid >5 initiatives in "now".
Input: {strategy, okrs, backlog_summary, team_capacity, audience}
```

```
System: You are an audience adapter. Given internal_roadmap.json and
  audience in {exec, engineering, customer}, emit Markdown stripped of
  fields that audience should not see (engineering = no revenue numbers,
  customer = no confidence levels or owners, exec = aggregate to themes).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh project` | GitHub Projects: model Now/Next/Later as iterations or fields | https://cli.github.com/manual/gh_project |
| `linear-cli` | Initiatives = themes, projects = initiatives, cycles = "Now" | https://developers.linear.app |
| `jira-cli` | Advanced roadmaps via REST | https://github.com/ankitpokhrel/jira-cli |
| `notion-sdk-py` | Maintain a Notion roadmap database from agents | https://github.com/ramnes/notion-sdk-py |
| `roadmunk` REST | Visual roadmap export, agent-writable | https://help.roadmunk.com/api |
| `mermaid-cli` | Render roadmap diagrams from text | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST) | Strongest objectives → features → roadmap chain. |
| Aha! Roadmaps | SaaS | Yes (REST) | Multi-format, audience-specific views built-in. |
| Productplan | SaaS | Limited (REST) | Visual lanes, weak write API. |
| Roadmunk | SaaS | Yes (REST) | Timeline + Swimlane export. |
| Linear | SaaS | Yes (GraphQL) | Initiatives + projects = roadmap primitives. |
| Plane | OSS | Yes (REST) | Self-host roadmap-style projects. |
| Notion DB template | SaaS | Yes (REST) | Cheap, brittle for >100 items. |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Free, integrated with code. |

## Templates & scripts
See `README.md` for the Now-Next-Later, Quarterly Outcome, and External Customer templates. Inline rule-set to gate publication of an internal roadmap:

```python
import sys, yaml
RULES = {
    "max_now": 5,
    "max_next": 8,
    "min_low_confidence_in_later": 1,
    "required_keys": {"vision", "objectives", "themes", "horizons", "not_doing"},
}
r = yaml.safe_load(open(sys.argv[1]))
errs = []
miss = RULES["required_keys"] - r.keys()
if miss: errs.append(f"missing top-level keys: {miss}")
if len(r["horizons"]["now"]) > RULES["max_now"]:
    errs.append("too many initiatives in Now")
if not r.get("not_doing"):
    errs.append("not_doing list is empty — explicit exclusions required")
for h in ("now", "next"):
    for i in r["horizons"].get(h, []):
        if "confidence" not in i or "objective_id" not in i:
            errs.append(f"{h}/{i.get('id')}: missing confidence or objective_id")
for e in errs: print("FAIL:", e)
sys.exit(1 if errs else 0)
```

## Best practices
- Maintain two artefacts: `roadmap_internal.md` (full detail) and `roadmap_external.md` (themes + benefits only). Sync via script, not copy-paste.
- Use confidence levels honestly: at least 30% of items should be Medium or Low; if everything is High, the labelling is decoration.
- Update cadence: monthly review, quarterly rewrite. Do not rewrite the whole doc each sprint — that destroys signal.
- Always include an "Explicitly Not Doing" section with reasons; it doubles as a future review log when stakeholders ask "why didn't we…".
- Tie every initiative back to one objective ID; orphan initiatives are leakage from strategy.
- For solo founders, the roadmap should fit on one screen. If it doesn't, you have a backlog, not a roadmap.
- Treat the external roadmap as marketing copy: features become benefits; remove jargon and internal codenames.

## AI-agent gotchas
- Models default to "everything is High confidence". Force a target distribution in the prompt (e.g. now=mostly High, next=mostly Medium, later=mostly Low).
- Without explicit theme limits, agents produce 8+ themes and lose strategic signal. Cap themes at 3–5 in the system prompt.
- LLMs cannot reliably estimate effort or sequence dependencies; treat their estimates as relative ordering only.
- "Not doing" lists are dropped silently; mark the field required and reject documents missing it.
- Audience adaptation often leaks internal terminology to customers ("MLP", "tech debt"). Strip via post-processor or named-entity allowlist.
- Roadmaps stored only in chat outputs go stale; persist to a tracker and have the agent diff next run.
- When fed last quarter's roadmap, agents simply restate it. Force "what changed since last review" as an explicit section.
- Human-in-loop: never let the agent ship the external roadmap; review for commitments, NDAs, and competitive signalling.

## References
- Roman Pichler — "GO Product Roadmap": https://www.romanpichler.com/tools/go-product-roadmap/
- Janna Bastow — "Now / Next / Later" roadmap origin: https://www.prodpad.com/blog/the-now-next-later-roadmap/
- Marty Cagan — *Inspired*, chapters on product strategy and roadmaps.
- C. Todd Lombardo et al. — *Product Roadmaps Relaunched* (O'Reilly).
- Atlassian — "How to build a product roadmap": https://www.atlassian.com/agile/product-management/product-roadmaps
- Productboard glossary — roadmap formats: https://www.productboard.com/glossary/
