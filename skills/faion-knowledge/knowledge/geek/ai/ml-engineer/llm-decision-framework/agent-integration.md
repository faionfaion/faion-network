# Agent Integration — LLM Decision Framework

## When to use
- At the start of any AI feature design: choose the right architecture before writing code
- Evaluating whether to augment an existing LLM feature (RAG vs fine-tuning vs prompting)
- During cost optimization: deciding whether a fine-tuned cheaper model can replace an expensive general model
- When accuracy is inadequate: diagnosing if the root cause is knowledge, style, or reasoning
- Business justification for AI budget: quantify cost/benefit of each approach before committing

## When NOT to use
- Prototype in <1 day: default to prompt engineering, evaluate later
- Decision is already made by stakeholders — use the framework to document trade-offs, not re-litigate the decision
- Task is purely generative (creative writing, brainstorming) — no retrieval or fine-tuning applies
- No eval data exists: the framework assumes measurable accuracy targets; skip until you can measure

## Where it fails / limitations
- Framework assumes stable accuracy metrics exist; many teams skip eval and apply the framework subjectively
- Cost comparisons are point-in-time (2026 prices); LLM pricing drops 50-70% annually — re-evaluate yearly
- RAFT (fine-tuning + RAG hybrid) is theoretically optimal but operationally fragile; most teams over-estimate their ability to maintain it
- Fine-tuning ROI calculations often ignore ongoing maintenance cost (retraining on data drift)
- "Start with prompting" advice breaks down for tasks needing >10K-token context or >100 few-shot examples
- Framework does not cover model selection within a tier (GPT-4o vs Claude vs Gemini) — use a separate provider comparison

## Agentic workflow
A meta-agent applies this framework at the planning stage of a feature. It takes a requirements document as input, scores each approach against the decision matrix (data freshness, accuracy target, cost budget, latency requirement), and outputs a structured recommendation with rationale. The recommendation is then used to configure downstream subagents. For iterative improvement, the meta-agent monitors live metrics and re-triggers the decision framework when accuracy or cost thresholds drift beyond acceptable bounds.

### Recommended subagents
- `faion-sdd-executor-agent` — can apply the framework to populate the "architecture decision" section of a design doc

### Prompt pattern
```xml
<task>
  Evaluate the optimal LLM enhancement strategy for the following feature.
  Score each approach (prompting, RAG, fine-tuning) on:
  - data_freshness: does the LLM's training data cover the domain?
  - accuracy_target: required accuracy percentage
  - budget_usd_monthly: infrastructure budget
  - latency_ms: max acceptable p95 latency
  Output a JSON recommendation with approach, rationale, and next steps.
</task>
<feature>
  {feature_description}
</feature>
<constraints>
  data_freshness: {days_since_last_training_cutoff}
  accuracy_target: {target_pct}
  budget_usd_monthly: {budget}
  latency_ms: {latency}
</constraints>
```

