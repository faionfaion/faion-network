# Tax Compliance & Filing

## Summary

An operational checklist for US-based solopreneurs to stay penalty-free: compute quarterly estimated payments using the safe-harbor rule (100% of prior-year tax, 110% if AGI exceeds $150K), pay by the IRS quarterly due dates, maintain a structured record-keeping system, execute year-end deduction sweep (retirement contributions, Section 179, expense acceleration), and file on time or extend. Non-US jurisdictions require localization.

## Why

Underpayment penalties compound at the federal short-term rate and accrue quarterly; missing even one payment while also underpaying creates compounding liability. The safe-harbor rule eliminates the penalty risk entirely — the methodology's primary rule — without requiring accurate current-year income projections, which are hard for variable-income businesses.

## When To Use

- First profitable year as a solopreneur or LLC: setting up quarterly estimate cadence
- Multi-state nexus surfaces (SaaS selling into CA/NY/WA, or physical goods crossing thresholds)
- Year-end planning when LLC profit clears the threshold for S-Corp election (~$80K SE income)
- International seller hitting EU/UK VAT thresholds or Stripe Tax onboarding

## When NOT To Use

- Novel situations: equity comp, R&D credits, multi-entity structures, ERC, audit defense — require a CPA
- Determining nexus liability in previously unserved jurisdictions — LLM nexus reasoning is frequently wrong
- When an IRS or state notice has already arrived — go directly to a tax professional
- Real-time tax calculations on customer transactions — use Stripe Tax / Avalara / TaxJar APIs, not an LLM

## Content

| File | What's inside |
|------|---------------|
| `content/01-quarterly-estimates.xml` | Who must pay, quarterly due dates, safe-harbor vs. current-year calculation methods, setup checklist |
| `content/02-records-and-penalties.xml` | Record retention rules, folder structure, penalty types and avoidance, audit red flags |
| `content/03-year-end-and-state.xml` | December year-end action checklist, state compliance considerations, multi-state nexus checklist |

## Templates

| File | Purpose |
|------|---------|
| `templates/safe-harbor.py` | Quarterly federal estimate calculator: safe-harbor vs. current-year, outputs higher of the two |
| `templates/tax-calendar.md` | US federal and state tax deadlines with action descriptions |
