#!/usr/bin/env bash
# pd-assessment.sh — Emit a fresh PMBOK 7 eight-domain assessment skeleton.
#
# Usage: ./pd-assessment.sh "Project Name"
# Output: Markdown assessment template on stdout.
set -euo pipefail

PROJECT="${1:?project name required}"

cat <<MD
# Performance Domain Assessment: $PROJECT

**Date:** $(date +%F)
**Evidence window:** last 30 days (adjust as needed)
**Assessor:**

## Domain Health

| Domain | Health | Key Issues | Priority Actions |
|--------|--------|------------|-----------------|
| Stakeholder | G/A/R | | |
| Team | G/A/R | | |
| Development Approach | G/A/R | | |
| Planning | G/A/R | | |
| Project Work | G/A/R | | |
| Delivery | G/A/R | | |
| Measurement | G/A/R | | |
| Uncertainty | G/A/R | | |

## Rules

- Anchor every color with a quoted artifact; no vibes.
- G = performing as expected; A = gap with active mitigation; R = critical gap, no mitigation.
- Track domain health as a trend — direction matters more than absolute color.

## Weakest Domain

<name> — because <evidence quote + cross-domain impact explanation>.

## Priority Actions (max 3)

1.
2.
3.
MD
