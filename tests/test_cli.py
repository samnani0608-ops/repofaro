"""
Automated tests for the RepoFaro CLI.
"""

from repofaro.cli import main


def test_scan_command_displays_report(tmp_path, capsys):
    """Verify that the CLI displays a successful scan report."""

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text(
        "print('Hello RepoFaro')",
        encoding="utf-8"
    )

    exit_code = main(["scan", str(tmp_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PROJECT SCANNER" in captured.out
    assert "Files: 1" in captured.out
    assert ".py" in captured.out
    assert captured.err == ""


def test_scan_command_handles_missing_directory(tmp_path, capsys):
    """Verify that the CLI handles nonexistent directories."""

    invalid_path = tmp_path / "missing"

    exit_code = main(["scan", str(invalid_path)])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Project directory does not exist" in captured.err
    assert captured.out == ""


def test_scan_command_handles_file_path(tmp_path, capsys):
    """Verify that the CLI rejects file paths."""

    file_path = tmp_path / "example.txt"
    file_path.write_text("Example", encoding="utf-8")

    exit_code = main(["scan", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "not a directory" in captured.err.lower()


def test_cli_displays_help_without_command(capsys):
    """Verify that the CLI displays help when no command is provided."""

    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "usage:" in captured.out.lower()
    assert "scan" in captured.out

def test_detect_command_displays_report(tmp_path, capsys):
    """Verify that the CLI displays technology detection results."""

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'example'\n",
        encoding="utf-8"
    )

    (tmp_path / "main.py").write_text(
        "print('Hello')",
        encoding="utf-8"
    )

    exit_code = main(["detect", str(tmp_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "TECHNOLOGY DETECTOR" in captured.out
    assert "Python" in captured.out
    assert "CONFIRMED" in captured.out
    assert "pyproject.toml" in captured.out
    assert captured.err == ""


def test_detect_command_handles_missing_directory(tmp_path, capsys):
    """Verify that the detect command handles invalid paths."""

    invalid_path = tmp_path / "missing"

    exit_code = main(["detect", str(invalid_path)])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Project directory does not exist" in captured.err
    assert captured.out == ""