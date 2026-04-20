"""Table styling and borders."""
from dataclasses import dataclass
from typing import Literal

from .errors import StrTableError


@dataclass(frozen=True)
class TableStyle:
    """Border style definition with corner, edge, and intersection characters."""

    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str
    cross: str
    top_t: str
    bottom_t: str
    left_t: str
    right_t: str


# ASCII style
ASCII_STYLE = TableStyle(
    top_left="+",
    top_right="+",
    bottom_left="+",
    bottom_right="+",
    horizontal="-",
    vertical="|",
    cross="+",
    top_t="+",
    bottom_t="+",
    left_t="+",
    right_t="+",
)

# Unicode box-drawing style
UNICODE_STYLE = TableStyle(
    top_left="┌",
    top_right="┐",
    bottom_left="└",
    bottom_right="┘",
    horizontal="─",
    vertical="│",
    cross="┼",
    top_t="┬",
    bottom_t="┴",
    left_t="├",
    right_t="┤",
)

# Markdown style (no top/bottom, left/right borders)
MARKDOWN_STYLE = TableStyle(
    top_left="",
    top_right="",
    bottom_left="",
    bottom_right="",
    horizontal="-",
    vertical="|",
    cross="",
    top_t="",
    bottom_t="",
    left_t="|",
    right_t="|",
)

# None style (no borders)
NONE_STYLE = TableStyle(
    top_left="",
    top_right="",
    bottom_left="",
    bottom_right="",
    horizontal="",
    vertical="",
    cross="",
    top_t="",
    bottom_t="",
    left_t="",
    right_t="",
)


def get_style(
    border: Literal["ascii", "unicode", "markdown", "none"],
) -> TableStyle:
    """Get TableStyle by name.

    Args:
        border: Style name ("ascii", "unicode", "markdown", "none")

    Returns:
        TableStyle instance

    Raises:
        StrTableError: If border style is invalid
    """
    styles = {
        "ascii": ASCII_STYLE,
        "unicode": UNICODE_STYLE,
        "markdown": MARKDOWN_STYLE,
        "none": NONE_STYLE,
    }
    if border not in styles:
        raise StrTableError(f"Invalid border style: {border!r}")
    return styles[border]
