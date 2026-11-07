"""
Automated tests for the RepoFaro Rule Engine.
"""

from repofaro.detector import detect_technologies

from repofaro.models import (
    AuditContext,
    Severity,
)

from repofaro.rules.engine import run_rules
from repofaro.scanner import scan_project


def build_context(project_path):
    """Create an audit context from a project directory."""

    snapshot = scan_project(project_path)
    profile = detect_technologies(snapshot)

    return AuditContext(
        snapshot=snapshot,
        profile=profile
    )


def test_empty_project_generates_all_common_findings(tmp_path):
    """An empty project should generate four findings."""

    context = build_context(tmp_path)

    findings = run_rules(context)

    rule_ids = {
        finding.rule_id
        for finding in findings
    }

    assert len(findings) == 4

    assert rule_ids == {
        "COMMON-001",
        "COMMON-002",
        "COMMON-003",
        "COMMON-004",
    }


def test_complete_project_generates_no_findings(tmp_path):
    """A project with all expected conventions should pass."""

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

    context = build_context(tmp_path)

    findings = run_rules(context)

    assert findings == ()


def test_missing_readme_generates_warning(tmp_path):
    """Missing project documentation should generate a warning."""

    context = build_context(tmp_path)

    findings = run_rules(context)

    readme_finding = next(
        finding
        for finding in findings
        if finding.rule_id == "COMMON-001"
    )

    assert readme_finding.severity == Severity.WARNING
    assert readme_finding.recommendation


def test_readme_alternative_names_are_accepted(tmp_path):
    """README variants should be recognized."""

    (tmp_path / "readme.rst").write_text(
        "Example project",
        encoding="utf-8"
    )

    context = build_context(tmp_path)

    findings = run_rules(context)

    assert all(
        finding.rule_id != "COMMON-001"
        for finding in findings
    )