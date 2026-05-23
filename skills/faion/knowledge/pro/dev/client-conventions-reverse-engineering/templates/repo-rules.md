<!-- purpose: Guardrail Markdown skeleton with the canonical 6 sections. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (client-conventions-reverse-engineering) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# Repo Rules (client conventions)

## Lint / formatter

- Tool: <eslint | ruff | prettier | gofmt>
- Config: <path>
- Rules of note: <list>

## Naming conventions

- Files: <snake_case | kebab-case>
- Classes: <PascalCase>
- Functions: <camelCase | snake_case>

## Branching + commit

- Branch model: <trunk | gitflow | github-flow>
- Commit format: <conventional | sentence-case | type:scope:subject>

## Dependency policy

- Updates: <renovate | dependabot | manual>
- Allowed sources: <npm public | internal mirror>

## Layering rules

- <no DB calls from controllers; entities have no framework imports; etc.>

## Test placement

- Unit: <colocated | tests/>
- Integration: <tests/>
