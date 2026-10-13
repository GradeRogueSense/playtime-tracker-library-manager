"""Joined view model returned to the CLI and any future UI."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LibraryEntry:
    title: str
    store: str
    total_seconds: int
    last_played_at: datetime | None
    install_path: str | None
    tags: tuple[str, ...]