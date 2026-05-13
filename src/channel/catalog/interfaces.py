from __future__ import annotations

from typing import Protocol


class Catalog(Protocol):
    def search_tables(self, query: str) -> list[dict]: ...

    def describe_table(self, table_name: str) -> dict: ...

    def get_column_profile(self, table_name: str, column_name: str) -> dict: ...
