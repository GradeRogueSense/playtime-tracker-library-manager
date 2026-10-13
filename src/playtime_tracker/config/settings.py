"""TOML-backed settings loader. Lives at %APPDATA%/ptlm/config.toml."""
from __future__ import annotations

import os
from pathlib import Path

import tomli_w
from pydantic import BaseModel, Field

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "ptlm"
CONFIG_PATH = CONFIG_DIR / "config.toml"


class StoreConfig(BaseModel):
    enabled: bool = True
    library_path: Path | None = None
    poll_seconds: int = 15


class Settings(BaseModel):
    db_path: Path = Field(default_factory=lambda: CONFIG_DIR / "playtime.db")
    poll_seconds: int = 15
    idle_grace_seconds: int = 90
    ignore_processes: list[str] = Field(
        default_factory=lambda: ["explorer.exe", "steamwebhelper.exe", "EpicWebHelper.exe"]
    )
    stores: dict[str, StoreConfig] = Field(
        default_factory=lambda: {
            "steam": StoreConfig(),
            "epic": StoreConfig(),
            "gog": StoreConfig(),
            "standalone": StoreConfig(),
        }
    )


def load_settings(path: Path | None = None) -> Settings:
    path = path or CONFIG_PATH
    if not path.exists():
        settings = Settings()
        save_settings(settings, path)
        return settings
    with path.open("rb") as fh:
        raw = tomllib.load(fh)
    return Settings.model_validate(raw)


def save_settings(settings: Settings, path: Path | None = None) -> None:
    path = path or CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = settings.model_dump(mode="json")
    with path.open("wb") as fh:
        tomli_w.dump(payload, fh)