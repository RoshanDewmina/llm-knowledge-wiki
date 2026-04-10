#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${REPO_ROOT}"

echo "Starting first-time setup for LLM Knowledge Wiki..."
echo

./bin/llm-wiki onboard

echo
echo "Opening the beginner study guide..."
open "${REPO_ROOT}/START-HERE-STUDYING.md"

echo
echo "Next steps:"
echo "  1. Open Obsidian and select this folder as a vault"
echo "  2. Read START-HERE-STUDYING.md"
echo "  3. Add your class notes or transcripts into raw/"
echo "  4. Run ./bin/llm-wiki ingest raw/.../your-file.md"
echo
read -r -p "Press Enter to close this window..."
