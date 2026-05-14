from __future__ import annotations

import argparse
import json
import os

from channel.agent import create_channel_agent

# ANSI colors
_GREY   = "\033[90m"
_CYAN   = "\033[96m"
_YELLOW = "\033[93m"
_GREEN  = "\033[92m"
_RESET  = "\033[0m"


def _truncate(text: str, limit: int = 300) -> str:
    return text if len(text) <= limit else text[:limit] + " …"


def _print_update(node: str, messages: list) -> None:
    for msg in messages:
        kind = getattr(msg, "type", None)

        if kind == "ai":
            for tc in getattr(msg, "tool_calls", []):
                args = _truncate(json.dumps(tc["args"], ensure_ascii=False))
                print(f"{_YELLOW}[{node}] → {tc['name']}({args}){_RESET}")

            content = msg.content
            if isinstance(content, str) and content:
                print(f"{_CYAN}[{node}]{_RESET} {content}")
            elif isinstance(content, list):
                text = "\n".join(
                    b["text"] for b in content
                    if isinstance(b, dict) and b.get("type") == "text" and b.get("text")
                )
                if text:
                    print(f"{_CYAN}[{node}]{_RESET} {text}")

        elif kind == "tool":
            result = _truncate(str(msg.content))
            print(f"{_GREEN}[{node}] ✓ {msg.name}:{_RESET} {_GREY}{result}{_RESET}")


def _resolve_db_url(db_arg: str | None) -> str | None:
    if db_arg:
        return db_arg if "://" in db_arg else f"sqlite:///{db_arg}"
    return os.environ.get("DATABASE_URL")


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def _extract_tool_calls(msg) -> list[tuple[str, dict]]:
    calls: list[tuple[str, dict]] = []
    for tc in getattr(msg, "tool_calls", []) or []:
        name = tc.get("name")
        args = tc.get("args") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {"raw": args}
        if name:
            calls.append((name, args if isinstance(args, dict) else {"raw": str(args)}))
    return calls


def _reason_for_tool(tool_name: str) -> str:
    return {
        "sql_db_list_tables": "후보 테이블을 찾기 위해 전체 테이블 목록을 확인했습니다.",
        "sql_db_schema": "컬럼/타입 확인으로 정확한 SQL을 만들기 위해 스키마를 조회했습니다.",
        "sql_db_query_checker": "실행 전 SQL 문법/적합성 검증을 진행했습니다.",
        "sql_db_query": "검증된 읽기 전용 SQL을 실제 실행해 결과를 가져왔습니다.",
    }.get(tool_name, "요청 해결을 위해 필요한 중간 도구를 호출했습니다.")


def run_shell(db_url: str | None = None) -> None:
    agent = create_channel_agent(db_url=db_url)

    print(f"channel [{db_url}]. type 'exit' to quit.\n")
    while True:
        try:
            text = input("channel> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            break

        print()
        printed = False
        seen_calls: set[tuple[str, str]] = set()
        for chunk, _meta in agent.stream(
            {"messages": [{"role": "user", "content": text}]},
            stream_mode="messages",
        ):
            for name, args in _extract_tool_calls(chunk):
                sig = (name, json.dumps(args, ensure_ascii=False, sort_keys=True))
                if sig in seen_calls:
                    continue
                seen_calls.add(sig)
                print(f"\n{_YELLOW}[tool]{_RESET} {name}({json.dumps(args, ensure_ascii=False)})")
                print(f"{_GREY}  reasoning: {_reason_for_tool(name)}{_RESET}")
                if name == "sql_db_query" and "query" in args:
                    print(f"{_GREEN}  used_query:{_RESET} {args['query']}")

            if getattr(chunk, "type", None) != "AIMessageChunk":
                continue
            piece = _extract_text(getattr(chunk, "content", ""))
            if piece:
                print(piece, end="", flush=True)
                printed = True

        if printed:
            print("\n")
        else:
            print(f"{_GREY}(no streamed response){_RESET}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="channel — sql_db assistant")
    parser.add_argument(
        "--db",
        metavar="URL",
        help="SQLAlchemy DB URL or SQLite path (e.g. ./test.db or sqlite:///./test.db)",
    )
    args = parser.parse_args()
    run_shell(db_url=_resolve_db_url(args.db))
