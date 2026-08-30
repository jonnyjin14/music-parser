# Project Architecture Rules (Non-Obvious Only)

- There is an intentional disconnect between the CLI entry point (`__init__.py:main`) and the actual implementation (`main.py` → `helper.MusicParser`). Any feature work must decide which path to use and reconcile them.
- `MusicParser` is stateful — `scanLibrary()` mutates `self.df`; `writeCsv()` depends on it. Method call order is an implicit contract not enforced by the class.
- The project uses `uv_build` as build backend (not setuptools/hatchling). Packaging changes must target `uv_build` conventions.
- No test infrastructure beyond a placeholder file. Any testing plan must start from scratch (pytest is not listed as a dev dependency in `pyproject.toml` — add it under `[dependency-groups]` or `[project.optional-dependencies]`).
