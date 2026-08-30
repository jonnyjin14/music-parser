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
- **Supported formats**: `.mp3` only (case-insensitive suffix check). `.wav` support was intentionally disabled in `helper.py` for testing purposes.
- **CSV output**: saved to `~/OneDrive/桌面/Output_file.csv` (Windows OneDrive Chinese desktop path) with `encoding='utf-8-sig'` (BOM for Excel compatibility).
- `scanLibrary()` must be called before `writeCsv()` — `self.df` is only set after scanning. Calling `writeCsv()` first raises `AttributeError`. No regression test exists for this — add one before shipping any CSV-related feature.

## Tests

- `tests/test_main.py` — smoke test: verifies `MusicParser` is importable.
- `tests/test_validation.py` — behavioral tests for path validation (FileNotFoundError, NotADirectoryError). This is the reproduction test for GitHub Issue #1.

## Pipeline (Bob modes)

The project uses a four-stage bug-fix pipeline via Bob custom modes (`.bob/custom_modes.yaml`):

| Stage | Mode | Skill | Responsibility |
|---|---|---|---|
| 1 | Investigator | `github-issue-triage` | Reproduces bug, posts analysis comment, hands off evidence package |
| 2 | Developer | `developer` | Applies minimal patch, smoke-checks reproduction test |
| 3 | Tester | `tester` | Runs full test suite, issues VERIFIED / NOT_VERIFIED |
| 4 | Reviewer | `reviewer` | Reviews code, posts resolution comment, closes issue, asks about PR |

### GitHub token requirements

The pipeline makes GitHub API calls at two stages:
- **Investigator (Step 1):** checks `GITHUB_TOKEN` presence and validates `push` permission on the target repo. Sets `CAN_POST = true/false` for the rest of the session.
- **Reviewer (Step 5, APPROVE):** posts a `✅ Fix Reviewed and Approved` comment, then closes the issue via `PATCH /issues/:number`.

All API calls are guarded by `CAN_POST` and wrapped in `try/catch`. If the token is missing or lacks write access, comment text is shown for manual posting.

**Required token scopes:** `public_repo` (public repos) or `repo` (private repos).

## Skills

- **`github-issue-triage`** — installed globally at `~/.bob/skills/github-issue-triage/`. Fetches open GitHub issues, reproduces the chosen issue in the codebase, posts a structured analysis comment, and hands off a structured evidence package to the Developer. Requires `GITHUB_TOKEN` with write access for posting. Uses a supporting `fetch-issues.py` script (stdlib only, no extra deps). Invoke with `/github-issue-triage` or describe the task.
  - Note: `fetch-issues.py` is **not** in this workspace — it lives only in the global skill directory.
