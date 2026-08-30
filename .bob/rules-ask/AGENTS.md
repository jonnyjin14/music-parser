# Project Documentation Rules (Non-Obvious Only)

- `src/music_parser/main.py` looks like the main module but is actually a local dev script with a hardcoded path — it is NOT the installed entry point.
- The `[project.scripts]` entry `music-parser = "music_parser:main"` points to `__init__.py:main()`, which is a stub. The real scanning logic is only reachable by calling `helper.MusicParser` directly.
- `tests/test_main.py` currently contains only a `print` statement — there are no real test assertions yet.
