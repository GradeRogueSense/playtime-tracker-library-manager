"""Translates raw process events into tracker-service calls."""
from __future__ import annotations

import logging

from playtime_tracker.services.tracker_service import TrackerService

log = logging.getLogger(__name__)


class ProcessHandler:
    def __init__(self, tracker: TrackerService) -> None:
        self._tracker = tracker

    async def on_process_start(self, pid: int, name: str, exe_path: str) -> None:
        try:
            await self._tracker.note_process_start(pid=pid, name=name, exe_path=exe_path)
        except Exception:  # noqa: BLE001 — handler must never kill the poll loop
            log.exception("process_start handler failed pid=%s name=%s", pid, name)

    async def on_process_stop(self, pid: int) -> None:
        try:
            await self._tracker.note_process_stop(pid=pid)
        except Exception:  # noqa: BLE001
            log.exception("process_stop handler failed pid=%s", pid)