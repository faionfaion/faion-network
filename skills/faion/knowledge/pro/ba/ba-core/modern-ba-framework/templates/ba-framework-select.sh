# purpose: Shell helper running the scoring matrix.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env bash
# Helper running the scoring matrix.
set -euo pipefail
echo 'Score axes: rigour speed regulation (1-10 each)'
read -p 'rigour: ' R; read -p 'speed: ' S; read -p 'regulation: ' G
if (( R > S )); then echo 'BABOK'; elif (( S > R )); then echo 'Lean-BA'; else echo 'Hybrid'; fi
