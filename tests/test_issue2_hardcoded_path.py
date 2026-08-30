"""
Reproduction test for GitHub Issue #2:
writeCsv() has a hardcoded Windows-only OneDrive output path — not portable.
The fix: writeCsv() should accept an optional output_path parameter and default
to a portable location (e.g. Path.cwd() / "Output_file.csv").
"""
import pytest
from pathlib import Path
from music_parser.helper import MusicParser


def test_writeCsv_accepts_custom_output_path(tmp_path):
    """writeCsv() should accept an output_path argument so it is not hardcoded."""
    import inspect
    sig = inspect.signature(MusicParser.writeCsv)
    assert "output_path" in sig.parameters, (
        "writeCsv() must accept an 'output_path' parameter — "
        "hardcoded OneDrive path is not portable (Issue #2)"
    )


def test_writeCsv_writes_to_given_path(tmp_path):
    """writeCsv() should write the CSV to the path provided, not a hardcoded one."""
    # Build a tiny library in tmp_path
    (tmp_path / "Artist - Song.mp3").write_text("")
    parser = MusicParser(str(tmp_path))
    parser.scanLibrary()

    out_file = tmp_path / "output.csv"
    parser.writeCsv(output_path=out_file)       # <-- this call will fail before the fix

    assert out_file.exists(), "CSV was not written to the supplied output_path"
