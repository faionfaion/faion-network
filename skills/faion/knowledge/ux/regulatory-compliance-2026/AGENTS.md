# Regulatory Compliance 2026

## Summary

**One-sentence:** Produces an accessibility compliance report mapping product surfaces to ADA Title II + EAA + AODA + Section 508 obligations, with WCAG 2.1/2.2 AA conformance evidence and a dated remediation backlog.

**One-paragraph:** Accessibility regulation landscape shifted April 2026 (ADA Title II Final Rule → WCAG 2.1 AA), June 2025 (EU Accessibility Act effective date), and ongoing (AODA, Section 508). Map every product surface (web, native app, kiosk, e-book) to applicable regulations; document conformance against WCAG 2.1 AA as legal minimum but design to WCAG 2.2 AA. Publish a dated accessibility statement with concrete testing methodology (manual + automated + AT-user), a feedback channel, and remediation commitments. Audit annually + per major release. Treat overlay widgets as a litigation amplifier, not a fix. Most violations enter via CMS — train content authors.

**Ефективно для:**

- Pre-launch a11y audit для US/EU public site або mobile-app після April 2026 (ADA Title II) / June 2025 (EAA).
- Drafting accessibility statement з testing-methodology + feedback channel + remediation timeline.
- Mapping multi-surface product (web + iOS/Android + kiosk + e-book) до конкретних regulations.
- Quarterly / annual a11y audit cycle + remediation backlog prioritization (deadline + risk).

## Applies If (ALL must hold)

- Product surface includes a US- or EU-facing website, mobile app, kiosk, or e-book.
- A regulatory deadline (ADA April 2026, EAA June 2025, AODA, Section 508) is active or imminent.
- Legal/compliance owner exists who will sign off on the published accessibility statement.

## Skip If (ANY kills it)

- Implementation-level a11y fixes — use `accessibility-evaluation`, `wcag-22-compliance`, `testing-with-assistive-technology` instead.
- Privacy/data regulation (GDPR, CCPA, HIPAA) — different methodology family.
- Internal-only tooling not subject to public-accommodation rules — track risk, do not run a full audit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product surface inventory | Markdown table | PM / engineering |
| Jurisdiction list | list of countries / states | legal / GTM |
| Latest a11y audit (if any) | PDF / VPAT 2.x | prior vendor or in-house |
| Test methodology declaration | Markdown | a11y lead |
| Legal review owner | named individual | counsel |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | Source of the conformance criteria the report cites |
| [[testing-with-assistive-technology]] | Defines the manual + AT-user testing required for credible conformance claims |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: jurisdiction-mapping, WCAG-baseline, statement-publication, methodology-evidence, overlay-prohibition, CMS-author-training | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for compliance-report artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: jurisdiction-blind-spot, checkbox-conformance, overlay-as-fix, statement-without-evidence | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: inventory → map → test → draft statement → legal review → publish | 1000 |
| `content/05-examples.xml` | essential | Worked example: SaaS dashboard mapped to ADA + EAA with remediation backlog | 600 |
| `content/06-decision-tree.xml` | essential | Tree: surface-type → jurisdiction → applicable regs → required conformance level | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-surfaces` | haiku | Mechanical listing from PM artefacts. |
| `map-to-regulations` | sonnet | Jurisdictional reasoning + edge cases. |
| `draft-statement` | sonnet | Public-facing language with legal sensitivity. |
| `legal-review` | opus | Cross-jurisdiction risk synthesis; human sign-off mandatory. |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-report.md` | Compliance-report skeleton with surface table + reg matrix + remediation backlog |
| `templates/accessibility-statement.md` | Public accessibility statement with WCAG version, testing methodology, feedback channel, commitments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-regulatory-compliance-2026.py` | Validate compliance-report JSON against the schema (required fields, jurisdictions, conformance level) | CI on every report change; pre-publication gate |

## Related

- [[wcag-22-compliance]]
- [[testing-with-assistive-technology]]
- [[ada-title-ii-compliance-2026]]
- [[accessibility-first-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on product-surface type (web / native / kiosk / e-book) and user jurisdiction (US / EU / Ontario / federal-procurement), maps each combination to applicable regulations, and emits the required conformance level (2.1 AA legal minimum vs 2.2 AA design baseline). Every leaf references a rule from `01-core-rules.xml` so the agent knows which compliance behaviour is enforced.
