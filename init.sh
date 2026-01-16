#!/bin/bash
# Faion Network Installer
# Installs Claude Code skills and agents from faion-network repository

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Flags
AUTO_YES=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -y|--yes)
            AUTO_YES=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Faion Network Installer"
            echo ""
            echo "Usage: ./init.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -y, --yes      Non-interactive mode, answer yes to all prompts"
            echo "  -v, --verbose  Show detailed output"
            echo "  -h, --help     Show this help message"
            echo ""
            echo "This script installs Faion Network skills and agents to ~/.claude/"
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

confirm() {
    if [ "$AUTO_YES" = true ]; then
        return 0
    fi

    local prompt="$1 [y/N] "
    read -p "$prompt" -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# Get script directory (where faion-network repo is)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="$(basename "$SCRIPT_DIR")"

# Verify we're in the right place
if [[ ! -d "$SCRIPT_DIR/skills" ]] || [[ ! -d "$SCRIPT_DIR/agents" ]]; then
    log_error "This script must be run from the faion-network repository"
    log_error "Expected to find 'skills/' and 'agents/' directories"
    exit 1
fi

log_info "Faion Network Installer"
echo ""

# Go one level up
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$PARENT_DIR/.claude"

log_info "Repository location: $SCRIPT_DIR"
log_info "Target location: $CLAUDE_DIR"
echo ""

# Check if .claude exists
if [[ -d "$CLAUDE_DIR" ]]; then
    log_warning ".claude directory already exists"

    # Check for existing skills
    EXISTING_SKILLS=()
    if [[ -d "$CLAUDE_DIR/skills" ]]; then
        while IFS= read -r -d '' skill; do
            skill_name=$(basename "$skill")
            EXISTING_SKILLS+=("$skill_name")
        done < <(find "$CLAUDE_DIR/skills" -maxdepth 1 -mindepth 1 -type d -print0 2>/dev/null)
    fi

    # Check for existing agents
    EXISTING_AGENTS=()
    if [[ -d "$CLAUDE_DIR/agents" ]]; then
        while IFS= read -r -d '' agent; do
            agent_name=$(basename "$agent")
            EXISTING_AGENTS+=("$agent_name")
        done < <(find "$CLAUDE_DIR/agents" -maxdepth 1 -mindepth 1 -name "*.md" -print0 2>/dev/null)
    fi

    # Check for existing commands
    EXISTING_COMMANDS=()
    if [[ -d "$CLAUDE_DIR/commands" ]]; then
        while IFS= read -r -d '' cmd; do
            cmd_name=$(basename "$cmd")
            EXISTING_COMMANDS+=("$cmd_name")
        done < <(find "$CLAUDE_DIR/commands" -maxdepth 1 -mindepth 1 -name "*.md" -print0 2>/dev/null)
    fi

    # Report existing content
    TOTAL_EXISTING=$((${#EXISTING_SKILLS[@]} + ${#EXISTING_AGENTS[@]} + ${#EXISTING_COMMANDS[@]}))

    if [[ $TOTAL_EXISTING -gt 0 ]]; then
        log_warning "Found existing content in .claude:"

        if [[ ${#EXISTING_SKILLS[@]} -gt 0 ]]; then
            echo "  Skills (${#EXISTING_SKILLS[@]}): ${EXISTING_SKILLS[*]}"
        fi
        if [[ ${#EXISTING_AGENTS[@]} -gt 0 ]]; then
            echo "  Agents (${#EXISTING_AGENTS[@]}): ${EXISTING_AGENTS[*]}"
        fi
        if [[ ${#EXISTING_COMMANDS[@]} -gt 0 ]]; then
            echo "  Commands (${#EXISTING_COMMANDS[@]}): ${EXISTING_COMMANDS[*]}"
        fi
        echo ""

        log_info "These will be preserved as your personal/project customizations"
        log_info "They will be added to parent .gitignore ($PARENT_DIR/.gitignore)"
        echo ""
    fi

    # Check if .claude is a git repo
    if [[ -d "$CLAUDE_DIR/.git" ]]; then
        log_info ".claude is already a git repository"

        # Check remote
        CURRENT_REMOTE=$(git -C "$CLAUDE_DIR" remote get-url origin 2>/dev/null || echo "none")
        if [[ "$CURRENT_REMOTE" == *"faion-network"* ]]; then
            log_success "Already connected to faion-network"

            if ! confirm "Update from remote?"; then
                log_info "Skipping update"
                exit 0
            fi

            log_info "Pulling latest changes..."
            git -C "$CLAUDE_DIR" pull origin master
            log_success "Updated successfully"
            exit 0
        else
            log_warning "Connected to different remote: $CURRENT_REMOTE"
        fi
    fi

    # Confirm merge
    echo ""
    log_warning "This will merge faion-network into your existing .claude directory"
    log_info "Your existing skills/agents/commands will be preserved"
    log_info "New faion-network content will be added"
    echo ""

    if ! confirm "Continue with merge?"; then
        log_info "Installation cancelled"
        exit 0
    fi

    # Initialize git in .claude if needed
    if [[ ! -d "$CLAUDE_DIR/.git" ]]; then
        log_info "Initializing git repository in .claude..."
        git -C "$CLAUDE_DIR" init
    fi

    # Create/update .gitignore in PARENT directory for personal content
    PARENT_GITIGNORE="$PARENT_DIR/.gitignore"

    log_info "Updating parent .gitignore to preserve your customizations..."
    log_info "  Location: $PARENT_GITIGNORE"

    # Initialize git in parent if needed (for the .gitignore to make sense)
    if [[ ! -d "$PARENT_DIR/.git" ]]; then
        log_info "Initializing git repository in parent directory..."
        git -C "$PARENT_DIR" init
    fi

    # Add header if file is new or doesn't have our section
    if [[ ! -f "$PARENT_GITIGNORE" ]]; then
        echo "# Personal/Project .claude customizations" > "$PARENT_GITIGNORE"
        echo "# These are preserved during faion-network updates" >> "$PARENT_GITIGNORE"
        echo "" >> "$PARENT_GITIGNORE"
    elif ! grep -q "Personal/Project .claude customizations" "$PARENT_GITIGNORE" 2>/dev/null; then
        echo "" >> "$PARENT_GITIGNORE"
        echo "# Personal/Project .claude customizations" >> "$PARENT_GITIGNORE"
        echo "# These are preserved during faion-network updates" >> "$PARENT_GITIGNORE"
    fi

    # Add existing skills to parent gitignore
    for skill in "${EXISTING_SKILLS[@]}"; do
        if ! grep -q "^\.claude/skills/$skill/$" "$PARENT_GITIGNORE" 2>/dev/null; then
            echo ".claude/skills/$skill/" >> "$PARENT_GITIGNORE"
            log_info "  Added .claude/skills/$skill/ to parent .gitignore"
        fi
    done

    # Add existing agents to parent gitignore
    for agent in "${EXISTING_AGENTS[@]}"; do
        if ! grep -q "^\.claude/agents/$agent$" "$PARENT_GITIGNORE" 2>/dev/null; then
            echo ".claude/agents/$agent" >> "$PARENT_GITIGNORE"
            log_info "  Added .claude/agents/$agent to parent .gitignore"
        fi
    done

    # Add existing commands to parent gitignore
    for cmd in "${EXISTING_COMMANDS[@]}"; do
        if ! grep -q "^\.claude/commands/$cmd$" "$PARENT_GITIGNORE" 2>/dev/null; then
            echo ".claude/commands/$cmd" >> "$PARENT_GITIGNORE"
            log_info "  Added .claude/commands/$cmd to parent .gitignore"
        fi
    done

    # Copy new content
    log_info "Copying faion-network content..."

    # Copy skills (don't overwrite existing)
    for skill_dir in "$SCRIPT_DIR/skills/"*/; do
        skill_name=$(basename "$skill_dir")
        target_dir="$CLAUDE_DIR/skills/$skill_name"

        if [[ -d "$target_dir" ]]; then
            if [ "$VERBOSE" = true ]; then
                log_info "  Skipping skills/$skill_name (exists)"
            fi
        else
            cp -r "$skill_dir" "$target_dir"
            log_success "  Installed skills/$skill_name"
        fi
    done

    # Copy agents (don't overwrite existing)
    mkdir -p "$CLAUDE_DIR/agents"
    for agent_file in "$SCRIPT_DIR/agents/"*.md; do
        if [[ -f "$agent_file" ]]; then
            agent_name=$(basename "$agent_file")
            target_file="$CLAUDE_DIR/agents/$agent_name"

            if [[ -f "$target_file" ]]; then
                if [ "$VERBOSE" = true ]; then
                    log_info "  Skipping agents/$agent_name (exists)"
                fi
            else
                cp "$agent_file" "$target_file"
                log_success "  Installed agents/$agent_name"
            fi
        fi
    done

    # Copy commands (don't overwrite existing)
    mkdir -p "$CLAUDE_DIR/commands"
    for cmd_file in "$SCRIPT_DIR/commands/"*.md; do
        if [[ -f "$cmd_file" ]]; then
            cmd_name=$(basename "$cmd_file")
            target_file="$CLAUDE_DIR/commands/$cmd_name"

            if [[ -f "$target_file" ]]; then
                if [ "$VERBOSE" = true ]; then
                    log_info "  Skipping commands/$cmd_name (exists)"
                fi
            else
                cp "$cmd_file" "$target_file"
                log_success "  Installed commands/$cmd_name"
            fi
        fi
    done

    # Copy hooks
    if [[ -d "$SCRIPT_DIR/hooks" ]]; then
        mkdir -p "$CLAUDE_DIR/hooks"
        for hook_file in "$SCRIPT_DIR/hooks/"*; do
            if [[ -f "$hook_file" ]]; then
                hook_name=$(basename "$hook_file")
                target_file="$CLAUDE_DIR/hooks/$hook_name"

                if [[ -f "$target_file" ]]; then
                    if [ "$VERBOSE" = true ]; then
                        log_info "  Skipping hooks/$hook_name (exists)"
                    fi
                else
                    cp "$hook_file" "$target_file"
                    chmod +x "$target_file"
                    log_success "  Installed hooks/$hook_name"
                fi
            fi
        done
    fi

    # Copy other files (LICENSE, README, etc.)
    for file in "$SCRIPT_DIR"/*.md "$SCRIPT_DIR"/LICENSE; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")
            cp "$file" "$CLAUDE_DIR/$filename"
        fi
    done

    # Copy init.sh and update.sh
    cp "$SCRIPT_DIR/init.sh" "$CLAUDE_DIR/init.sh"
    cp "$SCRIPT_DIR/update.sh" "$CLAUDE_DIR/update.sh" 2>/dev/null || true
    chmod +x "$CLAUDE_DIR/init.sh"
    chmod +x "$CLAUDE_DIR/update.sh" 2>/dev/null || true

else
    # Fresh install - .claude doesn't exist
    log_info "Fresh installation - .claude directory will be created"
    echo ""

    if ! confirm "Install faion-network to $CLAUDE_DIR?"; then
        log_info "Installation cancelled"
        exit 0
    fi

    log_info "Creating .claude directory..."
    mkdir -p "$CLAUDE_DIR"

    # Copy everything
    log_info "Copying faion-network content..."
    cp -r "$SCRIPT_DIR/skills" "$CLAUDE_DIR/"
    cp -r "$SCRIPT_DIR/agents" "$CLAUDE_DIR/"
    cp -r "$SCRIPT_DIR/commands" "$CLAUDE_DIR/"
    [[ -d "$SCRIPT_DIR/hooks" ]] && cp -r "$SCRIPT_DIR/hooks" "$CLAUDE_DIR/"

    # Copy other files
    for file in "$SCRIPT_DIR"/*.md "$SCRIPT_DIR"/LICENSE "$SCRIPT_DIR"/init.sh "$SCRIPT_DIR"/update.sh; do
        if [[ -f "$file" ]]; then
            cp "$file" "$CLAUDE_DIR/"
        fi
    done
    chmod +x "$CLAUDE_DIR/init.sh"
    chmod +x "$CLAUDE_DIR/update.sh" 2>/dev/null || true
    chmod +x "$CLAUDE_DIR/hooks/"* 2>/dev/null || true

    # Initialize git
    log_info "Initializing git repository..."
    git -C "$CLAUDE_DIR" init

    log_success "Installed successfully"
fi

# Set up remote
log_info "Configuring git remote..."
git -C "$CLAUDE_DIR" remote remove origin 2>/dev/null || true
git -C "$CLAUDE_DIR" remote add origin https://github.com/faionfaion/faion-network.git
log_success "Remote set to faion-network"

# Initial commit if needed
if ! git -C "$CLAUDE_DIR" rev-parse HEAD >/dev/null 2>&1; then
    log_info "Creating initial commit..."
    git -C "$CLAUDE_DIR" add -A
    git -C "$CLAUDE_DIR" commit -m "Initial faion-network installation"
fi

# Clean up - remove faion-network directory
echo ""
if [[ -d "$SCRIPT_DIR" ]] && [[ "$SCRIPT_DIR" != "$CLAUDE_DIR" ]]; then
    log_warning "The faion-network directory is no longer needed"
    log_info "Location: $SCRIPT_DIR"

    if confirm "Delete faion-network directory?"; then
        rm -rf "$SCRIPT_DIR"
        log_success "Cleaned up faion-network directory"
    else
        log_info "Keeping faion-network directory"
        log_info "You can delete it manually: rm -rf $SCRIPT_DIR"
    fi
fi

# Final summary
echo ""
echo "════════════════════════════════════════════════════════"
log_success "Faion Network installed successfully!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Location: $CLAUDE_DIR"
echo ""
echo "What's included:"
echo "  • Skills - Automated workflows for Claude Code"
echo "  • Agents - Specialized sub-agents for complex tasks"
echo "  • Commands - Slash commands (/faion-net, etc.)"
echo "  • Hooks - Auto-update and other automation"
echo ""
echo "To update in the future:"
echo "  cd $CLAUDE_DIR && git pull origin master"
echo ""
echo "Or run:"
echo "  $CLAUDE_DIR/init.sh"
echo ""
log_info "Restart Claude Code to load new skills"
