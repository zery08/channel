from __future__ import annotations

import re


class SQLValidationError(ValueError):
    pass


BLOCKED_KEYWORDS = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke",
)


def validate_sql(sql: str) -> None:
    if not sql or not sql.strip():
        raise SQLValidationError("SQL must not be empty")

    normalized = re.sub(r"\s+", " ", sql).strip().lower()

    if ";" in normalized[:-1]:
        raise SQLValidationError("Multiple statements are not allowed")

    if not normalized.startswith(("select", "with", "explain")):
        raise SQLValidationError("Only read-only SQL is allowed")

    for kw in BLOCKED_KEYWORDS:
        if re.search(rf"\b{kw}\b", normalized):
            raise SQLValidationError(f"Blocked keyword detected: {kw}")
