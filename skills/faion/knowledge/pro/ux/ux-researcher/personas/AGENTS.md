# Personas

## Summary

Personas are research-based fictional characters representing key user types. Each persona distills observed goals, behaviors, frustrations, and usage context from real data into a shared team artifact that makes design decisions answerable: "Would Sarah want this?" Without them, teams design for themselves.

## Why

Teams without shared user models debate features as opinion battles with no resolution mechanism. Personas give every design and prioritization discussion a concrete reference: a named character with documented goals and pain points sourced from research. The artifact only carries signal when grounded in data — proto-personas and research-based personas serve different phases, but both must be explicit about their evidence basis.

## When To Use

- Synthesizing interview, survey, analytics, and support-ticket data into 3-5 representative user types.
- Aligning a team that disagrees about who the primary user is.
- Bootstrapping proto-personas before research with explicit assumptions to validate.
- Re-validating outdated personas after a product pivot or new market entry.
- Writing user stories, A/B hypotheses, and onboarding flows that reference a consistent user identity.

## When NOT To Use

- Marketing-only segmentation (psychographics, ad targeting) — those need separate marketing-persona models.
- Single-user products (internal tools with one stakeholder) where a persona adds zero signal.
- Teams with no plan to reference personas in design reviews — building them as posters wastes effort.
- High-stakes regulated domains (medical devices, aerospace) where formal user-task analysis supersedes lightweight personas.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Persona types, required elements, creation process, and validation rules. |
| `content/02-usage-patterns.xml` | How to use personas in design reviews, user stories, and prioritization; JTBD connection. |
| `content/03-antipatterns.xml` | Signs of bad personas, common mistakes, and agent-specific failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-template.md` | Full research-based persona document structure. |
| `templates/proto-persona-template.md` | Lightweight proto-persona with explicit assumption fields. |
| `templates/prompt-persona-drafter.txt` | LLM prompt for evidence-constrained persona drafting. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/persona_evidence_check.py` | Verify every persona claim cites an evidence ID; fail if quote lacks source. |
