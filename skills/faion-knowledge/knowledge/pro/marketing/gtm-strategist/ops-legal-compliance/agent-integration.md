# Agent Integration — Legal Compliance

## When to use
- Maintaining a compliance checklist (GDPR, CCPA, CAN-SPAM, COPPA, ADA, PCI-DSS) and tracking status across stages (Day 1, Month 1, Year 1, Ongoing).
- Drafting first-pass policy text (Terms, Privacy, Cookie, Refund) from a product+jurisdiction brief — ALWAYS for human + counsel review.
- Diff-checking generated policies against a baseline (e.g. last attorney-approved version) and surfacing changes for review.
- Auditing the website for legal-page presence, cookie banner behavior, footer links, accessibility (axe-core), and CCPA "Do Not Sell" link.
- Pulling and tracking subprocessor lists, DPA templates, and SOC2/ISO27001 evidence inventories.

## When NOT to use
- Final policy generation for production. LLM-drafted Terms or Privacy without attorney review is malpractice exposure. Use only for first drafts.
- Jurisdiction-specific tax/legal advice (e.g. nexus determinations, sanctions screening). Wrong advice has six-figure consequences.
- Incident response / breach notification. Legal counsel + privacy officer own the workflow; agent role is logistics, not decisions.
- Any case where output will be filed with a regulator (FTC complaint response, GDPR DPA correspondence). Human-only.

## Where it fails / limitations
- LLM policy drafts hallucinate references to specific laws (e.g. "Article 15 GDPR" cited incorrectly), invent contractual provisions, or omit jurisdiction-mandatory clauses.
- The methodology document is US-centric. Agents must not auto-apply to UK GDPR, EU DPDP, India DPDP Act, Brazilian LGPD, or AU Privacy Act without jurisdiction-aware prompts.
- Cookie-consent compliance differs sharply (EU opt-in vs CCPA opt-out vs Quebec Law 25 hybrid). Agents that recommend a single banner pattern violate at least one regime.
- HIPAA, GLBA, FERPA, and PCI-DSS each have prescriptive controls — generic compliance checklists fail audits.
- Children's apps (COPPA / under-13) require verifiable parental consent flows the agent cannot design alone.
- Policies become stale. Agent must alert when a jurisdiction's law updates (e.g. EU AI Act, US state privacy patchwork) — most do not.

## Agentic workflow
The compliance agent runs a periodic audit + draft loop: (1) inventory — scrape the live site (footer, cookie banner, /privacy, /terms, etc.) and compare to a checklist matrix; (2) gap report — list missing pages, broken links, banner misconfigurations, accessibility issues; (3) draft updates — propose copy diffs only, never auto-publish; (4) human + counsel review gate — all changes require sign-off; (5) publish — agent can apply approved diffs to CMS/static site. A separate watcher subscribes to regulatory RSS feeds (FTC, EDPB, ICO, CPPA) and files issues when a relevant change publishes.

### Recommended subagents
- `faion-growth-agent` (methodology frontmatter) — owns the operational checklist and audit reports.
- `faion-sdd-executor-agent` — wraps each policy update as an SDD task with mandatory test-plan: links resolve, page renders, banner respects consent state, accessibility passes axe-core.
- `password-scrubber-agent` — scrubs any PII or credential leakage from compliance reports before logging.

### Prompt pattern
```
Goal: audit faion.net legal-compliance state.
Inputs: jurisdiction set [US, EU, UK]; product type [SaaS, B2B, no children]; data classes processed.
Action: fetch /privacy, /terms, /cookie, /dpa, /subprocessors; verify presence of mandatory clauses per jurisdiction matrix; check cookie banner via Playwright in 3 EU + 3 US locales; run axe-core.
Output: gap report with severity tags. Do NOT propose copy changes in this pass.
```

