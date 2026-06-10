#!/usr/bin/env bash
# Install / preview shell-based cron entries for the personal-KB layer.
#
# These complement the existing Hermes skill-based cron in
# ~/.hermes/cron/jobs.json (those run AI agents). The entries below run plain
# shell scripts (health log, encrypted backup, leak audit, stale-fact
# reminder, source-coverage drift, sqlite VACUUM).
#
# Usage:
#   tools/install_personal_cron.sh             # preview
#   tools/install_personal_cron.sh --install   # append to user crontab
#   tools/install_personal_cron.sh --uninstall # remove the personal-KB block
#
# Re-running --install is idempotent; the block is identified by the marker
# comments PERSONAL_KB_BEGIN / PERSONAL_KB_END.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_LOG_DIR="${HOME}/.hermes/logs"
BEGIN_MARK="# PERSONAL_KB_BEGIN — managed by tools/install_personal_cron.sh"
END_MARK="# PERSONAL_KB_END"

mkdir -p "${HERMES_LOG_DIR}"

read -r -d '' BLOCK <<EOF || true
${BEGIN_MARK}
# Daily health check + log
15 8 * * * cd ${REPO_ROOT} && ./bin/llm-wiki health >> ${HERMES_LOG_DIR}/health-\$(date +\\%Y\\%m).log 2>&1
# Daily encrypted backup of personal files (silently no-ops if age unset up)
30 23 * * * cd ${REPO_ROOT} && tools/backup_encrypted.sh >> ${HERMES_LOG_DIR}/backup-\$(date +\\%Y\\%m).log 2>&1
# Weekly source-coverage drift report (Sunday 6 PM)
0 18 * * 0 cd ${REPO_ROOT} && python3 tools/source_coverage_report.py >> ${HERMES_LOG_DIR}/coverage-\$(date +\\%Y\\%m).log 2>&1
# Monthly PII leak audit (1st of month, 9 AM)
0 9 1 * * cd ${REPO_ROOT} && python3 tools/audit_pii_leaks.py --strict >> ${HERMES_LOG_DIR}/leak-audit-\$(date +\\%Y\\%m).log 2>&1
# Weekly stale-fact reminder (Monday 9 AM)
0 9 * * 1 cd ${REPO_ROOT} && python3 tools/check_expiring_facts.py --within 60d >> ${HERMES_LOG_DIR}/stale-facts-\$(date +\\%Y\\%m).log 2>&1
# Weekly SQLite VACUUM on Hermes state.db (Sunday 4 AM)
0 4 * * 0 sqlite3 ${HOME}/.hermes/state.db "VACUUM;" >> ${HERMES_LOG_DIR}/vacuum-\$(date +\\%Y\\%m).log 2>&1
${END_MARK}
EOF

mode="${1:-preview}"

case "${mode}" in
    preview|--preview)
        echo "${BLOCK}"
        ;;
    --install)
        existing="$(crontab -l 2>/dev/null || true)"
        if echo "${existing}" | grep -q "${BEGIN_MARK}"; then
            # Replace the existing block.
            new="$(echo "${existing}" | awk -v b="${BEGIN_MARK}" -v e="${END_MARK}" '
                BEGIN {p=1}
                $0==b {p=0; next}
                $0==e {p=1; next}
                p==1 {print}
            ')"
            printf "%s\n%s\n" "${new}" "${BLOCK}" | crontab -
            echo "install_personal_cron: replaced existing block"
        else
            printf "%s\n%s\n" "${existing}" "${BLOCK}" | crontab -
            echo "install_personal_cron: appended new block"
        fi
        crontab -l | grep -F "${BEGIN_MARK}" >/dev/null
        echo "active personal-KB cron entries:"
        crontab -l | awk -v b="${BEGIN_MARK}" -v e="${END_MARK}" 'b==$0,e==$0'
        ;;
    --uninstall)
        existing="$(crontab -l 2>/dev/null || true)"
        if ! echo "${existing}" | grep -q "${BEGIN_MARK}"; then
            echo "install_personal_cron: nothing to uninstall"
            exit 0
        fi
        new="$(echo "${existing}" | awk -v b="${BEGIN_MARK}" -v e="${END_MARK}" '
            BEGIN {p=1}
            $0==b {p=0; next}
            $0==e {p=1; next}
            p==1 {print}
        ')"
        printf "%s\n" "${new}" | crontab -
        echo "install_personal_cron: removed personal-KB block"
        ;;
    *)
        echo "usage: tools/install_personal_cron.sh [--preview|--install|--uninstall]" >&2
        exit 2
        ;;
esac
