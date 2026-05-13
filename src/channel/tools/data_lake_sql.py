from __future__ import annotations

from channel.catalog.interfaces import Catalog
from channel.connectors.impala import ImpalaConnector
from channel.sql.guard import validate_sql


class DataLakeSQLTools:
    def __init__(self, catalog: Catalog, connector: ImpalaConnector):
        self.catalog = catalog
        self.connector = connector

    def search_tables(self, query: str) -> list[dict]:
        return self.catalog.search_tables(query)

    def describe_table(self, table_name: str) -> dict:
        return self.catalog.describe_table(table_name)

    def get_column_profile(self, table_name: str, column_name: str) -> dict:
        return self.catalog.get_column_profile(table_name, column_name)

    def validate_sql(self, sql: str) -> dict:
        validate_sql(sql)
        return {"ok": True}

    def explain_sql(self, sql: str) -> str:
        validate_sql(sql)
        return self.connector.explain(sql)

    def run_sql(self, sql: str) -> list[dict]:
        # Mandatory safety check before execution
        self.validate_sql(sql)
        return self.connector.execute(sql)
