#!/bin/bash
# Unit tests for snapshot and integrity-check functions
# Uses temp directories — no side effects on the real system

TESTS_PASSED=0
TESTS_FAILED=0

# --- Test helpers ---
assert_eq() {
    local desc="$1" expected="$2" actual="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "  PASS: $desc"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "  FAIL: $desc (expected='$expected', actual='$actual')"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_ok() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "  FAIL: $desc (exit code $?)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_fail() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo "  FAIL: $desc (expected failure, got success)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    else
        echo "  PASS: $desc"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
}

# --- Setup ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Stub log functions (libraries expect these from caller)
log_info() { :; }
log_success() { :; }
log_warning() { :; }
log_error() { :; }
log_file() { :; }

# Source libraries
source "${REPO_DIR}/scripts/lib/snapshot.sh"
source "${REPO_DIR}/scripts/lib/integrity-check.sh"

# Override SNAPSHOT_DIR to use temp location
SNAPSHOT_DIR=$(mktemp -d)
TEST_REPO=$(mktemp -d)
trap 'rm -rf "$SNAPSHOT_DIR" "$TEST_REPO"' EXIT

# Create a fake repo structure
mkdir -p "$TEST_REPO"/{skills/my-skill,hooks,agents}
echo "# Agents" > "$TEST_REPO/AGENTS.md"
echo "hook1" > "$TEST_REPO/hooks/pre-commit.sh"
chmod +x "$TEST_REPO/hooks/pre-commit.sh"
echo "agent1" > "$TEST_REPO/agents/test-agent.md"
cat > "$TEST_REPO/skills/my-skill/SKILL.md" <<'SKILLEOF'
---
name: my-skill
description: "A test skill"
user-invocable: false
---

# My Skill
SKILLEOF

# Initialize git for HEAD saving
git -C "$TEST_REPO" init -q
git -C "$TEST_REPO" add -A
git -C "$TEST_REPO" commit -q -m "init"

# ============================================
echo "=== snapshot_create ==="

assert_ok "creates snapshot from valid repo" snapshot_create "$TEST_REPO"

snapshot_file=$(snapshot_latest)
assert_eq "snapshot file exists" "true" "$([[ -f "$snapshot_file" ]] && echo true || echo false)"

head_file="${snapshot_file%.tar.gz}.head"
assert_eq "head file created alongside snapshot" "true" "$([[ -f "$head_file" ]] && echo true || echo false)"

# Test with empty repo (nothing to snapshot)
EMPTY_REPO=$(mktemp -d)
assert_fail "fails on empty dir (nothing to snapshot)" snapshot_create "$EMPTY_REPO"
rm -rf "$EMPTY_REPO"

# ============================================
echo ""
echo "=== snapshot size limit ==="

BIG_REPO=$(mktemp -d)
mkdir -p "$BIG_REPO/skills"
dd if=/dev/urandom of="$BIG_REPO/skills/bigfile" bs=1M count=6 2>/dev/null
git -C "$BIG_REPO" init -q
git -C "$BIG_REPO" add -A
git -C "$BIG_REPO" commit -q -m "init"

assert_fail "rejects snapshot exceeding 5MB" snapshot_create "$BIG_REPO"
rm -rf "$BIG_REPO"

# ============================================
echo ""
echo "=== snapshot_list / snapshot_latest ==="

list_count=$(snapshot_list | grep -c "." 2>/dev/null || echo 0)
assert_eq "snapshot_list returns entries" "true" "$([[ $list_count -ge 1 ]] && echo true || echo false)"

latest=$(snapshot_latest)
assert_eq "snapshot_latest returns valid file" "true" "$([[ -f "$latest" ]] && echo true || echo false)"

# ============================================
echo ""
echo "=== snapshot_restore ==="

# Modify the test repo
echo "modified" > "$TEST_REPO/AGENTS.md"
rm -rf "$TEST_REPO/hooks"

assert_ok "restores from snapshot" snapshot_restore "$TEST_REPO" "$snapshot_file"

