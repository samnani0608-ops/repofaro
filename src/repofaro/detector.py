"""
Project Technology Detector.

Identifies technologies using project files
and file extension information.
"""

from .models import (
    DetectionStatus,
    ProjectProfile,
    ProjectSnapshot,
    TechnologyDetection,
)


# Files that strongly indicate a Python project.
PYTHON_MANIFESTS = (
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
)

# Files that provide weaker Python evidence.
PYTHON_WEAK_FILES = (
    "requirements.txt",
)

# Files that strongly indicate a Node.js project.
NODE_MANIFESTS = (
    "package.json",
)

# Files that provide weaker Node.js evidence.
NODE_WEAK_FILES = (
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
)

JAVASCRIPT_EXTENSIONS = (
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
)

# C and C++ source files.
CPP_SOURCE_EXTENSIONS = (
    ".c",
    ".cpp",
    ".cc",
    ".cxx",
)

# Header files are weaker evidence.
CPP_HEADER_EXTENSIONS = (
    ".h",
    ".hpp",
    ".hh",
    ".hxx",
)

CPP_BUILD_FILES = (
    "CMakeLists.txt",
    "meson.build",
)


def find_root_files(root, filenames):
    """Find existing regular files in the project root."""

    found = []

    for filename in filenames:
        candidate = root / filename

        if not candidate.is_symlink() and candidate.is_file():
            found.append(filename)

    return tuple(found)


def get_extension_evidence(snapshot, extensions):
    """Collect evidence based on file extension counts."""

    evidence = []

    for extension in extensions:
        count = snapshot.extension_counts.get(extension, 0)

        if count > 0:
            evidence.append(f"{extension} files ({count})")

    return tuple(evidence)


def build_detection(technology, strong_evidence, weak_evidence):
    """Determine a technology's detection status."""

    evidence = tuple(
        dict.fromkeys((*strong_evidence, *weak_evidence))
    )

    if strong_evidence:
        status = DetectionStatus.CONFIRMED

    elif weak_evidence:
        status = DetectionStatus.POSSIBLE

    else:
        status = DetectionStatus.NOT_DETECTED

    return TechnologyDetection(
        technology=technology,
        status=status,
        evidence=evidence,
    )


def detect_technologies(snapshot: ProjectSnapshot) -> ProjectProfile:
    """
    Identify technologies using a project snapshot.

    The detector does not recursively scan directories.
    It uses the information collected by the Project Scanner
    and checks recognized marker files in the project root.
    """

    root = snapshot.root

    # Python detection.
    python_strong = find_root_files(
        root,
        PYTHON_MANIFESTS
    )

    python_weak = (
        *find_root_files(root, PYTHON_WEAK_FILES),
        *get_extension_evidence(
            snapshot,
            (".py",)
        ),
    )

    # Node.js detection.
    node_strong = find_root_files(
        root,
        NODE_MANIFESTS
    )

    node_weak = (
        *find_root_files(root, NODE_WEAK_FILES),
        *get_extension_evidence(
            snapshot,
            JAVASCRIPT_EXTENSIONS
        ),
    )

    # C/C++ detection.
    cpp_strong = get_extension_evidence(
        snapshot,
        CPP_SOURCE_EXTENSIONS
    )

    cpp_weak = (
        *get_extension_evidence(
            snapshot,
            CPP_HEADER_EXTENSIONS
        ),
        *find_root_files(
            root,
            CPP_BUILD_FILES
        ),
    )

    detections = (
        build_detection(
            "Python",
            python_strong,
            python_weak,
        ),
        build_detection(
            "Node.js",
            node_strong,
            node_weak,
        ),
        build_detection(
            "C/C++",
            cpp_strong,
            cpp_weak,
        ),
    )

    return ProjectProfile(
        root=root,
        detections=detections,
    )