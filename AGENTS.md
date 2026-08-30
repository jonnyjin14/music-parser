# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Stack

- **Python 3.11** (pinned via `.python-version`)
- **Package manager**: `uv` (uses `uv_build` as the build backend; no `pip install` — use `uv` commands)
- **Dependencies**: Flask, pandas, numpy, requests (see `pyproject.toml`)
- **Test framework**: pytest (declared under `[dependency-groups.dev]` in `pyproject.toml`)

## Commands

```bash
# Install dependencies (includes dev group with pytest)
uv sync --group dev

# Run the CLI entry point
uv run music-parser

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_main.py

# Run a single test by name
uv run pytest tests/test_main.py::test_function_name
```

> There is no linter or formatter configured (no ruff/flake8/mypy config exists).

## Architecture

- **Entry point**: `music_parser:main` (defined in `pyproject.toml` `[project.scripts]`) resolves to `src/music_parser/__init__.py:main()`, **not** `main.py:main()`. The `__init__.py:main()` is currently a stub — intended to be wired to `helper.MusicParser` for real CLI behavior.
- `src/music_parser/main.py` is a standalone dev/debug script (hardcodes a local path `D:\Dell Files\Songs`) — it is **not** the installed entry point.
- Core logic lives in `src/music_parser/helper.py` — the `MusicParser` class.

## Key Conventions

- **Filename parsing**: `"Singer - Song"` format (split on first `"-"`); files without `"-"` get `singer = "Unknown"`.
- **Supported formats**: `.mp3` and `.wav` only (case-insensitive suffix check).
- **CSV output**: saved to `~/OneDrive/桌面/Output_file.csv` (Windows OneDrive Chinese desktop path) with `encoding='utf-8-sig'` (BOM for Excel compatibility).
- `scanLibrary()` must be called before `writeCsv()` — `self.df` is only set after scanning. Calling `writeCsv()` first raises `AttributeError`. No regression test exists for this — add one before shipping any CSV-related feature.

## Tests

- `tests/test_main.py` — smoke test: verifies `MusicParser` is importable.
- `tests/test_validation.py` — behavioral tests for path validation (FileNotFoundError, NotADirectoryError). This is the reproduction test for GitHub Issue #1.

## Skills

- **`github-issue-triage`** — installed globally at `~/.bob/skills/github-issue-triage/`. Fetches open GitHub issues, reproduces the chosen issue in the codebase, and posts a structured analysis comment via the GitHub REST API (PowerShell `Invoke-RestMethod`). Requires `GITHUB_TOKEN` env var for posting. Uses a supporting `fetch-issues.py` script (stdlib only, no extra deps). Invoke with `/github-issue-triage` or describe the task.
  - Note: `fetch-issues.py` is **not** in this workspace — it lives only in the global skill directory.