```python
# Decision output schema
{
  "recommended_approach": "rag",           # "prompting" | "rag" | "fine-tuning" | "raft"
  "rationale": "Data changes daily, RAG provides freshness...",
  "estimated_monthly_cost_usd": 450,
  "accuracy_gap_risk": "low",              # "low" | "medium" | "high"
  "next_steps": ["Set up Qdrant", "Ingest documents", "Eval on 100 test cases"],
  "revisit_trigger": "accuracy < 90% or cost > $800/month"
}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ragas` | RAG evaluation metrics (faithfulness, relevancy) | `pip install ragas` / [docs](https://docs.ragas.io/) |
| `promptfoo` | Prompt A/B testing and eval framework | `npm install -g promptfoo` / [docs](https://www.promptfoo.dev/) |
| `langfuse` | Track accuracy/cost metrics per approach in production | `pip install langfuse` / [docs](https://langfuse.com/docs) |
| `openai` fine-tuning CLI | Prepare and submit fine-tuning jobs | `pip install openai` / [fine-tuning docs](https://platform.openai.com/docs/guides/fine-tuning) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Braintrust | SaaS | Yes | Eval platform; tracks accuracy across prompting/RAG/FT approaches |
| Langfuse | OSS + SaaS | Yes | A/B test prompts; track cost per approach in production |
| OpenAI Fine-Tuning | SaaS | Yes | GPT-4o-mini fine-tuning; ~$25/1M training tokens |
| Vertex AI (GCP) | SaaS | Yes | Gemini fine-tuning + enterprise RAG; complex setup |
| Qdrant Cloud | SaaS | Yes | Managed vector DB for RAG; $0 for <1GB |
| Ragas | OSS | Yes | RAG evaluation; run in CI to gate RAG quality |

## Templates & scripts
```python
# decision_matrix.py — score and recommend LLM approach (≤45 lines)
from dataclasses import dataclass

@dataclass
class FeatureRequirements:
    data_changes_daily: bool
    accuracy_target_pct: float        # e.g. 95.0
    budget_usd_monthly: float
    latency_p95_ms: int
    training_data_available: bool     # labeled examples for fine-tuning
    domain_vocabulary_specialized: bool

def recommend(req: FeatureRequirements) -> dict:
    scores = {"prompting": 0, "rag": 0, "fine_tuning": 0}

    if req.data_changes_daily:
        scores["rag"] += 3
        scores["fine_tuning"] -= 2  # stale without retraining

    if req.accuracy_target_pct > 95:
        scores["rag"] += 2
        scores["fine_tuning"] += 2
        scores["prompting"] -= 1

    if req.budget_usd_monthly < 200:
        scores["prompting"] += 3
        scores["rag"] -= 1
        scores["fine_tuning"] -= 3

    if req.latency_p95_ms < 500:
        scores["fine_tuning"] += 2  # no retrieval overhead
        scores["rag"] -= 1

    if req.domain_vocabulary_specialized and req.training_data_available:
        scores["fine_tuning"] += 2

    best = max(scores, key=scores.get)
    return {"recommendation": best, "scores": scores}

# Example:
# req = FeatureRequirements(True, 95.0, 300, 1500, False, False)
# print(recommend(req))  # → {"recommendation": "rag", ...}
```

## Best practices
- Always run the "start with prompting" step first and measure baseline accuracy before investing in RAG or fine-tuning
- Define accuracy metrics before choosing an approach — "good enough" without measurement leads to over-engineering
- RAG vs fine-tuning is not either/or: use RAG for knowledge, fine-tuning for style/format, RAFT for both
- For fine-tuning ROI: calculate break-even at `(fine-tuning cost) / (savings per 1M tokens * volume)` — often >6 months
- Re-evaluate the decision after 3 months: cost/quality curves change as LLM providers compete
- Document the decision in an Architecture Decision Record (ADR) with the scoring rationale — avoids revisiting without data
- Test RAG before fine-tuning: RAG is reversible and often matches fine-tuning accuracy at lower cost for knowledge tasks

## AI-agent gotchas
- Agents applying this framework tend to default to RAG for everything — prompt them to score prompting first
- The framework output (a recommendation) should be a human-in-loop checkpoint: agent proposes, human approves before infra is provisioned
- Cost estimates must use current provider pricing — training an agent on stale cost data produces wrong recommendations
- RAFT recommendation from an agent is almost always premature — it requires continuous retraining infra that most teams lack
- When the agent recommends fine-tuning, validate that sufficient labeled data exists (≥1000 examples) before proceeding

## References
- [RAG vs Fine-Tuning — Monte Carlo](https://www.montecarlodata.com/blog-rag-vs-fine-tuning/)
- [RAG vs Fine-Tuning 2026 — Kanerika](https://kanerika.com/blogs/rag-vs-fine-tuning/)
- [RAFT: Adapting Language Model to Domain Specific RAG](https://arxiv.org/abs/2403.10131)
- [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Ragas Evaluation Framework](https://docs.ragas.io/)
- [Promptfoo](https://www.promptfoo.dev/)
