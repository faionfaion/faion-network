#!/usr/bin/env bash
# check-shadcn-pristine.sh
# Fail CI if components/ui/* was hand-edited outside the explicit allowlist.
# Add to .husky/pre-commit or GitHub Actions.
#
# Allowlist: create a .shadcn-allow file listing approved edits, one file per line.
# Example .shadcn-allow:
#   components/ui/button.tsx
set -euo pipefail

ALLOW_FILE=".shadcn-allow"

# Diff against the previous commit (HEAD~1) or the merge base in CI
if git rev-parse HEAD~1 &>/dev/null; then
  DIRTY=$(git diff --name-only HEAD~1 HEAD -- 'components/ui/*' 2>/dev/null || true)
else
  # First commit — nothing to check
  DIRTY=""
fi

if [[ -z "$DIRTY" ]]; then
  echo "shadcn primitives untouched."
  exit 0
fi

if [[ ! -f "$ALLOW_FILE" ]]; then
  echo "ERROR: Edits inside components/ui/ require an explicit allowlist ($ALLOW_FILE)."
  echo "Edited files:"
  echo "$DIRTY"
  echo ""
  echo "To approve an edit, add the file path to $ALLOW_FILE and commit."
  exit 1
fi

UNAPPROVED=""
while IFS= read -r file; do
  if ! grep -qxF "$file" "$ALLOW_FILE"; then
    UNAPPROVED="${UNAPPROVED}  ${file}\n"
  fi
done <<< "$DIRTY"

if [[ -n "$UNAPPROVED" ]]; then
  echo "ERROR: Unapproved edits in components/ui/:"
  echo -e "$UNAPPROVED"
  echo "Add these paths to $ALLOW_FILE or revert the changes."
  exit 1
fi

echo "shadcn primitives: all edits approved via $ALLOW_FILE."
