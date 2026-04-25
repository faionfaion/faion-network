# Agent Integration — AI-Enabled Business Analysis (BA Core)

## When to use
- Integrating AI tools into core BA workflows: requirements extraction, stakeholder analysis, process discovery, and documentation generation
- Defining the BA competency requirements for an AI initiative: AI opportunity identification, AI requirements specification, AI TRiSM management
- Applying the AI TRiSM (Trust, Risk, and Security Management) framework to an AI project before it enters development
- Establishing the BA's role in an agentic system: defining agent boundaries, human oversight requirements, and escalation criteria
- Generating structured BA deliverables (requirements registers, gap analyses, acceptance criteria) from unstructured source material
- Identifying AI adoption opportunities within a business domain and building the business case for AI integration

## When NOT to use
- The project has no AI component — use standard BA core methodologies (requirements elicitation, process modeling, stakeholder analysis) without the AI overlay
- Domain expertise is the primary bottleneck — AI tools accelerate BA documentation work, not domain knowledge acquisition; if the BA lacks domain knowledge, AI tools will produce confident-sounding but incorrect outputs
- Data governance has not been established for feeding organizational documents and stakeholder communications to external AI models
- The BA's primary output for the project is a workshop facilitation or a negotiated agreement — AI adds marginal value in real-time human engagement contexts

## Where it fails / limitations
- AI-extracted requirements lack the implicit knowledge that experienced BAs surface through follow-up questions; the extraction is as good as the source documents, which are rarely complete
- The AI TRiSM framework assessment requires organizational context (existing data governance, security controls, accountability structures) that an agent cannot infer without explicit input
- 60% of AI project failures trace to poor data quality — if the BA does not perform a data quality assessment early, the AI initiative requirements will be correct on paper but undeliverable in practice
- By 2028, 40% of generative AI interactions will use autonomous agents (Gartner) — this projection is driving demand for BA skills in agentic system specification, but most BA practitioners lack training in agent boundary definition and escalation design
- AI-generated acceptance criteria are often too coarse to be testable without human refinement; they describe the happy path but miss edge cases, negative cases, and performance thresholds
- Process mining (data-driven process discovery) requires structured event logs that many organizations do not have; without event log data, AI-powered process discovery falls back to document analysis

## Agentic workflow
A requirements-extraction subagent processes source documents and produces a structured requirements register. A compliance subagent applies the AI TRiSM framework and flags missing governance elements. An acceptance-criteria subagent generates testable ACs for each functional requirement. An agentic-system-spec subagent produces the agent boundary document when the project involves an autonomous AI system. All outputs are reviewed by a BA before being finalized. For ongoing AI initiative work, a monitoring-spec subagent generates the continuous improvement and performance monitoring plan.

### Recommended subagents
- `requirements-extractor` — processes source documents (PDFs, Word, transcripts) and returns structured requirements with source references
- `ai-trsim-reviewer` — applies AI TRiSM framework; outputs trust/risk/security gap table for the AI initiative
- `ac-writer` — generates Given/When/Then acceptance criteria for each functional requirement; flags requirements that are too vague to test
- `agent-boundary-definer` — for agentic AI initiatives, produces the agent boundary specification: autonomous actions, human oversight checkpoints, escalation triggers, decision rules

### Prompt pattern
```
You are a business analyst. Given this AI initiative description, apply the
AI TRiSM framework (Trust, Risk, Security Management) and produce:

1. Risk classification (unacceptable / high / limited / minimal risk per EU AI Act)
2. Trust gaps: where is AI bias, explainability, or fairness not addressed?
3. Risk controls: what oversight mechanisms are missing?
4. Security gaps: what data protection or adversarial attack risks are unaddressed?

Format as a gap table: Category | Gap | Severity (High/Medium/Low) | Recommended Control

AI Initiative: {initiative_description}
Existing controls: {existing_controls}
```

