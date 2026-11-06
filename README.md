# RepoFaro 🧭

**A Local Project Structure & Quality Auditor**

RepoFaro is an open-source developer tool designed to inspect software project structures, identify organizational issues, and provide useful insights about project maintainability.

Its goal is to help independent developers understand how their projects are organized and identify opportunities for improvement.

## 🎯 Project Goals

- Inspect software project structures.
- Identify files and directories.
- Detect project technologies.
- Evaluate projects through configurable rules.
- Identify organizational issues.
- Generate understandable audit reports.

## ✨ Current Features

- [x] Recursive directory scanning.
- [x] File and directory counting.
- [x] File extension identification and distribution.
- [x] Configurable directory exclusions.
- [x] Symbolic link handling.
- [x] Filesystem error handling.
- [x] Command-line interface.
- [x] Automated tests with Pytest.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pytest | Automated testing |
| SQLite | Planned data persistence |
| Git | Version control |
| GitHub | Project hosting and collaboration |
| GTK4 / libadwaita | Planned graphical interface |

## 💻 Installation

### Requirements

- Linux (initial development platform).
- Python 3.10 or newer.
- Git.

### Clone the repository

```bash
git clone https://github.com/samnani0608-ops/repofaro.git
cd repofaro
```

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install RepoFaro

```bash
python -m pip install -e ".[dev]"
```

## 🚀 Usage

Analyze the current directory:

```bash
repofaro scan .
```

Analyze a specific project:

```bash
repofaro scan /path/to/project
```

Display available commands:

```bash
repofaro --help
```

Display the current version:

```bash
repofaro --version
```

## 🧪 Testing

RepoFaro uses Pytest for automated testing.

Run the test suite:

```bash
python -m pytest -v
```

Tests cover scanner functionality, CLI behavior, filesystem errors, directory exclusions and symbolic links.

## 🏗️ Project Architecture

RepoFaro follows a modular architecture based on Python's `src` layout.

Its main components are:

- **CLI:** Handles user commands and application interaction.
- **Project Scanner:** Inspects filesystem structures.
- **Project Detector:** Planned technology detection component.
- **Rule Engine:** Planned evaluation system.
- **Reporters:** Planned reporting components.

For additional technical information, see:

- `docs/ARCHITECTURE.md`
- `docs/REQUIREMENTS.md`

## 🗺️ Roadmap

- [x] Initial project structure.
- [x] Python CLI implementation.
- [x] Project Scanner.
- [x] Initial automated testing.
- [ ] Project Detector.
- [ ] Rule Engine.
- [ ] JSON report generation.
- [ ] SQLite audit history.
- [ ] HTML reports.
- [ ] GTK4 graphical interface.

## 🔒 Security and Privacy

RepoFaro is designed to operate locally.

Its initial scanning functionality is read-only: it does not intentionally modify project files or execute code from inspected projects.

## 📌 Project Status

**Version:** 0.1.0

**Development stage:** Early development.

RepoFaro is an independent software project built incrementally, with an emphasis on maintainability, modularity and software engineering practices.

## 📄 License

MIT License.