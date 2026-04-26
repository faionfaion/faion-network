# Agent Integration — Legal Basics

## When to use
- Pre-launch legal foundation for a new SaaS / info-product / service: entity choice, ToS, Privacy Policy, IP basics.
- Drafting first-version contracts (customer agreement, contractor agreement, NDA, affiliate agreement) from templates.
- Quick reference when a regulator or customer asks about GDPR / CCPA / CAN-SPAM / COPPA posture.
- Trademark scoping before naming/launch — USPTO/TESS pre-search workflow.
- Budget triage: deciding which legal needs use templates vs. require a lawyer.

## When NOT to use
- Litigation, demand letters, takedowns, IP enforcement — adversarial work; always lawyer-led.
- Investment / fundraising / M&A documentation (term sheets, SAFEs, share purchase) — too high stakes for templates.
- Regulated industries: HIPAA, FINRA, GDPR DPIA, EU AI Act, FDA — domain-specific counsel mandatory.
- Cross-border data transfers requiring SCCs / DPF — needs counsel and DPA inventory.
- Employment law (W-2 hires, terminations, harassment) — out of scope for solopreneur basics.

## Where it fails / limitations
- Heavily US-centric: LLC choice, USPTO trademark, IRS EIN. Outside US, agent must localize entity formation, IP office, tax authority.
- Templates tab is generic; "essential clauses" listed but not actually drafted. Agent + human must produce the wording.
- "When to get a lawyer" table is conservative for solo SaaS; in practice many will need counsel earlier than listed (privacy at the SCC level, app-store + Apple/Google contracts, AI training data).
- No coverage of Apple/Google app-store legal terms, payment-platform compliance (PCI-DSS), or DSA/DMA EU obligations.
- Doesn't address open-source license obligations (GPL, AGPL contagion) for software businesses.

## Agentic workflow
Treat agents as legal-document drafting assistants under human counsel review. Workflow: agent collects business facts (entity, jurisdiction, data flows, vendor list, payment processor) → produces draft policies and contracts using a template library → human counsel reviews and signs off → policies versioned in git → agent monitors for drift via `ops-legal-compliance-checklist` cycle. Pair with `ops-legal-compliance` and `ops-legal-compliance-checklist` for the audit loop, `ops-tax-basics` for tax registrations, `ops-contractor-basics` for IC paperwork.

### Recommended subagents
- `faion-growth-agent` (source README) — owns the legal-foundation workflow.
- `faion-researcher` — jurisdiction-specific research (state-of-formation cost, Annual Report obligations, sales tax nexus).
- `security-review` skill — overlaps with privacy and data-handling review.
- General-purpose Claude subagent — clause-extraction and diff against canonical template; flag non-standard or risky additions.

### Prompt pattern
```
Inputs: business_type=<SaaS|info-product|service>, jurisdiction=US-DE, data_flows=<list>,
processors=<list>, target_geos=[US,EU,UK].
Output: (1) entity recommendation with reasoning, (2) required policy list with rationale,
(3) regulation matrix (which apply), (4) IP priorities ranked.
For each item, cite the source rule (e.g., "GDPR Art. 13") and mark "needs counsel review" if the answer depends on jurisdiction-specific exception.
```

```
Compare draft <ToS_v2.md> against canonical <ToS_template.md>. Output added clauses,
removed clauses, materially changed clauses. Flag any clause that creates new
liability for the company or reduces user rights. Do NOT recommend acceptance.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Version-control policies + contracts; PR review per change | cli.github.com |
| `git diff --word-diff` | Reviewing legal text edits with high precision | system |
| `pandoc` | Convert clause libraries between md / docx / PDF | pandoc.org |
| `pdftotext` (poppler) | Extract counterparty contracts for clause comparison | poppler.freedesktop.org |
| `usptoeo` (community) or USPTO TSDR API | Trademark-status lookups | data.uspto.gov |
| `whois` / RDAP CLI | Domain availability + IP-conflict pre-launch checks | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Atlas | SaaS | Partial | One-shot LLC formation + Stripe; not iterative. |
| Firstbase | SaaS | Partial | Similar to Atlas; for non-US founders forming US entity. |
| Clerky | SaaS | Yes | Lawyer-friendly; API limited but docs are lawyer-grade. |
| LegalZoom / Rocket Lawyer | SaaS | Limited | Templates; weak APIs. |
| Termly | SaaS | Partial | Policy generator + monitoring. |
| Iubenda | SaaS | Yes | API for policy generation + DPA inventory. |
| Cooley GO | Free templates | n/a | High-quality startup templates; not a service. |
| DocuSign / HelloSign / PandaDoc | SaaS | Yes | E-sign workflows for contracts + NDAs. |
| Ironclad | SaaS | Yes | Contract lifecycle; enterprise-tier API. |
| LinkSquares | SaaS | Yes | AI contract review (already LLM-driven). |
| Spellbook | SaaS | Yes | LLM clause-suggestion in Word; agent-friendly category. |
| USPTO TESS / TSDR | Free | Yes (TSDR API) | Trademark search + status. |

## Templates & scripts
See `templates.md` for ToS, Privacy Policy, contractor agreement, and NDA scaffolds. Inline trademark pre-search:

```python
# Quick USPTO trademark availability hint via TSDR (status only — full search needs TESS web UI or API)
import requests

