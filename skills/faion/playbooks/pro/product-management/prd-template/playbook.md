---
name: prd-template
description: Write a stakeholder-ready PRD covering problem, personas, user stories, functional and non-functional requirements, success metrics, out-of-scope items, open questions, and risks.
tier: pro
group: product-management
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a complete Product Requirements Document (PRD) that a product manager, designer, and engineering lead can independently read, align on, and act from — without a follow-up meeting. The worked example throughout is an "Export to PDF" feature for a SaaS reporting tool.

> **PRD vs. spec.md:** A `spec.md` (see `writing-first-spec`) is an engineering-facing document — it lists Functional Requirements and Acceptance Criteria that drive implementation tasks. A PRD is stakeholder-facing — it answers *why* the feature exists, *who* it serves, and *how success is measured*, then hands those decisions to engineering as input for a `spec.md`. In an agency context you write the PRD for the client; the `spec.md` is internal.

## Prerequisites

- You have a confirmed feature request or initiative from a client stakeholder (email thread, Notion doc, Jira epic, or verbal brief captured in writing).
- You have access to any existing user research, NPS data, or support ticket clusters related to this problem area.
- Optional: a shared doc space (Notion, Confluence, or a Git repo `/docs/` folder) where the client can leave comments.
- Familiarity with user story format: "As a [persona], I want [action] so that [outcome]."

## Steps

1. **Open a new file.** Create `docs/prd/export-to-pdf.md` in your client project repo (or the equivalent Notion page). Title it: `PRD: Export to PDF — ReportFlow`.

2. **Write the Problem Statement.** One to three sentences: what pain exists, for whom, and what evidence you have.

   ```
   ## Problem Statement

   ReportFlow users on the Growth plan spend an average of 40 minutes per month
   manually screenshotting dashboards and pasting them into slide decks before
   client calls (source: support ticket analysis, March 2026, 23 tickets tagged
   "export"). There is no native export path; users leave the product to finish
   their deliverable.
   ```

3. **Define Personas.** List the 1–3 primary users who will interact with this feature. Use real names from your research or CRM segments — not generic labels.

   ```
   ## Personas

   | Persona | Role | Primary need |
   |---------|------|-------------|
   | Agency Analyst (Marta) | Junior analyst at a digital agency | Produce a branded PDF report for client delivery without leaving the tool |
   | Account Manager (James) | Client-facing AM at a media buying agency | Attach a one-page summary PDF to a weekly email update in under 2 minutes |
   ```

4. **Write User Stories.** One story per distinct user goal. Format: `As a [Persona], I want [action] so that [outcome]`. Number them US1–USn.

   ```
   ## User Stories

   US1. As Marta (Agency Analyst), I want to export any saved dashboard as a
        paginated PDF so that I can attach it to a client deliverable without
        reformatting in Google Slides.

   US2. As James (Account Manager), I want to generate a one-page PDF summary
        from a pinned "Weekly Overview" dashboard with a single click so that I
        can attach it to my Friday email within 2 minutes.

   US3. As a Growth plan subscriber, I want the exported PDF to include the
        ReportFlow logo and my agency's name in the header so that the document
        looks branded when shared externally.
   ```

5. **Write Functional Requirements (F1–Fn).** Each requirement maps to one or more user stories. Use "The system shall" for system behaviour, "The user can" for user actions. Keep them atomic.

   ```
   ## Functional Requirements

   F1. The user can trigger a PDF export from any saved dashboard via an "Export
       → PDF" menu item in the dashboard toolbar.                          (US1, US2)
   F2. The system shall generate a paginated PDF that preserves the layout and
       data visible at export time (no live re-fetch).                     (US1, US2)
   F3. The system shall include the authenticated user's agency name and the
       ReportFlow logo in the PDF header on every page.                    (US3)
   F4. The system shall deliver the PDF as a file download within 15 seconds
       for dashboards with ≤20 chart widgets.                              (US1, US2)
   F5. The user can choose between A4 and Letter paper size before export. (US1)
   F6. The system shall log each export event (user, dashboard ID, timestamp,
       paper size) for billing and audit purposes.                         (US1–US3)
   ```

6. **Write Non-Functional Requirements (NF1–NFn).** Quality attributes: performance SLAs, security constraints, accessibility standards, browser support.

   ```
   ## Non-Functional Requirements

   NF1. Export generation time ≤15 s at p95 for dashboards with ≤20 widgets
        (measured server-side; client network excluded).
   NF2. Exported PDFs must be accessible: text in charts must be selectable
        (not rasterised images), meeting WCAG 2.1 AA text-contrast ratio
        for printed output.
   NF3. The export endpoint must enforce the user's existing dashboard read
        permission — users cannot export dashboards they cannot view in-app.
   NF4. PDF generation must not degrade dashboard load performance for other
        concurrent users; run in a background worker queue.
   ```

7. **Write the Out of Scope section.** Name what the PRD explicitly excludes to prevent scope creep. Be specific.

   ```
   ## Out of Scope

   - Excel / CSV export (separate initiative, backlog Q3 2026).
   - Scheduled / automated PDF delivery via email (phase 2).
   - White-labelling the PDF with a fully custom cover page template (enterprise tier only).
   - Real-time data refresh during export (export reflects the state at click time).
   ```

