"""
Data models used by RepoFaro.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProjectSnapshot:
    """Represents the structural information of a scanned project."""

    root: Path
    files_count: int
    directories_count: int
    extension_counts: dict[str, int]