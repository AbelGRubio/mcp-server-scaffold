# Define the expected virtual environment path
VENV_DIR := .venv
ENV_SCRIPT := activate_env.sh

.DEFAULT_GOAL := default

# Declare phony targets to avoid conflicts with files
.PHONY: check-venv qa build update all qa

default: qa

rst:
	@echo "Running rst documentation.."
	uv run sphinx-apidoc -f -e -o docs/source/ src/
	@echo "✅ Correct rst execution"

docs1:
	@echo "Running creating documentation.."
	PYTHONPATH=src uv run sphinx-build docs/source docs/build/html
	@echo "✅ Correct docs execution"

semantic-release: check-venv
	@echo "🔍 Running semantic-release..."
	uv run semantic-release version
	@echo "✅ Correct semantic-release execution"

publish: check-venv
	@echo "🔍 Running semantic-release publish..."
	uv run semantic-release publish
	@echo "✅ Correct semantic-release publish execution"


pre-commit: check-venv
	uv run pre-commit run --all-files
	@echo "✅ Correct pre-commit execution"


venv:
	@echo "Environment activation..."
	@bash -c "source .venv/bin/activate && exec bash"
	@echo "✅ Correct virtual environment is active: .venv"

# Check if the correct virtual environment is active
check-venv: check-uv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "❌ No virtual environment is active. Please activate the virtual environment by running 'source ./setup.sh'."; \
		exit 1; \
	fi
	@if [ "$$VIRTUAL_ENV" != "$(PWD)/$(VENV_DIR)" ]; then \
		echo "❌ Wrong virtual environment is active ($$VIRTUAL_ENV). Expected $(PWD)/$(VENV_DIR). Please deactivate the current one with 'deactivate' and run 'source ./setup.sh'."; \
		exit 1; \
	fi

	@uv lock --locked

	@echo "✅ Correct virtual environment is active: $$VIRTUAL_ENV"

# Run quality assurance checks
qa: check-venv
	@echo "🔍 Running quality assurance checks..."
	@git add . || { echo "❌ Failed to stage changes."; exit 1; }
	@pre-commit run --all-files || { echo "❌ Quality assurance checks failed."; exit 1; }
	@echo "✅ Quality assurance checks complete!"

# Build the package
build: check-venv
	@echo "🔨 Building the project..."
	@uv build || { echo "❌ Build failed."; exit 1; }
	@echo "✅ Build complete!"


# Update dependencies and pre-commit hooks
update: check-venv
	@echo "🔄 Updating dependencies and pre-commit hooks..."
	@uv lock --upgrade || { echo "❌ Failed to upgrade uv lock."; exit 1; }
	@uv sync --extra optional  || { echo "❌ Failed to sync uv."; exit 1; }
	@pre-commit autoupdate || { echo "❌ Failed to update pre-commit hooks."; exit 1; }
	@echo "✅ Update complete!"

unused-packages:
	@echo "🔍 Detecting unused packages..."
	@deptry src

test:
	@echo "🔍 Running tests..."
	@pytest -v --tb=short --disable-warnings --maxfail=1 || { echo "❌ Tests failed."; exit 1; }
	@echo "✅ All tests passed!"


check-uv:
	@command -v uv >/dev/null 2>&1 && { \
		echo "✅ uv is already installed: $$(uv --version)"; \
	} || { \
		echo "⚠️  uv not found. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "✅ uv installed successfully."; \
	}

ci-setup:
	@export PATH="$$HOME/.local/bin:$$PATH" && \
	make check-uv && \
	uv sync


semantic-release-gitlab:
	@echo "Running semantic-release inside venv..."
	@. .venv/bin/activate && semantic-release version


publish-gitlab:
	@echo "Running publish inside venv..."
	@. .venv/bin/activate && python -m twine upload --repository-url ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi dist/*
