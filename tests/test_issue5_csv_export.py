"""
Reproduction test for GitHub Issue #5:
main() calls scanLibrary() but never calls writeCsv(), so no CSV is exported.
The fix: add parser.writeCsv() after parser.scanLibrary() in main.py.
"""
from unittest.mock import patch, MagicMock
import music_parser.main as main_module


def test_main_calls_write_csv():
    """main() must call writeCsv() after scanLibrary() — Issue #5."""
    mock_parser = MagicMock()

    with patch("music_parser.main.helper.MusicParser") as MockCls:
        MockCls.return_value = mock_parser
        main_module.main()

    mock_parser.scanLibrary.assert_called_once()
    mock_parser.writeCsv.assert_called_once()
