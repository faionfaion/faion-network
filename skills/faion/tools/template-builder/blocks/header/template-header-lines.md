<!--
purpose: The five-key template header as five one-line HTML comments — the incumbent form in 1,613 of the 3,242 Markdown/text templates in the corpus.
consumes: the five header values, supplied or defaulted
produces: the leading comment block validate-methodology-templates.py scans
depends-on: retrieval-content-contracts.md 2.1
token-budget-impact: ~45 tokens
variables:
  - name: purpose
    type: text
    required: true
    description: What this artefact is, in one line. Ask the author; never invent it.
  - name: consumes
    type: string
    required: true
    default: "see content/02-output-contract.xml inputs"
    description: Where the filler gets the inputs. Default is the corpus-wide phrasing.
  - name: produces
    type: string
    required: true
    default: "artefact conforming to content/02-output-contract.xml"
    description: What a filled copy is. Default is the corpus-wide phrasing.
  - name: depends_on
    type: string
    required: true
    default: "content/01-core-rules.xml"
    description: The content part this template is bound to.
  - name: token_budget_impact
    type: string
    required: true
    default: "~400-1000 tokens when loaded as context"
    description: Cost of loading this template as context.
-->
<!-- purpose: {{purpose}} -->
<!-- consumes: {{consumes}} -->
<!-- produces: {{produces}} -->
<!-- depends-on: {{depends_on}} -->
<!-- token-budget-impact: {{token_budget_impact}} -->
