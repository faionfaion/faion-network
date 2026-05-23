<!--
purpose: 100-200 token project-glossary template, included in every bundle.
consumes: nothing — author once per project; reuse + trim per task.
produces: domain-anchored bundle that reduces LLM hallucinated terminology.
depends-on: project-specific terms inventory.
token-budget-impact: ~150 tokens when included in a bundle.
-->

# Project glossary (excerpt)

## Domain
- &lt;domain term&gt;: &lt;1-line definition&gt;
- &lt;acronym&gt;: &lt;expansion + 1-line&gt;

## Architecture
- &lt;service name&gt;: &lt;what it does&gt;
- &lt;pattern name&gt;: &lt;where it's used + alias&gt;

## File / folder naming
- `*.spec.ts`: unit test
- `*.e2e.ts`: end-to-end test
- `src/&lt;domain&gt;/`: bounded context
- `docs/architecture.png`: source of truth diagram

## Sample (faion-net)
- TBD = trunk-based development
- LLM = large language model
- AGENTS.md = the auto-loaded routing doc for AI agents
- F-NNN = Feature ticket id in `.aidocs/`
