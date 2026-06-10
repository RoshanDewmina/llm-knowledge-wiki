#!/usr/bin/env bash
# Encrypted backup of personal-sensitive knowledge-base files.
#
# Bundles every file matched by tools/enforce_chmod.py's globs, tars them, and
# encrypts the bundle with age to the recipient public key in
# ${AGE_RECIPIENT_FILE} (default: ~/.hermes/secure/age.recipient).
#
# Output: ${REPO_ROOT}/secure/encrypted/<UTC-timestamp>-personal-backup.age
#
# Bootstrap (one-time, passphrase-protected restore key):
#   brew install age
#   mkdir -p ~/.hermes/secure
#   tmp="$(mktemp)"
#   age-keygen -o "$tmp"
#   age-keygen -y "$tmp" > ~/.hermes/secure/age.recipient
#   age --passphrase -o ~/.hermes/secure/age.key "$tmp"
#   rm -f "$tmp"
#   chmod 600 ~/.hermes/secure/age.key ~/.hermes/secure/age.recipient
#
# Decrypt:
#   age -d -i ~/.hermes/secure/age.key <bundle.age> | tar -tzf -
#
# Cleartext bundles are written to a tmp file and deleted before exit. The
# encrypted output is the only artifact that lands on disk.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGE_KEY_FILE="${AGE_KEY_FILE:-${HOME}/.hermes/secure/age.key}"
AGE_RECIPIENT_FILE="${AGE_RECIPIENT_FILE:-${HOME}/.hermes/secure/age.recipient}"
OUT_DIR="${REPO_ROOT}/secure/encrypted"

cd "${REPO_ROOT}"

if ! command -v age >/dev/null 2>&1; then
    cat >&2 <<'EOF'
error: `age` is not installed.

Install once:
    brew install age

Then create a passphrase-protected restore key:
    mkdir -p ~/.hermes/secure
    tmp="$(mktemp)"
    age-keygen -o "$tmp"
    age-keygen -y "$tmp" > ~/.hermes/secure/age.recipient
    age --passphrase -o ~/.hermes/secure/age.key "$tmp"
    rm -f "$tmp"
    chmod 600 ~/.hermes/secure/age.key ~/.hermes/secure/age.recipient

Then re-run this script.
EOF
    exit 2
fi

if [[ ! -f "${AGE_RECIPIENT_FILE}" ]]; then
    echo "error: recipient file missing: ${AGE_RECIPIENT_FILE}" >&2
    echo "see header comment for bootstrap instructions" >&2
    exit 2
fi

if [[ ! -f "${AGE_KEY_FILE}" ]]; then
    echo "error: passphrase-protected restore identity missing: ${AGE_KEY_FILE}" >&2
    echo "see header comment for bootstrap instructions" >&2
    exit 2
fi

if grep -q '^AGE-SECRET-KEY-' "${AGE_KEY_FILE}"; then
    cat >&2 <<EOF
error: restore identity is not passphrase-protected: ${AGE_KEY_FILE}

Create a passphrase-protected identity before running backups:
    mkdir -p ~/.hermes/secure
    mv ~/.hermes/secure/age.key ~/.hermes/secure/age.key.unencrypted.deprecated
    tmp="\$(mktemp)"
    age-keygen -o "\$tmp"
    age-keygen -y "\$tmp" > ~/.hermes/secure/age.recipient
    age --passphrase -o ~/.hermes/secure/age.key "\$tmp"
    rm -f "\$tmp"
    chmod 600 ~/.hermes/secure/age.key ~/.hermes/secure/age.recipient

Existing backups encrypted to the old recipient remain decryptable with
age.key.unencrypted.deprecated until you replace them.
EOF
    exit 2
fi

mkdir -p "${OUT_DIR}"
chmod 700 "${OUT_DIR}"

# Use the same globs as tools/enforce_chmod.py.
mapfile -t TARGETS < <(python3 - <<'PY'
import sys
sys.path.insert(0, "tools")
from enforce_chmod import iter_targets, PERSONAL_GLOBS
from wiki_utils import REPO_ROOT
for path in iter_targets(PERSONAL_GLOBS):
    print(path.relative_to(REPO_ROOT))
PY
)

if [[ ${#TARGETS[@]} -eq 0 ]]; then
    echo "no personal files matched; nothing to back up" >&2
    exit 0
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_FILE="${OUT_DIR}/${TIMESTAMP}-personal-backup.age"

# Stream tar through age — never write the cleartext tar to disk.
tar -czf - "${TARGETS[@]}" \
    | age -R "${AGE_RECIPIENT_FILE}" \
    > "${OUT_FILE}"

chmod 600 "${OUT_FILE}"

BYTES="$(stat -f '%z' "${OUT_FILE}")"
echo "backup_encrypted: ${#TARGETS[@]} files -> ${OUT_FILE} (${BYTES} bytes)"
