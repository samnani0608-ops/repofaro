"""
Automated tests for the RepoFaro Project Scanner.
"""

import pytest

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