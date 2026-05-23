#!/usr/bin/env python3
"""estimate-tokens.py — Estimate token budget for task context components.

Usage:
  python3 estimate-tokens.py --sdd-docs docs.txt --research research.txt --impl impl.txt

Or use interactively: provide text strings for each budget phase.
Outputs component breakdown and total with pass/fail against 100k limit.

Requires: tiktoken (pip install tiktoken)
Falls back to word-count approximation (1 word ~ 1.3 tokens) if tiktoken unavailable.
"""
import sys


def count_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        # Approximation: 1 word ~ 1.3 tokens
        return int(len(text.split()) * 1.3)


def check_budget(
    sdd_docs: str = "",
    dependency_tree: str = "",
    research: str = "",
    implementation: str = "",
    tests: str = "",
    limit: int = 100_000,
) -> dict:
    budget = {
        "sdd_docs": count_tokens(sdd_docs),
        "dependency_tree": count_tokens(dependency_tree),
        "research": count_tokens(research),
        "implementation": count_tokens(implementation),
        "tests": count_tokens(tests),
    }
    budget["total"] = sum(budget.values())
    budget["limit"] = limit
    budget["ok"] = budget["total"] < limit
    budget["remaining"] = limit - budget["total"]
    return budget


def print_report(b: dict) -> None:
    print("=== Task Token Budget ===")
    print(f"  SDD Docs:         {b['sdd_docs']:>7,} tokens  (target ~15k)")
    print(f"  Dependency Tree:  {b['dependency_tree']:>7,} tokens  (target ~10k)")
    print(f"  Research:         {b['research']:>7,} tokens  (target ~25k)")
    print(f"  Implementation:   {b['implementation']:>7,} tokens  (target ~40k)")
    print(f"  Tests:            {b['tests']:>7,} tokens  (target ~10k)")
    print(f"  {'─' * 40}")
    print(f"  Total:            {b['total']:>7,} tokens")
    print(f"  Limit:            {b['limit']:>7,} tokens")
    print(f"  Remaining:        {b['remaining']:>7,} tokens")
    print()
    if b["ok"]:
        print("RESULT: OK — within 100k token budget")
    else:
        over = b["total"] - b["limit"]
        print(f"RESULT: FAIL — {over:,} tokens over budget; split task before proceeding")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Demo mode
        sample = check_budget(
            sdd_docs="constitution spec design " * 1000,
            dependency_tree="prior task summary " * 500,
            research="existing code patterns " * 1000,
        )
        print_report(sample)
    else:
        import argparse
        p = argparse.ArgumentParser(description="Estimate task token budget")
        p.add_argument("--sdd-docs", default="", help="SDD document text")
        p.add_argument("--dependency-tree", default="", help="Dependency tree text")
        p.add_argument("--research", default="", help="Research context text")
        p.add_argument("--impl", default="", help="Implementation text")
        p.add_argument("--tests", default="", help="Test code text")
        args = p.parse_args()
        report = check_budget(
            sdd_docs=args.sdd_docs,
            dependency_tree=args.dependency_tree,
            research=args.research,
            implementation=args.impl,
            tests=args.tests,
        )
        print_report(report)
        sys.exit(0 if report["ok"] else 1)
