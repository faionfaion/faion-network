<!--
purpose: Markdown skeleton matching the Article 11 technical documentation outline
consumes: structured system facts (model_name, version, training data lineage, eval results)
produces: a model card / technical documentation draft for human legal review
depends-on: content/02-output-contract.xml (model-card schema)
token-budget-impact: ~600 tokens when filled
-->

# Model Card: <model_name>

## Identification

- Provider: <legal entity name and address>
- Model name and version: <model_name> <version>
- Risk tier (EU AI Act): <unacceptable | high | limited | minimal>
- EU AI database registration: <reg-id or "pending">

## Intended purpose and users

- Intended purpose (Article 13.3(b)(ii)): <purpose>
- Intended user groups: <user_types>
- Geographic scope: <list of EU member states + non-EU>

## Training data and lineage

- Sources: <list of training data sources>
- Copyright opt-out compliance: <yes / partial / no, with explanation>
- Date range: <YYYY-MM-DD to YYYY-MM-DD>
- Demographic coverage notes: <gaps + mitigation>

## Performance metrics

- Accuracy on benchmark: <value> on <benchmark name and version>
- Bias metrics by protected attribute: see attached `bias-report.json`
- Robustness: <adversarial test summary>

## Limitations and known failure modes

- <limitation 1>
- <limitation 2>
- <limitation 3>

## Human oversight (Article 14)

- Human-in-the-loop checkpoints: <description>
- Override mechanism for affected persons: <description>
- Training requirements for human reviewers: <description>

## Transparency disclosures (Article 13)

- User-facing disclosure copy: <text>
- Machine-readable watermark on generated content: <yes / no / N/A>

## Post-market monitoring (Article 72)

- Metrics dashboard URL: <url>
- Alert rules: <list>
- Re-classification trigger: <CI script path>

## Reviewer sign-off

- Reviewer: <reviewer_id>
- Date: <YYYY-MM-DDThh:mm:ssZ>
- Statement: I attest the contents of this model card have been validated against the official EU AI Act text and the system facts on the listed date.
