"""Reference handler for `/agent escalate-trust <incident_id>`.

Creates an ephemeral remediate RoleBinding for the SRE agent's
ServiceAccount and schedules its revoke. Verifies the requester is
the on-caller and has a fresh MFA proof.

Wire `oncall`, `mfa`, `rbac`, `incidents`, `audit` to your stack.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

DEFAULT_TTL_SECONDS = 60 * 60  # 60 minutes hard cap


@dataclass
class EscalationResult:
    binding_name: str
    expires_at: int
    incident_id: str


def escalate_trust(
    incident_id: str,
    requesting_user: str,
    *,
    oncall,
    mfa,
    rbac,
    incidents,
    audit,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> EscalationResult:
    if not oncall.is_oncaller(incident_id, requesting_user):
        raise PermissionError("requester is not the on-caller for this incident")
    if not mfa.challenge_passed(requesting_user, max_age_seconds=60):
        raise PermissionError("fresh MFA challenge required")
    if ttl_seconds > DEFAULT_TTL_SECONDS:
        raise ValueError("TTL exceeds 60-minute hard cap")

    expires_at = int(time.time()) + ttl_seconds
    binding_name = f"sre-agent-remediate-{incident_id}"
    rbac.create_clusterrolebinding(
        name=binding_name,
        service_account=("sre-agent", "ops"),
        cluster_role="sre-agent-remediate",
        annotations={
            "incident_id": incident_id,
            "approver":    requesting_user,
            "expires_at":  str(expires_at),
        },
    )
    incidents.on_close(incident_id, lambda: rbac.delete_clusterrolebinding(binding_name))
    rbac.schedule_delete(binding_name, at=expires_at)
    audit.append(
        action="escalate_trust",
        incident_id=incident_id,
        approver=requesting_user,
        binding=binding_name,
        expires_at=expires_at,
    )
    return EscalationResult(binding_name=binding_name, expires_at=expires_at, incident_id=incident_id)
