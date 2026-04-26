#!/usr/bin/env python3
"""kr-lint.py — fail OKR YAML files containing task-shaped or unbaselined KRs.

Usage: python kr-lint.py okrs.yaml
Exit 0 = all KRs are valid outcomes with baselines.
Exit 1 = violations found (list printed to stdout).

Expected YAML structure:
  objectives:
    - name: "Objective text"
      key_results:
        - text: "KR text"
          baseline: 25
          target: 40
          deadline: "2026-Q2"
"""
import sys

TASK_VERBS = {
    "ship", "launch", "build", "release", "create",
    "design", "implement", "deploy", "complete", "finish",
    "write", "develop", "add", "set up", "establish",
}


def lint(path: str) -> list[str]:
    try:
        import yaml
    except ImportError:
        return ["ERROR: PyYAML not installed. Run: pip install pyyaml"]

    with open(path) as f:
        doc = yaml.safe_load(f)

    errors: list[str] = []

    for obj in doc.get("objectives", []):
        obj_name = obj.get("name", "?")
        for kr in obj.get("key_results", []):
            text = kr.get("text", "")
            first_word = text.lower().split()[0] if text.strip() else ""

            if first_word in TASK_VERBS:
                errors.append(
                    f"[{obj_name}] task-shaped KR (starts with '{first_word}'): '{text}'"
                )
            if "baseline" not in kr or kr["baseline"] is None:
                errors.append(
                    f"[{obj_name}] KR missing baseline: '{text}'"
                )
            if "target" not in kr or kr["target"] is None:
                errors.append(
                    f"[{obj_name}] KR missing target: '{text}'"
                )
            if "deadline" not in kr or not kr["deadline"]:
                errors.append(
                    f"[{obj_name}] KR missing deadline: '{text}'"
                )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: kr-lint.py <okrs.yaml>")
        sys.exit(1)

    errors = lint(sys.argv[1])
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
