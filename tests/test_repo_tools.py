from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parent.parent


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(REPO_ROOT / "bin" / "llm-wiki"), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class RepoToolingTests(unittest.TestCase):
    def test_lint_citations_passes(self) -> None:
        process = run_tool("tools/lint_citations.py")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)

    def test_query_filters_return_expected_section(self) -> None:
        process = run_tool(
            "tools/query_index.py",
            "transformer",
            "--section",
            "concepts",
            "--type",
            "concept",
            "--json",
        )
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        payload = json.loads(process.stdout)
        self.assertGreaterEqual(len(payload), 1)
        self.assertTrue(all(item["section"] == "concepts" for item in payload))
        self.assertTrue(all(item["type"] == "concept" for item in payload))

    def test_check_wiki_json_includes_generators_and_citation_lint(self) -> None:
        process = run_tool("tools/check_wiki.py", "--json")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        payload = json.loads(process.stdout)
        for key in ("coverage_dashboard", "review_queue", "daily_review", "build_site_manifest", "lint_citations"):
            self.assertIn(key, payload)
            self.assertEqual(payload[key]["exit_code"], 0, payload[key])

    def test_site_manifest_contains_review_pages(self) -> None:
        manifest_path = REPO_ROOT / "wiki" / ".cache" / "site-manifest.json"
        process = run_tool("tools/build_site_manifest.py")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        targets = {page["target"] for page in payload["pages"]}
        self.assertIn("reviews/review-queue", targets)
        self.assertIn("reviews/coverage-dashboard", targets)
        self.assertIn("reviews/daily-review", targets)
        self.assertGreaterEqual(len(payload["raw_documents"]), 3)

    def test_doctor_fast_mode_reports_repo_paths(self) -> None:
        process = run_tool("tools/doctor.py", "--json", "--skip-site-build", "--skip-vault-checks")
        self.assertIn(process.returncode, (0, 1), process.stdout or process.stderr)
        payload = json.loads(process.stdout)
        self.assertIn("commands", payload)
        self.assertIn("paths", payload)
        self.assertTrue(payload["paths"]["wiki"]["ok"])

    def test_cli_status_reports_wiki_counts(self) -> None:
        process = run_cli("status", "--json")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        payload = json.loads(process.stdout)
        self.assertIn("wiki", payload)
        self.assertGreaterEqual(payload["wiki"]["page_count"], 1)
        self.assertGreaterEqual(payload["wiki"]["raw_documents"], 1)

    def test_cli_doctor_fast_mode_matches_core_doctor(self) -> None:
        process = run_cli("doctor", "--json", "--skip-site-build", "--skip-vault-checks")
        self.assertIn(process.returncode, (0, 1), process.stdout or process.stderr)
        payload = json.loads(process.stdout)
        self.assertIn("commands", payload)
        self.assertIn("paths", payload)
        self.assertTrue(payload["paths"]["wiki"]["ok"])

    def test_cli_completion_lists_common_commands(self) -> None:
        process = run_cli("completion", "zsh")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        self.assertIn("onboard", process.stdout)
        self.assertIn("doctor", process.stdout)
        self.assertIn("health", process.stdout)

    def test_export_defaults_to_slides_subfolder(self) -> None:
        process = run_cli("export", "wiki/syntheses/transformer-orientation.md")
        self.assertEqual(process.returncode, 0, process.stdout or process.stderr)
        self.assertIn("wiki/outputs/slides/transformer-orientation.slides.md", process.stdout)


if __name__ == "__main__":
    unittest.main()
