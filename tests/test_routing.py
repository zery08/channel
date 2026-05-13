from channel.agents.supervisor import route_user_query


def test_channel_routing_to_data_lake_sql():
    assert route_user_query("Impala table schema 알려줘") == "data-lake-sql"


def test_channel_routing_general():
    assert route_user_query("hello") == "general"
