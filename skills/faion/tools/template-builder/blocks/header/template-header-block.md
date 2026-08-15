<!--
purpose: The five-key template header as one multi-line HTML comment — used by 871 of the 3,242 Markdown/text templates, the second of the two header forms actually in the corpus.
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
    default: "see AGENTS.md Prerequisites"
    description: Where the filler gets the inputs.
  - name: produces
    type: string
    required: true
    default: "artefact conforming to content/02-output-contract.xml"
    description: What a filled copy is.
  - name: depends_on
    type: string
    required: true
    default: "content/02-output-contract.xml schema"
    description: The content part this template is bound to.
  - name: token_budget_impact
    type: string
    required: true
    default: "~400 tokens when filled"
    description: Cost of loading this template as context.
-->
<!--
purpose: {{purpose}}
consumes: {{consumes}}
produces: {{produces}}
depends-on: {{depends_on}}
token-budget-impact: {{token_budget_impact}}
-->
