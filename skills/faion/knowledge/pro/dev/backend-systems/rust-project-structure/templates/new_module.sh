#!/usr/bin/env bash
# new_module.sh <name>
# Creates stub files for a new domain entity across routes/handlers/services/db/models.
# Usage: ./scripts/new_module.sh products
set -euo pipefail

N="${1:?Usage: new_module.sh <name>}"

for dir in routes handlers services db models; do
    f="src/$dir/${N}.rs"
    if [ -e "$f" ]; then
        echo "ERROR: $f already exists" >&2
        exit 1
    fi
    printf "// %s/%s.rs\n\n// TODO: implement %s %s\n" "$dir" "$N" "$dir" "$N" > "$f"
    # Add pub mod declaration if not present
    MOD="src/$dir/mod.rs"
    if ! grep -q "pub mod $N;" "$MOD" 2>/dev/null; then
        echo "pub mod $N;" >> "$MOD"
    fi
    echo "created $f"
done

echo "Done. Created $N stubs in routes/handlers/services/db/models."
echo "Next: implement each file, then register routes in src/routes/mod.rs."
