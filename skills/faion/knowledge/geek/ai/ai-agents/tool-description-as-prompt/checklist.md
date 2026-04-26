# Checklist — Tool Description as Prompt

## Design

- [ ] Tool name is verb_object (e.g., `search_docs`, `apply_patch`, `validate_path`)
- [ ] Description has one-sentence "use this when ..." trigger
- [ ] Description has one-sentence "do NOT use this when ..." anti-trigger
- [ ] Input contract clarified (paths, units, formats)
- [ ] Output contract clarified (shape, limits, sort order)
- [ ] Side effects called out ("modifies state", "idempotent", "dry-run available")
- [ ] Description is < 200 tokens
- [ ] No marketing prose, no implementation details

## Review

- [ ] Two tools with similar names have CLEARLY differentiated when-to-use lines
- [ ] Description matches input_schema (no fields described that don't exist; no fields existing that aren't described)
- [ ] Description does not duplicate the JSON schema (it complements it)
- [ ] Description matches the function's actual behavior — drift kills agent reliability faster than anything

## Verify

- [ ] On 50 tasks, count tool-selection errors (wrong tool chosen)
- [ ] On the same 50, count argument-fill errors
- [ ] After improving descriptions, both should drop measurably
- [ ] If they don't, look at *which* description was misleading

## Composition

- [ ] Tool description is reviewed alongside the function it wraps
- [ ] Description is updated whenever the function's behavior changes
- [ ] Description is part of the eval loop (regress when description quality drops)
