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
echo "agent1" > "$TEST_REPO/agents/test-agent.md"
echo "# Skill" > "$TEST_REPO/skills/my-skill/SKILL.md"

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
echo "# Skill" > "$TEST_REPO/skills/my-skill/SKILL.md"

# ============================================
echo ""
echo "================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "================================"

[[ $TESTS_FAILED -eq 0 ]]
