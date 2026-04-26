#!/usr/bin/env bash
# bashrc-integration.sh — Shell hook lines for .bashrc
# Copy these lines into ~/.bashrc in the correct order.
# mise MUST come before direnv; direnv MUST be last.

# === Add to ~/.bashrc ===

# 1. mise — polyglot runtime manager (before direnv)
eval "$(mise activate bash)"

# 2. direnv — per-directory environment loader (MUST be last)
eval "$(direnv hook bash)"