```
Goal: draft Privacy Policy diff vs baseline B for jurisdictions [US, EU].
Constraints: only modify sections flagged in audit AUD-42; preserve all defined terms; keep change list small.
Output: redline + change summary; mark "REQUIRES COUNSEL REVIEW".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Audit cookie banner behavior, page presence, footer links | `pip install playwright` |
| `axe-core` / `pa11y` | Accessibility (ADA / WCAG) automated checks | `npm i -g pa11y` |
| `osquery` / `nuclei` | Surface infra-side compliance posture | https://osquery.io |
| `gitleaks` / `trufflehog` | Secret scanning for code repos | https://github.com/gitleaks/gitleaks |
| `iubenda` CLI / `termly` API | Generate policy text from product description | https://www.iubenda.com/api |
| `vanta` / `drata` API | SOC2 / ISO27001 evidence collection | https://developer.vanta.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Iubenda | SaaS | Yes (API) | Generates Privacy/Cookie/Terms with attorney updates; jurisdiction-aware. |
| Termly | SaaS | Yes | Similar to Iubenda; cheaper for small biz. |
| Termageddon | SaaS | Partial | Auto-update policies; manual export. |
| OneTrust / TrustArc | Enterprise SaaS | Yes (API) | Consent management + DSR workflows. |
| Cookiebot / Osano | SaaS | Yes | Cookie banner + consent log. |
| Vanta / Drata / Secureframe | SaaS | Yes (API) | SOC2 / ISO automation; agent-friendly evidence APIs. |
| LegalZoom / Clerky / Stripe Atlas | SaaS | Partial | Entity formation; agent can prep, lawyer files. |
| Ironclad / Concord / Juro | SaaS CLM | Yes | Contract lifecycle; AI-assisted clause review. |

## Templates & scripts
Inline: nightly compliance presence audit. Confirms mandatory legal pages exist + banner shows on EU IP.

```python
import asyncio
from playwright.async_api import async_playwright

REQUIRED = ["/privacy", "/terms", "/cookies", "/dpa"]

async def audit(domain: str, locales: list[str]) -> dict:
    issues = []
    async with async_playwright() as p:
        for loc in locales:
            ctx = await p.chromium.launch_persistent_context(
                user_data_dir=f"/tmp/audit-{loc}", locale=loc,
                args=[f"--accept-lang={loc}"]
            )
            page = await ctx.new_page()
            for path in REQUIRED:
                resp = await page.goto(f"https://{domain}{path}")
                if not resp or resp.status >= 400:
                    issues.append({"locale": loc, "path": path, "status": resp.status if resp else None})
            await page.goto(f"https://{domain}/")
            banner = await page.locator("[data-testid='cookie-banner']").count()
            if loc.startswith("de") or loc.startswith("fr") or loc.startswith("en-GB"):
                if not banner:
                    issues.append({"locale": loc, "issue": "no cookie banner shown in EU/UK"})
            await ctx.close()
    return {"domain": domain, "issues": issues}

# asyncio.run(audit("faion.net", ["en-US", "de-DE", "fr-FR", "en-GB"]))
```

See `ops-legal-compliance-checklist.md` and `ops-legal-basics.md` (sibling methodology files referenced from this README) for the canonical checklist and policy components.

## Best practices
- Treat agents as draft + audit tools only. Every legal change goes through counsel of record before publish.
- Maintain a `legal/` folder under version control: policies, DPA, subprocessor list, change log. Agent only edits via PR.
- Pin policy text to a "last reviewed by counsel" date; surface red banner in admin if stale >12 months or after major regulatory event.
- Decouple cookie consent state from analytics initialization. Agent audits should verify analytics fires only post-consent in EU.
- Run accessibility checks on every PR. WCAG 2.1 AA is the de facto US/EU bar.
- Subprocessor list must match the actual stack — agent can diff `package.json` + infra inventory against the published list and alert on drift.
- For multi-region products, segment policies per jurisdiction rather than one sprawling doc — easier to maintain and clearer for users.

## AI-agent gotchas
- LLMs cite legal articles incorrectly with high confidence (hallucinated GDPR articles, invented FTC orders). Require source URL + verification.
- "Compliance" is jurisdiction-conditional. Same data flow can be lawful in US and unlawful in EU. Agent prompts must always declare jurisdiction set.
- Cookie banner UX: many auto-generated banners fail EDPB guidelines (preselected boxes, "reject" not equivalent to "accept"). Agents must test the dark-pattern rules, not just presence.
- DSR (Data Subject Request) handling needs identity verification — auto-responding to a "delete my data" email is dangerous. Always queue for human.
- COPPA verifiable parental consent cannot be a checkbox — needs documented method (credit card, government ID, signed form). Agent flow must reject the lightweight option.
- Sanctions screening and KYC are NOT optional in fintech / crypto. Treating them as paper-checklist items is the failure mode.
- Don't let the agent "fix" privacy issues by quietly editing the policy — that hides the change from counsel and creates litigation risk. All policy edits must produce a redline + log entry.

## References
- https://www.ftc.gov/business-guidance
- https://gdpr.eu/ + EDPB guidelines: https://www.edpb.europa.eu/our-work-tools/our-documents
- https://oag.ca.gov/privacy/ccpa
- https://www.ada.gov/resources/web-guidance/
- https://www.pcisecuritystandards.org/
- ICO (UK) guidance: https://ico.org.uk/for-organisations/
- *The Privacy Engineer's Manifesto* — Dennedy, Fox, Finneran
- IAPP resources: https://iapp.org/resources/
