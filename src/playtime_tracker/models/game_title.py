"""Canonical game record — one row per unique title across all stores."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class GameTitle(BaseModel):
    id: int | None = None
    slug: str
    display_name: str
    store: str
    install_path: Path | None = None
    executable: Path | None = None
    steam_appid: int | None = None
    last_played_at: datetime | None = None
    total_seconds: int = 0
    tags: list[str] = Field(default_factory=list)

    @property
    def hours(self) -> float:
        return round(self.total_seconds / 3600, 2)