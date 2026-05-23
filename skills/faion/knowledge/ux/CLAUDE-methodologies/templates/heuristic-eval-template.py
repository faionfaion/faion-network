# purpose: Pre-existing template carried into the CLAUDE-methodologies methodology
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml for produces=playbook-step
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""
Print a Nielsen's 10 Usability Heuristics evaluation scoring template.
Usage: python heuristic-eval-template.py > evaluation.md
"""

HEURISTICS = [
    ("H1", "Visibility of system status",
     "Does the system always keep users informed about what is going on?"),
    ("H2", "Match between system and real world",
     "Does the system use words, phrases, and concepts familiar to the user?"),
    ("H3", "User control and freedom",
     "Do users have clearly marked exits and undo/redo support?"),
    ("H4", "Consistency and standards",
     "Does the interface follow platform conventions and maintain internal consistency?"),
    ("H5", "Error prevention",
     "Does the design prevent problems from occurring in the first place?"),
    ("H6", "Recognition rather than recall",
     "Are objects, actions, and options visible? Is user memory load minimized?"),
    ("H7", "Flexibility and efficiency of use",
     "Are there accelerators for expert users? Can users personalize frequent actions?"),
    ("H8", "Aesthetic and minimalist design",
     "Does the UI contain only relevant information? Is irrelevant information absent?"),
    ("H9", "Help users recognize, diagnose, and recover from errors",
     "Are error messages in plain language? Do they suggest a solution?"),
    ("H10", "Help and documentation",
     "Is help easy to search? Is it task-focused and concise?"),
]

SEVERITY_SCALE = """
Severity scale:
  0 = Cosmetic — fix only if time allows
  1 = Minor — low priority fix
  2 = Major — high priority; fix before release
  3 = Catastrophic — must fix before release
"""


def print_template(product_name: str = "Product Name", evaluator: str = "Evaluator"):
    print(f"# Heuristic Evaluation: {product_name}")
    print(f"Evaluator: {evaluator}\n")
    print(SEVERITY_SCALE)
    print("---\n")

    for hid, name, description in HEURISTICS:
        print(f"## {hid}: {name}")
        print(f"*{description}*\n")
        print("- Rating: `pass` / `partial` / `fail` / `N/A`")
        print("- Issue: ")
        print("- Evidence (screenshot or element): ")
        print("- Severity: 0 / 1 / 2 / 3")
        print("- Proposed fix: ")
        print()


if __name__ == "__main__":
    import sys
    product = sys.argv[1] if len(sys.argv) > 1 else "Product Name"
    evaluator = sys.argv[2] if len(sys.argv) > 2 else "Evaluator"
    print_template(product, evaluator)
