"""Tests for CSV formatting."""
import pytest

from strtable import format_csv, StrTableError


class TestFormatCSV:
    """Test format_csv function."""

    def test_simple_csv(self):
        """Test simple CSV formatting."""
        csv_text = "name,age\nAlice,30\nBob,25"
        result = format_csv(csv_text, border="ascii")
        assert "name" in result
        assert "age" in result
        assert "Alice" in result
        assert "Bob" in result

    def test_csv_with_commas_in_quotes(self):
        """Test CSV with quoted fields containing commas."""
        csv_text = 'title,value\n"hello, world",100\n"test",200'
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_with_quotes(self):
        """Test CSV with quoted fields."""
        csv_text = 'col1,"col2"\n"value1","value2"'
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_empty_string(self):
        """Test empty CSV string."""
        csv_text = ""
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_single_line(self):
        """Test CSV with only headers."""
        csv_text = "a,b,c"
        result = format_csv(csv_text, border="ascii")
        assert "a" in result

    def test_csv_with_border_ascii(self):
        """Test CSV formatting with ASCII border."""
        csv_text = "x,y\n1,2"
        result = format_csv(csv_text, border="ascii")
        assert "+" in result
        assert "-" in result

    def test_csv_with_border_unicode(self):
        """Test CSV formatting with Unicode border."""
        csv_text = "x,y\n1,2"
        result = format_csv(csv_text, border="unicode")
        assert "┌" in result or "│" in result

    def test_csv_with_padding(self):
        """Test CSV formatting with custom padding."""
        csv_text = "a,b\n1,2"
        result = format_csv(csv_text, border="ascii", padding=2)
        assert isinstance(result, str)

    def test_csv_with_alignment(self):
        """Test CSV formatting with alignment."""
        csv_text = "name,value\ntest,123"
        result = format_csv(csv_text, border="ascii", align=["left", "right"])
        assert isinstance(result, str)

    def test_csv_with_max_width(self):
        """Test CSV formatting with max_width."""
        csv_text = "verylongtext,short\nvalue,x"
        result = format_csv(csv_text, border="ascii", max_width=5, truncate=True)
        assert isinstance(result, str)

    def test_csv_with_newlines_in_data(self):
        """Test CSV with newlines in data."""
        csv_text = "col1,col2\nline1\nline2,value"
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_multiline_quoted_field(self):
        """Test CSV with multiline quoted fields."""
        csv_text = 'name,description\n"Alice","Line 1\nLine 2"'
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_trailing_comma(self):
        """Test CSV with trailing comma."""
        csv_text = "a,b,\n1,2,"
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_inconsistent_columns(self):
        """Test CSV with inconsistent column counts."""
        csv_text = "a,b,c\n1,2\n3,4,5,6"
        result = format_csv(csv_text, border="ascii")
        assert isinstance(result, str)

    def test_csv_invalid_border(self):
        """Test CSV with invalid border style."""
        csv_text = "a,b\n1,2"
        with pytest.raises(StrTableError):
            format_csv(csv_text, border="invalid")
