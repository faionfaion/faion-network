# Agent Integration — Procurement Management (PM Traditional)

## When to use
- Make-or-buy decisions: agent compares total cost of ownership (TCO) of internal build vs vendor across cost, control, speed, expertise, risk.
- Drafting Statement of Work (SOW) skeletons from a scope doc, with explicit deliverables, acceptance criteria, and milestones.
- Preparing RFI / RFP / RFQ packages and weighted vendor evaluation matrices.
- Selecting contract type (FFP, T&M, T&M with cap, CPFF, CPIF) given scope clarity and risk allocation.
- Vendor performance monitoring: tracking deliverables vs SOW, invoice reconciliation, milestone sign-off.
- Solopreneur freelancer / agency engagement at small scale (single SOW, fixed price, milestone-based).

## When NOT to use
- One-off micro-purchases (sub-$1k SaaS, single contractor day) — overhead exceeds value, use a credit card and a Slack receipt.
- Open-source dependencies where there is no vendor relationship; treat as supply-chain risk, not procurement.
- Internal cross-charging between business units — uses transfer pricing, not procurement contracts.
- Highly regulated procurements (defence, public sector) where bespoke FAR/DFARS/EU directives apply; the methodology omits regulatory clauses.

## Where it fails / limitations
- Weighted scoring matrix is anchorable: change one weight by 5% and the winner flips. Sensitivity analysis is rarely shown.
- LLMs draft SOW boilerplate that lacks jurisdiction-specific clauses (limitation of liability cap, indemnification scope, data-residency); legal review is non-negotiable.
- Make-vs-buy ignores transition cost (knowledge transfer, vendor lock-in, switching cost) which often exceeds the cost delta.
- Fixed-price contracts incentivise vendors to minimise scope; buyers chronically under-define acceptance criteria, creating disputes the methodology won't catch.
- "References" criterion at 5-10% weight is gameable; agents cannot verify reference quality from text alone.
- Procurement methodology assumes one buyer, one vendor; multi-supplier / partner ecosystems (alliances, prime + sub) need different framing.
- Currency and FX terms are missing; cross-border SOWs need price adjustment clauses.

## Agentic workflow
The agent is a procurement document drafter and evaluator. Inputs: scope doc + budget + risk profile → outputs SOW, RFP, evaluation matrix, draft contract clause set. A second agent ingests vendor responses (PDF / DOCX) and emits a side-by-side comparison + scored matrix. A third agent monitors live engagements (deliverable status, invoice variance) and flags drift. Humans own all final selections, contract signatures, and dispute escalation.

### Recommended subagents
- `sow-drafter` — turns scope doc into SOW skeleton with deliverables, acceptance criteria, milestones, payment schedule.
- `rfp-builder` — composes RFP package (background, scope, requirements, response format, evaluation criteria, timeline).
- `proposal-comparator` — ingests vendor PDFs, normalises against RFP fields, outputs matrix.
- `vendor-monitor` — reads invoices + status reports + milestone deliverables, emits health RAG and variance flags.
- `make-vs-buy-analyst` — TCO model with switching cost and lock-in factor.

### Prompt pattern
```
Inputs:
- scope.md: business need + functional requirements
- budget_usd: cap
- timeline: weeks_to_kickoff, target_delivery
- risk_profile: low|medium|high (drives contract type)
- jurisdictions: ["US-CA", "EU-DE", ...]

Output JSON:
{ "recommended_contract_type": "FFP|T&M|T&M_cap|CPFF|CPIF",
  "rationale": "...",
  "sow": { "scope_in":[...], "scope_out":[...],
           "deliverables":[{id,name,acceptance_criteria,due}],
           "milestones":[{name,date,payment_pct}] },
  "rfp": { "evaluation_criteria":[{name,weight}],
           "response_format": {...} },
  "required_legal_clauses": ["IP", "indemnity", "LoL cap",
                             "data residency", "termination", "audit"],
  "open_questions_for_legal": [...] }

Rules:
- Always flag legal review required.
- No invented vendor names.
- For risk_profile=high, prefer FFP only if scope is ≥80% defined.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pdfplumber` / `pypdf` | Parse vendor proposals + invoices | https://github.com/jsvine/pdfplumber |
| `pandoc` | Convert SOW markdown → DOCX/PDF for signature workflow | https://pandoc.org/ |
| `git` + `git-lfs` | Version-control SOW + redlines | https://git-lfs.com/ |
| `docusign-cli` (community) | Send SOW for signature | https://developers.docusign.com/ |
| `openpyxl` | Generate evaluation matrix in Excel | https://openpyxl.readthedocs.io/ |
| `xmllint` | Validate UBL / e-invoicing XML | https://gnome.pages.gitlab.gnome.org/libxml2/ |
| `currency-converter` | FX for multi-jurisdiction SOWs | ECB / OpenExchangeRates |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Coupa | SaaS | Yes — REST | Enterprise procure-to-pay |
| SAP Ariba | SaaS | Yes — REST/SOAP | Source-to-pay, sourcing events |
| Ivalua | SaaS | Yes — REST | Spend management |
| Procurify / Tropic | SaaS | Yes — REST | SaaS-spend management for SMB |
| Vendr / Sastrify | SaaS | Yes — API | SaaS contract negotiation as a service |
| DocuSign / PandaDoc | SaaS | Yes — REST | Contract signing |
| Ironclad / LinkSquares | SaaS | Yes — REST | CLM (contract lifecycle management) with AI clause extraction |
| Bill.com | SaaS | Yes — REST | Invoice + payment automation |
| Spendesk / Ramp | SaaS | Yes — REST | Card + invoice spend |
| Notion / Confluence | SaaS | Yes — REST | SOW templates |

