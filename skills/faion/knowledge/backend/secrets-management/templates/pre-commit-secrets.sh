#!/bin/bash
# purpose: Template fixture for secrets-management: pre-commit-secrets.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
# .git/hooks/pre-commit — Block commits containing secret patterns
#
# Install: cp pre-commit-secrets.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Scans staged file contents for API key patterns and private keys.
# Skips .env.example and .env.tpl (intentionally contain placeholder syntax).

PATTERNS=(
    'sk-ant-api[0-9a-zA-Z-]+'     # Anthropic API keys
    'sk-[a-zA-Z0-9]{20,}'         # OpenAI-style API keys
    'PRIVATE KEY'                   # PEM private keys
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)
FOUND=0

for FILE in $STAGED_FILES; do
    # Skip example and template files — they're supposed to reference key names
    [[ "$FILE" == *.example ]] && continue
    [[ "$FILE" == *.tpl ]] && continue
    [[ "$FILE" == *.md ]] && continue

    for PATTERN in "${PATTERNS[@]}"; do
        if git show ":$FILE" 2>/dev/null | grep -qEi "$PATTERN"; then
            echo "BLOCKED: Potential secret in $FILE (pattern: $PATTERN)"
            FOUND=1
        fi
    done
done

if [ "$FOUND" -eq 1 ]; then
    echo ""
    echo "Commit blocked. Remove secrets from staged files."
    echo "Secrets belong in .env files (not committed), not in source code."
    exit 1
fi

exit 0
