from __future__ import annotations


class InMemoryCatalog:
    def __init__(self, tables: list[dict] | None = None):
        self._tables = tables or []

    def search_tables(self, query: str) -> list[dict]:
        q = query.lower()
        return [t for t in self._tables if q in t.get("name", "").lower()]

    def describe_table(self, table_name: str) -> dict:
        for t in self._tables:
            if t.get("name") == table_name:
                return t
        raise KeyError(f"Unknown table: {table_name}")

    def get_column_profile(self, table_name: str, column_name: str) -> dict:
        table = self.describe_table(table_name)
        profiles = table.get("column_profiles", {})
        if column_name not in profiles:
            raise KeyError(f"Unknown column profile: {column_name}")
        return profiles[column_name]
