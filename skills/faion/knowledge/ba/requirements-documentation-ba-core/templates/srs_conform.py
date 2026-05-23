#!/usr/bin/env python3
# purpose: fail CI if SRS source violates the conformance schema
# consumes: path/to/srs.md, srs-conformance.yaml schema definition
# produces: violation list on stderr; exit 0 pass, exit 1 fail
# depends-on: content/02-output-contract.xml (schema reference), srs-conformance.yaml
# token-budget-impact: ~200 tokens of header + script body
"""srs_conform.py — fail CI if SRS source violates the conformance schema.
Usage: python srs_conform.py path/to/srs.md [schema.yaml]
Exit 0 = pass. Exit 1 = violations found.
"""
import re, sys, yaml
from pathlib import Path

schema_path = sys.argv[2] if len(sys.argv) > 2 else "srs-conformance.yaml"
schema = yaml.safe_load(Path(schema_path).read_text())
src = Path(sys.argv[1])
text = src.read_text()
errs: list[str] = []

for s in schema["mandatory_sections"]:
    if s not in text:
        errs.append(f"missing section: {s}")

fm_match = re.search(r"^---\n(.*?)\n---", text, re.S)
fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
for k in schema["mandatory_frontmatter"]:
    if k not in fm:
        errs.append(f"missing frontmatter: {k}")

req_pat = re.compile(schema["requirement_rules"]["id_pattern"])
for line in text.splitlines():
    m = re.match(r"^\s*\*\*((BR|UR|FR|NFR)-\d{3})\*\*", line)
    if m and not req_pat.match(m.group(1)):
        errs.append(f"bad id format: {m.group(1)}")

for w in schema["requirement_rules"]["forbidden_words"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(rf"\b{w}\b", ln, re.I):
            errs.append(f"line {n}: forbidden word '{w}'")

if schema["requirement_rules"]["shall_only"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(r"\b(should|may|might)\b", ln, re.I):
            errs.append(f"line {n}: non-shall modal in '{ln.strip()[:60]}'")

if errs:
    sys.stderr.write("\n".join(errs) + "\n")
    sys.exit(1)
print(f"OK — {src} passes conformance schema")
