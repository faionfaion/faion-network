<!--
purpose: language audit report skeleton (Nielsen H#2)
consumes: UI string corpus + user-vocabulary corpus (tickets/transcripts/search logs)
produces: a match-real-world artefact validating against scripts/validate-match-real-world.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# Language Audit: [Feature / Product Area]

**Date:** [Date]
**Reviewer:** [Name]
**Target user persona:** [e.g., "small business owner, non-technical, age 30-55"]

## Terminology Review

| Current Term | User-Friendly? | Issue | Suggested Alternative |
|--------------|----------------|-------|-----------------------|
| [Term] | Y/N | [Jargon / technical / abbreviation / unclear] | [Plain alternative] |

## Error Messages Review

| Current Message | Clear? | Issue | Suggested Improvement |
|-----------------|--------|-------|-----------------------|
| [Message] | Y/N | [Blame / vague / no action] | [Rewrite] |

## Labels and Instructions

| Element | Current Label | Issue | Recommendation |
|---------|---------------|-------|----------------|
| [Button / field / nav item] | [Current] | [Issue] | [Fix] |

## Information Order

| Form / Flow | Current Order | Natural Order | Change Needed? |
|-------------|---------------|---------------|----------------|
| [Form name] | [Current] | [User-natural] | Y/N |

## Localization Gaps

| Element | Issue | Fix |
|---------|-------|-----|
| [Date format] | [US format shown to EU users] | [Use locale detection] |
| [Currency] | [Hardcoded $] | [Localize by user region] |

## Overall Recommendations

1. [Highest priority: term/message causing most user confusion]
2. [Second priority]
3. [Third priority]

## Inconsistencies Across Product

| Concept | Page A | Page B | Canonical Choice |
|---------|--------|--------|------------------|
| [Login action] | "Sign in" | "Log in" | [Pick one] |
