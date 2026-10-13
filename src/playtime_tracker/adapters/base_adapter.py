"""Abstract base for store adapters."""
from __future__ import annotations

from abc import ABC, abstractmethod

from playtime_tracker.config.settings import StoreConfig
from playtime_tracker.models.game_title import GameTitle


class StoreAdapter(ABC):
    store_name: str = "unknown"

    def __init__(self, config: StoreConfig | None) -> None:
        self.config = config

    @abstractmethod
    async def discover(self) -> list[GameTitle]:
        """Return every title this store exposes. Must not raise on empty install."""