assert_eq "AGENTS.md content restored" "# Agents" "$(cat "$TEST_REPO/AGENTS.md")"
assert_eq "hooks/ directory restored" "true" "$([[ -d "$TEST_REPO/hooks" ]] && echo true || echo false)"

# Test restore with nonexistent path
assert_fail "fails with nonexistent snapshot" snapshot_restore "$TEST_REPO" "/nonexistent/path.tar.gz"

# ============================================
echo ""
echo "=== snapshot_rotate ==="

# Create extra snapshots to trigger rotation
for i in 1 2 3 4; do
    sleep 1
    snapshot_create "$TEST_REPO" >/dev/null 2>&1 || true
done

count_after=$(snapshot_list | grep -c "." 2>/dev/null || echo 0)
assert_eq "rotate keeps at most $MAX_SNAPSHOTS snapshots" "true" "$([[ $count_after -le $MAX_SNAPSHOTS ]] && echo true || echo false)"

# ============================================
echo ""
echo "=== integrity_check ==="

# Ensure test repo has required structure (snapshot_restore may have failed)
mkdir -p "$TEST_REPO/hooks"
echo "hook1" > "$TEST_REPO/hooks/pre-commit.sh"
chmod +x "$TEST_REPO/hooks/pre-commit.sh"

assert_ok "passes on valid repo structure" integrity_check "$TEST_REPO"

# Missing AGENTS.md
mv "$TEST_REPO/AGENTS.md" "$TEST_REPO/AGENTS.md.bak"
assert_fail "fails when AGENTS.md missing" integrity_check "$TEST_REPO"
mv "$TEST_REPO/AGENTS.md.bak" "$TEST_REPO/AGENTS.md"

# Missing hooks/
mv "$TEST_REPO/hooks" "$TEST_REPO/hooks_bak"
assert_fail "fails when hooks/ missing" integrity_check "$TEST_REPO"
mv "$TEST_REPO/hooks_bak" "$TEST_REPO/hooks"

# Missing SKILL.md
rm "$TEST_REPO/skills/my-skill/SKILL.md"
assert_fail "fails when SKILL.md missing in skill dir" integrity_check "$TEST_REPO"
cat > "$TEST_REPO/skills/my-skill/SKILL.md" <<'SKILLEOF'
---
name: my-skill
description: "A test skill"
user-invocable: false
---

# My Skill
SKILLEOF

# ============================================
echo ""
echo "=== integrity_check: case-mismatch ==="

# lowercase skill.md detected as case-mismatch error
mkdir -p "$TEST_REPO/skills/bad-case"
echo "# wrong" > "$TEST_REPO/skills/bad-case/skill.md"
assert_fail "fails when skill.md (lowercase) exists instead of SKILL.md" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/bad-case"

# ============================================
echo ""
echo "=== integrity_check: schema validation ==="

# Missing name field
mkdir -p "$TEST_REPO/skills/no-name"
cat > "$TEST_REPO/skills/no-name/SKILL.md" <<'EOF'
---
description: "Has description but no name"
---

# No Name
EOF
assert_fail "fails when SKILL.md missing 'name' field" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/no-name"

# Missing description field
mkdir -p "$TEST_REPO/skills/no-desc"
cat > "$TEST_REPO/skills/no-desc/SKILL.md" <<'EOF'
---
name: no-desc
---

# No Desc
EOF
assert_fail "fails when SKILL.md missing 'description' field" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/no-desc"

# No frontmatter at all
mkdir -p "$TEST_REPO/skills/no-fm"
echo "# Just content, no frontmatter" > "$TEST_REPO/skills/no-fm/SKILL.md"
assert_fail "fails when SKILL.md has no frontmatter" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/no-fm"

# ============================================
echo ""
echo "=== integrity_check: cross-reference ==="

# Ensure hooks/ exists (snapshot_restore may have failed, leaving hooks/ missing)
mkdir -p "$TEST_REPO/hooks"
echo "hook1" > "$TEST_REPO/hooks/pre-commit.sh"
chmod +x "$TEST_REPO/hooks/pre-commit.sh"

# Broken Skill() reference
mkdir -p "$TEST_REPO/skills/ref-test"
cat > "$TEST_REPO/skills/ref-test/SKILL.md" <<'EOF'
---
name: ref-test
description: "Tests cross-refs"
---

