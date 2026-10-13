"""Windows-path normalization so executable matching survives casing quirks."""
from __future__ import annotations

import os


def normalize_exe(path: str) -> str:
    if not path:
        return ""
    return os.path.normcase(os.path.normpath(path))