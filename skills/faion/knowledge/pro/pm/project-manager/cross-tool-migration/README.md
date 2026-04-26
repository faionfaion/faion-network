---
id: tool-migration-process
name: "Cross-Tool Migration - Process"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Cross-Tool Migration - Process

## Migration Phases

```
Phase 1: Planning (2-4 weeks)
├── Stakeholder alignment
├── Tool selection/evaluation
├── Migration scope definition
├── Timeline creation
└── Risk assessment

Phase 2: Preparation (2-3 weeks)
├── Target tool setup
├── Field mapping design
├── Migration script development
├── Test environment creation
└── Team communication

Phase 3: Pilot Migration (1-2 weeks)
├── Select pilot project
├── Execute migration
├── Validate data
├── Gather feedback
└── Adjust approach

Phase 4: Full Migration (1-4 weeks)
├── Execute in waves
├── Validate each wave
├── Address issues
└── Monitor progress

Phase 5: Cutover (1 week)
├── Final sync
├── Disable source tool
├── Enable target tool
└── Support team

Phase 6: Stabilization (2-4 weeks)
├── Active support
├── Fix issues
├── Training sessions
└── Document learnings
```

## Data Migration Scripts

### Generic Migration Framework

```python
# migration_framework.py
from dataclasses import dataclass
from typing import Dict, List, Any
import json

@dataclass
class MigrationConfig:
    source_tool: str
    target_tool: str
    field_mapping: Dict[str, str]
    status_mapping: Dict[str, str]
    priority_mapping: Dict[str, str]
    dry_run: bool = True

class MigrationEngine:
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.source_client = self._init_source()
        self.target_client = self._init_target()
        self.migration_log = []

    def extract(self, project_key: str) -> List[Dict]:
        """Extract all issues from source"""
        issues = self.source_client.get_issues(project_key)
        self.log(f"Extracted {len(issues)} issues")
        return issues

    def transform(self, issues: List[Dict]) -> List[Dict]:
        """Transform issues to target format"""
        transformed = []
        for issue in issues:
            try:
                transformed.append(self._transform_issue(issue))
            except Exception as e:
                self.log(f"Transform error {issue['key']}: {e}", "ERROR")
        return transformed

    def _transform_issue(self, issue: Dict) -> Dict:
        """Transform single issue"""
        return {
            "title": issue["summary"],
            "description": issue.get("description", ""),
            "state": self.config.status_mapping.get(
                issue["status"], "backlog"
            ),
            "priority": self.config.priority_mapping.get(
                issue["priority"], "medium"
            ),
            "labels": self._map_labels(issue),
            "assignee_email": issue.get("assignee", {}).get("email"),
            # Custom field mapping
            **self._map_custom_fields(issue)
        }

    def load(self, issues: List[Dict]) -> Dict[str, str]:
        """Load issues to target, return ID mapping"""
        id_mapping = {}
        for issue in issues:
            if self.config.dry_run:
                self.log(f"Would create: {issue['title']}")
                continue

            result = self.target_client.create_issue(issue)
            id_mapping[issue["source_id"]] = result["id"]
            self.log(f"Created: {result['id']}")

        return id_mapping

    def migrate_links(self, id_mapping: Dict[str, str]):
        """Migrate issue links using ID mapping"""
        # Implementation depends on source/target tools
        pass

    def migrate_attachments(self, issues: List[Dict], id_mapping: Dict):
        """Migrate attachments separately"""
        # Download from source, upload to target
        pass

    def validate(self, id_mapping: Dict[str, str]) -> Dict:
        """Validate migration completeness"""
        return {
            "total_source": len(id_mapping),
            "total_target": self.target_client.count_issues(),
            "missing": self._find_missing(id_mapping)
        }
```

## Rollback Planning

### Rollback Strategy

