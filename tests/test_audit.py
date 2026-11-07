"""
Automated tests for the RepoFaro Audit Controller.
"""

from repofaro.audit import run_audit
from repofaro.models import DetectionStatus


def test_empty_project_generates_four_findings(tmp_path):
    """An empty project should generate four common findings."""

    report = run_audit(tmp_path)

    assert report.rules_executed == 4
    assert len(report.findings) == 4

    rule_ids = {
        finding.rule_id
        for finding in report.findings
    }

    assert rule_ids == {
        "COMMON-001",
        "COMMON-002",
        "COMMON-003",
        "COMMON-004",
    }


def test_complete_project_generates_no_findings(tmp_path):
    """A complete project should generate no findings."""

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

    (tmp_path / "tests").mkdir()

    report = run_audit(tmp_path)

    assert report.findings == ()
    assert report.rules_executed == 4


def test_audit_detects_project_technology(tmp_path):
    """The audit should include technology detection results."""

    (tmp_path / "package.json").write_text(
        '{"name": "example"}',
        encoding="utf-8"
    )

    (tmp_path / "app.js").write_text(
        "console.log('Hello')",
        encoding="utf-8"
    )

    report = run_audit(tmp_path)

    node_detection = next(
        detection
        for detection in report.profile.detections
        if detection.technology == "Node.js"
    )

    assert node_detection.status == DetectionStatus.CONFIRMED
    assert report.snapshot.files_count == 2