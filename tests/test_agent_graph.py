"""Verify the channel agent graph can be built without making API calls."""

import os

import pytest

from channel.agent import create_channel_agent


@pytest.fixture(autouse=True)
def dummy_env(monkeypatch):
    if not os.environ.get("API_KEY"):
        monkeypatch.setenv("API_KEY", "sk-or-test-dummy")
    if not os.environ.get("BASE_URL"):
        monkeypatch.setenv("BASE_URL", "https://openrouter.ai/api/v1")
    if not os.environ.get("MODEL"):
        monkeypatch.setenv("MODEL", "anthropic/claude-sonnet-4-5")


def test_channel_agent_builds(tmp_path):
    # Create a minimal SQLite DB so SQLDatabase.from_uri doesn't fail
    import sqlite3
    db = tmp_path / "test.db"
    sqlite3.connect(db).execute("CREATE TABLE t (id INTEGER PRIMARY KEY)")

    agent = create_channel_agent(db_url=f"sqlite:///{db}")
    assert callable(getattr(agent, "invoke", None))
    assert callable(getattr(agent, "stream", None))
