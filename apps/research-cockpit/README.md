# Research Cockpit

Research Cockpit is a native macOS MVP for guided source-grounded study workflows on top of the existing local Markdown wiki.

The app keeps the vault as the source of truth:

- imported originals are copied under `raw/courses/<course-slug>/`
- course metadata is stored in `.research-cockpit/courses/<course-slug>.json`
- user-visible course notes live under `wiki/studies/courses/<course-slug>/`
- generated outputs remain files in the vault wherever possible

Hermes is hidden by default. Normal users see Research, Study, Schedule, and Health. Advanced mode reveals Hermes status, gateway, cron, skills, and launchd checks.

## Build

```bash
swift build
swift test
./script/build_and_run.sh --verify
```

The run script stages `dist/ResearchCockpit.app` from the SwiftPM executable and launches it as a foreground macOS app bundle.

## Release Packaging

```bash
./script/package_release.sh --skip-notarize
```

By default, packaging performs an ad-hoc signature so the app bundle has a valid local signature for testing. For Developer ID distribution, set:

```bash
export DEVELOPER_ID_APPLICATION="Developer ID Application: Your Name (TEAMID)"
export APPLE_ID="you@example.com"
export APPLE_TEAM_ID="TEAMID"
export APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
./script/package_release.sh
```

That produces a zip under `dist/release/` and submits it to Apple notarization when credentials are present.
