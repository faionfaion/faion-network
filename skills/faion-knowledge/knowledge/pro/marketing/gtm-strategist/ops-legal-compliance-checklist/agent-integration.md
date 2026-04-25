# Agent Integration — Legal Compliance Checklist

## When to use
- Pre-launch audit: confirm ToS, Privacy Policy, Cookie Policy, Refund Policy are in place and linked.
- Quarterly self-review of legal pages: detect drift between policies and actual data flows / vendors.
- After adding a new third-party integration (analytics, payments, AI provider) — re-check what gets disclosed.
- Tracking GDPR/CCPA/CAN-SPAM/COPPA obligations as the business expands into new jurisdictions or audiences.
- Generating compliance status snapshots for due-diligence (investor, acquirer, enterprise customer security review).

## When NOT to use
- Drafting policy text from scratch — use a generator (Termly/Iubenda) or counsel; this checklist verifies coverage, not wording.
- Industry-regulated sectors (HIPAA health, FINRA finance, FERPA edu, PCI-DSS payments) — minimum baseline only; need vertical-specific checklists + lawyer.
- M&A or fundraising legal due diligence — broader scope (cap table, IP chain, employment, contracts).
- Disputes, takedowns, demand letters — adversarial, not checklist-driven.

## Where it fails / limitations
- US-centric assumptions; LLC formation paths and CCPA framing don't translate to EU/UK/Asia markets.
- Static checklist — doesn't update when regulators issue new guidance (DSA, EU AI Act, state-level US privacy laws).
- "Have a privacy policy" is not the same as "privacy policy is accurate." The checklist verifies presence, not truthfulness vs reality.
- Cookie consent compliance has subtle UX requirements (no pre-ticked boxes, equal-prominence reject button, granular categories) that a binary checklist can miss.
- IAB TCF v2.2 and Google Consent Mode v2 specifics not covered.

## Agentic workflow
Run the checklist as an automated audit pass: agent fetches the live site, parses footer links, checks policy pages exist, scrapes the cookie banner, diffs declared vs actual third parties (cross-reference against `<script>` tags and network requests). Output structured findings with status per item. Pair with `ops-legal-basics` for context on each obligation, and `ops-tax-compliance` for entity/payment registrations. Human counsel reviews any flagged item before action.

### Recommended subagents
- `faion-growth-agent` (source README) — owns the audit pass and report generation.
- `faion-researcher` — for jurisdiction-specific obligations when expanding markets.
- `security-review` skill — overlap on data-handling and vendor inventory.
- General-purpose Claude subagent with WebFetch — pulls live policy pages and produces a diff against the canonical version stored in repo.

### Prompt pattern
```
Fetch <url>/privacy and <url>/terms. Parse and return:
- last-updated date,
- list of third parties named,
- list of user rights stated,
- presence/absence of: GDPR DPO contact, CCPA "Do Not Sell" link, CAN-SPAM physical address.
Output as JSON aligned with the checklist in ops-legal-compliance-checklist/README.md.
```

```
Given declared vendors=<list> and actual vendors detected from network log=<list>,
output the gap (declared-not-used, used-not-declared) and rank by privacy impact.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` | Audit cookie + privacy basics | `npm i -g lighthouse` |
| `puppeteer` / `playwright` | Headless render → capture cookies + 3rd-party requests | playwright.dev |
| `curl` + `jq` | Pull and parse policy pages | system |
| `pa11y` | Accessibility (sometimes coupled with consent banner usability) | pa11y.org |
| `cookiepedia-cli` (community) | Identify third-party cookie origins | github search; or use OneTrust Cookiepedia.com directly |
| `gh` | Track policy versions in git, diff updates | cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Termly | SaaS | Partial | Generator + monitor; no public API for solo tier. Manual export. |
| Iubenda | SaaS | Yes | API for policy generation, consent tracking, DPA inventory. |
| OneTrust | SaaS | Yes | Enterprise-tier API; overkill for solopreneur. |
| Cookiebot (Usercentrics) | SaaS | Yes | API + JS SDK; generates cookie reports automatically. |
| Osano | SaaS | Yes | API + dashboard; good agent fit for DSAR workflows. |
| Vanta / Drata / Secureframe | SaaS | Yes | Compliance automation (SOC 2, ISO, GDPR) — API surfaces evidence, controls, vendor reviews. |
| TrustArc | SaaS | Partial | Enterprise; API limited. |
| Stripe Atlas | SaaS | No | One-time formation; not an audit tool. |

## Templates & scripts
See `templates.md` for site-legal page checklist, policy update notification, and stage-by-stage compliance tracker. Inline live-site auditor:

```python
# Quick legal-pages presence audit
import requests
from urllib.parse import urljoin

def audit_footer_legal(base_url):
    html = requests.get(base_url, timeout=10).text.lower()
    needed = {
        "terms": ["terms of service", "terms-of-service", "/terms"],
        "privacy": ["privacy policy", "privacy-policy", "/privacy"],
        "cookie": ["cookie policy", "cookie-policy", "/cookies"],
        "refund": ["refund policy", "refund-policy", "/refund"],
    }
    return {k: any(s in html for s in v) for k, v in needed.items()}

print(audit_footer_legal("https://example.com"))
```

## Best practices
- Version-control your policies in git; review every PR that changes `/privacy` or `/terms`. Treat them as code.
- Maintain a vendor-inventory file (CSV or JSON) that lists every third party receiving user data; update whenever a new SDK/script is added. The privacy policy must match this file.
- Re-audit on every: new feature launch, new vendor integration, new market entry, regulatory news event.
- Notify users by email on material privacy changes — silent updates erode trust and violate some jurisdictions' rules.
- Date-stamp every policy and keep an immutable changelog at the bottom of the page.
- For GDPR specifically: implement a working DSAR (data subject access request) endpoint and test it quarterly. The checkmark is meaningless if the workflow is broken.

## AI-agent gotchas
- Agents will mark "ToS exists" as compliant without reading content. Always require a content-extraction step that verifies key sections (limitation of liability, governing law, IP ownership, payment terms).
- LLM-drafted policies often hallucinate clauses or import US-specific terms into EU contexts. Treat all generated text as a draft for human counsel.
- Agents struggle to distinguish CCPA's "Do Not Sell or Share" from GDPR's "Object to Processing" — both must coexist for cross-border sites; check separately.
- Cookie scanners run against logged-out state by default and miss authenticated-only trackers. Re-run after login.
- Auto-generated DSAR responses risk leaking other users' data when joins are misconfigured. Mandatory human review before sending.
- Compliance is a moving target — don't pin the agent to a static checklist; re-derive obligations on each major regulatory update (state privacy laws in US ship monthly).
- Privilege concerns: legal-counsel work product fed to LLMs may lose attorney-client privilege. Don't pipe lawyer drafts through external LLM APIs without review.

## References
- GDPR.eu compliance guide — https://gdpr.eu/
- CCPA / CPRA official — https://oag.ca.gov/privacy/ccpa
- CAN-SPAM compliance guide — https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- IAB TCF v2.2 — https://iabeurope.eu/transparency-consent-framework/
- Google Consent Mode v2 — https://developers.google.com/tag-platform/security/concepts/consent-mode
- Sibling methodology: `ops-legal-basics/README.md`
- Sibling methodology: `ops-legal-compliance/README.md`
