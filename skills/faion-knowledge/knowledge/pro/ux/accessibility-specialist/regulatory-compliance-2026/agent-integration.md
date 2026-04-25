# Agent Integration — Regulatory Compliance 2026

## When to use
- Before launching or expanding into US, EU, UK, Canada, Australia, or APAC markets where digital accessibility is regulated.
- Drafting / refreshing the Accessibility Statement, VPAT-ACR, and procurement language.
- ADA Title II (US public sector) deadline planning: April 2026 (large) / April 2027 (small) — must hit WCAG 2.1 AA.
- European Accessibility Act (EAA) — June 28 2025 already passed for new products; legacy products by June 2030.
- Vendor / SaaS due diligence — when a customer demands a VPAT, agent prepares the draft.

## When NOT to use
- Pure technical conformance work — use `wcag-22-compliance` for criterion-level requirements, `a11y-basics` for triage.
- Accessibility testing execution — use `testing-with-assistive-technology`.
- Generating legal opinion or filing a defense — agents draft, attorneys decide. Always.
- Sector-specific regulations (HIPAA, FedRAMP, banking) where accessibility is one of many overlays.

## Where it fails / limitations
- Regulatory landscape changes mid-year — DOJ rule clarifications, EAA member-state transpositions, new state laws (CA AB 1757, NY S6047). The README's table can drift; agents must verify dates from primary sources before use.
- "WCAG 2.1 AA" is the floor in most rules, but some courts apply WCAG 2.2 by default — under-specifying a deliverable target invites trouble.
- Exemptions (undue burden, fundamental alteration, archived content) are narrow and fact-specific. Agents over-claim them.
- US ADA Title III still has no formal regulation for private businesses; case law (Robles v. Domino's) governs — agents cannot reason from rules alone.
- Procurement clauses must be mirror-tight; LLM-drafted contract language without legal review is a liability.

## Agentic workflow
Agents drive the *paperwork* — accessibility statements, VPAT-ACR drafts, procurement-clause libraries, training-tracking spreadsheets, and quarterly-audit calendars — and a regulatory-compliance triage that maps a product's markets to a deadline matrix. They do **not** make compliance determinations; final sign-off is legal counsel + accessibility lead. Pair with `wcag-22-compliance` for the technical criteria checklist and `testing-with-assistive-technology` for evidence-of-conformance.

### Recommended subagents
- `faion-accessibility-specialist-agent` — map markets to standards, draft Accessibility Statement, structure VPAT.
- `faion-ba-core-agent` — populate VPAT-ACR rows from test reports and known issues backlog.
- `faion-business-analyst-agent` — risk register: lawsuits / fines exposure per region.
- `faion-pm-traditional-agent` — schedule compliance milestones (April 2026 ADA II, EAA monitoring).
- A real attorney — any final external statement, contract clause, or response to a complaint.

### Prompt pattern
```
Role: compliance triage.
Input: product description, target markets, customer types (B2B/B2C, public/private),
sectors (e-commerce, banking, transport, e-books, public sector).
Output: matrix {market, applicable_regulations, standard, deadline, evidence_required,
risk_if_noncompliant} grounded in primary sources (cite URL per row).
```

```
Role: VPAT-ACR row author.
For SC <2.1.1 Keyboard>, given test result <pass with notes>, write the
"Conformance Level" + "Remarks and Explanations" cells in ITI VPAT 2.5 Rev WCAG
2.2 format. Be precise; do not over-claim conformance. Note exception via §
references where applicable.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vpat-tools` (community) | Markdown ↔ VPAT 2.5 templates | https://github.com/voluntaryproductaccessibility |
| `axe-core` + `pa11y-ci` | Generate evidence-of-conformance test reports | `npm i -D @axe-core/playwright pa11y-ci` |
| `lighthouse-ci` | Accessibility scores attached to PR + budgets | `npm i -D @lhci/cli` |
| Pandoc + Word/PDF templates | Render Accessibility Statement / VPAT to required formats | https://pandoc.org |
| OPA (Open Policy Agent) | Encode procurement / accessibility policy as code | https://www.openpolicyagent.org |
| GitHub Actions / GitLab CI | Wire continuous a11y monitoring evidence | Native |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe Auditor / Manage | SaaS | Yes — REST | Tracks remediation against WCAG / EN 301 549 |
| SiteImprove | SaaS | Yes — REST | Enterprise compliance crawl + reporting |
| Level Access (eSSENTIAL) | SaaS + services | Partial — REST | Managed compliance program; agents draft for counsel review |
| TPGi ARC / JAWS Inspect | SaaS | Yes — APIs | JAWS-led testing evidence |
| Allyant / Crownpeak DQM | SaaS | Yes — REST | Site-wide governance + audit trail |
| Fable Tech Labs | SaaS | Partial — managed | Real-user evidence for VPAT remarks |
| Tota11y / Pa11y Dashboard | OSS | Yes | Cheap evidence baseline |

## Templates & scripts
See `templates.md` for accessibility-statement, VPAT skeleton, procurement clauses, and audit-cadence calendar. Inline accessibility-statement frontmatter that agents can populate per product:

```yaml
# accessibility-statement.yaml
product: "Faion Network"
url: "https://faion.net"
date: "2026-04-25"
conformance:
  standard: "WCAG 2.2 Level AA"
  also_targets: ["EN 301 549", "Section 508 Refresh"]
status: "Partially conformant — known issues below."
known_limitations:
  - "Third-party video player (vendor X) lacks captions on legacy uploads. Mitigation: human-authored transcripts at /transcripts/."
  - "PDF documents pre-2024 not remediated. Mitigation: contact accessibility@faion.net for accessible alternative."
contact:
  email: "accessibility@faion.net"
  response_sla_hours: 48
last_audit:
  date: "2026-03-15"
  scope: "Web app, marketing site, mobile (iOS/Android)"
  by: "Internal team + Deque axe Auditor"
preparation_methods:
  - "Self-evaluation"
  - "Automated testing (axe, pa11y-ci, Lighthouse)"
  - "Manual + assistive-tech testing (NVDA, VoiceOver, TalkBack)"
  - "User testing with people with disabilities (Fable, n=12)"
formal_complaints_route: "https://faion.net/legal/accessibility-complaint"
```

## Best practices
- Aim at WCAG 2.2 AA now even though regulation cites 2.1 — minimal cost to over-deliver, easier to defend.
- Publish the Accessibility Statement at a stable URL (`/accessibility`); link from footer on every page.
- Treat VPAT-ACR as a living document, refresh on major releases or annually whichever is sooner.
- Keep evidence-of-conformance: dated test reports, AT logs, user-test recordings (with consent) — discoverable in lawsuit.
- Insert accessibility into procurement: VPAT required, remediation timelines in contract, audit rights.
- Train every developer + designer + content owner annually; track completion (regulators ask).
- When a complaint arrives, respond inside 48 hours with substantive engagement — settlement leverage rests on response history.

## AI-agent gotchas
- Agents conflate ADA Title II (public sector) and Title III (private) — keep them separate.
- LLMs cite outdated standards (WCAG 2.0 AA) by training-data inertia; force WCAG 2.2 AA in every prompt.
- Generated VPAT remarks tend to overstate conformance — require "Partially Supports" / "Does Not Support" justifications grounded in tests.
- Exemption claims (undue burden, fundamental alteration) get inserted casually; force agents to cite the specific § and provide rationale.
- Region coverage drifts (Quebec law differs from federal Canada; CA AB 1757 specifics; Texas HB 4090) — agents miss state/provincial nuance.
- Penalty figures are quoted as gospel ($75,000 first offense, $150,000 subsequent for ADA) — those are DOJ ranges, not damages from private suits; agents conflate.
- Human-in-loop checkpoints: every published Accessibility Statement, every VPAT shipped to a customer, every procurement clause, every response to a complaint or demand letter.

## References
- DOJ ADA Web Accessibility Rule (Title II, 2024) — https://www.ada.gov/resources/2024-03-08-web-rule/
- European Accessibility Act — https://ec.europa.eu/social/main.jsp?catId=1202
- EN 301 549 v3.2.1 — https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- Section 508 (US federal) — https://www.section508.gov/
- ITI VPAT templates — https://www.itic.org/policy/accessibility/vpat
- WebAIM legal landscape — https://webaim.org/articles/laws/
- AODA (Ontario) — https://accessibilitycanada.ca/
- UK Equality Act + PSBAR — https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps
