"""Merges per-store library data into a single queryable view."""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from playtime_tracker.adapters.steam_adapter import SteamAdapter
from playtime_tracker.adapters.epic_adapter import EpicAdapter
from playtime_tracker.adapters.gog_adapter import GogAdapter
from playtime_tracker.adapters.standalone_adapter import StandaloneAdapter
from playtime_tracker.config.settings import Settings
from playtime_tracker.models.library_entry import LibraryEntry
from playtime_tracker.repositories.title_repository import TitleRepository

log = logging.getLogger(__name__)


class LibraryService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._titles = TitleRepository(settings.db_path)
        self._adapters = [
            SteamAdapter(settings.stores.get("steam")),
            EpicAdapter(settings.stores.get("epic")),
            GogAdapter(settings.stores.get("gog")),
            StandaloneAdapter(settings.stores.get("standalone")),
        ]

    async def rescan_all(self) -> int:
        imported = 0
        for adapter in self._adapters:
            try:
                titles = await adapter.discover()
            except Exception:  # noqa: BLE001 — one broken store must not break the scan
                log.exception("adapter %s failed", adapter.store_name)
                continue
            for title in titles:
                self._titles.upsert(title)
                imported += 1
        return imported

    async def iter_library(self, *, min_minutes: int = 0) -> AsyncIterator[LibraryEntry]:
        threshold = max(0, min_minutes) * 60
        for row in self._titles.iter_joined():
            if row.total_seconds < threshold:
                continue
            yield row