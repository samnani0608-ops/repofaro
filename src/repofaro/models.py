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