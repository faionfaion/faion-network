#!/usr/bin/env bash
# Check which external review tools are installed and authenticated.
# Usage: bash check-review-tools.sh [--json]
# Exit code 0 = at least one tool available, 1 = none available.

set -euo pipefail

JSON=false
[[ "${1:-}" == "--json" ]] && JSON=true

CODEX_INSTALLED=false
CODEX_AUTHED=false
KIRO_INSTALLED=false
KIRO_AUTHED=false

# --- Codex CLI ---
if command -v codex &>/dev/null; then
    CODEX_INSTALLED=true
    # Codex uses OPENAI_API_KEY env var or ~/.codex/auth.json
    if [[ -n "${OPENAI_API_KEY:-}" ]] || [[ -f "$HOME/.codex/auth.json" ]]; then
        # Quick sanity: try codex --version (doesn't hit API)
        if codex --version &>/dev/null; then
            CODEX_AUTHED=true
        fi
    fi
fi

# --- Kiro CLI ---
if command -v kiro &>/dev/null; then
    KIRO_INSTALLED=true
    # Kiro auth check: kiro auth status or config file
    if kiro auth status &>/dev/null 2>&1; then
        KIRO_AUTHED=true
    elif [[ -f "$HOME/.kiro/config.json" ]] || [[ -f "$HOME/.config/kiro/credentials" ]]; then
        KIRO_AUTHED=true
    fi
fi

# --- Output ---
if $JSON; then
    cat <<EOF
{
  "codex": {"installed": $CODEX_INSTALLED, "authenticated": $CODEX_AUTHED},
  "kiro": {"installed": $KIRO_INSTALLED, "authenticated": $KIRO_AUTHED}
}
EOF
else
    echo "=== SDD Review Tools ==="
    echo ""
    if $CODEX_INSTALLED; then
        echo "Codex CLI:  installed ($(command -v codex))"
        $CODEX_AUTHED && echo "            authenticated" || echo "            NOT authenticated"
    else
        echo "Codex CLI:  not installed"
        echo "            install: npm i -g @openai/codex"
    fi
    echo ""
    if $KIRO_INSTALLED; then
        echo "Kiro CLI:   installed ($(command -v kiro))"
        $KIRO_AUTHED && echo "            authenticated" || echo "            NOT authenticated"
    else
        echo "Kiro CLI:   not installed"
        echo "            install: https://kiro.dev"
    fi
    echo ""
    if $CODEX_AUTHED || $KIRO_AUTHED; then
        echo "Status: external reviewers available"
    else
        echo "Status: no external reviewers (Claude Code subagent only)"
    fi
fi

# Exit code: 0 if at least one tool is available
($CODEX_AUTHED || $KIRO_AUTHED) && exit 0 || exit 1
