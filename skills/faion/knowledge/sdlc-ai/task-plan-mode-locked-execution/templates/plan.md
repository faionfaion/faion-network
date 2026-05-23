<!-- purpose: Markdown skeleton for the locked plan (numbered steps, verify cmds, out-of-scope, risks). -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

# Plan: <change-title>

> Generated in Plan Mode (read-only). Approval required before execution.
> Branch: <feat/...>
> Scope estimate: <N files>, <approx runtime>

## Steps

1. <imperative step, names files / commands>
2. <step>
3. <step>
4. <step>

## Verification

```bash
# the exact commands that prove success
<test command 1>
<lint command>
<typecheck command>
```

## Out of scope

- <explicit exclusion 1>
- <explicit exclusion 2>
- <explicit exclusion 3>

## Rollback

- <one-line revert command>
- <or: "no rollback path because <reason>" — caller MUST confirm risk>

## Approval

- [ ] human reviewer: ____________  date: ______
