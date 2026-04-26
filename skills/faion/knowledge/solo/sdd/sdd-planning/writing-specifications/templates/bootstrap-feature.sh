#!/usr/bin/env bash
# bootstrap-feature.sh
#
# Create feature directory structure for a new spec.
# Usage: bash bootstrap-feature.sh [feature-slug]
#
# Creates: .aidocs/features/backlog/NN-slug/spec.md

set -euo pipefail

DOCS_DIR=".aidocs/features/backlog"

if [ ! -d "$DOCS_DIR" ]; then
    echo "ERROR: $DOCS_DIR not found. Run from the project root." >&2
    exit 1
fi

# Find next available two-digit prefix
last=$(ls "$DOCS_DIR" 2>/dev/null | grep -Eo "^[0-9]+" | sort -n | tail -1 || echo "0")
next=$(printf "%02d" $(( ${last:-0} + 1 )))

# Accept slug from argument or prompt
if [ -n "${1:-}" ]; then
    slug="$1"
else
    read -rp "Feature slug (e.g. user-auth): " slug
fi

feature_dir="$DOCS_DIR/${next}-${slug}"
mkdir -p "$feature_dir"

cat > "$feature_dir/spec.md" <<EOF
# Feature: ${slug}

**Version:** 1.0
**Status:** Draft
**Author:**
**Date:** $(date +%Y-%m-%d)
**Project:**

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | \`.aidocs/constitution.md\` |

---

## Overview

{2-3 sentences describing the feature and its purpose}

---

## Problem Statement

**Who:** {User persona}
**Problem:** {What they cannot do}
**Impact:** {Business/user impact}
**Solution:** {High-level approach — no implementation details}
**Success Metric:** {How we measure success}

---

## User Personas

### Persona 1: {Name/Archetype}
- **Role:** {What they do}
- **Goal:** {What they want}
- **Pain Points:** {Current frustrations}
- **Context:** {When/where they use product}

---

## User Stories

### US-001: {Story Title}
**As a** {persona}
**I want to** {action}
**So that** {benefit}

**Priority:** Must | Should | Could

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL | US-001 | Must |

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |

---

## Acceptance Criteria

### AC-001: {Scenario Title}

**Given:** {precondition}
**When:** {action}
**Then:** {expected result}

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| {Feature} | {Why excluded} | {Phase 2 / Never} |

---

## Assumptions & Constraints

### Assumptions
- {Assumption 1}

### Constraints
- {Constraint 1}

---

## Dependencies

### Internal
- {Other feature this depends on}

### External
- {Third-party service}
EOF

echo "Created: $feature_dir/spec.md"