```yaml
rollback_triggers:
  - data_loss_detected: immediate
  - critical_integration_failure: immediate
  - team_productivity_drop_50_percent: 48_hours
  - user_adoption_under_30_percent: 1_week

rollback_procedure:
  immediate:
    - pause_migration
    - notify_stakeholders
    - assess_damage
    - restore_source_access
    - document_failure

  planned:
    - disable_target_tool
    - sync_any_new_data_back
    - re_enable_source
    - communicate_timeline
    - reschedule_migration

data_preservation:
  - keep_source_read_only_30_days
  - export_target_data_before_rollback
  - document_mapping_for_retry
```

## Change Management

### Communication Plan

```yaml
communications:
  - timing: "4 weeks before"
    audience: "all users"
    message: "Migration announcement"
    channel: ["email", "slack", "meeting"]

  - timing: "2 weeks before"
    audience: "all users"
    message: "Training schedule"
    channel: ["email", "calendar"]

  - timing: "1 week before"
    audience: "all users"
    message: "Final preparation checklist"
    channel: ["email", "slack"]

  - timing: "migration day"
    audience: "all users"
    message: "Go-live announcement"
    channel: ["email", "slack", "meeting"]

  - timing: "daily for 2 weeks"
    audience: "all users"
    message: "Daily tips and support"
    channel: ["slack"]
```

## Templates

### Migration Project Plan

```markdown
# PM Tool Migration: Jira → Linear

## Project Overview
**Objective:** Migrate from Jira to Linear by Q2 2024
**Sponsor:** VP Engineering
**PM:** [Name]
**Timeline:** 12 weeks

## Scope
### In Scope
- All active projects (15)
- Issues from last 2 years
- Attachments under 10MB
- Key automations

### Out of Scope
- Archived projects
- Closed issues > 2 years
- Custom Jira plugins
- Time tracking data

## Timeline
| Phase | Duration | Dates | Owner |
|-------|----------|-------|-------|
| Planning | 2 weeks | Jan 1-14 | PM |
| Setup | 2 weeks | Jan 15-28 | Admin |
| Pilot | 2 weeks | Feb 1-14 | Team A |
| Migration | 4 weeks | Feb 15 - Mar 14 | PM |
| Cutover | 1 week | Mar 15-21 | All |
| Stabilization | 3 weeks | Mar 22 - Apr 11 | Support |

## Risk Register
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data loss | High | Low | Multiple backups |
| Team resistance | Medium | Medium | Training + champions |
| Integration breaks | High | Medium | Test all integrations |
| Timeline slip | Medium | Medium | Buffer time included |

## Success Criteria
- [ ] 100% active issues migrated
- [ ] All integrations working
- [ ] Team adoption > 80% by week 2
- [ ] No critical bugs in first month
```

### Cutover Checklist

```markdown
## Migration Cutover Checklist

### T-24 Hours
- [ ] Final data export from source
- [ ] Backup target environment
- [ ] Notify all users of timeline
- [ ] Prepare support team

### T-4 Hours
- [ ] Set source tool to read-only
- [ ] Run final migration sync
- [ ] Validate issue counts
- [ ] Test critical integrations

### T-0 (Go Live)
- [ ] Enable target tool for all users
- [ ] Send go-live announcement
- [ ] Support team on standby
- [ ] Monitor for errors

### T+1 Hour
- [ ] Check user login success
- [ ] Verify automations running
- [ ] Address immediate issues
- [ ] Update status to stakeholders

### T+24 Hours
- [ ] Review error logs
- [ ] Collect user feedback
- [ ] Document known issues
- [ ] Plan remediation

### T+1 Week
- [ ] User adoption metrics
- [ ] Complete missing migrations
- [ ] Conduct retrospective
- [ ] Plan source tool decommission
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## References

- [tool-migration-basics.md](tool-migration-basics.md) - Assessment, mapping, best practices
- [Atlassian Migration Guide](https://support.atlassian.com/jira-cloud/docs/migrate-from-jira-server-to-jira-cloud/)
- [Linear Import](https://linear.app/docs/import)
- [Change Management (ADKAR)](https://www.prosci.com/methodology/adkar)
