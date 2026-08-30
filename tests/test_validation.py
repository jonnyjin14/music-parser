"""
Reproduction test for GitHub Issue #1:
MusicParser does not validate that the input path exists or is a directory.
"""
import pytest
from pathlib import Path
from music_parser.helper import MusicParser


def test_nonexistent_path_raises():
    """MusicParser should raise FileNotFoundError for a path that does not exist."""
    with pytest.raises(FileNotFoundError):
        MusicParser("C:/nonexistent/path/that/does/not/exist")


def test_file_path_raises(tmp_path):
    """MusicParser should raise NotADirectoryError when given a file instead of a directory."""
    f = tmp_path / "not_a_dir.txt"
    f.write_text("hello")
    with pytest.raises(NotADirectoryError):
        MusicParser(str(f))
