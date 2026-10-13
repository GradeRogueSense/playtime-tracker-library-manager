"""CRUD for GameTitle rows plus the joined library view."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.models.library_entry import LibraryEntry
from playtime_tracker.utils.paths import normalize_exe

SCHEMA = """
CREATE TABLE IF NOT EXISTS titles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    store TEXT NOT NULL,
    install_path TEXT,
    executable TEXT,
    steam_appid INTEGER,
    last_played_at TEXT,
    total_seconds INTEGER NOT NULL DEFAULT 0,
    tags TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_titles_exe ON titles(executable);
CREATE INDEX IF NOT EXISTS idx_titles_store ON titles(store);
"""


class TitleRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def upsert(self, title: GameTitle) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO titles (slug, display_name, store, install_path, executable,
                                    steam_appid, last_played_at, total_seconds, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(slug) DO UPDATE SET
                    display_name=excluded.display_name,
                    install_path=excluded.install_path,
                    executable=excluded.executable,
                    steam_appid=excluded.steam_appid,
                    tags=excluded.tags
                """,
                (
                    title.slug,
                    title.display_name,
                    title.store,
                    str(title.install_path) if title.install_path else None,
                    str(title.executable) if title.executable else None,
                    title.steam_appid,
                    title.last_played_at.isoformat() if title.last_played_at else None,
                    title.total_seconds,
                    ",".join(title.tags),
                ),
            )
            return int(cur.lastrowid or 0)

    def find_by_executable(self, exe_path: str) -> GameTitle | None:
        normalized = normalize_exe(exe_path)
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM titles WHERE executable = ? LIMIT 1", (normalized,)
            ).fetchone()
        return self._row_to_title(row) if row else None

    def iter_joined(self) -> list[LibraryEntry]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT t.display_name, t.store, t.total_seconds, t.last_played_at,
                       t.install_path, t.tags
                FROM titles t
                ORDER BY t.total_seconds DESC, t.display_name ASC
                """
            ).fetchall()
        return [
            LibraryEntry(
                title=r["display_name"],
                store=r["store"],
                total_seconds=r["total_seconds"],
                last_played_at=datetime.fromisoformat(r["last_played_at"])
                if r["last_played_at"]
                else None,
                install_path=r["install_path"],
                tags=tuple(t for t in (r["tags"] or "").split(",") if t),
            )
            for r in rows
        ]

    @staticmethod
    def _row_to_title(row: sqlite3.Row) -> GameTitle:
        return GameTitle(
            id=row["id"],
            slug=row["slug"],
            display_name=row["display_name"],
            store=row["store"],
            install_path=Path(row["install_path"]) if row["install_path"] else None,
            executable=Path(row["executable"]) if row["executable"] else None,
            steam_appid=row["steam_appid"],
            last_played_at=datetime.fromisoformat(row["last_played_at"])
            if row["last_played_at"]
            else None,
            total_seconds=row["total_seconds"],
            tags=[t for t in (row["tags"] or "").split(",") if t],
        )