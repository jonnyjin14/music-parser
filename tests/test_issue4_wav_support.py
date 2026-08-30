"""
Reproduction test for GitHub Issue #4:
MusicParser.scanLibrary() ignores .wav files — only .mp3 is supported.
The fix: restore .wav to the suffix check in helper.py.
"""
from pathlib import Path
from music_parser.helper import MusicParser


def test_wav_file_is_scanned(tmp_path):
    """scanLibrary() must include .wav files in the result DataFrame."""
    (tmp_path / "Artist - Song.wav").write_text("")
    parser = MusicParser(str(tmp_path))
    parser.scanLibrary()
    assert len(parser.df) == 1, (
        f"Expected 1 row for .wav file, got {len(parser.df)} (Issue #4)"
    )


def test_wav_and_mp3_both_scanned(tmp_path):
    """scanLibrary() must include both .mp3 and .wav files."""
    (tmp_path / "Artist - Song.wav").write_text("")
    (tmp_path / "Singer - Track.mp3").write_text("")
    parser = MusicParser(str(tmp_path))
    parser.scanLibrary()
    assert len(parser.df) == 2, (
        f"Expected 2 rows (.mp3 + .wav), got {len(parser.df)} (Issue #4)"
    )
