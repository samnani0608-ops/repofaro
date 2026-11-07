"""
Data models used by RepoFaro.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass(slots=True)
class ProjectSnapshot:
    """Represents the structural information of a scanned project."""

    root: Path
    files_count: int
    directories_count: int
    extension_counts: dict[str, int]
    root_files: tuple[str, ...]
    root_directories: tuple[str, ...]


class DetectionStatus(str, Enum):
    """Possible technology detection states."""

    CONFIRMED = "CONFIRMED"
    POSSIBLE = "POSSIBLE"
    NOT_DETECTED = "NOT DETECTED"


@dataclass(slots=True)
class TechnologyDetection:
    """Represents the detection result of a technology."""

    technology: str
    status: DetectionStatus
    evidence: tuple[str, ...]


@dataclass(slots=True)
class ProjectProfile:
    """Represents the technology profile of a project."""

    root: Path
    detections: tuple[TechnologyDetection, ...]


class Severity(str, Enum):
    """Severity levels for project audit findings."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(slots=True)
class Finding:
    """Represents an issue or recommendation."""

    rule_id: str
    title: str
    severity: Severity
    description: str
    recommendation: str
    path: str | None = None


@dataclass(slots=True)
class AuditContext:
    """Contains the information required by audit rules."""

    snapshot: ProjectSnapshot
    profile: ProjectProfile

@dataclass(slots=True)
class AuditReport:
    """Represents the complete results of a project audit."""

    snapshot: ProjectSnapshot
    profile: ProjectProfile
    findings: tuple[Finding, ...]
    rules_executed: int