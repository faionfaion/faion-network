# purpose: Shell smoke test driver for every recipe.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml (codemod-recipe-library)
# depends-on: content/01-core-rules.xml
# token-budget-impact: small (template is loaded only when an artefact is being authored)
#!/usr/bin/env bash
set -euo pipefail
for r in recipes/*.js; do
  name=$(basename "$r" .js)
  out=$(mktemp -d)
  cp "fixtures/${name}.before.js" "${out}/in.js"
  jscodeshift -t "$r" "${out}/in.js"
  diff -u "fixtures/${name}.after.js" "${out}/in.js"
done
