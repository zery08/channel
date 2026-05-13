---
name: query-writing
description: Write and execute read-only SQL queries from simple SELECTs to complex multi-table JOINs and aggregations. Use when the user asks to query data, run SQL, retrieve records, filter rows, aggregate, or generate a report.
---

# Query Writing Skill

## Available Tools
- `sql_db_list_tables` — list all tables
- `sql_db_schema` — get schema + sample rows for tables
- `sql_db_query_checker` — verify SQL is correct before running
- `sql_db_query` — execute the query (writes are blocked at code level)

## Workflow

### Simple Query (single table)
1. `sql_db_schema` — confirm column names
2. `sql_db_query_checker` — verify the SQL
3. `sql_db_query` — execute

### Complex Query (JOIN / aggregation)
1. Use `write_todos` to plan: which tables, which joins, what aggregation
2. `sql_db_schema("table1, table2")` — inspect all tables at once
3. `sql_db_query_checker` — verify before running
4. `sql_db_query` — execute

## Query Guidelines
- Default LIMIT 20 unless the user specifies otherwise
- Prefer specific columns over `SELECT *`
- Always use `sql_db_query_checker` before `sql_db_query`
- Only SELECT and WITH (CTEs) are allowed — INSERT/UPDATE/DELETE/DROP are blocked

## Error Recovery
- **Empty result**: check WHERE conditions and column names via `sql_db_schema`
- **Syntax error**: re-read the error; fix and re-check with `sql_db_query_checker`
- **Blocked by guard**: the query contains a write statement — rewrite as SELECT

## Example: "최근 주문 10개"
```sql
SELECT order_id, customer_id, order_date, total_amount
FROM orders
ORDER BY order_date DESC
LIMIT 10
```
