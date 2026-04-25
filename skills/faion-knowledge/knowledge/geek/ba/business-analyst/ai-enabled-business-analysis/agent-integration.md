# Agent Integration — AI-Enabled Business Analysis

## When to use
- Extracting requirements from large document corpora (contracts, meeting transcripts, policy documents) where manual reading is impractical
- Performing stakeholder sentiment analysis on communication logs, survey responses, or interview transcripts before requirements prioritization
- Generating first-draft requirements documents, process flows, or gap analysis reports that a BA then reviews and refines
- Validating AI system requirements against the AI TRiSM framework (trust, risk, security management) before a project proceeds
- Defining agent boundaries, escalation rules, and human oversight requirements for an agentic AI initiative being analyzed as a BA
- Accelerating repetitive BA documentation tasks: acceptance criteria writing, RACI matrices, glossary generation

## When NOT to use
- Requirements involve highly sensitive stakeholder dynamics (political, interpersonal conflict) where AI analysis of communications would be inappropriate or ethically problematic
- Domain is too specialized for the model's training (e.g., proprietary financial instruments, classified government processes) — model hallucinations on domain terms produce plausible-but-wrong requirements
- Organization has not assessed data privacy obligations for feeding stakeholder communications to an external AI model
- The BA role in the project is primarily facilitation (workshops, negotiations) rather than document analysis — AI adds little value in real-time human facilitation

## Where it fails / limitations
- NLP-based requirements extraction misses implicit or unstated requirements that an experienced BA would surface through questioning; treat AI-extracted requirements as a starting point, not a complete list
- Sentiment analysis on formal business documents is less reliable than on consumer text; stakeholders in corporate settings communicate strategically, not emotionally
- Process mining requires structured event log data (timestamp, case ID, activity); if the organization does not have this data, process discovery is limited to document analysis
- AI-generated acceptance criteria often lack testability specifics; they need human review to add precise thresholds, edge cases, and negative test cases
- 60% of AI projects fail due to poor data quality (per the README) — BA work on AI initiatives must explicitly include data quality assessment, not just functional requirements
- AI TRiSM compliance assessment requires organizational context (data governance structure, existing controls) that an agent cannot infer from documents alone

## Agentic workflow
Use a requirements-extraction subagent to process source documents (contracts, transcripts, RFPs) and produce a structured list of functional and non-functional requirements. A gap-analysis subagent then compares extracted requirements against an existing system spec or as-is process description and produces a structured gap report. A separate compliance-check subagent applies the AI TRiSM framework to any AI-specific requirements and flags missing governance elements. All outputs go to a BA for review before being written into the project's requirements baseline.

### Recommended subagents
- `requirements-extractor` — reads source documents, applies NLP extraction, returns structured requirement candidates with source references
- `gap-analyzer` — compares current-state requirements or process description against target-state spec; outputs structured gap table
- `ac-writer` — generates acceptance criteria for each functional requirement in Given/When/Then or structured table format
- `ai-trsim-reviewer` — applies AI TRiSM framework to AI initiative requirements; flags missing trust, risk, and security controls

### Prompt pattern
```
You are a business analyst. Extract all functional and non-functional requirements
from the document below.

For each requirement:
- Assign a unique ID (REQ-001, REQ-002, ...)
- Classify: Functional | Non-Functional | Constraint | Assumption
- Note the source sentence/paragraph
- Flag ambiguity (yes/no) with a one-line explanation if ambiguous

Document:
{document_text}
```

