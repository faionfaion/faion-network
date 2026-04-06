#!/bin/bash
# Post-update integrity check for faion-network
# Verifies critical files and structure after update

integrity_check() {
    local repo_dir="$1"
    local errors=0
    local warnings=0

    log_info "Running post-update integrity check..."

    # 1. Check root AGENTS.md exists
    if [[ ! -f "${repo_dir}/AGENTS.md" ]]; then
        log_error "Missing: AGENTS.md"
        errors=$((errors + 1))
    fi

    # 2. Check hooks/ directory and files
    if [[ ! -d "${repo_dir}/hooks" ]]; then
        log_error "Missing: hooks/ directory"
        errors=$((errors + 1))
    else
        local hook_count
        hook_count=$(find "${repo_dir}/hooks" -type f | wc -l)
        if [[ $hook_count -eq 0 ]]; then
            log_error "hooks/ directory is empty"
            errors=$((errors + 1))
        fi
    fi

    # 3. Check skills/ directory
    if [[ ! -d "${repo_dir}/skills" ]]; then
        log_error "Missing: skills/ directory"
        errors=$((errors + 1))
    else
        # 4. Check each skill dir has SKILL.md
        local skill_errors=0
        for skill_dir in "${repo_dir}/skills"/*/; do
            [[ ! -d "$skill_dir" ]] && continue
            local skill_name
            skill_name=$(basename "$skill_dir")

            # Skip CLAUDE.md — it's a file, not a skill dir
            [[ "$skill_name" == "CLAUDE.md" ]] && continue

            if [[ ! -f "${skill_dir}/SKILL.md" ]]; then
                log_error "Missing SKILL.md in: skills/${skill_name}/"
                skill_errors=$((skill_errors + 1))
            fi
        done

        if [[ $skill_errors -gt 0 ]]; then
            log_error "${skill_errors} skill(s) missing SKILL.md"
            errors=$((errors + skill_errors))
        fi
    fi

    # 5. Check agents/ directory
    if [[ ! -d "${repo_dir}/agents" ]]; then
        log_warning "Missing: agents/ directory"
        warnings=$((warnings + 1))
    fi

    # Summary
    echo ""
    if [[ $errors -gt 0 ]]; then
        log_error "Integrity check FAILED: ${errors} error(s), ${warnings} warning(s)"
        return 1
    elif [[ $warnings -gt 0 ]]; then
        log_warning "Integrity check passed with ${warnings} warning(s)"
        return 0
    else
        log_success "Integrity check passed"
        return 0
    fi
}
