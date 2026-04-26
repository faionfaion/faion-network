# Agent Integration — Synthetic Users

## When to use
- Early ideation: generating directional feedback on concepts before recruiting real participants
- Hypothesis generation: stress-testing assumptions with AI-simulated user archetypes before committing to a study design
- Rapid concept testing at low cost when research budget is zero and timeline is days, not weeks
- Producing illustrative failure scenarios for edge-case personas (e.g., low-literacy users, non-native speakers)
- Supplementing thin real-user datasets when real recruitment would cause delay to a critical decision

## When NOT to use
- Go/no-go product decisions — synthetic feedback is directional only, never confirmatory
- Demand forecasting or willingness-to-pay studies — synthetic users are trained on internet text, not real economic behavior
- Sensitive population research (healthcare, legal, financial) — bias and hallucination risk is unacceptable
- Any study where the research output will be presented to investors or regulators as real user evidence
- When you already have access to real users — synthetic users do not improve on real data

## Where it fails / limitations
- Synthetic feedback skews positive — AI-generated users are prone to "sycophantic" responses that favor the described product
- No nonverbal data: body language, tone, hesitation, confusion signals are absent
- Persona consistency breaks down across long sessions; AI "forgets" constraints mid-interview
- No industry standard for synthetic user quality; outputs from Synthetic Users, Aaru, and Viewpoints.ai are not comparable
- Hallucinated domain knowledge: synthetic users in specialist fields (medicine, law, finance) make up plausible-sounding but wrong behaviors
- Reproducing results is impossible without pinning exact model version and temperature
- "Validation-as-a-Service" market is early; most providers lack transparent methodology documentation

## Agentic workflow
Claude subagents can simulate synthetic user interviews directly: given a persona definition and a discussion guide, the agent responds as the simulated user across multiple questions. A second agent (researcher role) then analyzes the synthetic interview transcripts for themes. The pattern is: human defines persona + study → agent plays user → agent analyzes → human validates key findings with at least 3 real users. Never skip the real-user validation gate.

### Recommended subagents
- `sonnet` — synthetic user simulation (requires nuanced persona adherence), interview analysis, theme extraction
- `haiku` — persona attribute generation, quantitative response scoring (Likert-scale surveys at scale)

### Prompt pattern
```xml
<system>
You are a synthetic research participant. Persona:
- Name: Maya, 34, marketing manager
- Tech comfort: medium (uses Slack, Notion, G-Suite daily; avoids CLI tools)
- Goal: reduce time spent on weekly reporting
- Pain: current tool requires manual CSV exports
Respond only as Maya. Stay in character. Do not be generically positive.
If a question is unclear to Maya, say so. If Maya would not use the product, say so.
</system>
<human>What is your first reaction when you see this onboarding screen? [describe screen]</human>
```

```
Analyze these 5 synthetic interview transcripts [paste].
Extract: (1) top 3 recurring pain points with evidence quotes, (2) 2 positive reactions, (3) 2 areas where synthetic users gave suspiciously consistent or positive responses (flag as low-confidence).
Output structured report with confidence level per finding.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` Python SDK | Run synthetic user simulations directly via Claude API | pip install anthropic |
| `openai` Python SDK | Run synthetic user simulations via GPT-4 for cross-model validation | pip install openai |
| `faker` | Generate realistic persona attribute datasets (names, locations, jobs) | pip install faker |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Synthetic Users (syntheticusers.com) | SaaS | Yes (API) | REST API for persona-based interview simulation |
| Viewpoints.ai | SaaS | Yes (API) | Rapid concept validation; quantitative + qualitative output |
| Aaru | SaaS | Partial | Scenario testing; API in beta; best for predictive analysis |
| SyntheticAudience.ai | SaaS | Partial | Quantitative survey simulation at scale |
| Qualtrics Edge Audience | SaaS | No | Modeled panels; requires Qualtrics subscription + sales |
| UserIntelligence | SaaS | No | Simulation engine; no public API |

## Templates & scripts
Run a synthetic panel interview via Claude API:

```python
import anthropic

client = anthropic.Anthropic()

PERSONAS = [
    {"name": "Maya", "role": "Marketing manager", "tech": "medium", "pain": "manual CSV exports"},
    {"name": "Tom",  "role": "Sales rep",         "tech": "low",    "pain": "too many apps"},
]

QUESTIONS = [
    "What is your first reaction to this product description?",
    "What would stop you from adopting this tool?",
    "What feature would make you pay for this immediately?",
]

def simulate_interview(persona: dict, questions: list[str]) -> list[dict]:
    system = (
        f"You are {persona['name']}, {persona['role']}. "
        f"Tech comfort: {persona['tech']}. Main pain: {persona['pain']}. "
        "Respond naturally. Be honest — include doubts and objections."
    )
    history = []
    results = []
    for q in questions:
        history.append({"role": "user", "content": q})
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            system=system,
            messages=history,
        )
        answer = resp.content[0].text
        history.append({"role": "assistant", "content": answer})
        results.append({"persona": persona["name"], "question": q, "answer": answer})
    return results

all_results = []
for p in PERSONAS:
    all_results.extend(simulate_interview(p, QUESTIONS))

for r in all_results:
    print(f"[{r['persona']}] Q: {r['question']}\nA: {r['answer']}\n")
```

## Best practices
- Define personas from real behavioral data (analytics segments, CRM attributes) not from stereotypes — garbage persona in, garbage output
- Run at least 5 synthetic participants per concept; single-participant outputs are not meaningful
- Flag synthetic findings explicitly in research reports: "Synthetic research — directional only, not validated"
- Always follow synthetic research with at least 3 real user sessions before any product decision
- Cross-validate with two different AI providers (Claude + GPT-4) and note where outputs diverge — divergence signals low-confidence areas
- Retire synthetic personas after 30 days or major product changes; stale personas drift from current user reality

## AI-agent gotchas
- Agents playing synthetic users will break character when pushed on technical details — they answer as AI, not as persona; the simulation degrades under probing
- Temperature = 0 makes synthetic responses too consistent (all personas converge); use temperature 0.7–0.9 for realistic variation
- Synthetic users always know more about your product than they should — they're trained on product descriptions on the web; prime explicitly to limit awareness
- Agent-analyzed synthetic interview themes have double hallucination risk: first in simulation, then in analysis; require evidence quotes for every theme

## References
- https://www.nngroup.com/articles/synthetic-users/ (NNGroup critical assessment)
- https://syntheticusers.com/docs (Synthetic Users API)
- https://www.viewpoints.ai/ (Viewpoints.ai)
- https://aaru.ai/ (Aaru scenario testing)
- https://doi.org/10.1145/3544549.3573882 (ACM CHI 2023: LLMs as user surrogates)
