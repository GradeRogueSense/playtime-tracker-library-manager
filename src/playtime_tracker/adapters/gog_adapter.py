"""GOG Galaxy adapter — reads the registry install list (Windows only)."""
from __future__ import annotations

import logging
from pathlib import Path

from playtime_tracker.adapters.base_adapter import StoreAdapter
from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.utils.slugify import slugify

log = logging.getLogger(__name__)

try:  # pywin32 only available on Windows
    import winreg  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    winreg = None  # type: ignore[assignment]


class GogAdapter(StoreAdapter):
    store_name = "gog"

    async def discover(self) -> list[GameTitle]:
        if winreg is None:
            log.debug("gog adapter requires Windows registry; skipping")
            return []
        titles: list[GameTitle] = []
        try:
            root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\GOG.com\Games")
        except FileNotFoundError:
            return []
        with root:
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(root, index)
                except OSError:
                    break
                index += 1
                with winreg.OpenKey(root, subkey_name) as sub:
                    try:
                        name, _ = winreg.QueryValueEx(sub, "gameName")
                        path, _ = winreg.QueryValueEx(sub, "path")
                    except FileNotFoundError:
                        continue
                titles.append(
                    GameTitle(
                        slug=slugify(f"gog-{subkey_name}"),
                        display_name=name,
                        store="gog",
                        install_path=Path(path),
                        tags=["gog"],
                    )
                )
        return titles