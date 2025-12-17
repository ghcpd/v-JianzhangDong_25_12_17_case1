Dependency installation notes

- Creating a clean virtual environment at .venv/ was attempted and .venv/ was recreated.
- Installing requirements from requirements.txt failed for pydantic-core (a build-time dependency of pydantic) on this Python/OS configuration because Rust/Cargo was not available.

Suggested fixes:
- Install Rust and Cargo (https://rustup.rs/) so pydantic-core can build, or
- Use a Python version with pre-built wheels for pydantic-core (e.g., CPython 3.11/3.12) or
- Pin to package versions that provide binary wheels for your platform.

Logs: see logs/venv_install.log for the full pip output.
