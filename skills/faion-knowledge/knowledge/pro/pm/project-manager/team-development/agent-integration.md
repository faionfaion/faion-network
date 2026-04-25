# Agent Integration — Team Development

## When to use
- Forming a new team and producing a team charter, working agreements, RACI, and skills matrix in one pass.
- Diagnosing a struggling team via Tuckman stage assessment (Forming/Storming/Norming/Performing/Adjourning) and recommending PM actions.
- Building a skills-gap plan: agent reads role expectations + current matrix, proposes training, pairing, hires.
- Coaching the solo → team transition (first-hire integration plan, ramp checklist).
- Generating retro prompts and synthesizing patterns across multiple sprints.

## When NOT to use
- Pure HR / performance-management actions (compensation, PIPs, hiring decisions) — those need a human + HR system, not an agent.
- Crisis interventions (harassment, mental-health, layoffs) — agents must escalate to humans immediately.
- Cross-cultural mediation where nuance, language, and confidentiality dominate — automation backfires.
- Single-person projects — there is no team to develop.

## Where it fails / limitations
- Tuckman is a model, not a measurement instrument; agents stage teams confidently from sparse signals and can be wrong.
- Skills matrices are a proxy: real performance depends on context, not numbers; an agent that hires from "matrix gaps" can miss culture fit.
- Retro patterns repeat (communication, planning, scope) regardless of project; agents that surface only the top theme miss outliers.
- Confidentiality: 1-on-1 notes contain sensitive content. Agents must not auto-aggregate or store them across sessions.
- Bias: LLMs trained on tech-bro retros recommend "more standups" as a fix to almost everything.
- Conflict mediation requires presence; agents can summarise positions but cannot actually mediate.
- Working agreements drafted by an agent are generic unless seeded with team-specific examples.

## Agentic workflow
The agent is a documentation and pattern-extraction layer. Phase 1: a `team-charter-builder` produces the charter from team list + project context. Phase 2: a `retro-synthesiser` extracts themes and action items from raw retro notes (max-N sprints) and proposes experiments. Phase 3: a `tuckman-coach` reads recent signals (retro themes, throughput, conflict reports) and stages the team with PM actions. All outputs require human review; never publish to the team without sign-off.

### Recommended subagents
- `team-charter-builder` (define inline) — input: team list, project context; output: charter markdown.
- `retro-synthesiser` (define inline) — input: N retro markdown files; output: themes + recurring action items + experiments.
- `tuckman-coach` (define inline) — input: signals; output: stage + recommended PM actions.
- `skills-matrix-analyzer` (define inline) — input: role expectations + matrix; output: gap plan (training / pair / hire).
- `faion-brainstorm` — to generate options for stuck retros (e.g. "we keep talking about scope").

