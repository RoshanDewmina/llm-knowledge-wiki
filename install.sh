#!/usr/bin/env bash

set -euo pipefail

REPO_URL="${LLM_WIKI_REPO_URL:-https://github.com/RoshanDewmina/llm-knowledge-wiki.git}"
TARGET_DIR="${LLM_WIKI_DIR:-$HOME/llm-knowledge-wiki}"
OPEN_OBSIDIAN="${LLM_WIKI_OPEN_OBSIDIAN:-1}"

echo "==> LLM Knowledge Wiki installer"
echo "==> Repo: ${REPO_URL}"
echo "==> Target: ${TARGET_DIR}"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "error: this installer currently targets macOS." >&2
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

if ! command -v git >/dev/null 2>&1; then
  echo "==> Installing git"
  brew install git
fi

if [[ -e "${TARGET_DIR}" && ! -d "${TARGET_DIR}" ]]; then
  echo "error: target exists and is not a directory: ${TARGET_DIR}" >&2
  exit 1
fi

if [[ -d "${TARGET_DIR}/.git" ]]; then
  echo "==> Repo already exists, updating it"
  git -C "${TARGET_DIR}" pull --ff-only
else
  if [[ -d "${TARGET_DIR}" ]] && [[ -n "$(find "${TARGET_DIR}" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
    echo "error: target directory exists and is not empty: ${TARGET_DIR}" >&2
    echo "Set LLM_WIKI_DIR to another path and rerun the installer." >&2
    exit 1
  fi
  echo "==> Cloning repository"
  git clone "${REPO_URL}" "${TARGET_DIR}"
fi

cd "${TARGET_DIR}"

echo "==> Running native onboarding"
./bin/llm-wiki setup
if [[ "${OPEN_OBSIDIAN}" == "1" ]]; then
  ./bin/llm-wiki onboard --open-obsidian
else
  ./bin/llm-wiki onboard
fi

cat <<EOF

Install complete.

Your repo is here:
  ${TARGET_DIR}

Next commands:
  cd "${TARGET_DIR}"
  ./bin/llm-wiki health
  make site-dev

For the beginner study workflow, read:
  START-HERE-STUDYING.md
EOF
