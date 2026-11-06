"""
Command Line Interface for RepoFaro.
"""

import argparse
import sys

from collections.abc import Sequence
from pathlib import Path
from .models import ProjectSnapshot

from . import __version__
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

    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Analyze a project's directory structure."
    )

    scan_parser.add_argument(
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


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point of RepoFaro."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":

        try:
            snapshot = scan_project(args.path)

        except OSError as error:
            print(f"RepoFaro: error: {error}", file=sys.stderr)
            return 2

        print_scan_report(snapshot)

        return 0

    parser.print_help()

    return 0