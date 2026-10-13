"""Deterministic slug used as the natural key for a title."""
from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = _NON_ALNUM.sub("-", ascii_value.lower()).strip("-")
    return slug or "unnamed"