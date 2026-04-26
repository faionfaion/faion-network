# Naming and Domains

## Summary

Systematic methodology for generating product names and validating domain/handle availability before launch. Combines 7 naming strategies (descriptive, invented, compound, metaphor, portmanteau, alliteration, acronym) with parallel availability checking across .com/.io/.co, GitHub, npm, PyPI, and social handles. Generate 30+ candidates, filter by availability and criteria, then shortlist 3 viable options.

## Why

Pre-launch naming is a single high-stakes decision with permanent consequences: an unavailable .com, a trademark conflict, or a culturally negative meaning can kill a brand before launch. Systematic multi-strategy generation with availability gating prevents the "name everything looks great until we check" failure mode. LLMs default to mode-collapsed names (Spark, Nova, Atlas, Loop); explicit anti-pattern injection forces diversity.

## When To Use

- Pre-launch: locking name + domain + core social handles in one batch.
- Rebrand or sub-product launch: testing 20+ candidates against availability and trademark.
- Naming a project where domain availability is the binding constraint (no .com → no go).
- Generating localized variants (UA/EN/DE) of a brand for multi-region launch.

## When NOT To Use

- Established brand — naming agents will not improve mature trademarks.
- Highly regulated industries (pharma, finance) where naming triggers regulator review — manual lawyer step required.
- Internal/code-name only — domain check is wasted effort.
- No budget for trademark attorney — agent-generated trademark pre-filter is informational risk band, not legal clearance.

## Content

| File | What's inside |
|------|---------------|
| `content/01-naming-strategies.xml` | 7 naming strategies with definitions, criteria for a good name, and the generation process. |
| `content/02-domain-availability.xml` | Domain/handle check priority, availability actions, alternative strategies, agentic workflow, and gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/naming-brief.md` | Structured brief capturing brand attributes, keywords, candidates table, and top 3 recommendations. |
| `templates/domain-check-report.md` | Domain/handle availability matrix with trademark check section and fallback alternatives. |
| `templates/check-names.sh` | Bash script: reads names.txt, runs WHOIS + GitHub + npm + PyPI + Twitter checks, outputs matrix.csv. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/check-names.sh` | Bulk availability runner: WHOIS + handle checks in parallel, outputs CSV matrix. |
