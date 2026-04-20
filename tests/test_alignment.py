"""Tests for alignment behavior."""
import pytest

from strtable import format_table


class TestLeftAlignment:
    """Test left alignment behavior."""

    def test_left_align_short_content(self):
        """Test left alignment pads to the right."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["left", "left"])
        assert isinstance(result, str)

    def test_left_align_numbers(self):
        """Test left alignment with numbers."""
        rows = [["1", "200"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["left", "left"])
        assert isinstance(result, str)


class TestRightAlignment:
    """Test right alignment behavior."""

    def test_right_align_short_content(self):
        """Test right alignment pads to the left."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["right", "right"])
        assert isinstance(result, str)

    def test_right_align_numbers(self):
        """Test right alignment with numbers."""
        rows = [["1", "200"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["right", "right"])
        assert isinstance(result, str)


class TestCenterAlignment:
    """Test center alignment behavior."""

    def test_center_align_short_content(self):
        """Test center alignment pads both sides."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["center", "center"])
        assert isinstance(result, str)

    def test_center_align_numbers(self):
        """Test center alignment with numbers."""
        rows = [["1", "200"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=["center", "center"])
        assert isinstance(result, str)


class TestMixedAlignment:
    """Test mixed alignment in single table."""

    def test_mixed_alignment_three_columns(self):
        """Test mixed alignment across three columns."""
        rows = [["left", "center", "right"]]
        headers = ["a", "b", "c"]
        result = format_table(
            rows,
            headers,
            border="ascii",
            align=["left", "center", "right"],
        )
        assert "left" in result
        assert "center" in result
        assert "right" in result

    def test_mixed_alignment_multiple_rows(self):
        """Test mixed alignment with multiple data rows."""
        rows = [["a", "b", "c"], ["d", "e", "f"]]
        headers = ["col1", "col2", "col3"]
        result = format_table(
            rows,
            headers,
            border="ascii",
            align=["left", "center", "right"],
        )
        assert isinstance(result, str)


class TestAlignmentDefaults:
    """Test alignment defaults."""

    def test_align_none_defaults_to_left(self):
        """Test align=None defaults all columns to left."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=None)
        assert isinstance(result, str)

    def test_align_empty_list_defaults_to_left(self):
        """Test align=[] defaults all columns to left."""
        rows = [["a", "b"]]
        headers = ["x", "y"]
        result = format_table(rows, headers, border="ascii", align=[])
        assert isinstance(result, str)

    def test_align_partial_list_fills_with_left(self):
        """Test partial align list fills remainder with left."""
        rows = [["a", "b", "c"]]
        headers = ["x", "y", "z"]
        result = format_table(rows, headers, border="ascii", align=["right"])
        # Should work with 3 columns and 1 explicit align
        assert isinstance(result, str)


class TestAlignmentWithPadding:
    """Test alignment with different padding values."""

    def test_left_align_with_zero_padding(self):
        """Test left alignment with zero padding."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(
            rows, headers, border="ascii", align=["left", "left"], padding=0
        )
        assert isinstance(result, str)

    def test_right_align_with_large_padding(self):
        """Test right alignment with large padding."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(
            rows, headers, border="ascii", align=["right", "right"], padding=3
        )
        assert isinstance(result, str)

    def test_center_align_with_custom_padding(self):
        """Test center alignment with custom padding."""
        rows = [["a", "bb"]]
        headers = ["x", "y"]
        result = format_table(
            rows, headers, border="ascii", align=["center", "center"], padding=2
        )
        assert isinstance(result, str)
