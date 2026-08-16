<!--
purpose: Guardrail Markdown skeleton with the canonical 6 sections.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (client-conventions-reverse-engineering)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
-->
# Repo Rules (client conventions)

## Lint / formatter

- Tool: <tool>
- Config: <path>
- Rules of note: <list>

## Naming conventions

- Files: <files>
- Classes: <pascal_case>
- Functions: <functions>

## Branching + commit

- Branch model: <branch_model>
- Commit format: <conventional | sentence-case | type:scope:subject>

## Dependency policy

- Updates: <renovate_dependabot_manual>
- Allowed sources: <allowed_sources>

## Layering rules

- <no DB calls from controllers; entities have no framework imports; etc.>

## Test placement

- Unit: <colocated_tests>
- Integration: <tests>