## Templates & scripts
See `templates.md` for SOW + evaluation matrix. Vendor scoring snippet (~30 lines):

```python
def score(criteria, vendors):
    """criteria: [{name, weight 0-1}]; vendors: {name: {crit_name: 1-5 score}}"""
    if abs(sum(c["weight"] for c in criteria) - 1.0) > 0.01:
        raise ValueError("weights must sum to 1.0")
    out = {}
    for v, scores in vendors.items():
        out[v] = round(sum(c["weight"] * scores[c["name"]] for c in criteria), 3)
    # sensitivity: flip top 2 if any weight ±10%
    sorted_v = sorted(out.items(), key=lambda x: -x[1])
    margin = sorted_v[0][1] - sorted_v[1][1] if len(sorted_v) > 1 else 1
    return {"scores": out, "winner": sorted_v[0][0],
            "margin": margin, "robust": margin > 0.3}
```

## Best practices
- Always pair FFP with a strong change-control clause; without it, fixed price becomes "vendor minimises scope".
- T&M needs a NOT-TO-EXCEED cap and weekly burn report; uncapped T&M is open-ended risk.
- Require references AND a reference-call rubric — references are positive bias unless interviewed structured.
- Negotiate exit terms before signing: notice period, data hand-back, transition assistance, IP transfer. Trapped-buyer is the most common procurement failure mode.
- Tie payment to acceptance, not to milestones — milestone-based payment without acceptance criteria is "pay for activity, not value".
- Build a vendor scorecard quarterly (on-time delivery %, defect rate, escalation count). Renew or churn based on data, not relationship.
- Keep an MSA + SOW model: MSA covers legal terms once, SOWs add scope per engagement. Avoids re-negotiating IP/indemnity each time.

## AI-agent gotchas
- Legal clauses are jurisdiction-specific; LLMs default to US-style clauses and miss EU GDPR processor terms, UK MAC clauses, German UWG provisions.
- Indemnification caps drift: agents draft "uncapped" indemnification by default — require explicit cap (often 1x or 2x annual fees).
- Data residency / sub-processor language is missing from generic LLM SOW templates; mandatory for GDPR, HIPAA, SOC 2 buyers.
- Currency drift in multi-region SOWs: agents put a USD figure in a EU SOW without an exchange clause; demand price-adjustment language.
- Make-vs-buy bias: agents tend to recommend "buy" for software (training data favours SaaS marketing); explicitly weight switching cost and IP ownership.
- Vendor-name hallucination is common in shortlist drafting; always require a user-supplied vendor list, never let the agent invent.
- Evaluation matrix can be reverse-engineered: if you tell an LLM the answer, it will weight the criteria to justify it. Lock weights before scoring.
- Acceptance criteria written by agents are often subjective ("high quality"); demand testable criteria (% test coverage, defect density, response time).

## References
- PMI PMBOK Guide 6th Ed., Chapter 12 — Project Procurement Management.
- ISO 20400:2017 — Sustainable Procurement.
- ICCRC/IACCM Contract Management Body of Knowledge.
- World Commerce & Contracting (WCC) Standards.
- US FAR (Federal Acquisition Regulation) for public-sector context.
- "The Vendor Management Office" (Joe Auer) — supplier scorecards.
- a16z, "How to Buy SaaS at a Startup" — practical SMB procurement.
