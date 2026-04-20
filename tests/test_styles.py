"""Tests for styles module."""
import pytest

from strtable.styles import (
    get_style,
    ASCII_STYLE,
    UNICODE_STYLE,
    MARKDOWN_STYLE,
    NONE_STYLE,
    TableStyle,
)
from strtable import StrTableError


class TestTableStyle:
    """Test TableStyle dataclass."""

    def test_ascii_style_characters(self):
        """Test ASCII style has correct characters."""
        assert ASCII_STYLE.horizontal == "-"
        assert ASCII_STYLE.vertical == "|"
        assert ASCII_STYLE.cross == "+"

    def test_unicode_style_characters(self):
        """Test Unicode style has correct characters."""
        assert UNICODE_STYLE.horizontal == "─"
        assert UNICODE_STYLE.vertical == "│"
        assert UNICODE_STYLE.cross == "┼"

    def test_markdown_style_characters(self):
        """Test Markdown style has correct characters."""
        assert MARKDOWN_STYLE.vertical == "|"
        assert MARKDOWN_STYLE.horizontal == "-"

    def test_none_style_empty(self):
        """Test None style has empty characters."""
        assert NONE_STYLE.horizontal == ""
        assert NONE_STYLE.vertical == ""
        assert NONE_STYLE.cross == ""

    def test_table_style_is_frozen(self):
        """Test TableStyle is immutable."""
        with pytest.raises(AttributeError):
            ASCII_STYLE.horizontal = "="

    def test_style_has_all_chars(self):
        """Test all styles have all required characters."""
        for style in [ASCII_STYLE, UNICODE_STYLE, MARKDOWN_STYLE, NONE_STYLE]:
            assert hasattr(style, "top_left")
            assert hasattr(style, "top_right")
            assert hasattr(style, "bottom_left")
            assert hasattr(style, "bottom_right")
            assert hasattr(style, "horizontal")
            assert hasattr(style, "vertical")
            assert hasattr(style, "cross")


class TestGetStyle:
    """Test get_style function."""

    def test_get_ascii_style(self):
        """Test get_style returns ASCII style."""
        style = get_style("ascii")
        assert style == ASCII_STYLE
        assert style.horizontal == "-"

    def test_get_unicode_style(self):
        """Test get_style returns Unicode style."""
        style = get_style("unicode")
        assert style == UNICODE_STYLE
        assert style.horizontal == "─"

    def test_get_markdown_style(self):
        """Test get_style returns Markdown style."""
        style = get_style("markdown")
        assert style == MARKDOWN_STYLE

    def test_get_none_style(self):
        """Test get_style returns None style."""
        style = get_style("none")
        assert style == NONE_STYLE

    def test_invalid_style_raises_error(self):
        """Test invalid style name raises StrTableError."""
        with pytest.raises(StrTableError):
            get_style("invalid")

    def test_case_sensitive_style(self):
        """Test style names are case-sensitive."""
        with pytest.raises(StrTableError):
            get_style("ASCII")

    def test_none_as_string_returns_style(self):
        """Test 'none' as string is valid."""
        style = get_style("none")
        assert style is NONE_STYLE
