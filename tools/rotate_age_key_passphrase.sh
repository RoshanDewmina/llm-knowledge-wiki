#!/usr/bin/env bash
# Rotate the personal-KB backup recipient to a passphrase-protected age identity.
#
# This intentionally prompts locally for the restore passphrase. Do not pass the
# passphrase through chat, shell history, or environment variables.
#
# Usage:
#   tools/rotate_age_key_passphrase.sh
#   tools/rotate_age_key_passphrase.sh --reencrypt-existing
#
# The second form re-encrypts existing repo-local secure/encrypted/*.age bundles
# to the new recipient before deleting the old identity.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SECURE_DIR="${HOME}/.hermes/secure"
KEY_FILE="${SECURE_DIR}/age.key"
RECIPIENT_FILE="${SECURE_DIR}/age.recipient"
REENCRYPT_EXISTING=0

case "${1:-}" in
    "")
        ;;
    --reencrypt-existing)
        REENCRYPT_EXISTING=1
        ;;
    *)
        echo "usage: tools/rotate_age_key_passphrase.sh [--reencrypt-existing]" >&2
        exit 2
        ;;
esac

if ! command -v age >/dev/null 2>&1 || ! command -v age-keygen >/dev/null 2>&1; then
    echo "error: age and age-keygen are required; run: brew install age" >&2
    exit 2
fi

mkdir -p "${SECURE_DIR}"
chmod 700 "${SECURE_DIR}"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "${WORK_DIR}"' EXIT

RAW_KEY="${WORK_DIR}/age.identity.raw"
NEW_KEY="${WORK_DIR}/age.key"
NEW_RECIPIENT="${WORK_DIR}/age.recipient"

age-keygen -o "${RAW_KEY}" >/dev/null
age-keygen -y "${RAW_KEY}" > "${NEW_RECIPIENT}"

echo "Enter a new passphrase for ${KEY_FILE}." >&2
age --passphrase -o "${NEW_KEY}" "${RAW_KEY}"
chmod 600 "${NEW_KEY}" "${NEW_RECIPIENT}"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OLD_KEY_BACKUP=""
OLD_RECIPIENT_BACKUP=""

if [[ -f "${KEY_FILE}" ]]; then
    OLD_KEY_BACKUP="${SECURE_DIR}/age.key.deprecated.${TS}"
    mv "${KEY_FILE}" "${OLD_KEY_BACKUP}"
    chmod 600 "${OLD_KEY_BACKUP}"
fi
if [[ -f "${RECIPIENT_FILE}" ]]; then
    OLD_RECIPIENT_BACKUP="${SECURE_DIR}/age.recipient.deprecated.${TS}"
    mv "${RECIPIENT_FILE}" "${OLD_RECIPIENT_BACKUP}"
    chmod 600 "${OLD_RECIPIENT_BACKUP}"
fi

cp "${NEW_KEY}" "${KEY_FILE}"
cp "${NEW_RECIPIENT}" "${RECIPIENT_FILE}"
chmod 600 "${KEY_FILE}" "${RECIPIENT_FILE}"

if [[ "${REENCRYPT_EXISTING}" == "1" && -n "${OLD_KEY_BACKUP}" ]]; then
    shopt -s nullglob
    for bundle in "${REPO_ROOT}"/secure/encrypted/*.age; do
        tmp="${bundle}.tmp"
        age -d -i "${OLD_KEY_BACKUP}" "${bundle}" | age -R "${RECIPIENT_FILE}" > "${tmp}"
        chmod 600 "${tmp}"
        mv "${tmp}" "${bundle}"
        echo "reencrypted: ${bundle}" >&2
    done
    rm -f "${OLD_KEY_BACKUP}" "${OLD_RECIPIENT_BACKUP}"
    echo "old identity deleted after re-encrypting repo-local bundles" >&2
elif [[ -n "${OLD_KEY_BACKUP}" ]]; then
    cat >&2 <<EOF
new key installed.

Old identity retained at:
  ${OLD_KEY_BACKUP}

Run with --reencrypt-existing to re-encrypt repo-local backup bundles and delete
the old identity automatically after successful re-encryption.
EOF
fi

echo "age key rotation complete"
