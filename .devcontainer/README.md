# Development Container

This devcontainer provides a consistent development environment for the Flight Price Tracker project.

## Features

### Package Management
- **UV Package Manager**: Modern, fast Python package manager with lock file support
- Configured for reproducible builds with `uv.lock`
- Automatic dependency installation on container creation

### Development Tools
- **Python 3.12**: Latest stable Python version
- **Jupyter**: Full Jupyter notebook support with integrated kernel
  - `jupyter` - Core Jupyter functionality
  - `ipykernel` - Python kernel for Jupyter
  - `notebook` - Classic notebook interface
- **Ruff**: Fast Python linter and formatter
  - Configured for code quality checks
  - Auto-fix capabilities for common issues
  - Import sorting and code style enforcement

### IDE Integration
- **VS Code Extensions**:
  - Python language support (ms-python.python)
  - Pylance for type checking
  - Ruff linting integration
  - TOML file support
  - **GitHub Copilot** - AI-powered code completion
  - **GitHub Copilot Chat** - AI assistant for coding
  - Jupyter notebook support with renderers and keymaps

### Environment Configuration
- Virtual environment at `.venv/` (persisted via Docker volume)
- UV cache optimization for faster builds
- Python configured for unbuffered output and no bytecode compilation

## Usage

### Starting the Container

1. Open the project in VS Code
2. Press `F1` and select "Dev Containers: Reopen in Container"
3. Wait for the container to build and dependencies to install

### Running Code

The virtual environment is automatically activated. You can run Python files directly:

```bash
python plane_tickets.py
python visualize.py
```

### Using Jupyter

Open or create `.ipynb` files in VS Code. The Jupyter kernel will automatically use the project's virtual environment.

### Linting with Ruff

Check code quality:
```bash
ruff check *.py
```

Auto-fix issues:
```bash
ruff check *.py --fix
```

Format code:
```bash
ruff format *.py
```

### Managing Dependencies

Add a new dependency:
```bash
uv add package-name
```

Add a dev dependency:
```bash
uv add --dev package-name
```

Sync dependencies after manual `pyproject.toml` edits:
```bash
uv sync --dev
```

## Configuration Files

- `.devcontainer/devcontainer.json` - Container configuration
- `pyproject.toml` - Project metadata, dependencies, and tool configuration
- `uv.lock` - Locked dependency versions for reproducible builds
