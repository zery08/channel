"""sql_db subagent — SQL assistant backed by SQLAlchemy + SQLDatabaseToolkit."""

from __future__ import annotations

from pathlib import Path

from deepagents import SubAgent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from channel.agent import build_model
from channel.sql.guard import SQLValidationError, validate_sql

_SKILLS_DIR = str(Path(__file__).parent.parent / "skills")

_SYSTEM_PROMPT = """You are a SQL assistant for a sql_db.

Use the schema-exploration skill to discover tables and columns.
Use the query-writing skill to build and run SQL queries.

Only SELECT queries are allowed — writes are blocked at the code level.
"""


def _wrap_query_tool(tool):
    """Wrap sql_db_query to add guard.py safety check before execution."""
    from langchain_core.tools import StructuredTool
    from pydantic import BaseModel

    original_run = tool._run

    class _Input(BaseModel):
        query: str

    def safe_run(query: str) -> str:
        try:
            validate_sql(query)
        except SQLValidationError as e:
            return f"Blocked: {e}"
        return original_run(query)

    return StructuredTool.from_function(
        func=safe_run,
        name=tool.name,
        description=tool.description,
        args_schema=_Input,
    )


def create_sql_db_subagent(db_url: str) -> SubAgent:
    """Return a SubAgent spec for the sql_db agent."""
    model = build_model("SQL_DB")
    db = SQLDatabase.from_uri(db_url)
    toolkit = SQLDatabaseToolkit(db=db, llm=model)

    tools = [
        _wrap_query_tool(t) if t.name == "sql_db_query" else t
        for t in toolkit.get_tools()
    ]

    return {
        "name": "sql_db",
        "description": (
            "Handles all sql_db work: table discovery, schema inspection, "
            "SQL validation, and query execution."
        ),
        "system_prompt": _SYSTEM_PROMPT,
        "tools": tools,
        "model": model,
        "skills": [_SKILLS_DIR],
    }
