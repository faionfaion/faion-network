#!/usr/bin/env python3
"""webhook-handler.py — Receive ticket-created events, invoke classifier, write triage record, route.

When to call: On ticket creation.

This is a methodology-shipped stub. Replace with the project-specific
implementation when wiring into a real pipeline.

Usage:
    --self-test    run a smoke check
    --help         this message
"""
from __future__ import annotations

import argparse
import sys


def self_test() -> int:
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
