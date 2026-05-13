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
        for update in agent.stream(
            {"messages": [{"role": "user", "content": text}]},
            stream_mode="updates",
        ):
            for node, state in update.items():
                if state:
                    _print_update(node, state.get("messages", []))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="channel — data lake assistant")
    parser.add_argument(
        "--db",
        metavar="URL",
        help="SQLAlchemy DB URL or SQLite path (e.g. ./test.db or sqlite:///./test.db)",
    )
    args = parser.parse_args()
    run_shell(db_url=_resolve_db_url(args.db))
