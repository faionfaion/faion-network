# Six Core Principles (PMBOK 7)

## Summary

PMBOK 7 defines six guiding principles for every project management decision: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, and Build Empowered Teams. Each principle acts as a pre-commitment heuristic — run the six-question audit before committing to a plan, scope change, or architectural decision to surface violations before they compound.

## Why

Process-based PM produces compliance but not necessarily value. Principle-based framing forces the PM and agent to answer "why is this decision good?" for each of six dimensions rather than checking boxes. A mandatory principle audit run before commitment catches value drift, quality debt, and unaccountable decisions at the cheapest moment — before execution.

## When To Use

- Validating a PM decision (scope cut, scope add, vendor choice) against principle-based heuristics before committing.
- Auditing an existing project plan to find which guiding principle is being violated.
- Bootstrapping a constitution.md or charter for a new project with first-principles framing.
- Coaching a junior PM on why a recommendation is sound, not just what to do.

## When NOT To Use

- Pure tactical work (sprint board updates, status reports) — principles add overhead with no decision content.
- Compliance-driven projects where regulatory mandates already prescribe behavior.
- Emergency incident response — use OODA or incident runbooks instead.
- Running on every issue; gate to decisions worth meaningful scope or budget impact.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | All six principles with description, application question, and common violation pattern. |
| `content/02-audit.xml` | Principle audit procedure: PASS/WARN/FAIL protocol, weighting, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pmbok7-audit.sh` | Shell script: emits a markdown audit table for a decision (six-row PASS/WARN/FAIL form). |
