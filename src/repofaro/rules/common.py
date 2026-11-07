"""
Common project audit rules.

These rules apply independently of the project's
main programming language.
"""

from ..models import AuditContext, Finding, Severity


def check_readme(context: AuditContext) -> Finding | None:
    """Check whether the project has a root README file."""

    files = {
        filename.casefold()
        for filename in context.snapshot.root_files
    }

    has_readme = any(
        filename == "readme"
        or filename.startswith("readme.")
        for filename in files
    )

    if has_readme:
        return None

    return Finding(
        rule_id="COMMON-001",
        title="Missing project documentation",
        severity=Severity.WARNING,
        description="The project does not contain a root README file.",
        recommendation=(
            "Create a README.md describing the project, "
            "installation and usage."
        )
    )


def check_gitignore(context: AuditContext) -> Finding | None:
    """Check whether the project contains a .gitignore file."""

    files = {
        filename.casefold()
        for filename in context.snapshot.root_files
    }

    if ".gitignore" in files:
        return None

    return Finding(
        rule_id="COMMON-002",
        title="Missing .gitignore",
        severity=Severity.INFO,
        description="The project does not contain a .gitignore file.",
        recommendation=(
            "Consider adding a .gitignore to exclude "
            "temporary files and generated artifacts."
        )
    )


def check_tests_directory(context: AuditContext) -> Finding | None:
    """Check whether a conventional tests directory exists."""

    directories = {
        directory.casefold()
        for directory in context.snapshot.root_directories
    }

    if directories.intersection({"test", "tests"}):
        return None

    return Finding(
        rule_id="COMMON-003",
        title="No conventional tests directory found",
        severity=Severity.INFO,
        description=(
            "The project does not contain a root 'tests' or 'test' directory."
        ),
        recommendation=(
            "Consider organizing automated tests in a dedicated directory."
        )
    )


def check_license(context: AuditContext) -> Finding | None:
    """Check whether the project contains a recognizable license file."""

    files = {
        filename.casefold()
        for filename in context.snapshot.root_files
    }

    has_license = any(
        filename == "license"
        or filename.startswith("license.")
        or filename == "copying"
        or filename.startswith("copying.")
        for filename in files
    )

    if has_license:
        return None

    return Finding(
        rule_id="COMMON-004",
        title="No license file detected",
        severity=Severity.INFO,
        description="The project does not contain a recognized license file.",
        recommendation=(
            "Consider adding a software license if you intend "
            "to distribute the project."
        )
    )