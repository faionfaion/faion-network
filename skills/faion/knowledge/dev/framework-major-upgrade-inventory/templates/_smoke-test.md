<!-- purpose: filled-in canonical inventory for calibration (Django 4.2 to 5.0) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: inventory instance that MUST validate via scripts/validate-framework-major-upgrade-inventory.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~900 tokens -->

# Framework Major Upgrade Inventory — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-framework-major-upgrade-inventory.py --self-test` runs it.

```json
{
  "repository": "github.com/acme/billing-api",
  "framework": {
    "name": "Django",
    "current_version": "4.2.11",
    "target_version": "5.0.6",
    "current_major": 4,
    "target_major": 5,
    "major_gap": 1,
    "step_index": 1,
    "steps_total": 1,
    "upgrade_guide_url": "https://docs.djangoproject.com/en/5.0/howto/upgrade-version/"
  },
  "deprecation_run": {
    "command": "python -W error::DeprecationWarning -W error::PendingDeprecationWarning -m pytest",
    "ran_on_version": "4.2.11",
    "log_url": "https://ci.acme.example/billing-api/runs/48211",
    "distinct_warnings": 3,
    "every_warning_has_an_entry": true
  },
  "release_notes_covered": [
    {
      "version": "5.0",
      "url": "https://docs.djangoproject.com/en/5.0/releases/5.0/"
    }
  ],
  "breaking_changes": [
    {
      "id": "bc-form-rendering-div",
      "title": "Default form template changed to div-based rendering",
      "vendor_citation": {
        "url": "https://docs.djangoproject.com/en/5.0/releases/5.0/#forms",
        "version": "5.0"
      },
      "from_deprecation_run": false,
      "call_sites": {
        "count": 14,
        "search_kind": "ripgrep",
        "search_pattern": "as_table\\(\\)|\\{\\{ *form *\\}\\}",
        "search_link": "https://github.com/acme/billing-api/blob/main/docs/upgrade/5.0/searches.md#forms"
      },
      "status": "affected",
      "classification": "manual",
      "risk": {
        "runs_in": "production_requests",
        "blast_radius": 28,
        "detectability": "runtime_no_test",
        "characterisation_test": "tests/characterisation/test_form_rendering_snapshots.py"
      }
    },
    {
      "id": "bc-uslugify-usc-removed",
      "title": "django.utils.text.unescape_string_literal and USE_L10N removed",
      "vendor_citation": {
        "url": "https://docs.djangoproject.com/en/5.0/releases/5.0/#features-removed-in-5-0",
        "version": "5.0"
      },
      "from_deprecation_run": true,
      "call_sites": {
        "count": 2,
        "search_kind": "deprecation_run",
        "search_pattern": "RemovedInDjango50Warning: The USE_L10N setting is deprecated",
        "search_link": "https://ci.acme.example/billing-api/runs/48211#L212"
      },
      "status": "affected",
      "classification": "codemod",
      "codemod": {
        "tool": "django-upgrade",
        "command": "django-upgrade --target-version 5.0 $(git ls-files '*.py')",
        "dry_run_diff_lines": 6,
        "documented_as_partial_or_experimental": false
      },
      "risk": {
        "runs_in": "both",
        "blast_radius": 4,
        "detectability": "compile_time"
      }
    },
    {
      "id": "bc-index-together-removed",
      "title": "Meta.index_together removed in favour of Meta.indexes",
      "vendor_citation": {
        "url": "https://docs.djangoproject.com/en/5.0/releases/5.0/#features-removed-in-5-0",
        "version": "5.0"
      },
      "from_deprecation_run": true,
      "call_sites": {
        "count": 0,
        "search_kind": "ripgrep",
        "search_pattern": "index_together",
        "search_link": "https://github.com/acme/billing-api/blob/main/docs/upgrade/5.0/searches.md#index-together"
      },
      "status": "not_affected",
      "classification": "manual",
      "risk": {
        "runs_in": "neither",
        "blast_radius": 0,
        "detectability": "compile_time"
      }
    }
  ],
  "unverified": [
    {
      "suspected_change": "Admin changelist row colouring in dark mode looks different on 5.0 in a screenshot from a colleague",
      "search_tried": "release notes 5.0 admin section and the django/django changelog grep 'changelist' -- no entry found"
    }
  ],
  "dependent_packages": [
    {
      "name": "djangorestframework",
      "current_version": "3.14.0",
      "earliest_compatible_version": "3.15.0",
      "compatible_release_available": true,
      "release_notes_url": "https://www.django-rest-framework.org/community/release-notes/",
      "blocker": false
    },
    {
      "name": "django-polymorphic",
      "current_version": "3.1.0",
      "earliest_compatible_version": "none",
      "compatible_release_available": false,
      "release_notes_url": "https://github.com/jazzband/django-polymorphic/releases",
      "blocker": true,
      "plan": "replace",
      "plan_detail": "Replace the two polymorphic models with explicit multi-table inheritance; spike estimated in docs/upgrade/5.0/polymorphic.md"
    }
  ],
  "runtime_prerequisites": [
    {
      "kind": "language",
      "name": "Python",
      "target_minimum": "3.10",
      "source_url": "https://docs.djangoproject.com/en/5.0/releases/5.0/#python-compatibility",
      "environments": [
        {
          "name": "production",
          "current": "3.11.9",
          "meets_minimum": true
        },
        {
          "name": "staging",
          "current": "3.11.9",
          "meets_minimum": true
        },
        {
          "name": "ci",
          "current": "3.11.9",
          "meets_minimum": true
        }
      ],
      "blocker": false
    },
    {
      "kind": "database",
      "name": "PostgreSQL",
      "target_minimum": "12",
      "source_url": "https://docs.djangoproject.com/en/5.0/releases/5.0/#dropped-support-for-postgresql-11",
      "environments": [
        {
          "name": "production",
          "current": "15.6",
          "meets_minimum": true
        },
        {
          "name": "staging",
          "current": "15.6",
          "meets_minimum": true
        }
      ],
      "blocker": false
    }
  ],
  "review": {
    "status": "ready_for_review",
    "reviewer": "kim@acme.example",
    "upgrade_branch_opened_by_agent": false
  }
}
```
