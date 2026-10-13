"""Standalone adapter — user-declared exes from config or a drop folder."""
from __future__ import annotations

import logging
from pathlib import Path

from playtime_tracker.adapters.base_adapter import StoreAdapter
from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.utils.slugify import slugify

log = logging.getLogger(__name__)


class StandaloneAdapter(StoreAdapter):
    store_name = "standalone"

    async def discover(self) -> list[GameTitle]:
        root = self.config.library_path if self.config else None
        if root is None or not Path(root).exists():
            return []
        titles: list[GameTitle] = []
        for exe in Path(root).rglob("*.exe"):
            titles.append(
                GameTitle(
                    slug=slugify(f"standalone-{exe.stem}"),
                    display_name=exe.stem.replace("_", " ").title(),
                    store="standalone",
                    install_path=exe.parent,
                    executable=exe,
                    tags=["standalone"],
                )
            )
        return titles