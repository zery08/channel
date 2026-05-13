# AGENTS

## channel (supervisor)
- DeepAgent supervisor/orchestrator 역할만 수행한다.
- SQL을 직접 생성/실행하지 않는다.
- 데이터레이크/Impala/SQL 관련 질문은 `data-lake-sql`로 위임한다.

## data-lake-sql (subagent)
- 허용 tool: `search_tables`, `describe_table`, `get_column_profile`, `validate_sql`, `explain_sql`, `run_sql`
- `run_sql`은 내부에서 반드시 validation을 재호출한다.

## 안전성
- SQL safety는 prompt가 아니라 `src/channel/sql/guard.py` 코드로 강제한다.
