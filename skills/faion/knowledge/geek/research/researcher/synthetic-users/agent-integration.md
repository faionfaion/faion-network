# Agent Integration — Synthetic Users

## When to use
- Early ideation: generating directional signal before any real users can be recruited
- Hypothesis stress-testing: "Would our target persona care about X?" as a fast pre-filter
- Low-stakes concept validation where cost of being wrong is recoverable
- Generating adversarial edge-case responses to identify blind spots in a survey instrument
- Producing a research brief baseline that a human researcher then corrects

## When NOT to use
- Go/no-go product decisions — synthetic data cannot replace real demand signal
- Demand forecasting or pricing research — synthetic willingness-to-pay is systematically biased high
- Any research where legal, medical, or safety consequences follow from findings
- Final validation before launch — always run at least one round of real-user interviews
- Stakeholder-facing deliverables presented as real research without disclosure

## Where it fails / limitations
- Synthetic responses skew positive and fail to surface genuine emotional friction
- Results are sensitive to persona framing: minor prompt changes produce different "findings"
- No behavioral data — only stated preferences, which diverge from observed behavior
- No industry standard for synthetic data quality; results cannot be independently audited
- Nonverbal signals (hesitation, tone, body language) are absent — a major loss for usability research
- Hallucination risk: synthetic users may report features or experiences that do not exist in the product

## Agentic workflow
An agent generates synthetic user profiles by combining demographic inputs with behavioral archetypes, then runs a simulated interview or survey against each profile. Sonnet produces profiles with enough internal consistency for directional usefulness; Opus validates that profiles cover the ICP distribution and checks for systematic bias. Results feed into a gap-analysis step where the agent identifies which hypotheses received uniform synthetic agreement (low signal) vs. divergent responses (high signal worth real-user follow-up).

### Recommended subagents
- `faion-sdd-executor-agent` — can orchestrate multi-step research pipelines including synthetic + real validation stages
- General Claude subagent (Sonnet) — profile generation and response simulation
- General Claude subagent (Opus) — bias detection, persona coverage validation, governance framing

### Prompt pattern
```
Create 5 synthetic user profiles for [ICP description].
For each profile include:
- Name, age, job title, company size
- Primary job-to-be-done
- Tech comfort level (1-5)
- Top 3 frustrations with current solution
- Budget authority (yes/no)

Then simulate each profile responding to this question: "[research question]"
Flag any responses that look suspiciously uniform — that is low signal.
```

```
You are a research quality reviewer. Given these synthetic user responses: [responses]
Identify:
1. Topics where all profiles agreed (potentially synthetic bias, not real signal)
2. Topics with genuine divergence (worth real-user follow-up)
3. Any responses that appear to describe features not in [product description]
Output: bulleted gap analysis with recommended next steps.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Synthetic Users CLI (unofficial) | Profile generation and survey simulation | syntheticusers.com/api |
| Python + faker | Generate realistic demographic inputs for profiles | `pip install faker` / faker.readthedocs.io |
| jq | Parse and filter JSON synthetic response batches | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Synthetic Users | SaaS | Yes (API) | REST API for profile creation + survey response simulation |
| SyntheticAudience.ai | SaaS | Yes (API) | Quantitative research at scale; panel-style synthetic responses |
| Viewpoints.ai | SaaS | Partial | Fast concept validation; limited API access |
| Aaru | SaaS | Yes (API) | Scenario testing and predictive analysis; strongest for B2C |
| UserIntelligence | SaaS | Partial | Simulation engine; directional insights, not quantitative |
| Qualtrics Edge Audience | SaaS | No | Modeled audience layers; enterprise contract required |

## Templates & scripts
Profile generation + simulated interview runner (Python, inline):
```python
# synthetic_interview.py
import anthropic

client = anthropic.Anthropic()

def generate_profile(icp: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                f"Create a synthetic user profile for: {icp}. "
                "Include: name, age, role, company size, JTBD, tech comfort (1-5), "
                "top 3 frustrations, budget authority (yes/no). "
                "Be specific and internally consistent."
            )
        }]
    )
    return msg.content[0].text

def simulate_response(profile: str, question: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"You are this person:\n{profile}\n\n"
                f"Answer this research question as them: {question}\n"
                "If you feel neutral or positive, say so honestly. "
                "Do not manufacture enthusiasm."
            )
        }]
    )
    return msg.content[0].text
```

## Best practices
- Always label synthetic research outputs as "synthetic" in any document header; never present alongside real findings without clear separation
- Generate at least 5-8 profiles to detect uniformity bias; fewer profiles amplify the LLM's default persona
- Use adversarial prompting ("as a skeptical user, why would you NOT buy this?") to counteract positive bias
- Follow synthetic research immediately with 3-5 real user interviews before acting on findings
- Document the exact persona construction prompt — if results need to be reproduced or audited, the prompt is the methodology
- Retire personas every 6 months or after major market shifts; behavioral assumptions drift

## AI-agent gotchas
- Synthetic users are LLM personas — they encode training data biases, not your actual ICP's behavior; treat as directional only
- Agents may produce profiles that all share the same "frustrations" because the LLM defaults to common UX tropes; inject forced variation in the prompt
- Human-in-loop checkpoint required before synthetic findings influence product roadmap or budget decisions
- When an agent runs simulated interviews at scale (50+ profiles), the diversity of responses actually decreases — the LLM regresses to mean; use smaller batches with explicit diversity constraints
- Do not chain synthetic-user output directly into downstream agents (e.g., copy generation, pricing models) without human review; hallucinated preferences will propagate

## References
- https://www.syntheticusers.com/
- https://www.nngroup.com/articles/synthetic-users/ (NN/g critique)
- Aaru — https://www.aaru.ai/
- SyntheticAudience — https://syntheticaudience.ai/
- https://hbr.org/2023/10/the-danger-of-using-ai-generated-data-as-market-research (HBR, limitations)
