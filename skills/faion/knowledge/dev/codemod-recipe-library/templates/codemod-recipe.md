<!-- purpose: Markdown skeleton for one recipe with before/after. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (codemod-recipe-library) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# Codemod Recipe — <name>

**Tool:** <jscodeshift | ast-grep | libcst | Bowler>
**Owner:** <@handle>

## What it does

One sentence.

## Before

```js
// input fixture
```

## After

```js
// output fixture
```

## Invocation

```sh
jscodeshift -t recipes/<name>.js src/
```

## Smoke test

```sh
node recipes/<name>.test.js
```
