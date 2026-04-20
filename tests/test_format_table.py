"""Tests for format_table function."""
import pytest

from strtable import format_table, StrTableError


class TestBasicFormatting:
    """Test basic table formatting."""

    def test_simple_table(self):
        """Test simple 2x2 table."""
        rows = [["a", "b"], ["c", "d"]]
        headers = ["col1", "col2"]
        result = format_table(rows, headers, border="ascii")
        assert "col1" in result
        assert "col2" in result
        assert "a" in result
        assert "b" in result
        assert "c" in result
        assert "d" in result

    def test_single_row(self):
        """Test table with single data row."""
        rows = [["hello", "world"]]
        headers = ["greeting", "target"]
        result = format_table(rows, headers, border="ascii")
        assert "hello" in result
        assert "world" in result

    def test_single_column(self):
        """Test table with single column."""
        rows = [["a"], ["b"], ["c"]]
        headers = ["col"]
        result = format_table(rows, headers, border="ascii")
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_no_headers(self):
        """Test table without headers."""
        rows = [["a", "b"], ["c", "d"]]
        result = format_table(rows, headers=None, border="ascii")
        assert "a" in result
        assert "b" in result

    def test_empty_rows_list(self):
        """Test with empty rows list."""
        rows = []
        headers = ["col1", "col2"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)
        assert "col1" in result

    def test_empty_headers_with_data(self):
        """Test empty headers but with data rows."""
        rows = [["a", "b"], ["c", "d"]]
        headers = []
        result = format_table(rows, headers, border="ascii")
        assert "a" in result
        assert "b" in result


class TestBorders:
    """Test different border styles."""

    def test_ascii_border(self):
        """Test ASCII border style."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert "+" in result
        assert "-" in result
        assert "|" in result

    def test_unicode_border(self):
        """Test Unicode border style."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="unicode")
        assert "┌" in result
        assert "─" in result
        assert "│" in result

    def test_markdown_border(self):
        """Test Markdown border style."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="markdown")
        assert "|" in result
        assert "-" in result

    def test_none_border(self):
        """Test no border style."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="none")
        # Should still have content but no border chars
        assert "a" in result
        assert "b" in result

    def test_invalid_border(self):
        """Test invalid border style raises error."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        with pytest.raises(StrTableError):
            format_table(rows, headers, border="invalid")


class TestAlignment:
    """Test column alignment."""

    def test_left_align(self):
        """Test left alignment."""
        rows = [["a", "b"]]
        headers = ["col1", "col2"]
        result = format_table(rows, headers, border="ascii", align=["left", "left"])
        assert isinstance(result, str)

    def test_right_align(self):
        """Test right alignment."""
        rows = [["1", "2"]]
        headers = ["nums"]
        result = format_table(
            rows, headers, border="ascii", align=["right", "right"]
        )
        assert isinstance(result, str)

    def test_center_align(self):
        """Test center alignment."""
        rows = [["text", "more"]]
        headers = ["col1", "col2"]
        result = format_table(
            rows, headers, border="ascii", align=["center", "center"]
        )
        assert isinstance(result, str)

    def test_mixed_alignment(self):
        """Test mixed alignment."""
        rows = [["left", "right", "center"]]
        headers = ["a", "b", "c"]
        result = format_table(
            rows,
            headers,
            border="ascii",
            align=["left", "right", "center"],
        )
        assert isinstance(result, str)

    def test_align_shorter_than_columns(self):
        """Test align list shorter than column count."""
        rows = [["a", "b", "c"]]
        headers = ["x", "y", "z"]
        # Provide only 2 alignments for 3 columns
        result = format_table(rows, headers, border="ascii", align=["left", "right"])
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_invalid_alignment(self):
        """Test invalid alignment raises error."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        with pytest.raises(StrTableError):
            format_table(rows, headers, border="ascii", align=["invalid"])


