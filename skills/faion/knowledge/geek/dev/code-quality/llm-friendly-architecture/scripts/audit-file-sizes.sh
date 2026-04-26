#!/usr/bin/env bash
# audit-file-sizes.sh — Entry point for LLM architecture compliance audit.
# Wraps templates/llm-arch-audit.sh with project defaults.
# Usage: bash scripts/audit-file-sizes.sh [src-dir] [limit]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/../templates/llm-arch-audit.sh" "${1:-src}" "${2:-250}"
