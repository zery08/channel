import pytest

from channel.sql.guard import SQLValidationError, validate_sql


def test_sql_guard_allows_select():
    validate_sql("select * from t")


def test_unsafe_sql_blocked():
    with pytest.raises(SQLValidationError):
        validate_sql("drop table t")
