#!/usr/bin/env python3
"""validate-a11y-annotation-pattern-library.py

Validate Accessibility Annotation Pattern Library artefact JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['library_version', 'archetypes']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    if isinstance(obj.get('archetypes'), list):
        for i, a in enumerate(obj['archetypes']):
            for k in ('archetype', 'role', 'name_pattern', 'states', 'keyboard_map', 'focus_behaviour'):
                if not a.get(k):
                    errs.append(f'archetypes[{i}] missing field: {k}')
    return errs


OK = {'library_version': '1.0.0', 'archetypes': [{'archetype': 'button', 'role': 'button', 'name_pattern': 'imperative verb phrase', 'states': ['default', 'hover', 'active', 'disabled'], 'keyboard_map': {'Enter': 'activate', 'Space': 'activate'}, 'focus_behaviour': 'visible 2px outline'}, {'archetype': 'link', 'role': 'link', 'name_pattern': 'destination noun phrase', 'states': ['default', 'visited', 'focus'], 'keyboard_map': {'Enter': 'activate'}, 'focus_behaviour': 'underline + outline'}, {'archetype': 'dialog', 'role': 'dialog', 'name_pattern': 'modal title', 'states': ['open', 'closed'], 'keyboard_map': {'Esc': 'close', 'Tab': 'trap focus'}, 'focus_behaviour': 'focus first focusable on open; restore on close'}, {'archetype': 'menu', 'role': 'menu', 'name_pattern': 'menu purpose', 'states': ['collapsed', 'expanded'], 'keyboard_map': {'ArrowDown': 'next item', 'ArrowUp': 'previous', 'Esc': 'close'}, 'focus_behaviour': 'roving tabindex'}, {'archetype': 'tabs', 'role': 'tablist', 'name_pattern': 'tab group label', 'states': ['selected', 'unselected'], 'keyboard_map': {'ArrowRight': 'next tab', 'ArrowLeft': 'previous', 'Home': 'first', 'End': 'last'}, 'focus_behaviour': 'manual or automatic activation'}, {'archetype': 'combobox', 'role': 'combobox', 'name_pattern': 'field purpose', 'states': ['closed', 'open', 'filtering'], 'keyboard_map': {'ArrowDown': 'open list', 'Enter': 'select', 'Esc': 'close'}, 'focus_behaviour': 'aria-activedescendant on listbox option'}, {'archetype': 'form_field', 'role': 'textbox', 'name_pattern': 'field label', 'states': ['empty', 'filled', 'error', 'disabled'], 'keyboard_map': {'Tab': 'next field'}, 'focus_behaviour': 'visible outline + error message announced via aria-describedby'}, {'archetype': 'data_table', 'role': 'table', 'name_pattern': 'table caption', 'states': ['sortable', 'sorted-asc', 'sorted-desc'], 'keyboard_map': {'ArrowKeys': 'cell navigation'}, 'focus_behaviour': 'cell-by-cell focus, optional row activation'}]}
BAD = {'library_version': '1', 'archetypes': [{'archetype': 'thing', 'role': 'button'}]}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
