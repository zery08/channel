"""Channel agent — supervisor that routes to specialist subagents."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

_CHANNEL_DIR = Path(__file__).parent  # src/channel/


def build_model(prefix: str = "") -> ChatOpenAI:
    """Build a ChatOpenAI client from environment variables.

    ``prefix`` is the agent name in uppercase (e.g. ``"SUPERVISOR"``).

    Resolved env vars (first match wins):
    - model:    ``{PREFIX}_MODEL``    → ``MODEL``
    - api_key:  ``{PREFIX}_API_KEY``  → ``API_KEY``
    - base_url: ``{PREFIX}_BASE_URL`` → ``BASE_URL``
    """
    def _require(key: str) -> str:
        value = (
            (os.environ.get(f"{prefix}_{key}") if prefix else None)
            or os.environ.get(key)
        )
        if not value:
            candidates = f"{prefix}_{key} or {key}" if prefix else key
            raise EnvironmentError(f"Set {candidates} in your environment.")
        return value

    return ChatOpenAI(
        model=_require("MODEL"),
        api_key=_require("API_KEY"),
        base_url=_require("BASE_URL"),
    )


def create_channel_agent(db_url: str | None = None):
    """Create and return the compiled channel deepagents graph.

    Subagents are registered here. To add a new domain, create a module under
    ``channel/subagents/`` and append its spec to the list below.

    Usage::

        agent = create_channel_agent(db_url="sqlite:///./channel_test.db")
        result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
        print(result["messages"][-1].content)
    """
    from deepagents import create_deep_agent
    from deepagents.backends import FilesystemBackend

    from channel.subagents.data_lake_sql import create_data_lake_sql_subagent

    resolved_url = db_url or os.environ.get("DATABASE_URL")
    if not resolved_url:
        raise EnvironmentError("Set DATABASE_URL or pass db_url=...")

    # ── Register subagents here ───────────────────────────────────────────────
    subagents = [
        create_data_lake_sql_subagent(resolved_url),
        # create_reporting_subagent(resolved_url),   ← future
    ]
    # ─────────────────────────────────────────────────────────────────────────

    return create_deep_agent(
        model=build_model("SUPERVISOR"),
        memory=[str(_CHANNEL_DIR / "AGENTS.md")],
        subagents=subagents,
        backend=FilesystemBackend(root_dir=str(_CHANNEL_DIR), virtual_mode=True),
    )
