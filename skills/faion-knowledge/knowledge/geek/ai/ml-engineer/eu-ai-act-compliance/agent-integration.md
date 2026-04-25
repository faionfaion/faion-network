# Agent Integration — EU AI Act Compliance

## When to use
- Building or deploying an AI system for EU markets after August 2024
- Any system that processes biometrics, employment decisions, credit scoring, education admissions, or critical infrastructure — all are Annex III high-risk
- Deploying a GPAI (General Purpose AI) model with > 10^25 FLOPs training compute (systemic risk tier)
- Integrating third-party LLM APIs into a product where the provider's compliance does not cover downstream obligations
- Conducting compliance gap analysis before a product launch in EU

## When NOT to use
- Products deployed exclusively outside EU with no EU users or EU-based processing — Act does not apply
- Purely internal tools with no impact on individuals' rights or safety (minimal risk tier)
- Research and development activities exempt under Article 2(6) — testing in labs does not require compliance
- Open-source models released without commercial intent may have reduced obligations (verify per Article 2(12))

## Where it fails / limitations
- Risk classification is ambiguous for novel AI applications — the Act provides categories but edge cases require legal counsel
- Technical documentation requirements are extensive (Article 11) but the required level of detail is still being refined by EU bodies
- GPAI systemic risk rules (> 10^25 FLOPs) exclude most SME deployments but the threshold may change
- Conformity assessment for high-risk systems requires third-party audit for some categories — cannot be self-certified
- AI Act enforcement mechanisms vary by member state; penalties are national authority decisions, not EU Commission
- Prohibited practices list (Article 5) is broadly worded — agents generating persuasive content or behavioral profiling may inadvertently fall in scope

## Agentic workflow
Compliance tasks are best handled by dedicated Opus-class agents given the legal reasoning complexity. A compliance agent runs in three phases: inventory (discover all AI systems), classify (map each to a risk tier using the Annex III checklist), and document (generate required technical documentation and conformity declarations). Human review is mandatory at the classification and final documentation steps — agents produce drafts, humans approve. The agent should flag ambiguous cases for legal review rather than making a binary determination.

### Recommended subagents
- `faion-sdd-executor-agent` — when compliance work is tracked as an SDD feature with tasks and approvals
- Opus-class Claude subagent — for legal/regulatory interpretation tasks (classification, gap analysis)

### Prompt pattern
```xml
<compliance-classification>
  <role>EU AI Act risk classification expert</role>
  <system-description>{description_of_ai_system}</system-description>
  <task>
    1. Identify the primary use case and affected individuals
    2. Check against Article 5 (prohibited practices)
    3. Check against Annex III (high-risk categories)
    4. Determine if GPAI model obligations apply
    5. Output: risk_tier (prohibited|high|limited|minimal), confidence (low|medium|high),
       rationale, and list of applicable articles
    6. Flag ambiguities requiring legal review
  </task>
</compliance-classification>
```

```python
# Compliance checklist runner — structured output from LLM
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": f"Classify this AI system under EU AI Act:\n{system_description}"
    }],
    system="You are an EU AI Act compliance specialist. Always cite specific articles."
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `presidio-analyzer` | PII detection for data documentation | `pip install presidio-analyzer` · microsoft.github.io/presidio |
| `evidently` | Data/model monitoring for ongoing compliance | `pip install evidently` · evidentlyai.com |
| `mlflow` | Experiment tracking for technical documentation | `pip install mlflow` · mlflow.org |
| `fairlearn` | Bias/fairness assessment for Annex III requirements | `pip install fairlearn` · fairlearn.org |
| `alibi-detect` | Data drift detection for high-risk monitoring | `pip install alibi-detect` · alibi-detect.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| FRIA.ai | SaaS | Partial (web UI) | Fundamental Rights Impact Assessment tool |
| Credo AI | SaaS | Yes — API | Governance platform; policy-as-code; EU AI Act modules |
| Holistic AI | SaaS | Partial | Risk assessment and auditing platform |
| Arthur AI | SaaS | Yes — REST API | Model monitoring; bias detection; audit trails |
| Weights & Biases | SaaS/OSS | Yes — Python SDK | Experiment tracking; technical documentation support |
| EU AI Act sandbox | Gov | No | National regulatory sandboxes per Article 57 |

## Templates & scripts
See `templates.md` for:
- Technical documentation template (Article 11 requirements)
- Conformity declaration template for high-risk systems
- GPAI transparency disclosure template (Article 53)

Inline: risk classification decision matrix (agent-readable):

```python
ANNEX_III_CATEGORIES = {
    "biometrics": ["remote identification", "emotion recognition", "categorization"],
    "critical_infrastructure": ["energy", "transport", "water", "digital infra"],
    "education": ["admissions", "assessment", "proctoring", "dropout prediction"],
    "employment": ["recruitment", "performance evaluation", "promotion", "termination"],
    "essential_services": ["credit scoring", "insurance", "emergency dispatch"],
    "law_enforcement": ["risk assessment", "crime prediction", "polygraph"],
    "migration": ["visa", "asylum", "border control"],
    "justice": ["legal research", "dispute resolution", "judicial decisions"],
}

PROHIBITED_PRACTICES = [
    "subliminal manipulation",
    "exploitation of vulnerable groups",
    "social scoring by public authorities",
    "real-time remote biometric ID in public spaces (with exceptions)",
    "predictive policing based on profiling",
    "emotion recognition in workplace/education",
    "untargeted facial recognition database scraping",
]
```

## Best practices
- Conduct risk classification before architectural decisions — it is cheaper to design for compliance than retrofit
- Document the training data lineage and quality measures from day one — Article 10 requires it for high-risk systems
- Implement human oversight mechanisms (Article 14) as first-class features, not afterthoughts — UI, audit log, override capability
- Keep a version-controlled technical file (Article 11) alongside the model artifacts — update it with every model change
- Register high-risk AI systems in the EU database (Article 71) before deployment, not after
- For GPAI models, publish model cards and capability evaluations before releasing via API or open source

## AI-agent gotchas
- Agents performing automated compliance classification must not make final binding determinations — output is advisory, human signs off
- LLM hallucination is particularly dangerous in compliance contexts — agents must cite specific articles and flag when they are uncertain
- Compliance documentation generated by agents must be reviewed by a human with legal authority — automated drafts cannot substitute for legal review
- Agents that help users find loopholes in the Act may themselves violate the spirit of Article 5 (manipulative AI) — always flag rather than advise workarounds
- The Act's requirements evolve (implementing acts, delegated acts) — agent knowledge cutoff may lag behind regulatory updates; always recommend checking official EUR-Lex sources

## References
- https://artificialintelligenceact.eu/ (official consolidated text)
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 (Official Journal)
- https://trilateralresearch.com/responsible-ai/eu-ai-act-implementation-timeline-mapping-your-models-to-the-new-risk-tiers
- https://www.credo.ai/eu-ai-act
- https://fairlearn.org/
