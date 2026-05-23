#!/usr/bin/env bash
# gh-backlog-export.sh — export GitHub Issues labeled "backlog" to RICE-ready CSV
# Usage: gh-backlog-export.sh OWNER/REPO
# Requires: gh CLI (https://cli.github.com) and jq

REPO="${1:?Usage: $0 owner/repo}"

gh issue list \
  --repo "$REPO" \
  --label "backlog" \
  --limit 100 \
  --json number,title,labels,assignees,body \
  | jq -r '
    ["ID","Title","Labels","Assignee"] ,
    (.[] | [
      .number,
      .title,
      ([.labels[].name] | join(",")),
      (if .assignees | length > 0 then .assignees[0].login else "" end)
    ])
    | @csv
  ' \
  > backlog-export.csv

echo "Exported $(wc -l < backlog-export.csv) rows to backlog-export.csv"
echo "Next: open in spreadsheet and add Reach, Impact, Confidence, Effort columns for RICE scoring"
