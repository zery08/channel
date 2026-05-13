# CATALOG_INDEX_SPEC

초기 구현은 in-memory mock catalog를 사용한다.

인터페이스:
- `search_tables(query)`
- `describe_table(table_name)`
- `get_column_profile(table_name, column_name)`

추후 실제 metastore/index로 교체할 수 있도록 `catalog/interfaces.py`로 분리했다.
