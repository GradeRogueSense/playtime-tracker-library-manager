"""Steam adapter — reads libraryfolders.vdf and the per-app manifest files."""
from __future__ import annotations

import logging
import re
from pathlib import Path

from playtime_tracker.adapters.base_adapter import StoreAdapter
from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.utils.slugify import slugify

log = logging.getLogger(__name__)

_STEAM_ROOTS = [
    Path(r"C:\Program Files (x86)\Steam"),
    Path(r"C:\Program Files\Steam"),
]


class SteamAdapter(StoreAdapter):
    store_name = "steam"

    async def discover(self) -> list[GameTitle]:
        library_roots = self._library_roots()
        titles: list[GameTitle] = []
        for root in library_roots:
            steamapps = root / "steamapps"
            if not steamapps.exists():
                continue
            for manifest in steamapps.glob("appmanifest_*.acf"):
                title = self._parse_manifest(manifest, root)
                if title is not None:
                    titles.append(title)
        log.info("steam adapter found %d titles across %d roots", len(titles), len(library_roots))
        return titles

    def _library_roots(self) -> list[Path]:
        roots: list[Path] = []
        for base in _STEAM_ROOTS:
            folders = base / "steamapps" / "libraryfolders.vdf"
            if not folders.exists():
                continue
            text = folders.read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r'"path"\s+"([^"]+)"', text):
                roots.append(Path(match.group(1).replace("\\\\", "\\")))
        if not roots:
            roots = [p for p in _STEAM_ROOTS if p.exists()]
        return roots

    def _parse_manifest(self, manifest: Path, root: Path) -> GameTitle | None:
        text = manifest.read_text(encoding="utf-8", errors="ignore")
        name = re.search(r'"name"\s+"([^"]+)"', text)
        appid = re.search(r'"appid"\s+"(\d+)"', text)
        installdir = re.search(r'"installdir"\s+"([^"]+)"', text)
        if not (name and appid):
            return None
        install_path = (root / "steamapps" / "common" / installdir.group(1)) if installdir else None
        return GameTitle(
            slug=slugify(f"steam-{appid.group(1)}"),
            display_name=name.group(1),
            store="steam",
            install_path=install_path,
            steam_appid=int(appid.group(1)),
            tags=["steam"],
        )