# Ref Test
Use `Skill(nonexistent-skill)` for magic.
EOF
assert_fail "fails on broken Skill(nonexistent-skill) cross-reference" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/ref-test"

# Placeholder Skill(skill-name) should be skipped, not flagged as broken
mkdir -p "$TEST_REPO/skills/placeholder-test"
cat > "$TEST_REPO/skills/placeholder-test/SKILL.md" <<'EOF'
---
name: placeholder-test
description: "Contains placeholder example"
---

# Placeholder Test
**CRITICAL:** Invoke skills using `Skill(skill-name)`. This is an example.
EOF
assert_ok "passes when Skill(skill-name) placeholder is used in docs" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/placeholder-test"

# Valid Skill() reference (should pass)
mkdir -p "$TEST_REPO/skills/ref-ok"
cat > "$TEST_REPO/skills/ref-ok/SKILL.md" <<'EOF'
---
name: ref-ok
description: "Valid cross-ref"
---

# Ref OK
Use `Skill(my-skill)` here.
EOF
assert_ok "passes with valid Skill(my-skill) cross-reference" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/ref-ok"

# Multiple Skill() refs on one line — both valid
mkdir -p "$TEST_REPO/skills/multi-ref"
cat > "$TEST_REPO/skills/multi-ref/SKILL.md" <<'EOF'
---
name: multi-ref
description: "Multiple refs per line"
---

# Multi Ref
Route to `Skill(my-skill)` and `Skill(my-skill)` for coverage.
EOF
assert_ok "passes with multiple valid Skill() refs on one line" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/multi-ref"

# Multiple Skill() refs on one line — one broken
mkdir -p "$TEST_REPO/skills/multi-ref-bad"
cat > "$TEST_REPO/skills/multi-ref-bad/SKILL.md" <<'EOF'
---
name: multi-ref-bad
description: "One valid, one broken ref"
---

# Multi Ref Bad
Route to `Skill(my-skill)` and `Skill(no-such-skill)` together.
EOF
assert_fail "fails when one of multiple Skill() refs on same line is broken" integrity_check "$TEST_REPO"
rm -rf "$TEST_REPO/skills/multi-ref-bad"

# ============================================
echo ""
echo "=== integrity_check: hook permissions ==="

# Ensure hooks/ exists for permission tests
mkdir -p "$TEST_REPO/hooks"
echo "hook1" > "$TEST_REPO/hooks/pre-commit.sh"
chmod +x "$TEST_REPO/hooks/pre-commit.sh"

# Non-executable hook file
chmod -x "$TEST_REPO/hooks/pre-commit.sh"
assert_fail "fails when hook file lacks execute permission" integrity_check "$TEST_REPO"
chmod +x "$TEST_REPO/hooks/pre-commit.sh"

# Verify it passes again after fix
assert_ok "passes after fixing hook permissions" integrity_check "$TEST_REPO"

# ============================================
echo ""
echo "=== integrity_check: verbose mode ==="

# Verbose mode should produce warning output when errors exist
mkdir -p "$TEST_REPO/skills/verbose-test"
echo "# no frontmatter" > "$TEST_REPO/skills/verbose-test/SKILL.md"
# Capture log_warning calls by temporarily redefining it
_verbose_output=""
log_warning() { _verbose_output="${_verbose_output}${1}\n"; }
INTEGRITY_VERBOSE=1 integrity_check "$TEST_REPO" >/dev/null 2>&1 || true
log_warning() { :; }  # Restore stub
rm -rf "$TEST_REPO/skills/verbose-test"

if echo -e "$_verbose_output" | grep -q "Schema:.*verbose-test.*no.*frontmatter\|Schema:.*verbose-test.*missing"; then
    echo "  PASS: INTEGRITY_VERBOSE=1 produces expected warning output"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  FAIL: INTEGRITY_VERBOSE=1 did not produce expected warning output (got: $_verbose_output)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================
echo ""
echo "================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "================================"

[[ $TESTS_FAILED -eq 0 ]]
