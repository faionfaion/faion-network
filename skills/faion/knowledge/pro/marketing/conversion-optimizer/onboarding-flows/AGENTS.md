# User Onboarding Flow Design

## Summary

A design framework for guiding new users from signup to their first "Aha moment" as fast as possible. Core principle: show value before asking for work. Segment users at signup (one question), route each segment to a matching pattern (template-first / wizard / interactive / self-serve / concierge), cap the critical path at 3-5 required steps, and pair every in-app step with a triggered email that stops the moment the user activates.

## Why

Most trial churn happens before users experience value. Each additional onboarding step loses users (8 → 3 steps can raise completion from 50% to 85%). Generic flows for all segments compound drop-off because individual users get team-setup screens and evaluators get power-user prompts. Paired in-app + email sequences that stop on activation lift D0 activation rate by 20-40% vs uncoordinated email blasts.

## When To Use

- Designing or rebuilding the first-run experience for a SaaS product where activation rate is below 50%.
- Choosing among onboarding patterns (template-first, wizard, interactive tutorial, self-serve, concierge) for a specific product.
- Reducing step count without losing necessary configuration.
- Adding progressive disclosure, contextual tooltips, and progress checklists to an existing flow.
- Coordinating in-app guidance with a triggered email sequence for the same activation goal.

## When NOT To Use

- The activation event is not yet defined — pause and run activation analysis first.
- Pre-PMF startups where onboarding optimization masks a value-prop problem.
- Enterprise products with bespoke deal-by-deal onboarding — focus on Customer Success playbooks instead.
- Products with extremely simple value (no setup needed) — over-engineered onboarding hurts more than it helps.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Five onboarding patterns with use-cases and examples; segment routing at signup; critical path definition; optimization tactics. |
| `content/02-rules.xml` | Concrete rules: step cap, email stop-on-activation, pre-fill defaults, single primary action for empty states, character limits for microcopy. Antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-spec.md` | Per-segment flow specification: segment, pattern, steps, copy, completion criterion, skip eligibility. |
| `templates/validate-flow.sh` | Bash validator: fails if any onboarding step lacks a mapped analytics event. |
