"""Core playtime tracker.

Owns the poll loop that samples running processes, matches them against
known game executables, and opens/closes PlaySession rows.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

import psutil

from playtime_tracker.config.settings import Settings
from playtime_tracker.handlers.process_handler import ProcessHandler
from playtime_tracker.repositories.session_repository import SessionRepository
from playtime_tracker.repositories.title_repository import TitleRepository

log = logging.getLogger(__name__)


class TrackerService:
    def __init__(self, settings: Settings, *, poll_seconds: float | None = None) -> None:
        self._settings = settings
        self._poll = poll_seconds or settings.poll_seconds
        self._titles = TitleRepository(settings.db_path)
        self._sessions = SessionRepository(settings.db_path)
        self._active: dict[int, int] = {}  # pid -> title_id
        self._handler = ProcessHandler(self)

    async def run_forever(self) -> None:
        log.info("tracker polling every %.1fs", self._poll)
        try:
            while True:
                await self._tick()
                await asyncio.sleep(self._poll)
        finally:
            await self._shutdown()

    async def _tick(self) -> None:
        seen: set[int] = set()
        for proc in psutil.process_iter(["pid", "name", "exe"]):
            try:
                pid = proc.info["pid"]
                name = proc.info["name"] or ""
                exe = proc.info["exe"] or ""
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            if name.lower() in {p.lower() for p in self._settings.ignore_processes}:
                continue
            seen.add(pid)
            if pid not in self._active:
                await self._handler.on_process_start(pid, name, exe)

        for pid in list(self._active):
            if pid not in seen:
                await self._handler.on_process_stop(pid)

    async def note_process_start(self, pid: int, name: str, exe_path: str) -> None:
        title = self._titles.find_by_executable(exe_path)
        if title is None or title.id is None:
            return
        session_id = self._sessions.open(
            title_id=title.id, pid=pid, process_name=name, started_at=datetime.now(timezone.utc)
        )
        self._active[pid] = session_id
        log.debug("session %s opened for pid=%s title=%s", session_id, pid, title.display_name)

    async def note_process_stop(self, pid: int) -> None:
        session_id = self._active.pop(pid, None)
        if session_id is None:
            return
        self._sessions.close(session_id, ended_at=datetime.now(timezone.utc))

    async def _shutdown(self) -> None:
        for pid in list(self._active):
            await self.note_process_stop(pid)