import pytest

from channel.catalog.mock import InMemoryCatalog
from channel.connectors.impala import ImpalaConnector
from channel.sql.guard import SQLValidationError
from channel.tools.data_lake_sql import DataLakeSQLTools


def test_run_sql_forces_validation():
    tools = DataLakeSQLTools(catalog=InMemoryCatalog([]), connector=ImpalaConnector())
    with pytest.raises(SQLValidationError):
        tools.run_sql("delete from t")
