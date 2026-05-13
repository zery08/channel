from channel.catalog.mock import InMemoryCatalog


def test_catalog_search_mock():
    catalog = InMemoryCatalog(tables=[{"name": "lake.orders"}, {"name": "lake.customers"}])
    out = catalog.search_tables("order")
    assert out == [{"name": "lake.orders"}]
