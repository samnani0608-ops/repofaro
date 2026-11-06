"""
Command Line Interface for RepoFaro.
"""

import argparse

from collections.abc import Sequence

from . import __version__


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

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point of RepoFaro."""

    parser = build_parser()
    parser.parse_args(argv)

    print()
    print("======================================")
    print("             REPOFARO")
    print("======================================")
    print(f"Version: {__version__}")
    print()
    print("Local Project Structure & Quality Auditor")
    print()
    print("Status: Application initialized.")
    print("Scanner: Not implemented yet.")
    print("Detector: Not implemented yet.")
    print()
    print("Welcome to RepoFaro!")
    print()

    return 0