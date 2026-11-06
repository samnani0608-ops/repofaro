"""
Project Scanner.

Responsible for inspecting project directories
and collecting structural information.
"""

import os

from collections import Counter
from pathlib import Path

from .models import ProjectSnapshot


DEFAULT_EXCLUDED_DIRS = frozenset({
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
})


def scan_project(project_path: Path) -> ProjectSnapshot:
    """
    Scan a project directory and collect structural information.

    The scanner does not modify files or execute project code.
    Symbolic links inside the project are ignored.
    """

    root = Path(project_path).expanduser()

    # Validate the provided path.
    if not root.exists():
        raise FileNotFoundError(
            f"Project directory does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"The provided path is not a directory: {root}"
        )

    root = root.resolve()

    files_count = 0
    directories_count = 0

    extension_counts = Counter()

    def raise_walk_error(error: OSError) -> None:
        raise error

    # Explore the directory tree.
    for current_root, dirnames, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=raise_walk_error
    ):

        current_path = Path(current_root)

        # Exclude unnecessary directories and symbolic links.
        dirnames[:] = [
            name
            for name in dirnames
            if name not in DEFAULT_EXCLUDED_DIRS
            and not (current_path / name).is_symlink()
        ]

        directories_count += len(dirnames)

        # Process files.
        for filename in filenames:

            file_path = current_path / filename

            # Ignore symbolic links.
            if file_path.is_symlink():
                continue

            files_count += 1

            extension = file_path.suffix.lower()

            if not extension:
                extension = "[no extension]"

            extension_counts[extension] += 1

    return ProjectSnapshot(
        root=root,
        files_count=files_count,
        directories_count=directories_count,
        extension_counts=dict(sorted(extension_counts.items()))
    )