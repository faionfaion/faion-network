# Checklist — Field Descriptions as Inline Mini-Prompts

## Design

- [ ] Every non-trivial field has a `description=`
- [ ] Each description is 1-3 sentences, not a paragraph
- [ ] Format / units / range stated when non-obvious
- [ ] Edge cases covered (missing input, ambiguous input, conflicts)
- [ ] Forbidden patterns called out where the model commonly mis-fills

## Review

- [ ] No description duplicates the field name verbatim
- [ ] No description asks for reasoning (reasoning has its own field)
- [ ] No description contradicts the field name or type
- [ ] No description duplicates enum values verbatim
- [ ] Dependent fields reference their dependencies by name in their description

## Verify

- [ ] On a 50-task eval, format-compliance rate is > 99%
- [ ] Field-by-field error analysis: which descriptions still leak edge cases?
- [ ] Iterate descriptions on the most-failed fields; re-measure

## Maintenance

- [ ] Descriptions are version-controlled with the schema
- [ ] Renamed fields keep their description aligned
- [ ] When schema changes shape, descriptions are reviewed for staleness
- [ ] Cold-cache vs warm-cache descriptions are NOT split — keep one source of truth

## Composition

- [ ] Field name covers what; description covers how / when
- [ ] In dependent fields, description references earlier fields by name
