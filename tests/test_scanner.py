"""
Automated tests for the RepoFaro Project Scanner.
"""

import pytest
import os

from repofaro.scanner import scan_project


def test_scan_counts_files_and_directories(tmp_path):
    """Verify that files and directories are counted correctly."""

    # Create a temporary project.
    (tmp_path / "src" / "utils").mkdir(parents=True)
    (tmp_path / "tests").mkdir()

    # Create sample files.
    (tmp_path / "src" / "main.py").write_text("print('Hello')")
    (tmp_path / "src" / "utils" / "helpers.py").write_text("# Helpers")
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / "LICENSE").write_text("MIT License")

    snapshot = scan_project(tmp_path)

    assert snapshot.files_count == 4
    assert snapshot.directories_count == 3

    assert snapshot.extension_counts == {
        ".md": 1,
        ".py": 2,
        "[no extension]": 1
    }


def test_scan_excludes_unnecessary_directories(tmp_path):
    """Verify that excluded directories are not scanned."""

    (tmp_path / "src").mkdir()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".venv" / "lib").mkdir(parents=True)
    (tmp_path / "node_modules").mkdir()

    (tmp_path / "src" / "main.py").write_text("# Application")
    (tmp_path / ".git" / "config").write_text("git config")
    (tmp_path / ".venv" / "lib" / "dependency.py").write_text("# Dependency")

    snapshot = scan_project(tmp_path)

    assert snapshot.files_count == 1
    assert snapshot.directories_count == 1


def test_scan_empty_directory(tmp_path):
    """Verify that an empty project produces an empty snapshot."""

    snapshot = scan_project(tmp_path)

    assert snapshot.files_count == 0
    assert snapshot.directories_count == 0
    assert snapshot.extension_counts == {}


def test_scan_nonexistent_directory(tmp_path):
    """Verify that nonexistent directories raise an error."""

    invalid_path = tmp_path / "nonexistent"

    with pytest.raises(FileNotFoundError):
        scan_project(invalid_path)


def test_scan_file_instead_of_directory(tmp_path):
    """Verify that files cannot be scanned as project directories."""

    file_path = tmp_path / "example.txt"
    file_path.write_text("Hello")

    with pytest.raises(NotADirectoryError):
        scan_project(file_path)

def test_scan_ignores_symbolic_links(tmp_path):
    """Verify that symbolic links are not followed or counted."""

    real_dir = tmp_path / "real"
    real_dir.mkdir()

    real_file = real_dir / "inside.py"
    real_file.write_text("# Real file")

    root_file = tmp_path / "main.py"
    root_file.write_text("# Main file")

    directory_link = tmp_path / "linked_dir"
    file_link = tmp_path / "linked_file.py"

    try:
        directory_link.symlink_to(
            real_dir,
            target_is_directory=True
        )

        file_link.symlink_to(root_file)

    except (OSError, NotImplementedError) as error:
        pytest.skip(f"Symbolic links unavailable: {error}")

    snapshot = scan_project(tmp_path)

    assert snapshot.files_count == 2
    assert snapshot.directories_count == 1

    assert snapshot.extension_counts == {
        ".py": 2
    }

@pytest.mark.skipif(
    os.name != "posix"
    or not hasattr(os, "geteuid")
    or os.geteuid() == 0,
    reason="Permission test requires a non-root POSIX user."
)
def test_scan_raises_error_for_unreadable_directory(tmp_path):
    """Verify that inaccessible directories raise PermissionError."""

    restricted_dir = tmp_path / "restricted"
    restricted_dir.mkdir()

    (restricted_dir / "secret.txt").write_text(
        "Restricted content"
    )

    restricted_dir.chmod(0)

    try:
        with pytest.raises(PermissionError):
            scan_project(tmp_path)

    finally:
        restricted_dir.chmod(0o700)