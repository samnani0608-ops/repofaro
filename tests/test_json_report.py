"""
Automated tests for the RepoFaro JSON Reporter.
"""

import json

from repofaro.audit import run_audit
from repofaro.reporters.json_report import render_json_report


def test_json_report_contains_complete_project_information(tmp_path):
    """Verify that a complete project produces valid JSON."""

    (tmp_path / "README.md").write_text(
        "# Example project",
        encoding="utf-8"
    )

    (tmp_path / ".gitignore").write_text(
        ".venv/",
        encoding="utf-8"
    )

    (tmp_path / "LICENSE").write_text(
        "MIT License",
        encoding="utf-8"
    )

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'example'\n",
        encoding="utf-8"
    )

    (tmp_path / "main.py").write_text(
        "print('Hello')",
        encoding="utf-8"
    )

    (tmp_path / "tests").mkdir()

    report = run_audit(tmp_path)

    json_output = render_json_report(report)

    data = json.loads(json_output)

    assert data["schema_version"] == "1.0"

    assert data["project"]["root"] == str(tmp_path.resolve())
    assert data["project"]["files_count"] == 5

    assert data["rules_executed"] == 4

    assert data["summary"]["total_findings"] == 0
    assert data["summary"]["errors"] == 0
    assert data["summary"]["warnings"] == 0
    assert data["summary"]["information"] == 0

    assert data["findings"] == []

    python_detection = next(
        technology
        for technology in data["technologies"]
        if technology["name"] == "Python"
    )

    assert python_detection["status"] == "CONFIRMED"


def test_json_report_contains_findings_and_severities(tmp_path):
    """Verify that findings are correctly represented in JSON."""

    report = run_audit(tmp_path)

    json_output = render_json_report(report)

    data = json.loads(json_output)

    assert data["summary"]["total_findings"] == 4
    assert data["summary"]["errors"] == 0
    assert data["summary"]["warnings"] == 1
    assert data["summary"]["information"] == 3

    rule_ids = {
        finding["rule_id"]
        for finding in data["findings"]
    }

    assert rule_ids == {
        "COMMON-001",
        "COMMON-002",
        "COMMON-003",
        "COMMON-004",
    }