# ARCHITECTURE

`channel`은 단일 supervisor + 단일 SQL subagent 구조를 사용한다.
도메인별 agent/table별 agent는 만들지 않는다.

1. User -> `channel` CLI interactive shell
2. Supervisor routing -> `sql_db`
3. Subagent tools -> catalog 탐색, schema 조회, SQL validate/explain/run
4. Execution -> Impala connector
