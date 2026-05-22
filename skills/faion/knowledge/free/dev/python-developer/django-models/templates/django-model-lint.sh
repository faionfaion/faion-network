# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

#!/usr/bin/env bash
# django-model-lint.sh — AST-based lint for common Django model antipatterns.
# Fails (exit 1) if any issues found.
# Usage: bash scripts/django-model-lint.sh
set -euo pipefail

python - <<'PY'
import ast
import pathlib
import sys

fails = []

for p in pathlib.Path("apps").rglob("models.py"):
    try:
        tree = ast.parse(p.read_text())
    except SyntaxError as e:
        fails.append(f"{p}: SyntaxError: {e}")
        continue

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_attr = getattr(node.func, "attr", "")
        kwargs = {kw.arg for kw in node.keywords}

        # ForeignKey missing related_name
        if func_attr == "ForeignKey" and "related_name" not in kwargs:
            fails.append(f"{p}:{node.lineno}  ForeignKey missing related_name")

        # CharField with raw choices tuples instead of TextChoices
        if func_attr == "CharField":
            for kw in node.keywords:
                if kw.arg == "choices" and isinstance(kw.value, ast.List):
                    fails.append(
                        f"{p}:{node.lineno}  CharField uses raw choices list — use TextChoices"
                    )

for f in fails:
    print(f)

sys.exit(1 if fails else 0)
PY