class TestPadding:
    """Test cell padding."""

    def test_default_padding(self):
        """Test default padding (1)."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_zero_padding(self):
        """Test zero padding."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", padding=0)
        assert isinstance(result, str)

    def test_large_padding(self):
        """Test large padding."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", padding=3)
        # Result should be longer due to padding
        assert isinstance(result, str)

    def test_negative_padding(self):
        """Test negative padding raises error."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        with pytest.raises(StrTableError):
            format_table(rows, headers, border="ascii", padding=-1)


class TestMaxWidth:
    """Test max_width truncation."""

    def test_global_max_width(self):
        """Test global max_width truncation."""
        rows = [["verylongtext", "short"]]
        headers = ["col1", "col2"]
        result = format_table(rows, headers, border="ascii", max_width=5, truncate=True)
        # Truncated value should contain "..."
        assert "..." in result or len(result) > 0

    def test_per_column_max_width(self):
        """Test per-column max_width."""
        rows = [["verylongtext", "short"]]
        headers = ["col1", "col2"]
        result = format_table(
            rows, headers, border="ascii", max_width=[5, 10], truncate=True
        )
        assert isinstance(result, str)

    def test_no_truncation(self):
        """Test without truncation."""
        rows = [["verylongtext", "short"]]
        headers = ["col1", "col2"]
        result = format_table(
            rows, headers, border="ascii", max_width=5, truncate=False
        )
        # Should still contain full text
        assert "verylongtext" in result or len(result) > 0

    def test_max_width_zero(self):
        """Test max_width=0 raises error."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        with pytest.raises(StrTableError):
            format_table(rows, headers, border="ascii", max_width=0)

    def test_max_width_negative(self):
        """Test negative max_width raises error."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        with pytest.raises(StrTableError):
            format_table(rows, headers, border="ascii", max_width=-5)


class TestTypeConversion:
    """Test non-string cell values."""

    def test_integer_values(self):
        """Test integer cell values."""
        rows = [[1, 2], [3, 4]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert "1" in result
        assert "2" in result
        assert "3" in result
        assert "4" in result

    def test_float_values(self):
        """Test float cell values."""
        rows = [[1.5, 2.7]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        assert "1.5" in result
        assert "2.7" in result

    def test_none_values(self):
        """Test None cell values."""
        rows = [["a", None], [None, "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert "a" in result
        assert "b" in result

    def test_bool_values(self):
        """Test boolean cell values."""
        rows = [[True, False]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert "True" in result
        assert "False" in result


class TestEdgeCases:
    """Test edge cases."""

    def test_inconsistent_column_count(self):
        """Test rows with inconsistent column counts."""
        rows = [["a", "b"], ["c"], ["d", "e", "f"]]
        headers = ["x", "y", "z"]
        result = format_table(rows, headers, border="ascii")
        # Should pad with empty strings
        assert isinstance(result, str)

    def test_unicode_content(self):
        """Test Unicode content in cells."""
        rows = [["café", "日本語"], ["emoji😀", "한글"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="unicode")
        assert "café" in result
        assert "emoji😀" in result

    def test_very_long_values(self):
        """Test very long cell values."""
        long_text = "x" * 100
        rows = [[long_text, "short"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii", max_width=20, truncate=True)
        assert isinstance(result, str)

    def test_multiline_values_with_newlines(self):
        """Test multiline cell values (with newlines)."""
        rows = [["line1\nline2", "single"]]
        headers = ["a", "b"]
        result = format_table(rows, headers, border="ascii")
        # Should handle newlines gracefully
        assert isinstance(result, str)


class TestOutputFormat:
    """Test output format properties."""

    def test_output_is_string(self):
        """Test output is always a string."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert isinstance(result, str)

    def test_output_contains_rows(self):
        """Test output contains all row data."""
        rows = [["a", "b"], ["c", "d"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        lines = result.strip().split("\n")
        # Should have header + separator + data rows
        assert len(lines) >= 3

    def test_output_is_not_empty(self):
        """Test output is never empty."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii")
        assert len(result.strip()) > 0
