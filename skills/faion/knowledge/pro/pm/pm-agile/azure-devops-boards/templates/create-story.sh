#!/usr/bin/env bash
# create-story.sh — create a User Story work item via Azure DevOps REST API.
#
# Required environment variables:
#   ADO_ORG   — organization name (e.g. myorg)
#   ADO_PROJ  — project name (e.g. MyProject)
#   ADO_PAT   — Personal Access Token (api scope)
#
# Usage:
#   ADO_ORG=myorg ADO_PROJ=MyProject ADO_PAT=<token> \
#       bash create-story.sh "Title of story" "MyProject\\Release 1\\Sprint 1" "MyProject\\Backend"
#
# Arguments:
#   $1  Title
#   $2  Iteration path (backslash-separated, e.g. "MyProject\\Sprint 1")
#   $3  Area path (backslash-separated, e.g. "MyProject\\Backend")
set -euo pipefail

ORG="${ADO_ORG:?ADO_ORG required}"
PROJ="${ADO_PROJ:?ADO_PROJ required}"
PAT="${ADO_PAT:?ADO_PAT required}"

TITLE="${1:?Argument 1: title required}"
ITERATION="${2:?Argument 2: iteration_path required}"
AREA="${3:?Argument 3: area_path required}"

B64=$(printf ':%s' "$PAT" | base64 -w0)

curl -fsS -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $B64" \
  -d "[
    {\"op\":\"add\",\"path\":\"/fields/System.Title\",\"value\":\"$TITLE\"},
    {\"op\":\"add\",\"path\":\"/fields/System.IterationPath\",\"value\":\"$ITERATION\"},
    {\"op\":\"add\",\"path\":\"/fields/System.AreaPath\",\"value\":\"$AREA\"}
  ]" \
  "https://dev.azure.com/${ORG}/${PROJ}/_apis/wit/workitems/\$User%20Story?api-version=7.0"
