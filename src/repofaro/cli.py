"""
Command Line Interface for RepoFaro.
"""

import argparse
import sys

from collections.abc import Sequence
from pathlib import Path

from . import __version__

from .audit import run_audit
from .detector import detect_technologies

from .models import (
    AuditReport,
    ProjectProfile,
    ProjectSnapshot,
    Severity,
)

from .scanner import scan_project


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the command line argument parser."""

    parser = argparse.ArgumentParser(
        prog="repofaro",
        description="Local project structure and quality auditor."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )

    # Scan command.
    scan_parser = subparsers.add_parser(
        "scan",
        help="Analyze a project's directory structure."
    )

    scan_parser.add_argument(
        "path",
        type=Path,
        help="Path to the project directory."
    )

    # Detect command.
    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect technologies used in a project."
    )

    detect_parser.add_argument(
        "path",
        type=Path,
        help="Path to the project directory."
    )

    # Audit command.
    audit_parser = subparsers.add_parser(
        "audit",
        help="Perform a complete project audit."
    )

    audit_parser.add_argument(
        "path",
        type=Path,
        help="Path to the project directory."
    )

    return parser


def print_scan_report(snapshot: ProjectSnapshot) -> None:
    """Display project scan results in the terminal."""

    print()
    print("=" * 42)
    print("             REPOFARO")
    print("=" * 42)

    print("\nPROJECT SCANNER")
    print("-" * 42)

    print(f"Project: {snapshot.root}")

    print(f"Directories: {snapshot.directories_count}")
    print(f"Files: {snapshot.files_count}")

    print("\nFILE DISTRIBUTION")
    print("-" * 42)

    for extension, count in snapshot.extension_counts.items():
        print(f"{extension:<20} {count}")

    print("\nScan completed successfully.")
    print()


def print_detection_report(profile: ProjectProfile) -> None:
    """Display technology detection results."""

    print()
    print("=" * 42)
    print("             REPOFARO")
    print("=" * 42)

    print("\nTECHNOLOGY DETECTOR")
    print("-" * 42)

    print(f"Project: {profile.root}")

    print("\nDETECTED TECHNOLOGIES")
    print("-" * 42)

    for detection in profile.detections:
        print(
            f"{detection.technology:<15} "
            f"{detection.status.value}"
        )

    print("\nEVIDENCE")
    print("-" * 42)

    for detection in profile.detections:

        if not detection.evidence:
            continue

        print(f"\n{detection.technology}:")

        for evidence in detection.evidence:
            print(f"  - {evidence}")

    print("\nDetection completed successfully.")
    print()


def print_audit_report(report: AuditReport) -> None:
    """Display the complete project audit report."""

    print()
    print("=" * 48)
    print("                 REPOFARO")
    print("=" * 48)

    print("\nPROJECT AUDIT")
    print("-" * 48)

    print(f"Project: {report.snapshot.root}")

    # Technology information.
    print("\nTECHNOLOGIES")
    print("-" * 48)

    for detection in report.profile.detections:
        print(
            f"{detection.technology:<15} "
            f"{detection.status.value}"
        )

    # Audit findings.
    print("\nAUDIT FINDINGS")
    print("-" * 48)

    if not report.findings:
        print("No findings. All registered rules passed.")

    for finding in report.findings:

        print(
            f"\n[{finding.severity.value}] "
            f"{finding.rule_id}"
        )

        print(f"Title: {finding.title}")
        print(f"Description: {finding.description}")
        print(f"Recommendation: {finding.recommendation}")

        if finding.path is not None:
            print(f"Path: {finding.path}")

    # Calculate summary.
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

    print("\nAUDIT SUMMARY")
    print("-" * 48)

    print(f"Rules executed: {report.rules_executed}")
    print(f"Total findings: {len(report.findings)}")
    print(f"Errors: {error_count}")
    print(f"Warnings: {warning_count}")
    print(f"Information: {info_count}")

    print("\nAudit completed successfully.")
    print()


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point of RepoFaro."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":

        try:
            snapshot = scan_project(args.path)

        except OSError as error:
            print(
                f"RepoFaro: error: {error}",
                file=sys.stderr
            )
            return 2

        print_scan_report(snapshot)

        return 0

    elif args.command == "detect":

        try:
            snapshot = scan_project(args.path)
            profile = detect_technologies(snapshot)

        except OSError as error:
            print(
                f"RepoFaro: error: {error}",
                file=sys.stderr
            )
            return 2

        print_detection_report(profile)

        return 0

    elif args.command == "audit":

        try:
            report = run_audit(args.path)

        except OSError as error:
            print(
                f"RepoFaro: error: {error}",
                file=sys.stderr
            )
            return 2

        print_audit_report(report)

        return 0

    parser.print_help()

    return 0