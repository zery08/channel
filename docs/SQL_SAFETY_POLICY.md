# SQL_SAFETY_POLICY

정책:
- read-only SQL만 허용 (`SELECT`, `WITH`, `EXPLAIN`)
- 다중 statement 금지
- DDL/DML/권한 변경 키워드 차단

구현 위치: `src/channel/sql/guard.py`
