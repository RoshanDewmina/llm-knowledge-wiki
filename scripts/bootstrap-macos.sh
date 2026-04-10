#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BREWFILE="${REPO_ROOT}/Brewfile"
SITE_DIR="${REPO_ROOT}/apps/site"
TEMP_BREWFILE="$(mktemp "${TMPDIR:-/tmp}/llm-knowledge-wiki-bootstrap.XXXXXX")"

cleanup() {
  rm -f "${TEMP_BREWFILE}"
}

trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "error: scripts/bootstrap-macos.sh is for macOS. Use the manual setup docs on other platforms." >&2
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "==> Homebrew not found"
  echo "==> Installing Homebrew using the official installer from https://brew.sh/"
  echo "==> You may be prompted for your Mac password during this step"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [[ -x /usr/local/bin/brew ]]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

echo "==> Using ${BREWFILE##${REPO_ROOT}/} as the package manifest"
printf 'tap "oven-sh/bun"\n' > "${TEMP_BREWFILE}"

echo "==> Checking which dependencies are already satisfied"
for entry in "python@3.12:python3" "bun:bun" "git:git" "gh:gh" "ripgrep:rg"; do
  formula_name="${entry%%:*}"
  command_name="${entry##*:}"
  if brew list --formula "${formula_name}" >/dev/null 2>&1 || command -v "${command_name}" >/dev/null 2>&1; then
    printf '[skip] formula %s already available\n' "${formula_name}"
  else
    printf 'brew "%s"\n' "${formula_name}" >> "${TEMP_BREWFILE}"
  fi
done

for cask_name in obsidian claude-code codex; do
  cask_ok=0
  case "${cask_name}" in
    obsidian)
      if brew list --cask obsidian >/dev/null 2>&1 || command -v obsidian >/dev/null 2>&1 || [[ -d /Applications/Obsidian.app ]]; then
        cask_ok=1
      fi
      ;;
    claude-code)
      if brew list --cask claude-code >/dev/null 2>&1 || command -v claude >/dev/null 2>&1; then
        cask_ok=1
      fi
      ;;
    codex)
      if brew list --cask codex >/dev/null 2>&1 || command -v codex >/dev/null 2>&1; then
        cask_ok=1
      fi
      ;;
  esac

  if [[ "${cask_ok}" -eq 1 ]]; then
    printf '[skip] cask %s already available\n' "${cask_name}"
  else
    printf 'cask "%s"\n' "${cask_name}" >> "${TEMP_BREWFILE}"
  fi
done

if [[ "$(wc -l < "${TEMP_BREWFILE}")" -gt 1 ]]; then
  echo "==> Installing missing host tools with brew bundle"
  brew bundle --file="${TEMP_BREWFILE}" --no-upgrade
else
  echo "==> All required host tools are already available"
fi

echo "==> Verifying installed commands"
missing=0
for command_name in python3 bun git gh rg claude codex; do
  if command -v "${command_name}" >/dev/null 2>&1; then
    printf '[ok] %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
  else
    printf '[fail] missing command: %s\n' "${command_name}" >&2
    missing=1
  fi
done

if command -v obsidian >/dev/null 2>&1 || [[ -d /Applications/Obsidian.app ]]; then
  echo "[ok] Obsidian is available"
else
  echo "[fail] Obsidian is not available after brew bundle" >&2
  missing=1
fi

if [[ "${missing}" -ne 0 ]]; then
  echo "error: bootstrap completed with missing tools" >&2
  exit 1
fi

if [[ -f "${SITE_DIR}/package.json" ]]; then
  echo "==> Installing Bun dependencies for apps/site"
  (
    cd "${SITE_DIR}"
    bun install --frozen-lockfile
  )

  if [[ "${LLM_WIKI_INSTALL_PLAYWRIGHT:-0}" == "1" ]]; then
    echo "==> Installing Playwright Chromium for browser smoke tests"
    (
      cd "${SITE_DIR}"
      bunx playwright install chromium
    )
  else
    echo "==> Skipping Playwright browser install by default"
    echo "==> Set LLM_WIKI_INSTALL_PLAYWRIGHT=1 if you want browser-test dependencies too"
  fi
fi

cat <<EOF

Bootstrap complete.

Next commands:
  ./bin/llm-wiki doctor
  ./bin/llm-wiki health
  open -a Obsidian "${REPO_ROOT}"

Optional:
  make site-dev
EOF
