#!/bin/bash
# pushgateway-job.sh
# Push CI/CD job metrics to Prometheus Pushgateway.
# Usage: JOB_DURATION=120 JOB_STATUS=success PIPELINE=my-pipeline ./pushgateway-job.sh push
# Usage: ./pushgateway-job.sh delete  (to remove metrics after job group is done)

set -euo pipefail

PUSHGATEWAY_URL="${PUSHGATEWAY_URL:-http://pushgateway:9091}"
JOB_NAME="${JOB_NAME:-ci_pipeline}"
INSTANCE="${INSTANCE:-$(hostname)}"
JOB_DURATION="${JOB_DURATION:-0}"
JOB_STATUS="${JOB_STATUS:-unknown}"
JOB_TIMESTAMP="$(date +%s)"
PIPELINE="${PIPELINE:-unknown}"
BRANCH="${BRANCH:-unknown}"
COMMIT="${COMMIT:-unknown}"

push_metrics() {
  cat <<EOF | curl --fail --silent --data-binary @- \
    "${PUSHGATEWAY_URL}/metrics/job/${JOB_NAME}/instance/${INSTANCE}"
# HELP ci_job_duration_seconds Duration of CI job in seconds
# TYPE ci_job_duration_seconds gauge
ci_job_duration_seconds{pipeline="${PIPELINE}",branch="${BRANCH}",status="${JOB_STATUS}"} ${JOB_DURATION}
# HELP ci_job_last_timestamp Unix timestamp of last job run
# TYPE ci_job_last_timestamp gauge
ci_job_last_timestamp{pipeline="${PIPELINE}",branch="${BRANCH}"} ${JOB_TIMESTAMP}
# HELP ci_job_success Success status (1=success, 0=failure)
# TYPE ci_job_success gauge
ci_job_success{pipeline="${PIPELINE}",branch="${BRANCH}"} $([ "${JOB_STATUS}" = "success" ] && echo 1 || echo 0)
EOF
}

delete_metrics() {
  curl --fail --silent -X DELETE \
    "${PUSHGATEWAY_URL}/metrics/job/${JOB_NAME}/instance/${INSTANCE}"
}

case "${1:-push}" in
  push)   push_metrics;   echo "Metrics pushed"   ;;
  delete) delete_metrics; echo "Metrics deleted"  ;;
  *) echo "Usage: $0 [push|delete]"; exit 1        ;;
esac
