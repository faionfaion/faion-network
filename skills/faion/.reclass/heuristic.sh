#!/usr/bin/env bash
# Name-based tier heuristic. Reads inventory.txt, writes candidates.tsv.
# Columns: current_tier \t name_guess \t verdict \t path
# verdict: keep | move | ambiguous

set -eu
cd "$(dirname "$0")"

INV=inventory.txt
OUT=candidates.tsv

: >"$OUT"

while IFS= read -r path; do
  # path example: skills/faion/knowledge/free/dev/software-developer/api-graphql
  rel=${path#skills/faion/knowledge/}
  current=${rel%%/*}
  name=${path##*/}
  lc=$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')

  guess=""

  # GEEK signals (strongest - AI/ML)
  if [[ "$lc" =~ (^ml-|^ai-|^llm-|^rag-|^agent-sdk|^claude-|^multimodal-|^fine-tun|embedding|vector-db|^prompt-|gpt-|-transformer|neural-net|model-training|model-eval|llm-integration|-rag-|ai-agent|agent-orchestration|mcp-|tool-use|retrieval-augmented) ]]; then
    guess=geek
  # PRO signals
  elif [[ "$lc" =~ (kubernetes|k8s-|terraform|multi-cloud|sharding|cqrs|event-sourcing|microservic|sre-|-sre|observability|prometheus|grafana|opentelemetry|distributed-|-distributed|ppc|-smm|paid-|-safe$|^safe-|pmbok|evm-|wbs-|bpmn|^uml-|wcag|compliance|enterprise-|^enterprise|spring-|dotnet|^java-|\-java$|php-laravel|rails|sagas|saga-|outbox|circuit-breaker|load-balanc|service-mesh) ]]; then
    guess=pro
  # SOLO signals
  elif [[ "$lc" =~ (mvp|roadmap|-adr|^adr-|^ddd-|-ddd|monorepo|pwa|-tailwind|nextjs|openapi|rest-design|graphql|content-marketing|seo-technical|^sdd-|server-craft|docker-compose|single-server|landing-page|^contract-first) ]]; then
    guess=solo
  # FREE signals
  elif [[ "$lc" =~ (^basics|-basics$|fundamentals|^101|-101$|hello-world|^intro|-intro$|getting-started|^tutorial|-tutorial$|^standard-|^unit-testing|^git-basics|^js-basics|^python-basics|^refactoring-basics) ]]; then
    guess=free
  else
    guess=unknown
  fi

  if [[ "$guess" == "unknown" ]]; then
    verdict=ambiguous
  elif [[ "$guess" == "$current" ]]; then
    verdict=keep
  else
    verdict=move
  fi

  printf '%s\t%s\t%s\t%s\n' "$current" "$guess" "$verdict" "$path" >>"$OUT"
done <"$INV"

echo "=== Summary ==="
awk -F'\t' '{print $3}' "$OUT" | sort | uniq -c
echo "=== Moves by direction ==="
awk -F'\t' '$3=="move" {print $1 " -> " $2}' "$OUT" | sort | uniq -c | sort -rn
