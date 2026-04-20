"""Tests for edge cases and error conditions."""
import pytest

from strtable import format_table, StrTableError


class TestEmptyAndNullCases:
    """Test empty and null input cases."""

    def test_completely_empty_rows(self):
        """Test with empty rows list."""
        rows = []
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_empty_headers_empty_rows(self):
        """Test with both empty headers and rows."""
        rows = []
        headers = []
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_empty_string_cells(self):
        """Test with empty string cell values."""
        rows = [["", ""], ["", ""]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_none_in_cells(self):
        """Test None values are converted to string."""
        rows = [[None, None]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert "None" in result


class TestInconsistentColumns:
    """Test handling of inconsistent column counts."""

    def test_row_with_fewer_columns_than_headers(self):
        """Test row with fewer columns than headers."""
        rows = [["a"], ["b", "c"]]
        headers = ["x", "y", "z"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_row_with_more_columns_than_headers(self):
        """Test row with more columns than headers."""
        rows = [["a", "b", "c", "d"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_mixed_column_counts(self):
        """Test rows with varying column counts."""
        rows = [["a"], ["b", "c"], ["d", "e", "f"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_all_rows_empty_lists(self):
        """Test with all rows as empty lists."""
        rows = [[], [], []]
        headers = ["a"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)


class TestLongValues:
    """Test handling of long cell values."""

    def test_very_long_single_value(self):
        """Test very long value in single cell."""
        rows = [["x" * 1000]]
        headers = ["col"]
        result = format_table(rows, headers, border="ascii", max_width=50, truncate=True)
        assert isinstance(result, str)

    def test_long_header(self):
        """Test very long header."""
        headers = ["a" * 100]
        rows = [["short"]]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_multiple_long_columns(self):
        """Test multiple long column values."""
        rows = [["x" * 100, "y" * 100, "z" * 100]]
        headers = ["a", "b", "c"]
        result = format_table(
            rows, headers, border="ascii", max_width=20, truncate=True
        )
        assert isinstance(result, str)


class TestUnicodeHandling:
    """Test Unicode and special characters."""

    def test_emoji_in_cells(self):
        """Test emoji in cell values."""
        rows = [["😀", "😁"], ["😂", "😃"]]
        headers = ["smile", "laugh"]
        result = format_table(rows, headers, border="unicode")
        assert "😀" in result

    def test_cjk_characters(self):
        """Test CJK characters."""
        rows = [["日本語", "中文"], ["한글", "漢字"]]
        headers = ["japanese", "chinese"]
        result = format_table(rows, headers, border="unicode")
        assert "日本語" in result

    def test_mixed_scripts(self):
        """Test mixed scripts in same table."""
        rows = [["English", "中文"], ["العربية", "Ελληνικά"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="unicode")
        assert isinstance(result, str)

    def test_special_unicode_chars(self):
        """Test special Unicode characters."""
        rows = [["←", "→"], ["↑", "↓"]]
        headers = ["arrows"]
        result = format_table(rows, headers, border="unicode")
        assert isinstance(result, str)


class TestNewlinesAndSpecialChars:
    """Test multiline and special characters in cells."""

    def test_newlines_in_cells(self):
        """Test newline characters in cell values."""
        rows = [["line1\nline2", "single"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_tabs_in_cells(self):
        """Test tab characters in cell values."""
        rows = [["col1\tcol2", "value"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_multiple_newlines(self):
        """Test multiple consecutive newlines."""
        rows = [["a\n\n\nb", "c"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)


class TestTypeConversionEdges:
    """Test type conversion edge cases."""

    def test_float_with_many_decimals(self):
        """Test float with many decimal places."""
        rows = [[3.141592653589793, 2.718281828]]
        headers = ["pi", "e"]
        result = format_table(rows, headers, border="ascii")
        assert "3.14" in result or "3.1" in result

    def test_zero_values(self):
        """Test zero integer and float values."""
        rows = [[0, 0.0]]
        headers = ["int", "float"]
        result = format_table(rows, headers, border="ascii")
        assert "0" in result

    def test_negative_numbers(self):
        """Test negative number values."""
        rows = [[-1, -99.5]]
        headers = ["int", "float"]
        result = format_table(rows, headers, border="ascii")
        assert "-1" in result
        assert "-99" in result

    def test_bool_true_false(self):
        """Test boolean True and False values."""
        rows = [[True, False]]
        headers = ["t", "f"]
        result = format_table(rows, headers, border="ascii")
        assert "True" in result
        assert "False" in result


class TestValidationErrors:
    """Test validation and error cases."""

    def test_negative_padding_raises(self):
        """Test negative padding raises StrTableError."""
        with pytest.raises(StrTableError):
            format_table([["a"]], ["x"], padding=-1)

    def test_zero_max_width_raises(self):
        """Test zero max_width raises StrTableError."""
        with pytest.raises(StrTableError):
            format_table([["a"]], ["x"], max_width=0)

    def test_negative_max_width_raises(self):
        """Test negative max_width raises StrTableError."""
        with pytest.raises(StrTableError):
            format_table([["a"]], ["x"], max_width=-5)

    def test_invalid_align_value_raises(self):
        """Test invalid alignment value raises StrTableError."""
        with pytest.raises(StrTableError):
            format_table([["a", "b"]], ["x", "y"], align=["invalid"])

    def test_invalid_border_style_raises(self):
        """Test invalid border style raises StrTableError."""
        with pytest.raises(StrTableError):
            format_table([["a"]], ["x"], border="badstyle")


class TestEdgeSizeCombo:
    """Test edge case combinations."""

    def test_single_cell_table(self):
        """Test table with single cell."""
        rows = [["value"]]
        headers = ["header"]
        result = format_table(rows, headers, border="ascii")
        assert "value" in result
        assert "header" in result

    def test_single_row_many_columns(self):
        """Test single row with many columns."""
        rows = [list(range(20))]
        headers = [f"col{i}" for i in range(20)]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_many_rows_single_column(self):
        """Test many rows with single column."""
        rows = [[f"row{i}"] for i in range(50)]
        headers = ["value"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_wide_and_tall_table(self):
        """Test large table (wide and tall)."""
        rows = [[f"r{i}c{j}" for j in range(10)] for i in range(10)]
        headers = [f"col{i}" for i in range(10)]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)
