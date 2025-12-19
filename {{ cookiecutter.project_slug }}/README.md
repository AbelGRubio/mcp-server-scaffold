Autor: {{cookiecutter.project_author_name}}
Python: {{cookiecutter.python_version}}

# {{cookiecutter.application}} Quickstart Guide

## Description

This project template is designed for Python development using `uv` as the main environment and build manager. It includes:

- Python virtual environment (`.venv`)
- Code quality checks with `pre-commit`
- Documentation with Sphinx (`rst`)
- Unit testing with `pytest`
- Build and release automation using `uv` and `semantic-release`

The project is structured to be easily run, tested, and deployed via the provided `Makefile`.

---

## Prerequisites

Before starting, make sure you have:

- Python 3.10+ installed
- `pip` updated
- `make` installed
- `curl` (to install `uv` if not present)

---

## 1. Set up the virtual environment

Create and activate the virtual environment:

`bash python -m venv .venv source ./setup.sh   # Activates the environment and syncs dependencies `

> ⚠️ The Makefile will check that the correct virtual environment is active before running most commands.

---

## 2. Activate the virtual environment shell

Open a shell with `.venv` activated:

`bash make venv `

All commands run inside this shell will use the correct dependencies.

---

## 3. Run quality assurance (QA)

Run pre-commit hooks and check code quality:

`bash make qa `

This will:

- Run pre-commit hooks on all files
- Check linting and formatting

---

## 4. Build the project

To build the package:

`bash make build `

This will generate artifacts in the `dist/` folder.

---

## 5. Update dependencies

Update `uv` locks and pre-commit hooks:

`bash make update `

It will:

- Upgrade `uv` lockfile
- Sync the environment
- Update pre-commit hooks

---

## 6. Run tests

Execute unit tests:

`bash make test `

Features included:

- Verbose output (`-v`)
- Short tracebacks (`--tb=short`)
- Stops at the first failure (`--maxfail=1`)
- Suppresses warnings (`--disable-warnings`)

---

## 7. Generate documentation

Generate RST files:

`bash make rst `

Build HTML documentation:

`bash make docs1 `

---

## 8. Versioning and publishing

For semantic versioning:

`bash make semantic-release `

To publish the package (e.g., PyPI):

`bash make publish `

For GitLab CI pipelines:

`bash make semantic-release-gitlab make publish-gitlab `

---

## 9. Detect unused packages

`bash make unused-packages `

Uses `deptry` to detect dependencies in `src/` that are not used.

---

## Notes

- **UV**: The Makefile automatically installs `uv` if not detected.
- **Virtual environment**: Always activate `.venv` before running commands.
- **Project structure**:
  - Source code → `src/`
  - Documentation → `docs/source/` → `docs/build/html/`
  - Distribution → `dist/`

