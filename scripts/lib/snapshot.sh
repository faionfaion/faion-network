#!/bin/bash
# Snapshot management for faion-network updates
# Creates/restores/rotates lightweight tarballs of critical directories

SNAPSHOT_DIR="${HOME}/.cache/faion-network/snapshots"
MAX_SNAPSHOTS=3

# Directories and files to include in snapshot
SNAPSHOT_DIRS=(skills hooks agents)
SNAPSHOT_FILES=(AGENTS.md settings.local.json)

snapshot_init() {
    mkdir -p "$SNAPSHOT_DIR"
}

snapshot_create() {
    local repo_dir="$1"
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local snapshot_path="${SNAPSHOT_DIR}/snapshot_${timestamp}.tar.gz"

    snapshot_init

    local tar_args=()
    for dir in "${SNAPSHOT_DIRS[@]}"; do
        [[ -d "${repo_dir}/${dir}" ]] && tar_args+=("${dir}")
    done
    for file in "${SNAPSHOT_FILES[@]}"; do
        [[ -f "${repo_dir}/${file}" ]] && tar_args+=("${file}")
    done

    if [[ ${#tar_args[@]} -eq 0 ]]; then
        log_warning "Nothing to snapshot"
        return 1
    fi

    tar -czf "$snapshot_path" -C "$repo_dir" "${tar_args[@]}" 2>/dev/null || {
        log_error "Failed to create snapshot"
        return 1
    }

    # Save git HEAD alongside snapshot for reliable rollback
    git -C "$repo_dir" rev-parse HEAD > "${snapshot_path%.tar.gz}.head" 2>/dev/null || true

    local size
    size=$(du -h "$snapshot_path" | cut -f1)

    # Enforce 5MB size limit
    local size_bytes
    size_bytes=$(stat -c%s "$snapshot_path" 2>/dev/null || stat -f%z "$snapshot_path" 2>/dev/null || echo 0)
    if [[ $size_bytes -gt 5242880 ]]; then
        log_error "Snapshot exceeds 5MB limit (${size}): ${snapshot_path}"
        rm -f "$snapshot_path" "${snapshot_path%.tar.gz}.head"
        return 1
    fi

    log_success "Snapshot created: ${snapshot_path} (${size})"

    snapshot_rotate
    return 0
}

snapshot_list() {
    snapshot_init
    find "$SNAPSHOT_DIR" -name "snapshot_*.tar.gz" -type f | sort -r
}

snapshot_latest() {
    snapshot_list | head -1
}

snapshot_restore() {
    local repo_dir="$1"
    local snapshot_path="${2:-$(snapshot_latest)}"

    if [[ -z "$snapshot_path" ]] || [[ ! -f "$snapshot_path" ]]; then
        log_error "No snapshot found to restore"
        return 1
    fi

    log_info "Restoring from: $(basename "$snapshot_path")"

    # List what will be restored
    log_info "Contents:"
    tar -tzf "$snapshot_path" | head -20 | while read -r entry; do
        log_file "$entry"
    done

    # Extract to temp dir first, then swap — so a failed extract doesn't
    # leave us with deleted dirs and no restore
    local snapshot_contents
    snapshot_contents=$(tar -tzf "$snapshot_path")

    local tmp_dir
    tmp_dir=$(mktemp -d) || {
        log_error "Failed to create temp directory for restore"
        return 1
    }

    tar -xzf "$snapshot_path" -C "$tmp_dir" || {
        log_error "Failed to extract snapshot (tarball may be corrupt)"
        rm -rf "$tmp_dir"
        return 1
    }

    # Extraction succeeded — safe to remove and replace
    for dir in "${SNAPSHOT_DIRS[@]}"; do
        if echo "$snapshot_contents" | grep -q "^${dir}/"; then
            rm -rf "${repo_dir:?}/${dir}"
            mv "${tmp_dir}/${dir}" "${repo_dir}/${dir}"
        fi
    done

    # Restore individual files from snapshot
    for file in "${SNAPSHOT_FILES[@]}"; do
        if [[ -f "${tmp_dir}/${file}" ]]; then
            mv -f "${tmp_dir}/${file}" "${repo_dir}/${file}"
        fi
    done

    rm -rf "$tmp_dir"

    log_success "Restored from: $(basename "$snapshot_path")"
    return 0
}

snapshot_rotate() {
    local snapshots
    snapshots=$(snapshot_list)
    local count
    count=$(echo "$snapshots" | grep -c "." 2>/dev/null || echo 0)

    if [[ $count -gt $MAX_SNAPSHOTS ]]; then
        local to_delete
        to_delete=$(echo "$snapshots" | tail -n +$((MAX_SNAPSHOTS + 1)))
        echo "$to_delete" | while read -r old; do
            rm -f "$old" "${old%.tar.gz}.head"
            log_info "Removed old snapshot: $(basename "$old")"
        done
    fi
}
