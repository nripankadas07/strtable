"""Core table formatting functionality."""
import csv
from io import StringIO
from typing import Literal

from .errors import StrTableError
from .styles import get_style, TableStyle


def _validate_padding(padding: int) -> None:
    """Validate padding value."""
    if padding < 0:
        raise StrTableError(f"padding must be non-negative, got {padding}")


def _validate_max_width(max_width: int | list[int] | None) -> None:
    """Validate max_width value(s)."""
    if max_width is None:
        return
    if isinstance(max_width, int):
        if max_width <= 0:
            raise StrTableError(f"max_width must be positive, got {max_width}")
    elif isinstance(max_width, list):
        for w in max_width:
            if w is not None and w <= 0:
                raise StrTableError(f"max_width values must be positive, got {w}")


def _validate_align(align: list[str] | None) -> None:
    """Validate alignment values."""
    if align is None:
        return
    for a in align:
        if a not in ("left", "right", "center"):
            raise StrTableError(f"Invalid alignment: {a!r}")


def _convert_cell(value: object) -> str:
    """Convert cell value to string."""
    if value is None:
        return "None"
    return str(value)


def _normalize_rows(
    rows: list[list], headers: list[str] | None
) -> tuple[list[list[str]], list[str]]:
    """Normalize rows and headers.

    - Convert all cells to strings
    - Pad rows to consistent column count
    - Return normalized rows and headers
    """
    if not rows and not headers:
        return [], []

    # Determine column count
    max_cols = 0
    if headers:
        max_cols = len(headers)
    if rows:
        max_cols = max(max_cols, max(len(row) for row in rows) if rows else 0)

    if max_cols == 0:
        return [], headers or []

    # Normalize headers
    normalized_headers = list(headers) if headers else []
    # Pad headers if needed
    while len(normalized_headers) < max_cols:
        normalized_headers.append("")

    # Normalize rows
    normalized_rows = []
    for row in rows:
        # Convert all cells to strings
        str_row = [_convert_cell(cell) for cell in row]
        # Pad row to max_cols
        while len(str_row) < max_cols:
            str_row.append("")
        # Truncate if longer
        str_row = str_row[:max_cols]
        normalized_rows.append(str_row)

    return normalized_rows, normalized_headers


def _get_column_widths(
    rows: list[list[str]],
    headers: list[str],
    padding: int,
    max_width: int | list[int] | None,
) -> list[int]:
    """Calculate column widths."""
    num_cols = len(headers)
    widths: list[int] = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                widths[i] = max(widths[i], len(cell))

    # Apply max_width
    if max_width is not None:
        if isinstance(max_width, int):
            widths = [min(w, max_width) for w in widths]
        else:
            # Per-column max_width
            for i in range(num_cols):
                if i < len(max_width) and max_width[i] is not None:
                    widths[i] = min(widths[i], max_width[i])

    # Add padding
    widths = [w + 2 * padding for w in widths]

    return widths


def _truncate_cell(value: str, max_width: int, padding: int) -> str:
    """Truncate cell value if needed."""
    available = max_width - 2 * padding
    if len(value) > available and available >= 3:
        return value[: available - 3] + "..."
    return value


def _align_cell(value: str, width: int, align: str) -> str:
    """Align cell value within given width."""
    if len(value) >= width:
        return value[: width] if width > 0 else ""

    pad_total = width - len(value)

    if align == "left":
        return value + " " * pad_total
    elif align == "right":
        return " " * pad_total + value
    elif align == "center":
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        return " " * pad_left + value + " " * pad_right
    else:
        # Default to left
        return value + " " * pad_total


def _get_align_list(
    align: list[str] | None, num_cols: int
) -> list[str]:
    """Get alignment list, filling defaults."""
    if not align:
        return ["left"] * num_cols

    result = list(align)
    while len(result) < num_cols:
        result.append("left")

    return result[:num_cols]


def _build_separator_line(
    widths: list[int],
    style: TableStyle,
    left_char: str,
    mid_char: str,
    right_char: str,
) -> str:
    """Build a horizontal separator line."""
    if not widths:
        return ""

    parts = [left_char]
    for i, w in enumerate(widths):
        parts.append(style.horizontal * w)
        if i < len(widths) - 1:
            parts.append(mid_char)
    parts.append(right_char)

    return "".join(parts)