8. **Define Success Metrics.** Measurable outcomes tied to the problem statement. Include baseline, target, and measurement method.

   ```
   ## Success Metrics

   | Metric | Baseline | Target (90 days post-launch) | How measured |
   |--------|----------|------------------------------|--------------|
   | Support tickets tagged "export" | 23 / month | ≤5 / month | Zendesk tag report |
   | Monthly export actions per active Growth user | 0 | ≥2 | Product analytics event `dashboard.export_pdf` |
   | Export p95 generation time | n/a | ≤15 s | Server-side timer logged to Datadog |
   | Feature adoption (≥1 export in 30 days) | 0 % | ≥40 % of Growth plan MAU | Mixpanel cohort |
   ```

9. **Write Open Questions.** Unresolved decisions that block design or engineering. Assign an owner and a resolution deadline.

   ```
   ## Open Questions

   | # | Question | Owner | Due |
   |---|----------|-------|-----|
   | Q1 | Which PDF rendering library do we use — Puppeteer (headless Chrome) or a server-side PDF lib? Affects NF2 (accessibility) significantly. | Engineering lead | 2026-05-09 |
   | Q2 | Should the export button be visible to Starter plan users (paywalled with upgrade prompt) or hidden entirely? | Product / Growth | 2026-05-09 |
   | Q3 | Does the client's brand style guide provide a logo file in SVG for the header, or do we use the ReportFlow default? | Account Manager (James) | 2026-05-07 |
   ```

10. **Write the Risks section.** List technical, business, or timeline risks with mitigation notes.

    ```
    ## Risks

    | Risk | Likelihood | Impact | Mitigation |
    |------|-----------|--------|-----------|
    | Puppeteer adds 200 MB to the server image, complicating deployment | Medium | Medium | Evaluate wkhtmltopdf or a managed PDF API (e.g. PDFShift) as lighter alternatives |
    | Complex dashboard layouts (overlapping widgets, custom fonts) render incorrectly in PDF | High | High | Create a rendering test suite with 10 reference dashboards before launch; timebox layout fixes to 2 sprints |
    | Export feature used to extract data from dashboards a user should not see (F6 permission gap) | Low | Critical | Add explicit permission check in export worker, not just the API endpoint; include in security review checklist |
    | Growth plan users expect white-label options → pressure to scope-in cover templates | Medium | Low | Reference Out of Scope section in client sign-off email; document decision trail |
    ```

11. **Get stakeholder sign-off.** Share the PRD with the client, engineering lead, and designer. Require explicit written approval (Notion reaction, email reply, or PR approval) before implementation starts. Attach the signed-off PRD link in your project tracker.

## Verify

After completing the PRD, run these checks:

```bash
# Count top-level H2 sections — expect at least 9
grep -c "^## " docs/prd/export-to-pdf.md

# Confirm every user story number appears in at least one functional requirement
grep "US[0-9]" docs/prd/export-to-pdf.md

# Confirm success metrics have a baseline, target, and measurement method column
grep -E "Baseline|Target|How measured" docs/prd/export-to-pdf.md
```

Every US1–USn reference in the Functional Requirements section must appear in the User Stories section. Every Open Question must have an Owner field filled — unowned questions stall reviews.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Stakeholders keep adding scope after sign-off | Out of Scope section is vague or missing | Rewrite Out of Scope with specific named items; get fresh written approval after each addition |
| Engineering says "we need a spec, not a PRD" | PRD was handed to engineers without a downstream `spec.md` | Use `writing-first-spec` to translate each Functional Requirement into a numbered `spec.md` with Acceptance Criteria before sprint planning |
| Success Metrics have no baseline | Feature is new and no historical data exists | Use proxy metrics (support ticket volume, user interview quotes, competitive benchmarks) and set a 30-day observation period post-launch before evaluating the target |
| Open Questions stay open for weeks | No owner assigned; no deadline | Re-schedule the PRD review and block sign-off until every Q has an owner and a date; escalate to project sponsor if unresolved after 5 business days |
| Personas are too generic ("Admin user", "End user") | Personas taken from role labels rather than research | Pull the top 2–3 user segments from your CRM by usage volume or support ticket originator; give each a first name and a primary job-to-be-done |
| Functional Requirements and Non-Functional Requirements are mixed | Author confused behavioural requirements with quality attributes | FRs = what the system does (observable actions, states, outputs); NFRs = how well it does it (speed, security, accessibility, compliance) |

## Next

- `writing-first-spec` (solo) — translate the PRD's Functional Requirements into an engineering `spec.md` with numbered ACs, ready for implementation agents.
- `stakeholder-management` knowledge — apply structured stakeholder mapping to identify who must approve the PRD vs. who is informed-only, reducing back-and-forth.

## References

- [knowledge/pro/product/product-manager/stakeholder-management](../../../knowledge/pro/product/product-manager/stakeholder-management) — provides the stakeholder mapping framework used in Step 11 to identify approvers vs. informed parties, preventing sign-off loops.
- [knowledge/pro/ba/ba-core/requirements-documentation](../../../knowledge/pro/ba/ba-core/requirements-documentation) — defines the atomic requirement writing rules and the FR/NFR distinction applied in Steps 5–6, including the "The system shall / The user can" convention.
- [knowledge/pro/ba/ba-core/requirements-prioritization](../../../knowledge/pro/ba/ba-core/requirements-prioritization) — underpins the Out of Scope and Risks sections (Steps 7 and 10): how to make explicit, documented trade-off decisions rather than leaving them implicit.