```
Perform a gap analysis. Given the current-state process description and the
target-state requirements, identify:
1. Gaps: requirements in the target state not addressed in the current state
2. Conflicts: current-state elements that contradict target-state requirements
3. Redundancies: current-state elements not referenced in the target state

Format as a table: ID | Type | Description | Priority (High/Medium/Low)

Current state: {current_state}
Target state requirements: {requirements_list}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude for requirements extraction, gap analysis, AC writing | `pip install anthropic` / https://docs.anthropic.com |
| `pypdf2` / `pdfplumber` | Extract text from PDF source documents before NLP processing | `pip install pdfplumber` / https://github.com/jsvine/pdfplumber |
| `pm4py` | Process mining from event logs; structural process discovery | `pip install pm4py` / https://pm4py.fit.fraunhofer.de |
| `spacy` | Local NLP preprocessing (sentence splitting, entity extraction) before LLM call | `pip install spacy` / https://spacy.io |
| `docx2txt` | Extract text from Word documents for requirements source processing | `pip install docx2txt` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Best for long-context document analysis; 200K context handles large RFPs |
| OpenAI API | SaaS | Yes | GPT-4o for structured output extraction; response_format enforces schema |
| Notion | SaaS | Yes (API) | Requirements documentation; BA agents write structured outputs here |
| Confluence | SaaS | Partial | BA artifact storage; API supports page creation but formatting is limited |
| Jira | SaaS | Yes (API) | Requirements as issues; agents can create/update Jira issues via REST API |
| PM4Py | OSS | Yes | Process mining; integrates with Python agent pipelines |
| LACE (IBM) | SaaS | No | Enterprise process discovery; API not agent-friendly |

## Templates & scripts
See `templates.md` for the AI Initiative Requirements Checklist and gap analysis table templates.

Document batch processor for requirements extraction:
```python
import pdfplumber
import anthropic
import json

def extract_requirements_from_pdf(pdf_path: str) -> list[dict]:
    """Extract requirements from a PDF document using Claude."""
    # Extract text
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": f"""
Extract all requirements from this document. Return JSON array where each item has:
- id (REQ-001, REQ-002, ...)
- type (Functional|Non-Functional|Constraint|Assumption)
- description (the requirement text)
- source (verbatim source sentence)
- ambiguous (true/false)

Document:
{text[:50000]}
"""}],
    )
    return json.loads(resp.content[0].text)
```

## Best practices
- Always include a source reference for each AI-extracted requirement — traceability to the source document is a core BA practice and enables validation disputes to be resolved quickly
- Use Claude for long-context document analysis (200K context); switch to Gemini 2.5 Pro for very large document sets (contracts over 200K tokens or multi-document corpora)
- AI-generated acceptance criteria should be reviewed against the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable) before adding to a backlog
- For AI initiative BA work, always start with the data quality assessment before requirements elicitation — a well-specified AI system on poor-quality data delivers no value
- Run the AI TRiSM review subagent on every AI initiative regardless of perceived risk level; organizations that skip governance steps on "low-risk" AI systems consistently encounter compliance issues post-launch

## AI-agent gotchas
- Requirements extraction agents hallucinate implicit requirements that were not stated in the source document — every agent-extracted requirement must be traceable to a specific source passage; any requirement without a source is suspect
- Human-in-the-loop checkpoint: all agent-generated requirements documents must be reviewed by a qualified BA before being added to the project's official requirements baseline; agents accelerate drafting, they do not replace BA judgment
- Sentiment analysis on stakeholder communications must be disclosed to stakeholders if the organization's data governance policy requires it; running NLP on employee or customer communications without appropriate consent is a data privacy risk
- For AI initiative requirements, the agent must surface the "BA role in agentic systems" items explicitly: agent boundaries, decision rules, human oversight requirements, and escalation criteria — these are frequently missing from initial requirement drafts and create governance gaps later

## References
- https://docs.anthropic.com/en/docs (Claude API — long context document analysis)
- https://www.gartner.com/en/articles/ai-trism (Gartner AI TRiSM framework)
- https://pm4py.fit.fraunhofer.de (process mining)
- https://pdfplumber.readthedocs.io (PDF text extraction)
- https://www.iiba.org/professional-development/career-centre/business-analysis-competency-model/ (IIBA BA competency model with AI competencies)
