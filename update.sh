#!/bin/bash
# Faion Network Updater
# Updates Claude Code skills and agents from faion-network repository

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Flags
AUTO_YES=false
FORCE_REMOTE=false
SKIP_CONFLICTS=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -y|--yes)
            AUTO_YES=true
            shift
            ;;
        --theirs)
            FORCE_REMOTE=true
            shift
            ;;
        --skip-conflicts)
            SKIP_CONFLICTS=true
            shift
            ;;
        -h|--help)
            echo "Faion Network Updater"
            echo ""
            echo "Usage: ./update.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -y, --yes          Non-interactive mode"
            echo "  --theirs           Always take remote version on conflicts"
            echo "  --skip-conflicts   Skip conflicting files, update only clean ones"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./update.sh                    # Interactive update"
            echo "  ./update.sh -y --theirs        # Auto-update, take all from remote"
            echo "  ./update.sh -y --skip-conflicts # Auto-update, skip conflicts"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_file() {
    echo -e "  ${CYAN}→${NC} $1"
}

confirm() {
    if [ "$AUTO_YES" = true ]; then
        return 0
    fi

    local prompt="$1 [y/N] "
    read -p "$prompt" -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

select_option() {
    if [ "$FORCE_REMOTE" = true ]; then
        return 1  # Option 1: take remote
    fi
    if [ "$SKIP_CONFLICTS" = true ]; then
        return 2  # Option 2: skip conflicts
    fi

    echo ""
    echo "Choose how to handle conflicts:"
    echo "  1) Take ALL from remote (overwrite local changes)"
    echo "  2) Skip conflicts (update only non-conflicting files)"
    echo "  3) Cancel update"
    echo ""

    while true; do
        read -p "Your choice [1/2/3]: " -n 1 -r
        echo
        case $REPLY in
            1) return 1 ;;
            2) return 2 ;;
            3) return 3 ;;
            *) echo "Please enter 1, 2, or 3" ;;
        esac
    done
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verify we're in .claude directory
if [[ ! -d "$SCRIPT_DIR/skills" ]] || [[ ! -d "$SCRIPT_DIR/.git" ]]; then
    log_error "This script must be run from the .claude directory"
    log_error "Expected to find 'skills/' directory and git repository"
    exit 1
fi

cd "$SCRIPT_DIR"

echo ""
log_info "Faion Network Updater"
echo ""

# Check remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [[ -z "$REMOTE_URL" ]]; then
    log_error "No git remote configured"
    log_info "Run init.sh first to set up the repository"
    exit 1
fi

log_info "Remote: $REMOTE_URL"

# Fetch latest changes
log_info "Fetching latest changes..."
git fetch origin master 2>/dev/null || {
    log_error "Failed to fetch from remote"
    log_info "Check your internet connection"
    exit 1
}

# Check if we're behind
LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse origin/master 2>/dev/null)
BASE=$(git merge-base HEAD origin/master 2>/dev/null || echo "")

if [[ "$LOCAL" == "$REMOTE" ]]; then
    log_success "Already up to date!"
    exit 0
fi

if [[ -z "$BASE" ]]; then
    log_warning "Repositories have diverged significantly"
    log_info "Consider running init.sh for a fresh install"
    exit 1
fi

# Count commits behind
COMMITS_BEHIND=$(git rev-list --count HEAD..origin/master)
log_info "You are $COMMITS_BEHIND commit(s) behind"

# Show what will be updated
echo ""
log_info "Changes from remote:"
git log --oneline HEAD..origin/master | while read line; do
    log_file "$line"
done

# Check for local changes
LOCAL_CHANGES=$(git status --porcelain)
if [[ -n "$LOCAL_CHANGES" ]]; then
    echo ""
    log_warning "You have uncommitted local changes:"
    echo "$LOCAL_CHANGES" | while read line; do
        log_file "$line"
    done
    echo ""

    if ! confirm "Stash local changes and continue?"; then
        log_info "Update cancelled"
        exit 0
    fi

    git stash push -m "Auto-stash before faion-network update $(date +%Y-%m-%d)"
    log_success "Local changes stashed"
fi

# Try to merge
echo ""
log_info "Attempting to merge..."

# First, try a clean merge
if git merge origin/master --no-edit 2>/dev/null; then
    log_success "Updated successfully!"

    # Show updated files
    echo ""
    log_info "Updated files:"
    git diff --name-only HEAD~$COMMITS_BEHIND HEAD | while read file; do
        log_file "$file"
    done

    exit 0
fi

# Merge failed - we have conflicts
log_warning "Merge conflicts detected!"
echo ""

# Get list of conflicting files
CONFLICTING_FILES=$(git diff --name-only --diff-filter=U)
CONFLICT_COUNT=$(echo "$CONFLICTING_FILES" | wc -l)

log_warning "Conflicting files ($CONFLICT_COUNT):"
echo "$CONFLICTING_FILES" | while read file; do
    log_file "$file"
done

# Ask user what to do
select_option
CHOICE=$?

case $CHOICE in
    1)
        # Take all from remote
        log_info "Taking all changes from remote..."

        git merge --abort 2>/dev/null || true
        git reset --hard origin/master

        log_success "Updated to latest remote version"

        echo ""
        log_info "Updated files:"
        git diff --name-only HEAD~$COMMITS_BEHIND HEAD 2>/dev/null | while read file; do
            log_file "$file"
        done
        ;;
    2)
        # Skip conflicts, update only clean files
        log_info "Updating non-conflicting files only..."

        # Abort merge
        git merge --abort 2>/dev/null || true

        # Get list of files changed in remote that don't conflict
        ALL_REMOTE_FILES=$(git diff --name-only HEAD origin/master)

        UPDATED_COUNT=0
        SKIPPED_COUNT=0

        for file in $ALL_REMOTE_FILES; do
            # Check if this file is in conflict list
            if echo "$CONFLICTING_FILES" | grep -q "^$file$"; then
                log_warning "  Skipped (conflict): $file"
                ((SKIPPED_COUNT++))
            else
                # Checkout this file from remote
                git checkout origin/master -- "$file" 2>/dev/null && {
                    log_success "  Updated: $file"
                    ((UPDATED_COUNT++))
                } || {
                    log_warning "  Failed: $file"
                }
            fi
        done

        echo ""
        log_info "Summary: $UPDATED_COUNT updated, $SKIPPED_COUNT skipped"

        if [[ $UPDATED_COUNT -gt 0 ]]; then
            git add -A
            git commit -m "Partial update from faion-network (skipped $SKIPPED_COUNT conflicts)"
            log_success "Changes committed"
        fi

        echo ""
        log_warning "Skipped files still have your local version"
        log_info "To update them later, resolve conflicts manually or run:"
        log_info "  ./update.sh --theirs"
        ;;
    3)
        # Cancel
        git merge --abort 2>/dev/null || true
        log_info "Update cancelled"
        log_info "Your local files are unchanged"
        exit 0
        ;;
esac

# Restore stashed changes if any
if git stash list | grep -q "Auto-stash before faion-network update"; then
    echo ""
    if confirm "Restore your stashed local changes?"; then
        if git stash pop; then
            log_success "Local changes restored"
        else
            log_warning "Could not auto-restore changes (conflicts)"
            log_info "Your changes are saved in: git stash list"
            log_info "Restore manually with: git stash pop"
        fi
    else
        log_info "Changes kept in stash"
        log_info "Restore later with: git stash pop"
    fi
fi

echo ""
log_success "Update complete!"
log_info "Restart Claude Code to load updated skills"
