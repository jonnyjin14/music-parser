# Project Documentation Rules (Non-Obvious Only)

- `src/music_parser/main.py` looks like the main module but is actually a local dev script with a hardcoded path — it is NOT the installed entry point.
- The `[project.scripts]` entry `music-parser = "music_parser:main"` points to `__init__.py:main()`, which is a stub. **Intended architecture:** `__init__.py:main()` should be wired to call `helper.MusicParser` for real CLI behavior. The real scanning logic is currently only reachable by running `main.py` directly.
- `tests/test_main.py` contains a smoke test that only verifies `MusicParser` is importable. Real behavioral tests live in `tests/test_validation.py`.
