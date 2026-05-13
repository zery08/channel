from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ImpalaConfig:
    host: str = "localhost"
    port: int = 21050
    user: str | None = None


class ImpalaConnector:
    """Connector abstraction; Impala is not an agent."""

    def __init__(self, config: ImpalaConfig | None = None):
        self.config = config or ImpalaConfig()

    def execute(self, sql: str) -> list[dict[str, Any]]:
        # Placeholder for first implementation.
        return [{"status": "mock", "sql": sql}]

    def explain(self, sql: str) -> str:
        return f"EXPLAIN PLAN (mock): {sql}"
