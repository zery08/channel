from __future__ import annotations

from channel.agents.supervisor import build_supervisor_agent, route_user_query


def run_shell() -> None:
    _agent = build_supervisor_agent()
    print("channel interactive shell. type 'exit' to quit.")
    while True:
        try:
            text = input("channel> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in {"exit", "quit"}:
            break
        route = route_user_query(text)
        print(f"routed_to={route}")


def main() -> None:
    run_shell()
