<!-- purpose: Exclusion audiences checklist before launch. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Exclusion Audiences Checklist

- [ ] current_customers (CRM email list, hashed)
- [ ] subscribers (newsletter list, hashed)
- [ ] recent_purchasers_90d (pixel event)
- [ ] competitor employees (matched company list, optional)

Block launch until all required exclusions are populated.
