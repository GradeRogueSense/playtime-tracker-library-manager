"""Epic adapter — walks the Epic Games Launcher manifest directory."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from playtime_tracker.adapters.base_adapter import StoreAdapter
from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.utils.slugify import slugify

log = logging.getLogger(__name__)

_MANIFEST_DIR = Path(
    os.environ.get("PROGRAMDATA", r"C:\ProgramData")
) / "Epic" / "EpicGamesLauncher" / "Data" / "Manifests"


class EpicAdapter(StoreAdapter):
    store_name = "epic"

    async def discover(self) -> list[GameTitle]:
        if not _MANIFEST_DIR.exists():
            log.debug("epic manifests not present at %s", _MANIFEST_DIR)
            return []
        titles: list[GameTitle] = []
        for item in _MANIFEST_DIR.glob("*.item"):
            try:
                data = json.loads(item.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                log.warning("skipping malformed epic manifest %s", item.name)
                continue
            name = data.get("DisplayName")
            install = data.get("InstallLocation")
            if not name or not install:
                continue
            titles.append(
                GameTitle(
                    slug=slugify(f"epic-{data.get('CatalogItemId', name)}"),
                    display_name=name,
                    store="epic",
                    install_path=Path(install),
                    tags=["epic"],
                )
            )
        return titles