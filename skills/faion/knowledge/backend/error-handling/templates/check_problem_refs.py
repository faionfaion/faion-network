#!/usr/bin/env python3
# purpose: Legacy template for the error-handling methodology.
# consumes: inputs declared in error-handling/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
"""CI script: validate every 4xx/5xx OpenAPI response refs ProblemDetail.

Usage: python check_problem_refs.py openapi.yaml
Exit 0 = pass, Exit 1 = failures found.
"""
import sys
import yaml


def main() -> int:
    spec = yaml.safe_load(open(sys.argv[1]))
    ok = True
    for path, ops in spec.get("paths", {}).items():
        for method, op in ops.items():
            if method.startswith("x-") or method == "parameters":
                continue
            for code, resp in op.get("responses", {}).items():
                if not (str(code).startswith("4") or str(code).startswith("5")):
                    continue
                ref = (
                    resp.get("content", {})
                    .get("application/problem+json", {})
                    .get("schema", {})
                    .get("$ref", "")
                )
                if not ref.endswith("/ProblemDetail"):
                    print(
                        f"FAIL {method.upper()} {path} {code} "
                        f"-> {ref or 'no application/problem+json schema'}"
                    )
                    ok = False
    if ok:
        print("OK: all 4xx/5xx responses reference ProblemDetail")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