```
You are a business analyst specifying an agentic AI system.
Given the system description, produce the agent boundary specification:

1. Autonomous actions (what the agent may do without human approval)
2. Human oversight checkpoints (which decisions require human approval before proceeding)
3. Escalation triggers (conditions that pause the agent and alert a human)
4. Decision rules (the logic the agent follows to choose between actions)
5. Rollback conditions (when and how the system reverts to human operation)

System description: {system_description}
Business context: {business_context}
Regulatory constraints: {constraints}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude for long-context document analysis and structured output generation | `pip install anthropic` / https://docs.anthropic.com |
| `pdfplumber` | Extract text from PDF source documents | `pip install pdfplumber` / https://github.com/jsvine/pdfplumber |
| `pm4py` | Process mining from structured event logs | `pip install pm4py` / https://pm4py.fit.fraunhofer.de |
| `python-docx` | Read and write Word documents for BA artifact generation | `pip install python-docx` / https://python-docx.readthedocs.io |
| `jira` (Python) | Create/update Jira issues from extracted requirements | `pip install jira` / https://jira.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | 200K context; best for large document corpora (RFPs, contracts) |
| OpenAI API | SaaS | Yes | GPT-4o with response_format for schema-enforced structured output |
| Jira | SaaS | Yes (REST API) | Requirements as issues; agents create/update via REST |
| Confluence | SaaS | Partial | BA artifact storage; page creation via API but limited formatting control |
| Notion | SaaS | Yes (API) | Requirements and BA artifacts; more flexible than Confluence for agent writes |
| PM4Py | OSS | Yes | Process mining; Python-native, integrates directly into agent pipelines |
| Miro | SaaS | Partial | Process and requirements visualization; API limited for agent-driven creation |

## Templates & scripts
See `templates.md` for the AI Initiative Requirements Checklist and AI TRiSM gap table templates.

AI TRiSM gap assessment (lightweight version):
```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class TRiSMGap:
    category: Literal["Trust", "Risk", "Security"]
    gap: str
    severity: Literal["High", "Medium", "Low"]
    recommended_control: str

def assess_trism_gaps(initiative_description: str) -> list[TRiSMGap]:
    """
    Call Claude to assess AI TRiSM gaps for the given initiative.
    Returns list of gaps for BA review.
    """
    import anthropic, json
    client = anthropic.Anthropic()
    prompt = f"""
Assess this AI initiative against the AI TRiSM framework.
Return JSON array where each item has:
- category: Trust | Risk | Security
- gap: description of the gap
- severity: High | Medium | Low
- recommended_control: specific control to address the gap

Initiative: {initiative_description}
"""
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    gaps_data = json.loads(resp.content[0].text)
    return [TRiSMGap(**g) for g in gaps_data]
```

## Best practices
- Include data quality assessment as a mandatory early deliverable on every AI initiative — the checklist in the README is a good starting point, but adapt it to the specific data sources the AI system will use
- Always produce traceability from requirements to source document; this is a core BA practice and becomes even more important for AI initiatives where stakeholders will challenge AI-generated requirements
- For agentic system specifications, define the escalation criteria before the happy-path behavior; the escalation design is what enables organizational trust in the autonomous system
- Use Claude (200K context) for multi-document requirements extraction; process the full document corpus in one call rather than chunking, to avoid missing cross-document dependencies
- When applying AI TRiSM, engage a security professional for the security management column — BA practitioners can identify trust and risk gaps but may miss technical adversarial attack vectors

## AI-agent gotchas
- Human-in-the-loop checkpoint: no AI-extracted requirements document should enter the project's official requirements baseline without BA review — agents produce first drafts, not final deliverables; the BA is accountable for the output
- Agent boundary specifications for agentic systems are not complete without escalation triggers that cover model failures (e.g., low confidence, unexpected tool output, context window exhaustion) — purely business-logic-based escalations miss the technical failure modes
- AI TRiSM assessment quality depends on organizational context that agents cannot observe — prompt the agent explicitly with existing controls, data governance policies, and accountability structures to get a useful gap analysis rather than a generic checklist
- For AI initiative requirements that involve personal data, the BA must include data privacy impact assessment (DPIA) requirements explicitly — agents typically do not surface DPIA obligations without being prompted, and the omission creates a compliance risk

## References
- https://docs.anthropic.com/en/docs (Claude API — 200K context for large documents)
- https://www.gartner.com/en/articles/ai-trism (Gartner AI TRiSM — trust, risk, security management)
- https://pm4py.fit.fraunhofer.de (process mining)
- https://www.iiba.org (IIBA BA competency model with AI competencies)
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai (EU AI Act — risk classification)
- https://pdfplumber.readthedocs.io (PDF extraction for BA document processing)
