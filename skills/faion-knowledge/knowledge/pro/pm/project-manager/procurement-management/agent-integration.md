# Agent Integration — Procurement Management

## When to use
- Defining a make-or-buy framework before engaging external vendors.
- Drafting Statement of Work (SOW), Master Services Agreement (MSA), Data Processing Addendum (DPA) skeletons.
- Running an RFI / RFP / RFQ process: vendor list, evaluation matrix, weighted scoring.
- Selecting contract type (Fixed Price / T&M / Cost Plus) for a defined scope and risk profile.
- Vendor risk + security review (SOC 2, ISO 27001, GDPR DPA) intake.
- Ongoing vendor management: SLA tracking, change requests, performance reviews.

## When NOT to use
- Spot purchases under PO threshold (e.g. < $5K) where formal procurement is overhead.
- Highly regulated industries with established central procurement / legal teams — this is procurement *light*; defer to org policy.
- SaaS tools the engineering team can self-onboard with monthly billing (still need security review, but not RFP).

## Where it fails / limitations
- "Lowest price wins" anti-pattern is hard to dislodge once finance owns scoring weights.
- SOW without acceptance criteria collapses into endless revisions.
- T&M contracts without a cap or burn-rate alert produce silent budget overruns.
- IP / data-ownership clauses are hand-waved by both sides until a dispute reveals them.
- Termination clauses ("for convenience" with notice + transition) often missing — locks in bad vendors.
- Cross-border procurement adds tax, FX, and data-residency complexity that single-jurisdiction templates miss.
- AI/ML vendor procurement: training-data rights, model output IP, and indemnity for IP infringement are 2024-2026 hot zones; old templates don't cover them.

## Agentic workflow
The agent is a structured-document generator and an evaluation calculator, not a negotiator. Useful surfaces: (1) draft SOW from a feature spec + acceptance criteria, (2) ingest vendor proposals (PDFs / Markdown) and produce a normalized comparison matrix, (3) compute weighted scores and surface dissents, (4) flag missing clauses against a checklist (IP, DPA, termination, audit, SLA, indemnity, AI-output rights). Every output goes to a human (PM, legal, finance) before sending to vendor.

### Recommended subagents
- A `sow-author` subagent (define inline) — emits SOW skeleton from spec + acceptance criteria; validates against clause checklist.
- A `proposal-normalizer` subagent — reads vendor proposals (PDF/MD), outputs canonical JSON: price, timeline, team, references, assumptions.
- A `vendor-scorer` subagent — given normalized proposals + scoring rubric YAML, outputs weighted matrix + sensitivity analysis.
- A `contract-clause-auditor` — diff received contract against checklist; flag missing / weakened clauses.

### Prompt pattern
```
Inputs: feature_spec.md, acceptance_criteria.md, contract_type_preference="fixed-price",
data_classifications=["PII","financial"], jurisdictions=["EU","US"].

Output a SOW with sections:
1. Background / objective (≤ 5 lines).
2. Scope (in / out, bulleted).
3. Deliverables table (id, name, format, due).
4. Acceptance criteria per deliverable.
5. Timeline (milestone, date, payment %).
6. Assumptions and dependencies.
7. Required clauses checklist status:
   IP assignment, DPA, sub-processor list, audit right, SLA, indemnity (incl. AI),
   termination for cause, termination for convenience, change process, warranty.
   For each: [present | missing | weak] with line reference.

Reject and ask for input if any field unspecified. Do NOT invent dollar figures.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert SOW Markdown → PDF / DOCX for vendor delivery | https://pandoc.org/ |
| `docusign-cli` / `dropbox-sign-cli` | Programmatic e-sign workflows | https://developers.docusign.com/ |
| `gh issue` / `jira-cli` | Procurement intake tickets | https://cli.github.com/ |
| `pdfplumber` (Python) | Extract structured fields from vendor PDFs | https://github.com/jsvine/pdfplumber |
| `cuelang` | Validate SOW JSON schema | https://cuelang.org/ |
| `gpg` | Sign final contracts / NDA exchanges | https://gnupg.org/ |
| `git` (procurement-as-code) | Version control for SOW / MSA templates | https://git-scm.com/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Coupa | SaaS (P2P) | Yes — REST | Enterprise; heavyweight |
| SAP Ariba | SaaS (P2P) | Yes — REST | Enterprise; SAP-aligned |
| Procurify | SaaS | Yes — REST | Mid-market |
| Tropic | SaaS | Yes — REST | SaaS-spend negotiation focus |
| Vendr | SaaS | Yes — REST | SaaS procurement assistant |
| Sastrify / Cledara | SaaS | Yes — REST | SaaS cost + contract management |
| Ironclad / LinkSquares / Lexion | SaaS (CLM) | Yes — REST | Contract lifecycle, AI clause review |
| DocuSign / Dropbox Sign / Adobe Sign | SaaS (e-sign) | Yes — REST | Final signature step |
| Vanta / Drata / Whistic | SaaS (vendor risk) | Yes — REST | Security questionnaire automation |
| OneTrust / TrustArc | SaaS (privacy) | Yes — REST | DPA + sub-processor inventory |
| Notion / Confluence | SaaS | Yes — REST | Procurement docs hub |

## Templates & scripts
See `templates.md` for SOW, evaluation matrix, MSA. Inline: weighted scoring with sensitivity (Python).

```python
#!/usr/bin/env python3
import json, sys, statistics
def score(proposals, weights):
    out = []
    for p in proposals:
        total = sum(weights[k] * p["scores"][k] for k in weights)
        out.append({"vendor": p["vendor"], "score": round(total, 2)})
    return sorted(out, key=lambda x: -x["score"])
