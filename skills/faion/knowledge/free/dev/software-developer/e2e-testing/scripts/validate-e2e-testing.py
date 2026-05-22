#!/usr/bin/env python3
"""validate-e2e-testing.py — validate a Playwright E2E project against the methodology output contract.

Usage:
    validate-e2e-testing.py --root <e2e-dir>            # validate a real project
    validate-e2e-testing.py --self-test                  # run built-in fixture

Inputs: directory containing playwright.config.ts and e2e/.
Outputs: stdout JSON {ok: bool, violations: [{rule, file, line, snippet}]}
Exit codes: 0 = pass, 1 = violations found, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

FORBIDDEN = [
    (re.compile(r"page\.waitForTimeout\("), "rule:r4 hard sleep"),
    (re.compile(r"\{\s*force:\s*true\s*\}"), "rule:ap-05 force-click"),
    (re.compile(r"locator\(\s*['\"]css="), "rule:r3 css selector"),
    (re.compile(r"locator\(\s*['\"]//"), "rule:r3 xpath selector"),
    (re.compile(r"\b(test|describe)\.only\("), "spec: focused test"),
]


@dataclass
class Result:
    ok: bool = True
    violations: list[dict] = field(default_factory=list)


def scan(root: Path) -> Result:
    res = Result()
    e2e = root / "e2e"
    if not e2e.is_dir():
        res.ok = False
        res.violations.append({"rule": "structure", "file": str(e2e), "line": 0, "snippet": "missing e2e/ dir"})
        return res
    pages_dir = e2e / "pages"
    if not pages_dir.is_dir() or not any(pages_dir.glob("*.ts")):
        res.ok = False
        res.violations.append({"rule": "rule:r7", "file": str(pages_dir), "line": 0, "snippet": "missing Page Object files"})
    cfg = root / "playwright.config.ts"
    if not cfg.exists():
        res.ok = False
        res.violations.append({"rule": "structure", "file": str(cfg), "line": 0, "snippet": "missing playwright.config.ts"})
    for ts in e2e.rglob("*.ts"):
        for idx, line in enumerate(ts.read_text(encoding="utf-8").splitlines(), 1):
            for pat, rule in FORBIDDEN:
                if pat.search(line):
                    res.ok = False
                    res.violations.append({"rule": rule, "file": str(ts), "line": idx, "snippet": line.strip()})
    smoke_count = sum(
        1
        for ts in e2e.rglob("*.spec.ts")
        for line in ts.read_text(encoding="utf-8").splitlines()
        if "@smoke" in line or "@critical" in line
    )
    if smoke_count > 50:
        res.ok = False
        res.violations.append({"rule": "rule:r2", "file": "e2e/", "line": 0, "snippet": f"@smoke/@critical count = {smoke_count} > 50"})
    return res


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "playwright.config.ts").write_text("export default {};\n", encoding="utf-8")
        e2e = root / "e2e"
        (e2e / "pages").mkdir(parents=True)
        (e2e / "pages" / "LoginPage.ts").write_text("export class LoginPage {}\n", encoding="utf-8")
        (e2e / "fixtures.ts").write_text("export const test = base;\n", encoding="utf-8")
        bad = e2e / "bad.spec.ts"
        bad.write_text("test('bad', async ({page}) => { await page.waitForTimeout(1000); });\n", encoding="utf-8")
        res = scan(root)
        assert not res.ok, "self-test should detect waitForTimeout"
        assert any("rule:r4" in v["rule"] for v in res.violations), "should flag rule:r4"
        bad.write_text("test('good', async ({page}) => { await expect(page.getByTestId('x')).toBeVisible(); });\n", encoding="utf-8")
        res = scan(root)
        assert res.ok, f"self-test should pass after fix: {res.violations}"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, help="Project root containing playwright.config.ts and e2e/")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixture and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.root:
        ap.error("--root is required")
        return 2
    res = scan(args.root)
    sys.stdout.write(json.dumps({"ok": res.ok, "violations": res.violations}, indent=2) + "\n")
    return 0 if res.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
