#!/usr/bin/env bash
# new-feature.sh — scaffold a new feature directory with stub spec and impl plan
# Usage: new-feature.sh FEATURE_SLUG [DOCS_DIR]
# Example: new-feature.sh user-auth .aidocs

SLUG=${1:?Usage: new-feature.sh feature-slug [.aidocs]}
DIR=${2:-.aidocs}/backlog/$SLUG

mkdir -p "$DIR"/{todo,in-progress,done}

cat > "$DIR/spec.md" << 'EOF'
# Feature: {Feature Name}

**Version:** 1.0
**Status:** Draft
**Date:** YYYY-MM-DD

## Problem Statement
**Who:**
**Problem:**
**Impact:**
**Solution:**
**Success Metric:**

## User Stories

### US-001: {Title}
**As a**
**I want to**
**So that**
**Priority:** Must

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL | US-001 | Must |

## Acceptance Criteria

### AC-001: {Happy Path}
**Given:**
**When:**
**Then:**

### AC-002: {Error Case}
**Given:**
**When:**
**Then:**

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
EOF

cat > "$DIR/implementation-plan.md" << 'EOF'
# Implementation Plan: {Feature Name}

**Version:** 1.0
**Status:** Draft

## Overview

- **Total tasks:**
- **Complexity:**
- **Est. tokens:** ~k total
- **Critical path:**

## Task Summary

| Task | Name | Complexity | Est. Tokens | Depends On | Enables |
|------|------|------------|-------------|------------|---------|

## Dependency Graph

```
(add after wave analysis)
```

## Execution Waves

### Wave 1 (Parallel)
(add after WBS)

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
EOF

echo "Created $DIR with spec.md and implementation-plan.md stubs"
