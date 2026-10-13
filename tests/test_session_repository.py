from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from playtime_tracker.models.game_title import GameTitle
from playtime_tracker.repositories.session_repository import SessionRepository
from playtime_tracker.repositories.title_repository import TitleRepository


@pytest.fixture()
def db(tmp_path: Path) -> Path:
    return tmp_path / "playtime.db"


def test_open_close_rolls_up_total(db: Path):
    titles = TitleRepository(db)
    sessions = SessionRepository(db)
    title_id = titles.upsert(
        GameTitle(slug="steam-1145360", display_name="Hades", store="steam", tags=["steam"])
    )

    started = datetime(2026, 1, 4, 20, 0, tzinfo=timezone.utc)
    session_id = sessions.open(title_id=title_id, pid=4242, process_name="Hades.exe", started_at=start