#!/bin/bash
# Post-update integrity check for faion-network
# Verifies critical files, structure, content, and permissions after update

# Counters per category
_IC_STRUCTURAL=0
_IC_SCHEMA=0
_IC_CROSSREF=0
_IC_PERMISSION=0

_ic_verbose() {
    [[ "${INTEGRITY_VERBOSE:-0}" == "1" ]] && log_warning "$1" || true
}

# --- Check 1: Structural (root files, dirs, SKILL.md presence + case) ---

_check_structural() {
    local repo_dir="$1"
    _IC_STRUCTURAL=0

    # Root AGENTS.md
    if [[ ! -f "${repo_dir}/AGENTS.md" ]]; then
        _ic_verbose "Missing: AGENTS.md"
        _IC_STRUCTURAL=$((_IC_STRUCTURAL + 1))
    fi

    # hooks/ directory
    if [[ ! -d "${repo_dir}/hooks" ]]; then
        _ic_verbose "Missing: hooks/ directory"
        _IC_STRUCTURAL=$((_IC_STRUCTURAL + 1))
    else
        local hook_count
        hook_count=$(find "${repo_dir}/hooks" -type f | wc -l)
        if [[ $hook_count -eq 0 ]]; then
            _ic_verbose "hooks/ directory is empty"
            _IC_STRUCTURAL=$((_IC_STRUCTURAL + 1))
        fi
    fi

    # skills/ directory and per-skill SKILL.md
    if [[ ! -d "${repo_dir}/skills" ]]; then
        _ic_verbose "Missing: skills/ directory"
        _IC_STRUCTURAL=$((_IC_STRUCTURAL + 1))
    else
        for skill_dir in "${repo_dir}/skills"/*/; do
            [[ ! -d "$skill_dir" ]] && continue
            local skill_name
            skill_name=$(basename "$skill_dir")
            [[ "$skill_name" == "CLAUDE.md" ]] && continue

            if [[ ! -f "${skill_dir}/SKILL.md" ]]; then
                if [[ -f "${skill_dir}/skill.md" ]]; then
                    _ic_verbose "Case mismatch: skills/${skill_name}/skill.md should be SKILL.md (rename skill.md → SKILL.md)"
                else
                    _ic_verbose "Missing SKILL.md in: skills/${skill_name}/"
                fi
                _IC_STRUCTURAL=$((_IC_STRUCTURAL + 1))
            fi
        done
    fi

    # agents/ directory (warning only — does not increment errors)
    if [[ ! -d "${repo_dir}/agents" ]]; then
        _ic_verbose "Warning: Missing agents/ directory"
    fi
}

# --- Check 2: Frontmatter schema validation ---

_check_schema() {
    local repo_dir="$1"
    _IC_SCHEMA=0

    [[ ! -d "${repo_dir}/skills" ]] && return

    for skill_dir in "${repo_dir}/skills"/*/; do
        [[ ! -d "$skill_dir" ]] && continue
        local skill_name
        skill_name=$(basename "$skill_dir")
        [[ "$skill_name" == "CLAUDE.md" ]] && continue

        local skill_file="${skill_dir}/SKILL.md"
        [[ ! -f "$skill_file" ]] && continue

        # Extract frontmatter (between first two --- lines)
        local in_frontmatter=0
        local has_name=0
        local has_description=0
        local has_user_invocable=0
        local line_num=0

        while IFS= read -r line; do
            line_num=$((line_num + 1))
            if [[ "$line" == "---" ]]; then
                if [[ $in_frontmatter -eq 1 ]]; then
                    break  # End of frontmatter
                else
                    in_frontmatter=1
                    continue
                fi
            fi
            if [[ $in_frontmatter -eq 1 ]]; then
                # Check name field: non-empty value after "name:"
                if [[ "$line" =~ ^name:[[:space:]]*[^[:space:]] ]]; then
                    has_name=1
                fi
                # Check description field: non-empty value after "description:"
                if [[ "$line" =~ ^description:[[:space:]]*[^[:space:]] ]]; then
                    has_description=1
                fi
                if [[ "$line" =~ ^user-invocable: ]]; then
                    has_user_invocable=1
                fi
            fi
        done < "$skill_file"

        if [[ $in_frontmatter -eq 0 ]]; then
            _ic_verbose "Schema: skills/${skill_name}/SKILL.md has no YAML frontmatter"
            _IC_SCHEMA=$((_IC_SCHEMA + 1))
            continue
        fi

        if [[ $has_name -eq 0 ]]; then
            _ic_verbose "Schema: skills/${skill_name}/SKILL.md missing required field 'name'"
            _IC_SCHEMA=$((_IC_SCHEMA + 1))
        fi
        if [[ $has_description -eq 0 ]]; then
            _ic_verbose "Schema: skills/${skill_name}/SKILL.md missing required field 'description'"
            _IC_SCHEMA=$((_IC_SCHEMA + 1))
        fi
        if [[ $has_user_invocable -eq 0 ]]; then
            _ic_verbose "Schema: skills/${skill_name}/SKILL.md missing optional field 'user-invocable'"
        fi
    done
}

