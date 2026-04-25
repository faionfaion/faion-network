# Agent Integration — UX/UI Methodologies (CLAUDE-methodologies)

## When to use
- Agent needs to select an appropriate UX research or design method for a given product problem
- Automated heuristic evaluation is needed against Nielsen's 10 usability heuristics
- Sprint requires a structured UX deliverable (persona, journey map, IA sitemap) that an agent can scaffold
- UX review of an existing design must be documented systematically before a design critique session
- Cognitive walkthrough needs to be scripted for a new user flow

## When NOT to use
- User interviews, usability testing, focus groups, diary studies — these require real human participants; an agent cannot substitute for participant recruitment, moderation, or empathy-based interpretation
- Card sorting, tree testing — require actual user responses; agent can analyze results but not generate them
- A/B testing — requires live traffic; agent can design the test and analyze results, not run it
- Any method where the output quality depends on observed human behavior in context

## Where it fails / limitations
- Heuristic evaluation by LLM produces plausible-sounding but shallow findings without seeing the actual UI — without a screenshot or DOM, it evaluates descriptions, not the interface
- Persona generation from synthetic data produces stereotypes; personas must be grounded in actual user research data
- Journey maps generated without real user research data reflect assumptions, not reality — useful as a hypothesis artifact, not a research output
- Cognitive walkthrough scripted by an agent misses non-obvious task paths that real users take; it defaults to the happy path
- IA frameworks generated without content inventory are speculative; agent needs actual content list as input

## Agentic workflow
A Claude subagent is most useful as a methodology scaffolding and synthesis engine within this knowledge base: select the right method for a stated problem, generate structured templates (persona canvas, journey map skeleton, IA sitemap draft), and synthesize research findings into design recommendations. The agent drives analytical and documentary tasks; human designers and researchers own all participant-facing activities. Subagent handoffs are appropriate at the point where real user data arrives (after interviews, surveys, card sorts).

### Recommended subagents
- `faion-sdd-executor-agent` — executes UX deliverable tasks defined in an SDD implementation plan (e.g., "generate persona canvas", "draft IA sitemap")
- Custom ux-synthesizer agent — takes raw user interview notes (text), applies affinity clustering, generates design recommendations

### Prompt pattern
```
You are a UX strategist. Given this product problem statement:
<problem>{{problem_description}}</problem>

And these constraints:
- Budget: {{budget_level}} (low/medium/high)
- Timeline: {{timeline}} sprints
- Access to users: {{user_access}} (none/survey/interviews/usability)

Recommend the 3 most appropriate UX methods from this list:
[user-interviews, usability-testing, surveys, card-sorting, personas, journey-mapping,
wireframing, prototyping, ab-testing, heuristic-evaluation, contextual-inquiry,
tree-testing, competitive-analysis, cognitive-walkthrough]

For each: why it fits, what artifacts it produces, what input data it requires.
```

```
Apply Nielsen's 10 Usability Heuristics to evaluate this UI description:
<ui_description>{{ui_description}}</ui_description>

For each heuristic, rate compliance: pass / partial / fail.
For partial or fail: cite the specific issue and suggest a fix.
Skip heuristics that cannot be evaluated from the description alone — do not speculate.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `optimal-workshop` API | Tree testing and card sorting data collection | optimalworkshop.com/developers |
| `useberry` API | Usability testing result export | useberry.com/api |
| `maze` API | Remote usability testing metrics | maze.co/api |
| `userzoom` API | Enterprise usability + survey platform | userzoom.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop | SaaS | Yes — REST API | Card sorting + tree testing; agent can analyze result exports |
| Maze | SaaS | Yes — REST API | Remote usability testing; agent can generate test scripts and parse metrics |
| Lookback | SaaS | Partial | Session recording; no API for analysis automation |
| UserTesting | SaaS | Partial — limited API | Participant recruitment + recordings; analysis requires human review |
| Dovetail | SaaS | Yes — REST API | Research repository; agent can tag and synthesize notes |
| Notion / Confluence | SaaS | Yes — REST API | UX deliverable storage; agent can write personas, journey maps as pages |
| Miro | SaaS | Yes — REST API | Online whiteboard; agent can create affinity diagrams via API |

## Templates & scripts
See templates.md for persona canvas, journey map, and IA sitemap templates.

Inline: heuristic evaluation scoring script:
```python
HEURISTICS = [
    "Visibility of system status",
    "Match between system and real world",
    "User control and freedom",
    "Consistency and standards",
    "Error prevention",
    "Recognition rather than recall",
    "Flexibility and efficiency of use",
    "Aesthetic and minimalist design",
    "Help users recognize and recover from errors",
    "Help and documentation",
]

def print_eval_template():
    print("# Heuristic Evaluation\n")
    for h in HEURISTICS:
        print(f"## {h}")
        print("- Rating: pass / partial / fail")
        print("- Issue: ")
        print("- Severity: 0 (cosmetic) / 1 (minor) / 2 (major) / 3 (catastrophic)")
        print("- Fix: \n")

print_eval_template()
```

## Best practices
- Match method complexity to the question: a survey answers "how many?", an interview answers "why?" — don't over-engineer
- Generate persona canvases from actual interview data, not demographic assumptions; label clearly if synthetic
- Use cognitive walkthrough for new user flows before prototyping — cheaper to fix at script stage than post-prototype
- Journey maps are hypotheses until validated with real users; mark status explicitly (assumed vs. validated)
- Competitive analysis requires at least 3 direct competitors and 2 adjacent products to produce useful benchmarks
- Tree testing results below 70% directness score indicate IA restructuring is needed — don't optimize labels first

## AI-agent gotchas
- Agent persona generation without real data produces marketing stereotypes ("Sarah, 32, tech-savvy") — always pass interview quotes or survey data as input
- LLM heuristic evaluations without seeing the actual UI are evaluations of descriptions; agents must state this caveat explicitly in output
- Affinity clustering by LLM requires careful chunking — interview transcripts >4000 tokens require splitting; themes at chunk boundaries get lost
- Journey map emotional curves generated without user data are fiction; agents must flag when generating from assumptions
- When agents draft survey questions, they default to leading questions — prompt explicitly for neutral, balanced phrasing

## References
- Nielsen, J. "10 Usability Heuristics for User Interface Design" — nngroup.com/articles/ten-usability-heuristics
- Dovetail "Research Repository" methodology guide — dovetail.com/learn
- Optimal Workshop "Research Methods Guide" — optimalworkshop.com/learn
- "Just Enough Research" — Erika Hall, A Book Apart 2013
- UXPA "User Experience Body of Knowledge" — uxbok.org
- Steve Krug "Don't Make Me Think" — sensible.com
