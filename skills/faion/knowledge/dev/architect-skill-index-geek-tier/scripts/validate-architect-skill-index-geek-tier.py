#!/usr/bin/env python3
"""validate-architect-skill-index-geek-tier.py

Validate the artefact produced by the architect-skill-index-geek-tier methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only, self-contained:
`faion get-content` ships this file alone, so the schema and the checker live
here rather than in a shared module.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid / invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "faion://architect-skill-index-geek-tier/output.schema.json",
  "title": "Architect skill index (geek tier)",
  "type": "object",
  "required": [
    "index_title",
    "tier",
    "clusters",
    "entry_count",
    "uncovered_tasks",
    "relink",
    "evidence"
  ],
  "additionalProperties": False,
  "definitions": {
    "slug": {
      "type": "string",
      "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
    },
    "date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    }
  },
  "properties": {
    "__faion_header__": {
      "type": "object"
    },
    "index_title": {
      "type": "string",
      "minLength": 5
    },
    "tier": {
      "type": "string",
      "const": "geek"
    },
    "clusters": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "activity",
          "entries"
        ],
        "additionalProperties": False,
        "properties": {
          "name": {
            "type": "string",
            "minLength": 5,
            "not": {
              "pattern": "(?i)^(spec-?kit|plan-?mode|rag|graph-?reviewer|claude-?code|cursor|copilot)$"
            }
          },
          "activity": {
            "type": "string",
            "enum": [
              "elicit-requirements",
              "decide-and-record",
              "document-views",
              "evaluate-and-review",
              "govern-drift"
            ]
          },
          "entries": {
            "type": "array",
            "minItems": 3,
            "items": {
              "type": "object",
              "required": [
                "slug",
                "architect_why",
                "load_when",
                "est_tokens",
                "target_status"
              ],
              "additionalProperties": False,
              "properties": {
                "slug": {
                  "$ref": "#/definitions/slug"
                },
                "architect_why": {
                  "type": "string",
                  "minLength": 40,
                  "maxLength": 240,
                  "not": {
                    "pattern": "(?i)useful for architects|for architects\\.?$"
                  }
                },
                "load_when": {
                  "type": "string",
                  "minLength": 15
                },
                "est_tokens": {
                  "type": "integer",
                  "minimum": 50
                },
                "target_status": {
                  "type": "string",
                  "const": "active"
                }
              }
            }
          }
        }
      }
    },
    "entry_count": {
      "type": "integer",
      "minimum": 1
    },
    "shortfall": {
      "type": "object",
      "required": [
        "count_missing",
        "reason"
      ],
      "additionalProperties": False,
      "properties": {
        "count_missing": {
          "type": "integer",
          "minimum": 1
        },
        "reason": {
          "type": "string",
          "minLength": 20
        }
      }
    },
    "uncovered_tasks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "task",
          "closest_match"
        ],
        "additionalProperties": False,
        "properties": {
          "task": {
            "type": "string",
            "minLength": 10
          },
          "closest_match": {
            "type": "string",
            "pattern": "^(none|[a-z0-9]+(-[a-z0-9]+)*)$"
          }
        }
      }
    },
    "relink": {
      "type": "object",
      "required": [
        "script_path",
        "last_run",
        "run_url",
        "next_due"
      ],
      "additionalProperties": False,
      "properties": {
        "script_path": {
          "type": "string",
          "minLength": 3
        },
        "last_run": {
          "$ref": "#/definitions/date"
        },
        "run_url": {
          "type": "string",
          "format": "uri"
        },
        "next_due": {
          "$ref": "#/definitions/date"
        }
      }
    },
    "evidence": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "format": "uri"
      }
    }
  },
  "if": {
    "properties": {
      "entry_count": {
        "exclusiveMaximum": 50
      }
    }
  },
  "then": {
    "required": [
      "shortfall"
    ]
  }
}

OK = {
  "index_title": "Architect skill index (geek tier)",
  "tier": "geek",
  "clusters": [
    {
      "name": "Eliciting architecturally significant requirements",
      "activity": "elicit-requirements",
      "entries": [
        {
          "slug": "spec-requirements",
          "architect_why": "Turns stakeholder asks into numbered NFRs an architect can trace to a quality-attribute scenario.",
          "load_when": "A feature spec has adjectives (fast, secure) where the NFR numbers should be.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "definition-of-ready-template",
          "architect_why": "Gates the story until its architecture-relevant unknowns (data ownership, external edges) are named.",
          "load_when": "A story is about to enter the sprint with an unresolved boundary or data question.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "qa-test-strategy-template",
          "architect_why": "Fixes which quality attributes get which test layer before the pyramid is argued about per PR.",
          "load_when": "Planning a new service and the contract / e2e split is undecided.",
          "est_tokens": 5000,
          "target_status": "active"
        },
        {
          "slug": "cost-modeling-at-design-time",
          "architect_why": "Makes the run-cost of an option a stated quality attribute in the trade-off, not a surprise on the invoice.",
          "load_when": "Two candidate designs differ mainly in managed-service spend.",
          "est_tokens": 4500,
          "target_status": "active"
        },
        {
          "slug": "observability-as-design-input",
          "architect_why": "Elicits the signals each boundary must emit as a design requirement rather than an ops afterthought.",
          "load_when": "A design review has no answer to how a failure across a boundary will be seen.",
          "est_tokens": 5000,
          "target_status": "active"
        },
        {
          "slug": "stack-mandate-tradeoff-frame",
          "architect_why": "Names the quality attributes a mandated stack sacrifices so the ADR records the constraint honestly.",
          "load_when": "A client or platform team has fixed the stack before the design starts.",
          "est_tokens": 4800,
          "target_status": "active"
        },
        {
          "slug": "internal-rfc-template",
          "architect_why": "Frames a cross-cutting proposal for comment before it hardens into a decision.",
          "load_when": "A change touches more than one team's boundary and needs review before an ADR.",
          "est_tokens": 3800,
          "target_status": "active"
        },
        {
          "slug": "spike-protocol-template",
          "architect_why": "Time-boxes the investigation that settles an architecturally significant unknown.",
          "load_when": "An ADR is blocked on a question only a prototype can answer.",
          "est_tokens": 4900,
          "target_status": "active"
        },
        {
          "slug": "dependency-spike-kill-criteria-template",
          "architect_why": "Pre-commits the disqualifiers for a candidate platform so the spike ends on evidence, not sunk cost.",
          "load_when": "Evaluating a library or vendor that would become a load-bearing edge.",
          "est_tokens": 4900,
          "target_status": "active"
        },
        {
          "slug": "lock-in-risk-scoring-rubric",
          "architect_why": "Scores exit cost as an explicit quality attribute of a platform decision.",
          "load_when": "Choosing a managed service whose replacement would take more than a quarter.",
          "est_tokens": 4100,
          "target_status": "active"
        }
      ]
    },
    {
      "name": "Deciding and recording",
      "activity": "decide-and-record",
      "entries": [
        {
          "slug": "architecture-decision-records-planning",
          "architect_why": "Fixes the Nygard ADR format so every boundary decision has context, decision and consequences on record.",
          "load_when": "A decision is being made in chat that will constrain other teams.",
          "est_tokens": 3600,
          "target_status": "active"
        },
        {
          "slug": "adr-ai-drafted-with-review",
          "architect_why": "Lets an agent draft the ADR from the decision bundle while the architect keeps the accept step.",
          "load_when": "The context is documented but nobody has time to write the ADR prose.",
          "est_tokens": 3400,
          "target_status": "active"
        },
        {
          "slug": "adr-consequence-evidence-binding",
          "architect_why": "Binds each ADR consequence to a fitness function or KPI so it can be checked later.",
          "load_when": "An ADR's consequences section is a list of hopes with no measurement.",
          "est_tokens": 3400,
          "target_status": "active"
        },
        {
          "slug": "retro-adr-workflow",
          "architect_why": "Captures decisions already embodied in code as ADRs without blame, so the record matches the system.",
          "load_when": "Onboarding into a system whose structure nobody can explain from documents.",
          "est_tokens": 4400,
          "target_status": "active"
        },
        {
          "slug": "decision-log-reconstruction-from-git",
          "architect_why": "Rebuilds the decision history from commits and PRs when the ADR trail is missing.",
          "load_when": "Preparing a review of a legacy system with no written decisions.",
          "est_tokens": 4900,
          "target_status": "active"
        },
        {
          "slug": "cap-pacelc-walkthrough",
          "architect_why": "Records the consistency-versus-availability trade for a datastore or extraction decision.",
          "load_when": "Choosing a datastore or splitting a service where consistency guarantees change.",
          "est_tokens": 4300,
          "target_status": "active"
        },
        {
          "slug": "choreography-vs-orchestration-decision",
          "architect_why": "Records the coordination-style decision for a multi-service workflow as a versioned ADR.",
          "load_when": "A workflow spans three or more services and the coordinator question is open.",
          "est_tokens": 4300,
          "target_status": "active"
        },
        {
          "slug": "microservice-extraction-decision-tree",
          "architect_why": "Decides whether a boundary is ready to become a deployable now, on independence and team criteria.",
          "load_when": "A team proposes extracting a service from the monolith.",
          "est_tokens": 4100,
          "target_status": "active"
        },
        {
          "slug": "data-ownership-split-patterns",
          "architect_why": "Assigns a single writer per entity when several services read it.",
          "load_when": "Two services both write the same table or topic.",
          "est_tokens": 4500,
          "target_status": "active"
        },
        {
          "slug": "language-framework-guide",
          "architect_why": "Produces the stack recommendation with an ADR stub so the platform choice is a recorded decision.",
          "load_when": "Starting a new system or component where the runtime is not yet fixed.",
          "est_tokens": 3000,
          "target_status": "active"
        },
        {
          "slug": "caching-strategy",
          "architect_why": "Chooses the cache pattern as a consistency decision with a stated invalidation contract.",
          "load_when": "A latency requirement is pushing a cache into a boundary that owns writes.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "microservices-inter-service-comm",
          "architect_why": "Fixes the transport per edge (sync, async, gRPC) as a boundary property.",
          "load_when": "A new inter-service call is being added without a stated coupling choice.",
          "est_tokens": 5200,
          "target_status": "active"
        },
        {
          "slug": "task-spec-kit-three-step",
          "architect_why": "Orders spec, plan and tasks so the architecture is decided before agents generate code.",
          "load_when": "An agent-driven build is about to start from an unwritten spec.",
          "est_tokens": 5100,
          "target_status": "active"
        },
        {
          "slug": "task-plan-mode-locked-execution",
          "architect_why": "Locks the approved plan so an agent cannot re-decide a boundary mid-execution.",
          "load_when": "Delegating an implementation whose plan already encodes architectural choices.",
          "est_tokens": 5100,
          "target_status": "active"
        }
      ]
    },
    {
      "name": "Documenting views and contracts",
      "activity": "document-views",
      "entries": [
        {
          "slug": "diagram-as-code-mermaid-structurizr",
          "architect_why": "Keeps the C4 model as text under version control so views are diffable and reviewable.",
          "load_when": "A diagram lives in a drawing tool and nobody can tell what changed.",
          "est_tokens": 4900,
          "target_status": "active"
        },
        {
          "slug": "architecture-repo-scaffolding-template",
          "architect_why": "Lays out the architecture repository (ADRs, diagrams, fitness functions) as one versioned artefact.",
          "load_when": "Starting the architecture record for a new system or programme.",
          "est_tokens": 3400,
          "target_status": "active"
        },
        {
          "slug": "writing-design-documents",
          "architect_why": "Writes the design.md whose numbered AD-X decisions are the architecture view of a feature.",
          "load_when": "A feature spec is approved and the design has to answer how.",
          "est_tokens": 4300,
          "target_status": "active"
        },
        {
          "slug": "workflow-design-phase",
          "architect_why": "Runs the design phase that produces the file table and data model views a feature needs.",
          "load_when": "The SDD workflow has reached design and needs its artefacts in order.",
          "est_tokens": 4500,
          "target_status": "active"
        },
        {
          "slug": "microservices-service-boundaries",
          "architect_why": "Documents each boundary with ownership, data sovereignty and transaction scope.",
          "load_when": "Boundaries exist in code but not in any document the team agrees on.",
          "est_tokens": 5200,
          "target_status": "active"
        },
        {
          "slug": "domain-driven-design",
          "architect_why": "Documents the bounded context and its ubiquitous language as the source of boundary names.",
          "load_when": "Teams use different words for the same entity across services.",
          "est_tokens": 4300,
          "target_status": "active"
        },
        {
          "slug": "threat-model-as-code",
          "architect_why": "Keeps the threat model as a versioned artefact that diffs with the architecture.",
          "load_when": "A security review asks for the trust boundaries and nobody has a current model.",
          "est_tokens": 4100,
          "target_status": "active"
        },
        {
          "slug": "api-contract-first",
          "architect_why": "Makes the OpenAPI contract the documented boundary from which server and clients derive.",
          "load_when": "Two teams integrate on an API that exists only as code.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "openapi-specification",
          "architect_why": "Sets the authoring and CI gates that keep the published contract canonical.",
          "load_when": "The OpenAPI bundle has drifted from the running service.",
          "est_tokens": 5400,
          "target_status": "active"
        },
        {
          "slug": "cross-team-interface-change-log",
          "architect_why": "Records every change to a cross-team interface as a versioned log entry consumers can read.",
          "load_when": "A shared interface changes and downstream teams find out from a failure.",
          "est_tokens": 4400,
          "target_status": "active"
        }
      ]
    },
    {
      "name": "Evaluating and reviewing",
      "activity": "evaluate-and-review",
      "entries": [
        {
          "slug": "architectural-impact-pr-ranking",
          "architect_why": "Ranks the week's PRs by blast radius so the review session reads the ones that bend the architecture.",
          "load_when": "Preparing a time-boxed architecture review over hundreds of PRs.",
          "est_tokens": 3500,
          "target_status": "active"
        },
        {
          "slug": "weekly-arch-review-agenda-template",
          "architect_why": "Fixes the five agenda items so the weekly review covers ADRs, fitness functions and drift every time.",
          "load_when": "Running the recurring architecture review.",
          "est_tokens": 2900,
          "target_status": "active"
        },
        {
          "slug": "mr-graph-vs-diff-reviewer",
          "architect_why": "Chooses the reviewer architecture for cross-cutting changes where a diff-only view misses the coupling.",
          "load_when": "Setting up automated review on a repository with deep dependency graphs.",
          "est_tokens": 3600,
          "target_status": "active"
        },
        {
          "slug": "ai-cr-impact-suggestion",
          "architect_why": "Adds a per-PR impact comment listing affected modules so cross-cutting changes are visible at review.",
          "load_when": "Reviewers keep missing which modules a PR reaches.",
          "est_tokens": 3800,
          "target_status": "active"
        },
        {
          "slug": "stride-lite-checklist-for-architects",
          "architect_why": "Runs the six STRIDE categories against a new dependency or service edge at review time.",
          "load_when": "A PR adds an external edge or a new dependency with network access.",
          "est_tokens": 4100,
          "target_status": "active"
        },
        {
          "slug": "trust-boundary-diff-helper",
          "architect_why": "Diffs the trust boundaries before and after a change so a review sees new ingress and auth surfaces.",
          "load_when": "A change touches ingress, egress or authentication.",
          "est_tokens": 4800,
          "target_status": "active"
        },
        {
          "slug": "new-dependency-risk-checklist",
          "architect_why": "Reviews a new dependency as a trust and maintenance decision with a recorded risk score.",
          "load_when": "A PR adds a dependency that will be hard to remove.",
          "est_tokens": 3500,
          "target_status": "active"
        },
        {
          "slug": "load-bearing-dep-criteria",
          "architect_why": "Decides whether a dependency is load-bearing and therefore needs an ADR rather than a nod.",
          "load_when": "A dependency touches auth, payments, persistence or the runtime.",
          "est_tokens": 4100,
          "target_status": "active"
        },
        {
          "slug": "llm-friendly-architecture",
          "architect_why": "Audits file size, depth and naming so the structure is navigable by agents as well as people.",
          "load_when": "Agents keep producing wrong edits in one part of the codebase.",
          "est_tokens": 3500,
          "target_status": "active"
        },
        {
          "slug": "kb-codebase-rag-symbol-chunked",
          "architect_why": "Indexes the codebase on symbol boundaries so an architecture question retrieves whole units.",
          "load_when": "Answering architecture questions over a codebase too large to read.",
          "est_tokens": 4200,
          "target_status": "active"
        }
      ]
    },
    {
      "name": "Governing drift",
      "activity": "govern-drift",
      "entries": [
        {
          "slug": "evolutionary-architecture-fitness-functions",
          "architect_why": "Specifies the fitness-function suite that turns each quality attribute into a CI check.",
          "load_when": "An ADR's consequence has no automated guard.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "fitness-function-suite-bootstrap",
          "architect_why": "Starts the suite with the five to eight functions that catch the most common drift first.",
          "load_when": "No fitness functions exist yet and the backlog of candidates is long.",
          "est_tokens": 3500,
          "target_status": "active"
        },
        {
          "slug": "fitness-function-wiring",
          "architect_why": "Wires each high-priority scenario to a named CI job that fails the build.",
          "load_when": "Fitness functions exist as scripts nobody runs.",
          "est_tokens": 4500,
          "target_status": "active"
        },
        {
          "slug": "fitness-functions-as-code",
          "architect_why": "Codifies per-axis fitness functions as executable tests committed beside the code.",
          "load_when": "Modularity or layering rules are enforced only in review comments.",
          "est_tokens": 4600,
          "target_status": "active"
        },
        {
          "slug": "c4-drift-detection-from-iac",
          "architect_why": "Diffs the C4 model against applied IaC state so the diagram reports its own drift.",
          "load_when": "The living diagram and the running infrastructure disagree.",
          "est_tokens": 3500,
          "target_status": "active"
        },
        {
          "slug": "kb-adr-decay-detector-agent",
          "architect_why": "Scans ADRs against current code and reports the ones the code now contradicts.",
          "load_when": "The ADR log is old and nobody knows which decisions still hold.",
          "est_tokens": 4400,
          "target_status": "active"
        },
        {
          "slug": "adr-supersession-detection",
          "architect_why": "Finds ADRs that later decisions superseded without saying so.",
          "load_when": "Two ADRs give conflicting guidance on the same boundary.",
          "est_tokens": 3800,
          "target_status": "active"
        },
        {
          "slug": "debt-scoring-rubric",
          "architect_why": "Ranks architectural debt by impact and change frequency so the register drives the roadmap.",
          "load_when": "The debt list is long and the next quarter's slot has to be chosen.",
          "est_tokens": 4200,
          "target_status": "active"
        },
        {
          "slug": "slo-burn-rate-review-protocol",
          "architect_why": "Turns SLO burn data into named architecture actions in a weekly ritual.",
          "load_when": "SLOs are breached repeatedly and the review produces no structural change.",
          "est_tokens": 4600,
          "target_status": "active"
        },
        {
          "slug": "strangler-pattern-checklist-product-dev-team",
          "architect_why": "Gates a legacy replacement so each strangled slice keeps the contract frozen and the ACL covered.",
          "load_when": "Replacing a legacy system incrementally with a small team.",
          "est_tokens": 3800,
          "target_status": "active"
        }
      ]
    }
  ],
  "entry_count": 54,
  "uncovered_tasks": [
    {
      "task": "quality-attribute workshop facilitation (ATAM-style utility tree)",
      "closest_match": "spec-requirements"
    },
    {
      "task": "architecture runway sizing for a programme increment",
      "closest_match": "none"
    },
    {
      "task": "component-level drift inside a deployable (code-level C4)",
      "closest_match": "c4-drift-detection-from-iac"
    }
  ],
  "relink": {
    "script_path": "scripts/relink-architect-index.py",
    "last_run": "2026-09-01",
    "run_url": "https://ci.example.com/faion/relink/architect-index/118",
    "next_due": "2026-12-01"
  },
  "evidence": [
    "https://ci.example.com/faion/relink/architect-index/118",
    "https://github.com/faionfaion/faion-network/pull/3021"
  ]
}

BAD = {
  "index_title": "Architect skill index (geek tier)",
  "tier": "geek",
  "clusters": [
    {
      "name": "spec-kit",
      "activity": "decide-and-record",
      "entries": [
        {
          "slug": "task-spec-kit-three-step",
          "architect_why": "Produces three versioned artifacts (spec.md, plan.md, tasks.md) in fixed order; only tasks.md is executed.",
          "load_when": "Starting a build",
          "est_tokens": 5100,
          "target_status": "active"
        },
        {
          "slug": "task-plan-mode-locked-execution",
          "architect_why": "Useful for architects.",
          "load_when": "Planning",
          "est_tokens": 5100,
          "target_status": "active"
        },
        {
          "slug": "architecture-decision-records",
          "architect_why": "Records architecture decisions so the boundary choice has context and consequences on file.",
          "load_when": "A boundary decision is being made in chat.",
          "est_tokens": 3600,
          "target_status": "draft"
        }
      ]
    },
    {
      "name": "plan-mode",
      "activity": "decide-and-record",
      "entries": [
        {
          "slug": "task-plan-mode-locked-execution",
          "architect_why": "Locks the approved plan so an agent cannot re-decide a boundary mid-execution.",
          "load_when": "Delegating an implementation whose plan encodes architectural choices.",
          "est_tokens": 4000,
          "target_status": "active"
        },
        {
          "slug": "cap-pacelc-walkthrough",
          "architect_why": "Records the consistency-versus-availability trade for a datastore decision.",
          "est_tokens": 4300,
          "target_status": "active"
        }
      ]
    }
  ],
  "entry_count": 5,
  "uncovered_tasks": [],
  "relink": {
    "script_path": "scripts/relink-architect-index.py",
    "last_run": "2026-09-01",
    "run_url": "https://ci.example.com/faion/relink/architect-index/118",
    "next_due": "2026-12-01"
  },
  "evidence": [
    "https://ci.example.com/faion/relink/architect-index/118"
  ]
}

_FORMATS = {
    "date-time": re.compile(
        r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
        r"(?:Z|[+-]\d{2}:?\d{2})?$"
    ),
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "email": re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"),
    "uri": re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:\S*$"),
    "uri-reference": re.compile(r"^\S+$"),
}

_PY_TYPES = {"object": dict, "array": list, "string": str, "null": type(None)}


def _type_ok(value, declared) -> bool:
    names = declared if isinstance(declared, list) else [declared]
    for name in names:
        if name == "integer":
            ok = isinstance(value, int) and not isinstance(value, bool)
        elif name == "number":
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif name == "boolean":
            ok = isinstance(value, bool)
        elif name in _PY_TYPES:
            ok = isinstance(value, _PY_TYPES[name])
        else:
            ok = True
        if ok:
            return True
    return False


def _label(path: str) -> str:
    return path or "<root>"


def _resolve(ref: str):
    """Local `#/definitions/<name>` references only (draft-07 `$ref` replaces its siblings)."""
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref: {ref}")
    node = SCHEMA
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _valid(value, schema) -> bool:
    errs: list[str] = []
    _check(value, schema, "", errs)
    return not errs


def _check(value, schema, path: str, errs: list) -> None:
    """Draft-07 subset: required, type, enum, const, pattern, format, minimum /
    maximum (+exclusive), minLength / maxLength, minItems / maxItems,
    uniqueItems, items, properties, additionalProperties, allOf / anyOf /
    oneOf / not, if / then / else, local $ref."""
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{_label(path)}: schema forbids any value here")
        return
    if "$ref" in schema:
        schema = _resolve(schema["$ref"])
    declared = schema.get("type")
    if declared is not None and not _type_ok(value, declared):
        errs.append(f"{_label(path)}: expected type {declared}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{_label(path)}: {value!r} not in allowed enum {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{_label(path)}: {value!r} is not the required const {schema['const']!r}")

    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errs.append(f"{_label(path)}: {value!r} does not match pattern {pattern!r}")
        rx = _FORMATS.get(schema.get("format"))
        if rx is not None and not rx.match(value):
            errs.append(f"{_label(path)}: {value!r} is not a valid {schema['format']}")
        low, high = schema.get("minLength"), schema.get("maxLength")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: length {len(value)} is under minLength {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: length {len(value)} is over maxLength {high}")

    if isinstance(value, list):
        low, high = schema.get("minItems"), schema.get("maxItems")
        if isinstance(low, int) and len(value) < low:
            errs.append(f"{_label(path)}: {len(value)} items is under minItems {low}")
        if isinstance(high, int) and len(value) > high:
            errs.append(f"{_label(path)}: {len(value)} items is over maxItems {high}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True) for v in value]
            if len(set(seen)) != len(seen):
                errs.append(f"{_label(path)}: items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, element in enumerate(value):
                _check(element, item_schema, f"{_label(path)}[{i}]", errs)
        elif isinstance(item_schema, list):
            for i, (element, sub) in enumerate(zip(value, item_schema)):
                _check(element, sub, f"{_label(path)}[{i}]", errs)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        for key, test, word in (
            ("minimum", lambda v, b: v < b, "is below minimum"),
            ("maximum", lambda v, b: v > b, "is above maximum"),
            ("exclusiveMinimum", lambda v, b: v <= b, "is not above exclusiveMinimum"),
            ("exclusiveMaximum", lambda v, b: v >= b, "is not below exclusiveMaximum"),
        ):
            bound = schema.get(key)
            if isinstance(bound, (int, float)) and test(value, bound):
                errs.append(f"{_label(path)}: {value} {word} {bound}")

    if isinstance(value, dict):
        props = schema.get("properties") or {}
        for key in schema.get("required") or []:
            if key not in value:
                errs.append(f"{_label(path)}: missing required field: {key}")
        extra = schema.get("additionalProperties", True)
        for key in value:
            if key in props:
                continue
            if extra is False:
                errs.append(f"{_label(path)}: unknown field {key!r} (additionalProperties: false)")
            elif isinstance(extra, dict):
                _check(value[key], extra, f"{path}.{key}" if path else key, errs)
        for key, sub in props.items():
            if key in value and isinstance(sub, (dict, bool)):
                _check(value[key], sub, f"{path}.{key}" if path else key, errs)

    for sub in schema.get("allOf") or []:
        _check(value, sub, path, errs)
    any_of = schema.get("anyOf")
    if any_of and not any(_valid(value, s) for s in any_of):
        errs.append(f"{_label(path)}: matches none of the anyOf alternatives")
    one_of = schema.get("oneOf")
    if one_of:
        hits = sum(1 for s in one_of if _valid(value, s))
        if hits != 1:
            errs.append(f"{_label(path)}: matches {hits} oneOf alternatives, need exactly 1")
    if "not" in schema and _valid(value, schema["not"]):
        errs.append(f"{_label(path)}: matches the forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _valid(value, schema["if"]) else "else"
        if branch in schema:
            _check(value, schema[branch], path, errs)


def validate(obj: object) -> list[str]:
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    errs: list[str] = []
    _check(obj, SCHEMA, "", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-architect-skill-index-geek-tier.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