def _build_data_line(
    cells: list[str],
    widths: list[int],
    style: TableStyle,
    align_list: list[str],
) -> str:
    """Build a data line with aligned cells."""
    parts = [style.vertical]
    for i, (cell, width) in enumerate(zip(cells, widths)):
        alignment = align_list[i] if i < len(align_list) else "left"
        aligned = _align_cell(cell, width, alignment)
        parts.append(aligned)
        parts.append(style.vertical)

    return "".join(parts)


def format_table(
    rows: list[list],
    headers: list[str] | None = None,
    border: Literal["ascii", "unicode", "markdown", "none"] = "ascii",
    align: list[str] | None = None,
    padding: int = 1,
    max_width: int | list[int] | None = None,
    truncate: bool = True,
) -> str:
    """Format tabular data as aligned ASCII/Unicode table.

    Args:
        rows: List of row lists (each row is a list of cell values)
        headers: Optional list of header strings
        border: Border style - "ascii", "unicode", "markdown", or "none"
        align: Per-column alignment - "left", "right", "center"
        padding: Cell padding (default 1)
        max_width: Max width for cells (per-column list or global int)
        truncate: Whether to truncate long values with "..."

    Returns:
        Formatted table as string

    Raises:
        StrTableError: On invalid parameters
    """
    # Validate inputs
    _validate_padding(padding)
    _validate_max_width(max_width)
    _validate_align(align)

    style = get_style(border)

    # Normalize rows and headers
    norm_rows, norm_headers = _normalize_rows(rows, headers)

    # Handle empty case
    if not norm_headers and not norm_rows:
        return ""

    # Ensure we have headers even if empty
    if not norm_headers and norm_rows:
        norm_headers = [""] * len(norm_rows[0])

    # Get column widths
    widths = _get_column_widths(norm_rows, norm_headers, padding, max_width)

    # Get alignment list
    align_list = _get_align_list(align, len(norm_headers))

    # Build table
    lines = []

    # Top border
    if border != "none":
        lines.append(
            _build_separator_line(
                widths,
                style,
                style.top_left,
                style.top_t,
                style.top_right,
            )
        )

    # Headers
    if norm_headers:
        header_cells = []
        for i, h in enumerate(norm_headers):
            if truncate:
                h = _truncate_cell(h, widths[i], padding)
            header_cells.append(h)
        lines.append(_build_data_line(header_cells, widths, style, align_list))

        # Header separator
        if border != "none":
            lines.append(
                _build_separator_line(
                    widths,
                    style,
                    style.left_t,
                    style.cross,
                    style.right_t,
                )
            )

    # Data rows
    for row in norm_rows:
        row_cells = []
        for i, cell in enumerate(row):
            if truncate:
                cell = _truncate_cell(cell, widths[i], padding)
            row_cells.append(cell)
        lines.append(_build_data_line(row_cells, widths, style, align_list))

    # Bottom border
    if border != "none" and (norm_rows or norm_headers):
        lines.append(
            _build_separator_line(
                widths,
                style,
                style.bottom_left,
                style.bottom_t,
                style.bottom_right,
            )
        )

    return "\n".join(lines)


def format_csv(
    csv_text: str,
    border: Literal["ascii", "unicode", "markdown", "none"] = "ascii",
    align: list[str] | None = None,
    padding: int = 1,
    max_width: int | list[int] | None = None,
    truncate: bool = True,
) -> str:
    """Parse CSV string and format as table.

    Args:
        csv_text: CSV text (string)
        border: Border style
        align: Per-column alignment
        padding: Cell padding
        max_width: Max width for cells
        truncate: Whether to truncate long values

    Returns:
        Formatted table as string

    Raises:
        StrTableError: On invalid parameters
    """
    if not csv_text:
        return ""

    # Parse CSV
    reader = csv.reader(StringIO(csv_text))
    rows_list = list(reader)

    if not rows_list:
        return ""

    # First row is headers
    headers = rows_list[0] if rows_list else []
    data_rows = rows_list[1:] if len(rows_list) > 1 else []

    return format_table(
        data_rows,
        headers=headers,
        border=border,
        align=align,
        padding=padding,
        max_width=max_width,
        truncate=truncate,
    )