# --- Check 3: Cross-reference verification ---
# SCOPE: Only scans SKILL.md files. Skill() references in CLAUDE.md, README.md,
# and other files are not checked. Expand to glob **/*.md if needed.

_check_crossrefs() {
    local repo_dir="$1"
    _IC_CROSSREF=0

    [[ ! -d "${repo_dir}/skills" ]] && return

    for skill_dir in "${repo_dir}/skills"/*/; do
        [[ ! -d "$skill_dir" ]] && continue
        local skill_name
        skill_name=$(basename "$skill_dir")
        [[ "$skill_name" == "CLAUDE.md" ]] && continue

        local skill_file="${skill_dir}/SKILL.md"
        [[ ! -f "$skill_file" ]] && continue

        local line_num=0
        while IFS= read -r line; do
            line_num=$((line_num + 1))
            # Match Skill(name) or Skill("name") patterns using bash regex
            local remaining="$line"
            while [[ "$remaining" =~ Skill\(\"?([a-zA-Z0-9_-]+)\"?\) ]]; do
                local ref_name="${BASH_REMATCH[1]}"
                remaining="${remaining#*${BASH_REMATCH[0]}}"

                # Skip obvious placeholder names used in documentation/examples
                if [[ "$ref_name" =~ ^(skill-name|your-skill|example-skill|skill_name)$ ]]; then
                    continue
                fi

                if [[ ! -d "${repo_dir}/skills/${ref_name}" ]] || \
                   [[ ! -f "${repo_dir}/skills/${ref_name}/SKILL.md" ]]; then
                    _ic_verbose "Cross-ref: skills/${skill_name}/SKILL.md:${line_num} references '${ref_name}' but skills/${ref_name}/SKILL.md not found"
                    _IC_CROSSREF=$((_IC_CROSSREF + 1))
                fi
            done
        done < "$skill_file"
    done
}

# --- Check 4: Hook executability ---

_check_permissions() {
    local repo_dir="$1"
    _IC_PERMISSION=0

    [[ ! -d "${repo_dir}/hooks" ]] && return

    for hook_file in "${repo_dir}/hooks"/*; do
        [[ ! -f "$hook_file" ]] && continue
        if [[ ! -x "$hook_file" ]]; then
            _ic_verbose "Permission: hooks/$(basename "$hook_file") is not executable (chmod +x to fix)"
            _IC_PERMISSION=$((_IC_PERMISSION + 1))
        fi
    done
}

# --- Main entry point ---

integrity_check() {
    local repo_dir="$1"

    log_info "Running post-update integrity check..."

    _check_structural "$repo_dir"
    _check_schema "$repo_dir"
    _check_crossrefs "$repo_dir"
    _check_permissions "$repo_dir"

    local total_errors=$((_IC_STRUCTURAL + _IC_SCHEMA + _IC_CROSSREF + _IC_PERMISSION))

    # Summary
    echo ""
    if [[ $total_errors -gt 0 ]]; then
        log_error "Integrity check FAILED: ${total_errors} error(s) [structural=${_IC_STRUCTURAL}, schema=${_IC_SCHEMA}, cross-ref=${_IC_CROSSREF}, permission=${_IC_PERMISSION}]"
        return 1
    else
        log_success "Integrity check passed"
        return 0
    fi
}
