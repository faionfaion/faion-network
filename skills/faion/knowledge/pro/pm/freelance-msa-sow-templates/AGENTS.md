---
slug: freelance-msa-sow-templates
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "6fdc9c8aa7a009f4"
summary: "Contractual primitives the P3 freelancer signs every month: MSA + SOW skeleton with deposit, weekly invoicing, IP-transfer-on-payment, warranty clause — and an explicit gap between MSA umbrella terms and per-engagement SOW specifics that keeps both signable in a week."
tags: [pm, pro, p3-freelancer, msa, sow, contract, ip, warranty]
---
# Freelance MSA + SOW Templates

## Summary

ops-legal-compliance-checklist covers what a freelancer must be compliant with, but says nothing about the actual contractual primitives the solo freelancer signs every month. This methodology supplies a two-document pattern — a Master Services Agreement (MSA) that lives for the life of the relationship and a per-engagement Statement of Work (SOW) that ships in days — with five non-negotiable clauses surfaced as their own rules: deposit and weekly invoicing, IP transfer on payment (not on signature), warranty bounded in scope and time, defined acceptance, and a termination-for-convenience escape clause. The output is a contract pair a freelancer can hand to a client lawyer and expect minor red-lines, not a structural rewrite.

## Applies If

- The operator is a solo or two-person freelancer signing contracts under their own name or single-member entity.
- A new engagement is starting and there is no existing MSA in place, or the existing MSA is missing one of the five primitives.
- The client is a business buyer (not a consumer), so IP, indemnity and warranty actually matter.
- Local jurisdiction permits the freelancer to assign IP and indemnify within ordinary commercial limits.

## Skip If

- The client requires their own MSA which already covers all five primitives — read theirs, redline minimally, do not stack.
- The engagement is a one-off &lt; €1k consultation — a single short SOW with payment terms is sufficient overhead.
- The freelancer operates inside a marketplace (Upwork, Toptal) whose ToS supersede private contracts.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules covering the MSA/SOW split, deposit + weekly invoicing, IP-transfer-on-payment, warranty bounds, and termination clauses |

## Related

- parent skill: `pro/pm/`
- triggering activity: `Cold lead to signed contract (3-week acquisition flow)`, `Project kickoff to handover (typical 6-12 week engagement)`
- neighbouring: `pro/ba/freelance-proposal-template`, `pro/pm/contractor-audition-rubric`, `pro/marketing/freelance-pilot-pricing`
