from __future__ import annotations

from dataclasses import dataclass

from channel.catalog.mock import InMemoryCatalog
from channel.connectors.impala import ImpalaConnector
from channel.tools.data_lake_sql import DataLakeSQLTools


try:
    from deepagents import create_deep_agent
except Exception:  # pragma: no cover
    create_deep_agent = None


@dataclass
class SubAgentSpec:
    name: str
    tools: list[str]


def route_user_query(user_query: str) -> str:
    keywords = ("sql", "table", "impala", "query", "aggregate", "column", "schema", "데이터")
    if any(k in user_query.lower() for k in keywords):
        return "data-lake-sql"
    return "general"


def build_data_lake_sql_tools() -> DataLakeSQLTools:
    catalog = InMemoryCatalog(tables=[])
    connector = ImpalaConnector()
    return DataLakeSQLTools(catalog=catalog, connector=connector)


def build_supervisor_agent():
    subagent = SubAgentSpec(
        name="data-lake-sql",
        tools=[
            "search_tables",
            "describe_table",
            "get_column_profile",
            "validate_sql",
            "explain_sql",
            "run_sql",
        ],
    )

    if create_deep_agent is None:
        return {"name": "channel", "subagents": [subagent]}

    return create_deep_agent(
        name="channel",
        instruction="Route data-lake/Impala/SQL questions to data-lake-sql subagent.",
        subagents=[{"name": subagent.name}],
    )
