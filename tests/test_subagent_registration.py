from channel.agents.supervisor import build_supervisor_agent


def test_subagent_registered():
    sup = build_supervisor_agent()
    subagents = sup["subagents"]
    assert subagents[0].name == "data-lake-sql"
