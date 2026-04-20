"""strtable - Format tabular data as ASCII/Unicode tables."""

from .core import format_csv, format_table
from .errors import StrTableError
from .styles import TableStyle

__version__ = "0.1.0"
__all__ = [
    "format_table",
    "format_csv",
    "StrTableError",
    "TableStyle",
]