### Prompt pattern
```
You are a retro synthesiser. Inputs: <list of retro_*.md>.
Output JSON:
{ "themes": [
    { "theme": "...",
      "evidence_count": N,
      "first_seen_sprint": "...",
      "still_present": bool,
      "proposed_experiment": "imperative, time-boxed",
      "owner_suggestion": "role" } ],
  "tuckman_signal": "Forming|Storming|Norming|Performing|Adjourning",
  "tuckman_evidence": ["..."] }
Rules:
- Do NOT name individuals; preserve psychological safety.
- Themes must be backed by ≥ 2 distinct sprints.
- Experiments must be falsifiable within 2 sprints.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull throughput / cycle-time signals from PRs | https://cli.github.com/ |
| `jira-cli` | Pull velocity / WIP signals | https://github.com/ankitpokhrel/jira-cli |
| `pandoc` | Render charter / matrix to DOCX / PDF | https://pandoc.org/ |
| `mermaid-cli` | Tuckman state diagrams + skills heatmaps | https://github.com/mermaid-js/mermaid-cli |
| `wordcloud-cli` (Python) | Theme visualisation across retros | https://github.com/amueller/word_cloud |
| `ranger-mover` (custom) | Move retro notes between sprint folders | n/a |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Lattice | SaaS | Yes — REST | 1-on-1s, growth, reviews; agent can summarise |
| 15Five | SaaS | Yes — REST | Pulse + 1-on-1 notes |
| Culture Amp | SaaS | Yes — REST | Engagement surveys for team-stage signal |
| Officevibe | SaaS | Yes — REST | Lightweight pulse surveys |
| Range | SaaS | Yes — REST | Async standups + check-ins |
| Confluence / Notion | SaaS | Yes — REST | Where charter, matrix, retro outputs live |
| FunRetro / Parabol / Retrium | SaaS | Yes — REST / API | Retro boards with export to JSON |
| Slack + Polly / Geekbot | SaaS | Yes — REST / webhooks | Async retros and pulse |

## Templates & scripts
See `templates.md` for charter, skills matrix, and retro templates. Inline retro theme extractor (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Extract recurring themes across multiple retros (markdown bullet lists)."""
import sys, re, glob, json
from collections import Counter, defaultdict
def parse(path):
    bullets = []
    with open(path) as f:
        for line in f:
            m = re.match(r"\s*[-*]\s+(.+)", line)
            if m: bullets.append(m.group(1).strip().lower())
    return bullets
def cluster(bullets, by_sprint):
    # naive: token-overlap; replace with embeddings for production
    counts = Counter()
    sprints = defaultdict(set)
    for sprint, items in by_sprint.items():
        seen = set()
        for b in items:
            key = " ".join(sorted(set(re.findall(r"[a-z]{4,}", b))[:3]))
            if not key or key in seen: continue
            counts[key] += 1
            sprints[key].add(sprint)
            seen.add(key)
    return [{"theme": k, "evidence_count": v,
             "sprints": sorted(sprints[k])}
            for k, v in counts.most_common() if v >= 2]
def main(pattern):
    by_sprint = {}
    for p in sorted(glob.glob(pattern)):
        by_sprint[p] = parse(p)
    print(json.dumps(cluster(None, by_sprint), indent=2))
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Co-write the charter with the team in a 60-min workshop; do not let an agent author it solo.
- Refresh skills matrix quarterly; treat it as planning input, not performance data.
- Retros: rotate facilitator, time-box, capture an action with owner + sprint deadline.
- Action item without an owner = no action; reject.
- Storming is healthy and short-lived; do not "fix" it by suppressing conflict — facilitate it.
- Solo → team: document everything assumed-obvious; first hire onboarding fails on tribal knowledge.
- Track team health with one or two metrics (eNPS, throughput stability), not a dashboard with twenty.

## AI-agent gotchas
- LLMs name individuals in retro summaries by default — strip names; preserve psychological safety.
- "More standups / better communication" is a recommended-fix bias; require alternative options.
- Tuckman staging from sparse signals is overconfident; agents should emit a confidence score and surface evidence.
- Action items get reformulated into corporate-ese ("enhance synergy"); enforce imperative + measurable form.
- Recurring themes are flagged as "new" each sprint because the agent has no memory; pass last N synthesised theme files into context.
- Sensitive content (mental-health, harassment) leaks through summarisation; add a content-filter step that escalates to a human channel and aborts.
- Agents propose hires when the gap is process / pairing — require considering training + pairing before hire.
- Skills-matrix scores drift toward 3 (median) when the agent has no info; force "unknown" instead of guessing.

## References
- PMI — A Guide to the PMBOK 7th Edition, Team Performance Domain: https://www.pmi.org/standards/pmbok
- Bruce Tuckman — "Developmental Sequence in Small Groups" (1965), Psychological Bulletin
- Patrick Lencioni — "The Five Dysfunctions of a Team"
- Google re:Work — Project Aristotle (psychological safety): https://rework.withgoogle.com/print/guides/5721312655835136/
- Esther Derby & Diana Larsen — "Agile Retrospectives: Making Good Teams Great"
- Daniel Coyle — "The Culture Code"
- Manager's Path — Camille Fournier (engineering team development)