def sensitivity(proposals, weights, delta=0.1):
    """Re-score with each weight ±delta to find rank stability."""
    bumps = []
    for k in weights:
        for d in (-delta, delta):
            w2 = dict(weights); w2[k] = max(0, w2[k] + d)
            s = sum(w2.values())
            w2 = {kk: vv / s for kk, vv in w2.items()}
            bumps.append((k, d, score(proposals, w2)[0]["vendor"]))
    return bumps
if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    base = score(data["proposals"], data["weights"])
    print("ranking:", json.dumps(base, indent=2))
    print("sensitivity:", json.dumps(sensitivity(data["proposals"], data["weights"]), indent=2))
```

## Best practices
- Score on weighted criteria with the rubric *published before* proposals arrive. Retroactive weights = bias laundering.
- Use sensitivity analysis: if rank flips with a 10% weight change, the choice is not robust — re-evaluate.
- Always include the "do nothing" or "build internally" option in the matrix; otherwise procurement is a forced choice.
- Tie payments to acceptance of deliverables, not calendar dates. 25/50/25 with milestone gating is a good default for fixed-price.
- T&M contracts: enforce a hard cap and a weekly burn-rate report; trigger a change request at 70% of cap.
- Mandatory clauses checklist (do not let any contract bypass): IP assignment, sub-processor disclosure, DPA (if PII), termination-for-convenience with reasonable notice, audit right, SLA with credits (not just promises), indemnity (incl. open-source license + AI-output IP), warranty period.
- Maintain an approved-vendor list with security review status; expire reviews annually.
- Capture lessons-learned per vendor in a structured field; informs next RFP.

## AI-agent gotchas
- LLM-generated SOWs hallucinate "industry standard" clauses that don't exist; force a clause checklist input, not free-form drafting.
- Numeric extraction from vendor PDFs is brittle — currency symbols, footnotes, "+ taxes", "ex-GST" — agent often normalizes wrong. Always present extracted numbers next to the source string for human verify.
- Scoring agents that pick a winner without sensitivity analysis create false confidence. Mandate sensitivity output.
- Indemnity / liability cap clauses are minefields — agents weaken them without flagging. Run a dedicated `clause-auditor` over the final contract.
- AI-vendor procurement: agent forgets to ask about training-data rights, model output IP, prompt logging, opt-out from training. Add explicit checklist.
- DPA / GDPR: sub-processor list must be enumerated and updated; agents emit "TBD" and the gap ships to legal.
- Currency / FX: vendor quotes in EUR, internal budget in USD, agent compares directly. Always normalize and label.
- E-sign workflows: never let an agent dispatch DocuSign envelopes autonomously to vendors. Human gate before send.
- LLMs over-trust references the vendor provided; reference checks must be independent, not summarized from the proposal.

## References
- PMBOK Guide 7th Ed. — Delivery Performance Domain (Procurement) — https://www.pmi.org/pmbok-guide-standards
- ISO 20400 (Sustainable Procurement) — https://www.iso.org/standard/63026.html
- IACCM / WorldCC — https://www.worldcc.com/
- "Getting to Yes" (Fisher, Ury) — negotiation foundation
- AI vendor procurement guidance, Stanford HAI — https://hai.stanford.edu/
- GDPR DPA model clauses — https://commission.europa.eu/law/law-topic/data-protection/
- AICPA SOC 2 vendor review — https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2
