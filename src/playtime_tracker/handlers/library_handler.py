"""Handler for library rescan / query requests."""
from __future__ import annotations

from playtime_tracker.models.library_entry import LibraryEntry
from playtime_tracker.services.library_service import LibraryService


class LibraryHandler:
    def __init__(self, library: LibraryService) -> None:
        self._library = library

    async def rescan(self) -> int:
        return await self._library.rescan_all()

    async def list_entries(self, min_minutes: int = 0) -> list[LibraryEntry]:
        return [row async for row in self._library.iter_library(min_minutes=min_minutes)]