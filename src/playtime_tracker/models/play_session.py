"""A single tracked run of a game process."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PlaySession(BaseModel):
    id: int | None = None
    title_id: int
    started_at: datetime
    ended_at: datetime | None = None
    pid: int
    process_name: str

    @property
    def seconds(self) -> int:
        if self.ended_at is None:
            return 0
        return int((self.ended_at - self.started_at).total_seconds())