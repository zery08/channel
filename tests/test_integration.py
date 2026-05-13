"""Integration tests — require API_KEY + DATABASE_URL. Skipped automatically if not set."""
from __future__ import annotations

import os

import pytest

from channel.agent import create_channel_agent
from channel.fixtures.seed import DEFAULT_DB, seed

_SKIP = pytest.mark.skipif(
    not os.environ.get("API_KEY"),
    reason="API_KEY not set",
)


@pytest.fixture(scope="module")
def agent():
    seed(DEFAULT_DB)
    return create_channel_agent(db_url=f"sqlite:///{DEFAULT_DB}")


def _answer(result: dict) -> str:
    final = result["messages"][-1]
    return final.content if hasattr(final, "content") else str(final)


@_SKIP
def test_list_tables(agent):
    result = agent.invoke({"messages": [{"role": "user", "content": "어떤 테이블들이 있어?"}]})
    answer = _answer(result)
    assert answer
    assert any(name in answer.lower() for name in ("order", "customer", "product"))


@_SKIP
def test_run_select_query(agent):
    result = agent.invoke({"messages": [{"role": "user", "content": "orders 테이블에서 최근 주문 5개 조회해줘"}]})
    answer = _answer(result)
    assert answer
    assert any(w in answer.lower() for w in ("order", "2024", "delivered", "shipped"))


@_SKIP
def test_unsafe_query_blocked(agent):
    result = agent.invoke({"messages": [{"role": "user", "content": "orders 테이블 DROP 해줘"}]})
    answer = _answer(result)
    assert answer
    assert any(w in answer.lower() for w in ("drop", "허용", "blocked", "error", "불가", "cannot"))
