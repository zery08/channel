"""Seed a SQLite database with sample e-commerce data for local testing.

Usage:
    uv run python -m channel.fixtures.seed            # creates ./channel_test.db
    uv run python -m channel.fixtures.seed myfile.db  # custom path
"""

from __future__ import annotations

import random
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

DEFAULT_DB = Path(__file__).parent.parent.parent.parent / "channel_test.db"

DDL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    country       TEXT    NOT NULL,
    signup_date   TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id    INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    price         REAL    NOT NULL,
    stock         INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date    TEXT    NOT NULL,
    status        TEXT    NOT NULL CHECK(status IN ('pending','shipped','delivered','cancelled')),
    total_amount  REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id       INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL,
    unit_price    REAL    NOT NULL
);
"""

_CUSTOMERS = [
    ("Alice Kim",     "alice@example.com",   "KR"),
    ("Bob Lee",       "bob@example.com",     "KR"),
    ("Carol Park",    "carol@example.com",   "US"),
    ("David Wang",    "david@example.com",   "CN"),
    ("Eva Müller",    "eva@example.com",     "DE"),
    ("Frank Tanaka",  "frank@example.com",   "JP"),
    ("Grace Chen",    "grace@example.com",   "CN"),
    ("Henry Brown",   "henry@example.com",   "US"),
    ("Irene Choi",    "irene@example.com",   "KR"),
    ("James Smith",   "james@example.com",   "US"),
]

_PRODUCTS = [
    ("MacBook Pro 16",   "Electronics",   2499.00,  30),
    ("iPhone 15",        "Electronics",   1099.00, 120),
    ("AirPods Pro",      "Electronics",    249.00, 200),
    ("Samsung 4K TV",    "Electronics",    799.00,  45),
    ("Nike Air Max",     "Apparel",         149.00, 300),
    ("Levi's 501 Jeans", "Apparel",          89.00, 150),
    ("The Pragmatic Programmer", "Books",    49.00, 500),
    ("Clean Code",       "Books",            39.00, 400),
    ("Espresso Machine", "Home",            329.00,  60),
    ("Standing Desk",    "Home",            599.00,  25),
]

_STATUSES = ["pending", "shipped", "delivered", "delivered", "delivered", "cancelled"]


def seed(db_path: str | Path = DEFAULT_DB) -> Path:
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)

    conn.executescript(DDL)

    # customers
    base_date = date(2023, 1, 1)
    conn.executemany(
        "INSERT OR IGNORE INTO customers(name, email, country, signup_date) VALUES (?,?,?,?)",
        [
            (name, email, country, str(base_date + timedelta(days=i * 30)))
            for i, (name, email, country) in enumerate(_CUSTOMERS)
        ],
    )

    # products
    conn.executemany(
        "INSERT OR IGNORE INTO products(name, category, price, stock) VALUES (?,?,?,?)",
        _PRODUCTS,
    )

    conn.commit()

    # orders + order_items
    rng = random.Random(42)
    for order_id in range(1, 201):
        customer_id = rng.randint(1, len(_CUSTOMERS))
        order_date = str(date(2024, 1, 1) + timedelta(days=rng.randint(0, 364)))
        status = rng.choice(_STATUSES)
        num_items = rng.randint(1, 4)
        items = []
        total = 0.0
        for _ in range(num_items):
            product_id = rng.randint(1, len(_PRODUCTS))
            qty = rng.randint(1, 3)
            price = _PRODUCTS[product_id - 1][2]
            items.append((order_id, product_id, qty, price))
            total += qty * price

        conn.execute(
            "INSERT OR IGNORE INTO orders(order_id, customer_id, order_date, status, total_amount)"
            " VALUES (?,?,?,?,?)",
            (order_id, customer_id, order_date, status, round(total, 2)),
        )
        conn.executemany(
            "INSERT OR IGNORE INTO order_items(order_id, product_id, quantity, unit_price)"
            " VALUES (?,?,?,?)",
            items,
        )

    conn.commit()
    conn.close()

    print(f"Seeded: {db_path.resolve()}")
    print(f"  customers:   {len(_CUSTOMERS)} rows")
    print(f"  products:    {len(_PRODUCTS)} rows")
    print(f"  orders:      200 rows")
    print(f"  order_items: ~{200 * 2} rows (avg 2 items/order)")
    return db_path


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    seed(path)
