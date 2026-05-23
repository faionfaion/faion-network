# purpose: Lint accepted ADRs for format and required sections.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a architecture-decision-records artefact validating against scripts/validate-architecture-decision-records.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
#!/usr/bin/env bash
# adr-lint.sh — validate ADR files in docs/adr/
# Usage: ./adr-lint.sh [--dir docs/adr]
# Returns exit code 0 if all ADRs pass, 1 if any fail.
# Integrate into CI: add as a pre-commit hook or GitHub Actions step.

set -euo pipefail

ADR_DIR="${1:-docs/adr}"
VALID_STATUSES=("Draft" "Proposed" "Accepted" "Rejected" "Deprecated" "Superseded")
ERRORS=0
FILES_CHECKED=0

if [[ ! -d "$ADR_DIR" ]]; then
    echo "ERROR: ADR directory '$ADR_DIR' not found"
    exit 1
fi

for file in "$ADR_DIR"/*.md; do
    [[ -f "$file" ]] || continue
    FILES_CHECKED=$((FILES_CHECKED + 1))
    filename=$(basename "$file")
    file_errors=0

    # 1. Filename must match NNNN-kebab-case-title.md
    if ! echo "$filename" | grep -qP '^\d{4}-[a-z0-9-]+\.md$'; then
        echo "FAIL [$filename] Filename must match NNNN-kebab-case-title.md"
        file_errors=$((file_errors + 1))
    fi

    # 2. Status line must be present and valid
    status_line=$(grep -m1 "^\*\*Status:\*\*" "$file" 2>/dev/null || true)
    if [[ -z "$status_line" ]]; then
        echo "FAIL [$filename] Missing **Status:** line"
        file_errors=$((file_errors + 1))
    else
        status_valid=false
        for valid_status in "${VALID_STATUSES[@]}"; do
            if echo "$status_line" | grep -q "$valid_status"; then
                status_valid=true
                break
            fi
        done
        if [[ "$status_valid" == "false" ]]; then
            echo "FAIL [$filename] Invalid status in: $status_line"
            echo "       Valid statuses: ${VALID_STATUSES[*]}"
            file_errors=$((file_errors + 1))
        fi
    fi

    # 3. Nygard sections: Context, Decision, Consequences
    for section in "## Context" "## Decision" "## Consequences"; do
        if ! grep -q "^${section}" "$file"; then
            echo "FAIL [$filename] Missing required section: ${section}"
            file_errors=$((file_errors + 1))
        fi
    done

    # 4. Superseded ADRs must reference the superseding ADR
    if echo "$status_line" | grep -q "Superseded"; then
        if ! grep -q "Superseded by ADR-" "$file"; then
            echo "FAIL [$filename] Status is Superseded but no 'Superseded by ADR-NNNN' reference found"
            file_errors=$((file_errors + 1))
        fi
    fi

    if [[ $file_errors -eq 0 ]]; then
        echo "OK   [$filename]"
    fi

    ERRORS=$((ERRORS + file_errors))
done

echo ""
echo "Checked $FILES_CHECKED ADR file(s). Errors: $ERRORS"

if [[ $ERRORS -gt 0 ]]; then
    exit 1
fi
