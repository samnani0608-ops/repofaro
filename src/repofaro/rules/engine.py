"""
Rule Engine.

Executes registered rules and collects project findings.
"""

from collections.abc import Sequence
from typing import Callable

from ..models import AuditContext, Finding

from .common import (
    check_readme,
    check_gitignore,
    check_tests_directory,
    check_license,
)


RuleCheck = Callable[[AuditContext], Finding | None]


DEFAULT_RULES: tuple[RuleCheck, ...] = (
    check_readme,
    check_gitignore,
    check_tests_directory,
    check_license,
)


def run_rules(
    context: AuditContext,
    rules: Sequence[RuleCheck] = DEFAULT_RULES
) -> tuple[Finding, ...]:
    """
    Execute audit rules and return all generated findings.
    """

    findings = []

    for rule in rules:

        finding = rule(context)

        if finding is not None:
            findings.append(finding)

    return tuple(findings)