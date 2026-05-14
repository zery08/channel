# channel

Impala 데이터레이크에 자연어로 질문하는 AI SQL 에이전트.  
[deepagents](https://github.com/langchain-ai/deepagents) + OpenRouter 기반.

## 아키텍처

```
사용자 입력
    │
    ▼
channel supervisor  (deepagents graph)
    │  AGENTS.md로 identity 정의
    │  task("sql_db", ...) 로 위임
    ▼
sql_db subagent  (deepagents graph)
    │  skills: schema-exploration, query-writing
    ├── search_tables
    ├── describe_table
    ├── get_column_profile
    ├── validate_sql      ←─ sql/guard.py 가 코드 레벨에서 강제
    ├── explain_sql
    └── run_sql
            │
            ▼
    ImpalaConnector
```

---

## 설치

```bash
uv sync
uv sync --extra dev   # 테스트 포함
```

---

## 환경 설정

```bash
cp .env.example .env
```

`.env` 파일을 열고 값을 채웁니다:

```env
API_KEY=sk-or-...
BASE_URL=https://openrouter.ai/api/v1
MODEL=anthropic/claude-sonnet-4-5
```

| 변수 | 설명 |
|------|------|
| `API_KEY` | OpenRouter API 키 |
| `BASE_URL` | API 엔드포인트 |
| `MODEL` | 모든 에이전트의 기본 모델 |
| `SUPERVISOR_MODEL` | supervisor 전용 모델 오버라이드 (선택) |
| `SQL_DB_MODEL` | sql_db 전용 모델 오버라이드 (선택) |
| `{PREFIX}_API_KEY` | 에이전트별 API 키 오버라이드 (선택) |
| `{PREFIX}_BASE_URL` | 에이전트별 엔드포인트 오버라이드 (선택) |

---

## 실행

```bash
uv run channel
```

```
channel> orders 테이블 스키마 알려줘
orders 테이블의 컬럼 구성은 다음과 같습니다:
- order_id (BIGINT)
- customer_id (BIGINT)
...
```

### 모델 바꿔서 실행

```bash
MODEL=openai/gpt-4o uv run channel
MODEL=google/gemini-2.0-flash-001 uv run channel
```

### 코드에서 직접 사용

```python
from channel.agent import create_channel_agent

agent = create_channel_agent()
result = agent.invoke({"messages": [{"role": "user", "content": "orders 테이블 최근 주문 조회해줘"}]})
print(result["messages"][-1].content)
```

---

## 테스트

```bash
# 유닛 테스트 (API 키 불필요)
uv run pytest tests/ -v

# 통합 테스트 (API 키 필요)
uv run pytest tests/test_integration.py -v
```

---

## 프로젝트 구조

```
src/channel/
├── agent.py              # create_channel_agent() — supervisor 진입점
├── AGENTS.md             # supervisor identity
├── skills/
│   ├── query-writing/    # SQL 작성 절차 (SKILL.md)
│   └── schema-exploration/ # 카탈로그 탐색 절차 (SKILL.md)
├── subagents/
│   └── sql_db.py  # sql_db SubAgent 팩토리
├── catalog/
│   ├── interfaces.py     # Catalog 프로토콜
│   └── mock.py           # 인메모리 카탈로그 + 샘플 데이터
├── connectors/
│   └── impala.py         # Impala 커넥터 (현재 mock)
├── sql/
│   └── guard.py          # SQL 안전성 검증 (쓰기 차단)
├── tools/
│   └── sql_db.py  # LangChain StructuredTool 래퍼
└── cli.py                # 대화형 셸
```

---

## 지원 모델 (OpenRouter)

| 모델 | `MODEL` 값 |
|------|-----------|
| Claude Sonnet 4.5 | `anthropic/claude-sonnet-4-5` |
| Claude Haiku 3.5 | `anthropic/claude-3-5-haiku` |
| GPT-4o | `openai/gpt-4o` |
| GPT-4o mini | `openai/gpt-4o-mini` |
| Gemini 2.0 Flash | `google/gemini-2.0-flash-001` |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct` |

전체 목록: https://openrouter.ai/models
