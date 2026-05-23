<!-- purpose: Feed health audit checklist. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-1200 tokens when loaded as context -->

# Merchant Center Feed Health Checklist

- [ ] Titles: include brand + product + key attribute
- [ ] GTIN: present for ≥95% of SKUs
- [ ] Image URL: HTTPS, ≥800x800, no watermark
- [ ] price: matches landing page
- [ ] availability: in_stock / out_of_stock / preorder
- [ ] gtin / mpn / brand triplet completeness
- [ ] product_type taxonomy
