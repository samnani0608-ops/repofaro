"""
Project Audit Controller.

Coordinates the scanner, detector and rule engine
to generate a complete project audit report.
"""

from pathlib import Path

from .detector import detect_technologies

from .models import (
    AuditContext,
    AuditReport,
)

from .rules.engine import (
    DEFAULT_RULES,
    run_rules,
)

from .scanner import scan_project


def run_audit(project_path: Path) -> AuditReport:
    """
    Execute a complete project audit.

    Steps:
        1. Scan the project directory.
        2. Detect project technologies.
        3. Build the audit context.
        4. Execute registered audit rules.
        5. Generate the final audit report.
    """

    # Step 1: Scan project.
    snapshot = scan_project(project_path)

    # Step 2: Detect technologies.
    profile = detect_technologies(snapshot)

    # Step 3: Build audit context.
    context = AuditContext(
        snapshot=snapshot,
        profile=profile
    )

    # Step 4: Execute audit rules.
    findings = run_rules(context)

    # Step 5: Generate audit report.
    return AuditReport(
        snapshot=snapshot,
        profile=profile,
        findings=findings,
        rules_executed=len(DEFAULT_RULES)
    )