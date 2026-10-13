"""Open/close PlaySession rows and roll totals back into titles."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_id INTEGER NOT NULL REFERENCES titles(id) ON DELETE CASCADE,
    pid INTEGER NOT NULL,
    process_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_title ON sessions(title_id);
CREATE INDEX IF NOT EXISTS idx_sessions_open ON sessions(ended_at) WHERE ended_at IS NULL;
"""


class SessionRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def open(self, *, title_id: int, pid: int, process_name: str, started_at: datetime) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO sessions (title_id, pid, process_name, started_at) VALUES (?,?,?,?)",
                (title_id, pid, process_name, started_at.isoformat()),
            )
            return int(cur.lastrowid or 0)

    def close(self, session_id: int, *, ended_at: datetime) -> None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT title_id, started_at FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
            if row is None:
                return
            conn.execute("UPDATE sessions SET ended_at = ? WHERE id = ?", (ended_at.isoformat(), session_id))
            started = datetime.fromisoformat(row["started_at"])
            elapsed = int((ended_at - started).total_seconds())
            conn.execute(
                "UPDATE titles SET total_seconds = total_seconds + ?, last_played_at = ? WHERE id = ?",
                (elapsed, ended_at.isoformat(), row["title_id"]),
            )