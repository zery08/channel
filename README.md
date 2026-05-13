# channel

사내 데이터레이크 질의를 위한 DeepAgent 기반 supervisor/orchestrator 1차 구현.

## 핵심 원칙
- channel은 사용자 질의를 라우팅하는 supervisor
- SQL 생성/실행 책임은 `data-lake-sql` subagent + tools
- Impala는 agent가 아닌 connector
- SQL 안전성은 코드 기반 guard로 강제

## 실행
```bash
pip install -e .
channel
```

실행 시 persistent interactive shell이 시작됩니다.

## 구조
- `src/channel/agents/supervisor.py`: `create_deep_agent` 기반 supervisor 구성
- `src/channel/tools/data_lake_sql.py`: subagent toolset
- `src/channel/connectors/impala.py`: Impala connector abstraction
- `src/channel/sql/guard.py`: SQL 안전성 검증
- `src/channel/catalog/mock.py`: in-memory catalog mock
