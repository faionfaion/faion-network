#!/usr/bin/env bash
# purpose: Call Claude Code in --print mode to generate pytest test stubs for a source file.
# consumes: A source file path + repo CLAUDE.md context.
# produces: A pytest test file at tests/test_<source>.py.
# depends-on: claude CLI on PATH.
# token-budget-impact: ~600 tokens per invocation (Claude Code prompt + reply).
# gen-tests.sh — Generate pytest test stubs using Claude Code.
# Usage: bash gen-tests.sh <source_file>
# Input:  Python source file path
# Output: pytest test file at tests/test_<basename>.py (review before committing)

SOURCE=$1
if [ -z "$SOURCE" ]; then
  echo "Usage: gen-tests.sh <source_file>" && exit 1
fi

OUTFILE="tests/test_$(basename "$SOURCE" .py).py"
echo "Generating tests for $SOURCE → $OUTFILE"

claude --print "Generate pytest tests for the following Python file.
Cover: happy path, validation errors, edge cases, exception handling.
Use pytest fixtures. Follow AAA pattern (Arrange, Act, Assert).
Output only the Python code — no explanatory prose.

$(cat "$SOURCE")" > "$OUTFILE"

echo "Review $OUTFILE assertions for logical correctness before committing."
echo "Green CI from AI-generated tests does not guarantee meaningful coverage."