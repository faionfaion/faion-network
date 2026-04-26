-- JQL query collection for common Jira dashboard metrics
-- Use in Jira gadgets or REST API calls

-- Sprint scope (current sprint)
project = PROJ AND sprint in openSprints()

-- Completed this sprint
project = PROJ AND sprint in openSprints() AND status = Done

-- In progress
project = PROJ AND status = "In Progress"

-- Blocked items
project = PROJ AND labels = blocked AND status != Done

-- Bugs by priority (pie chart)
project = PROJ AND type = Bug AND status != Done

-- Created vs resolved last 30 days
project = PROJ AND created >= -30d

-- Velocity data (sum story points per closed sprint)
project = PROJ AND sprint in closedSprints() AND status = Done

-- Aging issues (stale in progress)
project = PROJ AND status = "In Progress" AND updated < -7d

-- Release scope
project = PROJ AND fixVersion = "1.0.0"
