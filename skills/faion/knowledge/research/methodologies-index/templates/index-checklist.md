<!-- purpose: Author / audit checklist for INDEX.xml against F-066 A2 -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->
# INDEX.xml audit checklist

- [ ] Root is <index domain count>
- [ ] One-paragraph <description>
- [ ] Every <methodology> has slug + tier + path + <summary>
- [ ] <summary> <=200 chars, output-first phrasing
- [ ] <groups> block partitions into 3-8 sub-clusters
- [ ] Every <methodology> carries complexity + produces attrs
- [ ] Alphabetically sorted by slug within each <group>
- [ ] count attr equals number of <methodology> entries
- [ ] validate-domain-index.py passes
