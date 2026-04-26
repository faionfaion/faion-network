# Checklist — Semantic Field Naming

## Design

- [ ] Every field name is English, lower_snake_case, and at least 2 tokens
- [ ] No `field1`, `val`, `data`, `output`, `result`, `flag`, `info`
- [ ] Booleans start with `is_`, `has_`, `should_`, `requires_`
- [ ] Numeric fields encode unit and (when bounded) range — `age_years`, `confidence_0_to_1`
- [ ] String fields encode format when constrained — `email`, `iso_date`, `slug_kebab`
- [ ] Enums use semantically-loaded values (`approve`/`reject`, not `1`/`0` or `a`/`b`)
- [ ] Field names match the cardinality (singular for `Item`, plural for `list[Item]`)

## Review

- [ ] Read the schema aloud — does each field name describe what's in it?
- [ ] Replaced any cryptic names that would require a reader to look up the description
- [ ] Did NOT use `final_*` / `_value` / `_data` redundant suffixes
- [ ] If migrating from legacy schema, kept old name + `description` referencing the rename

## Verify

- [ ] Renamed-field A/B test on at least 5 tasks
- [ ] No regression in field types after rename (rename is name-only, not shape change)
- [ ] Downstream consumers updated to new names (or aliased via Pydantic `validation_alias`)

## Composition

- [ ] Field name and field order both reinforce dependency direction
- [ ] Field descriptions extend (don't duplicate) the name
