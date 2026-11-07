"""
JSON Reporter.

Converts audit reports into structured JSON data.
"""

import json

from ..models import AuditReport, Severity


def audit_report_to_dict(report: AuditReport) -> dict:
    """
    Convert an AuditReport into a JSON-compatible dictionary.
    """

    # Calculate finding statistics.
    error_count = sum(
        finding.severity == Severity.ERROR
        for finding in report.findings
    )

    warning_count = sum(
        finding.severity == Severity.WARNING
        for finding in report.findings
    )

    info_count = sum(
        finding.severity == Severity.INFO
        for finding in report.findings
    )

    # Build the report structure.
    return {
        "schema_version": "1.0",

        "project": {
            "root": str(report.snapshot.root),
            "files_count": report.snapshot.files_count,
            "directories_count": report.snapshot.directories_count,
            "extension_counts": report.snapshot.extension_counts,
        },

        "technologies": [
            {
                "name": detection.technology,
                "status": detection.status.value,
                "evidence": list(detection.evidence),
            }
            for detection in report.profile.detections
        ],

        "rules_executed": report.rules_executed,

        "summary": {
            "total_findings": len(report.findings),
            "errors": error_count,
            "warnings": warning_count,
            "information": info_count,
        },

        "findings": [
            {
                "rule_id": finding.rule_id,
                "title": finding.title,
                "severity": finding.severity.value,
                "description": finding.description,
                "recommendation": finding.recommendation,
                "path": finding.path,
            }
            for finding in report.findings
        ],
    }


def render_json_report(report: AuditReport) -> str:
    """
    Serialize an audit report into formatted JSON text.
    """

    data = audit_report_to_dict(report)

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )