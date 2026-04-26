# Procurement Management

## Summary

Six-step framework for engaging external vendors: make-or-buy decision, Statement of Work (SOW) with explicit acceptance criteria, contract type selection (Fixed Price / T&M / Cost Plus), weighted vendor evaluation, contract negotiation, and ongoing vendor management. Every contract must pass a mandatory clause checklist before signing.

## Why

Vague SOWs and "lowest price wins" decisions are the primary causes of vendor disputes, cost overruns, and project delays. A structured procurement process forces explicit scope definition, distributes risk appropriately via contract type, and creates an audit trail from requirements through payment. Missing clauses (IP assignment, DPA, termination-for-convenience) create legal exposure that surfaces only during disputes.

## When To Use

- Defining a make-or-buy framework before engaging external vendors.
- Drafting SOW, Master Services Agreement (MSA), or Data Processing Addendum (DPA) skeletons.
- Running an RFI / RFP / RFQ process: vendor list, evaluation matrix, weighted scoring.
- Selecting contract type for a defined scope and risk profile.
- Vendor risk and security review (SOC 2, ISO 27001, GDPR DPA) intake.
- Ongoing vendor management: SLA tracking, change requests, performance reviews.

## When NOT To Use

- Spot purchases under a PO threshold (e.g. under $5K) where formal procurement is overhead.
- Highly regulated industries with established central procurement and legal teams — defer to org policy.
- SaaS tools the engineering team can self-onboard with monthly billing (security review still needed, but not a full RFP).

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Make-or-buy decision, contract type selection, sourcing methods, mandatory clause checklist. |
| `content/02-vendor-evaluation.xml` | Weighted scoring matrix, sensitivity analysis rule, evaluation anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sow.md` | Statement of Work with scope, deliverables, acceptance criteria, timeline, assumptions. |
| `templates/vendor-matrix.md` | Weighted evaluation matrix with scoring scale and recommendation sections. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/vendor_score.py` | Weighted vendor scoring with sensitivity analysis; flags rank instability. |