def tsdr_status(serial_number):
    url = f"https://tsdr.uspto.gov/ts/cd/casestatus/sn{serial_number}/info.json"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return {"error": "not found"}
    data = r.json()
    return {
        "mark": data.get("trademarks", [{}])[0].get("status", {}).get("markElement"),
        "status": data.get("trademarks", [{}])[0].get("status", {}).get("statusDescription"),
    }

# NOTE: USPTO TESS web search is the canonical pre-launch check;
# this stub only resolves a known serial. Use the search UI for proximity matches.
```

## Best practices
- Form the entity before taking real money. Liability flowing personally is the #1 fixable founder mistake.
- Keep all legal artifacts in a private git repo with PR review — diff is the contract reviewer's best friend.
- Use a "vendor inventory" file (CSV/JSON): for each third party, record what data flows to them and link the DPA. Required for accurate Privacy Policy.
- Never paste a competitor's policies — copyright + factual inaccuracies. Use a template, customize, get review.
- Write contracts in plain language where law allows; courts prefer comprehensible terms over Latin.
- Re-examine entity choice once revenue exceeds ~$80-100k (S-Corp election may save tax in US).
- Tag and date every policy at the top: "Effective Date: YYYY-MM-DD, Version: N." Maintain a version history page.
- Include severability + entire-agreement clauses in every contract; cheap insurance.

## AI-agent gotchas
- LLM-generated contracts hallucinate jurisdictions, statutes, and unenforceable clauses. Treat all output as a draft. Mandatory human counsel review before signing.
- "Legalese" temptation: agents bias toward florid clauses copied from training data; insist on plain-language style and limit clause count.
- ToS limitation-of-liability and arbitration clauses have jurisdiction-specific enforceability nuances (CA, MA consumer protections; EU consumer law). Agents flatten this — flag for review.
- Agent-drafted contractor agreements often re-introduce employee-style controls (set hours, supplied tools) that risk misclassification. Cross-check with `ops-contractor-basics`.
- Auto-generated privacy policies tend to disclose more processing than actually occurs (overclaiming), or less (under-disclosure) — both are enforcement risks. Ground every claim in the vendor inventory.
- Trademark "available?" decisions cannot be agent-final. Phonetic and visual proximity beat exact-string matches; use TESS or counsel.
- Privilege: client-counsel communications fed to a public LLM API may waive attorney-client privilege. Use local models or counsel's own tooling for privileged drafts.
- IP assignment language must include moral-rights waiver where allowed; agents often skip this. Critical for jurisdictions like France/Germany.

## References
- Stripe Atlas legal guides — https://stripe.com/atlas/guides
- Cooley GO startup templates — https://www.cooleygo.com/documents/
- Orrick startup forms — https://www.orrick.com/en/Total-Access/Tool-Kit/Start-Up-Forms
- USPTO TESS / TSDR — https://www.uspto.gov/trademarks/search
- IRS Independent Contractor — https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined
- GDPR Art. 13 / 14 (information to be provided) — https://gdpr-info.eu/art-13-gdpr/
- Sibling methodology: `ops-legal-compliance/README.md`
- Sibling methodology: `ops-legal-compliance-checklist/README.md`
- Sibling methodology: `ops-contractor-basics/README.md`
