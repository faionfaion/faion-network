# Checklist — Bundle vs Split Tools

## Audit current tool list

- [ ] Counted total tools exposed to the model
- [ ] If < 20: default to split, look for accidental bundles to expand
- [ ] If > 30: identify candidates for bundling
- [ ] Listed tools by audience (filesystem, git, http, ...)

## Grouping criteria for bundling

- [ ] Modes share the same audience
- [ ] Modes share most arguments (e.g., all take `path`)
- [ ] Training-data prior exists for the mode pattern
- [ ] Each mode has a distinct, easily-describable purpose

## Mode arg design

- [ ] Mode is `Literal[...]` / enum — never free-string
- [ ] Mode values are semantic ("list", "read", "write", "delete") — not codes ("a", "b")
- [ ] Each mode value has its own when-to-use line in the description

## Validate

- [ ] On a 50-task eval, measured tool-selection error rate
- [ ] Bundle didn't degrade the task — quality stable or improved
- [ ] If quality dropped, split the offending bundle

## Anti-pattern checks

- [ ] No bundle with unrelated audiences
- [ ] No `meta_tool(name, args)` wrapper
- [ ] No bundle whose mode the user must guess (mode should reflect user intent)
- [ ] No mode without enum constraint

## Composition

- [ ] Read-side bundles checked: should they be Resources instead?
- [ ] Each tool / mode has a tight description (use-when / NOT-use-when)
- [ ] Tool list size justified — count ≤ 25 is the sweet spot
