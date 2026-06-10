#!/usr/bin/env bash
set -euo pipefail

SKIP_NOTARIZE=0
if [[ "${1:-}" == "--skip-notarize" ]]; then
  SKIP_NOTARIZE=1
fi

APP_NAME="ResearchCockpit"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
RELEASE_DIR="$DIST_DIR/release"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
ZIP_PATH="$RELEASE_DIR/$APP_NAME.zip"
IDENTITY="${DEVELOPER_ID_APPLICATION:--}"

cd "$ROOT_DIR"

"$ROOT_DIR/script/build_and_run.sh" --verify
pkill -x "$APP_NAME" >/dev/null 2>&1 || true

mkdir -p "$RELEASE_DIR"

/usr/bin/codesign --force --deep --options runtime --timestamp=none --sign "$IDENTITY" "$APP_BUNDLE"
/usr/bin/codesign --verify --deep --strict --verbose=2 "$APP_BUNDLE"

rm -f "$ZIP_PATH"
/usr/bin/ditto -c -k --keepParent "$APP_BUNDLE" "$ZIP_PATH"

if [[ "$SKIP_NOTARIZE" == "1" || "$IDENTITY" == "-" ]]; then
  echo "packaged $ZIP_PATH"
  echo "notarization skipped"
  exit 0
fi

: "${APPLE_ID:?APPLE_ID is required for notarization}"
: "${APPLE_TEAM_ID:?APPLE_TEAM_ID is required for notarization}"
: "${APP_SPECIFIC_PASSWORD:?APP_SPECIFIC_PASSWORD is required for notarization}"

xcrun notarytool submit "$ZIP_PATH" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APP_SPECIFIC_PASSWORD" \
  --wait

xcrun stapler staple "$APP_BUNDLE"
echo "notarized $APP_BUNDLE"
