# Project Architecture Rules (Non-Obvious Only)

- There is an intentional disconnect between the CLI entry point (`__init__.py:main`) and the actual implementation (`main.py` → `helper.MusicParser`). Any feature work must decide which path to use and reconcile them. The intended fix is to wire `__init__.py:main()` to call `helper.MusicParser`.
- `MusicParser` is stateful — `scanLibrary()` mutates `self.df`; `writeCsv()` depends on it. Method call order is an implicit contract not enforced by the class.
- The project uses `uv_build` as build backend (not setuptools/hatchling). Packaging changes must target `uv_build` conventions.
- Test dependencies (pytest) are declared under `[dependency-groups.dev]` in `pyproject.toml`. Run `uv run pytest` to execute the suite. The `[tool.pytest.ini_options]` section sets `pythonpath = ["src"]` so `music_parser` imports resolve correctly.
