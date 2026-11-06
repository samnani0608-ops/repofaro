"""
Automated tests for the RepoFaro Technology Detector.
"""

from repofaro.detector import detect_technologies
from repofaro.models import DetectionStatus
from repofaro.scanner import scan_project


def get_detection(profile, technology):
    """Retrieve a technology detection by name."""

    return next(
        detection
        for detection in profile.detections
        if detection.technology == technology
    )


def test_detect_python_project_with_manifest(tmp_path):
    """A Python manifest should confirm Python detection."""

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'example'\n",
        encoding="utf-8"
    )

    (tmp_path / "main.py").write_text(
        "print('Hello')",
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    python = get_detection(profile, "Python")

    assert python.status == DetectionStatus.CONFIRMED
    assert "pyproject.toml" in python.evidence


def test_detect_python_from_source_files_only(tmp_path):
    """Python source files without a manifest are possible evidence."""

    (tmp_path / "main.py").write_text(
        "print('Hello')",
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    python = get_detection(profile, "Python")

    assert python.status == DetectionStatus.POSSIBLE


def test_detect_node_project_with_package_json(tmp_path):
    """A package.json file should confirm Node.js detection."""

    (tmp_path / "package.json").write_text(
        '{"name": "example"}',
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    node = get_detection(profile, "Node.js")

    assert node.status == DetectionStatus.CONFIRMED
    assert "package.json" in node.evidence


def test_detect_node_from_source_files_only(tmp_path):
    """JavaScript files without a manifest are possible evidence."""

    (tmp_path / "app.js").write_text(
        "console.log('Hello')",
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    node = get_detection(profile, "Node.js")

    assert node.status == DetectionStatus.POSSIBLE


def test_detect_cpp_from_source_files(tmp_path):
    """C++ source files should confirm C/C++ detection."""

    (tmp_path / "main.cpp").write_text(
        "int main() { return 0; }",
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    cpp = get_detection(profile, "C/C++")

    assert cpp.status == DetectionStatus.CONFIRMED


def test_detect_cpp_from_build_file_only(tmp_path):
    """A CMake file alone should provide possible evidence."""

    (tmp_path / "CMakeLists.txt").write_text(
        "project(example)",
        encoding="utf-8"
    )

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    cpp = get_detection(profile, "C/C++")

    assert cpp.status == DetectionStatus.POSSIBLE


def test_empty_project_has_no_detected_technologies(tmp_path):
    """An empty project should have no technology indicators."""

    snapshot = scan_project(tmp_path)
    profile = detect_technologies(snapshot)

    for detection in profile.detections:
        assert detection.status == DetectionStatus.NOT_DETECTED
        assert detection.evidence == ()