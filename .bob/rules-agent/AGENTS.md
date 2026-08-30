# Project Coding Rules (Non-Obvious Only)

- The installed CLI entry point (`music-parser`) calls `src/music_parser/__init__.py:main()`, which currently just prints a stub. Actual logic is in `main.py:main()` — these are **not** connected. When implementing real CLI behavior, wire `__init__.py:main()` to call `helper.MusicParser`.
- `self.df` is not initialized in `__init__` — accessing `writeCsv()` before `scanLibrary()` raises `AttributeError`. Guard or initialize `self.df = None` if adding error handling. **No regression test exists for this failure mode — add one before shipping any CSV-related feature.**
- CSV output path is hardcoded to a Windows OneDrive Chinese desktop path (`~/OneDrive/桌面/`). Any changes to output location must account for this.
- No linter, formatter, or type-checker is configured. Do not add type annotations expecting them to be enforced automatically.
- Use `uv run pytest` to run tests. The `.venv` is managed by `uv`; test dependencies (including `pytest`) live under `[dependency-groups.dev]` in `pyproject.toml`.
