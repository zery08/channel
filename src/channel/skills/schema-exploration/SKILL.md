---
name: schema-exploration
description: Discover tables in the database, inspect column definitions and types. Use when the user asks what tables exist, what columns a table has, data types, or relationships between tables.
---

# Schema Exploration Skill

## Workflow

### 1. List All Tables
Use `sql_db_list_tables` to get all available tables.

### 2. Inspect Schema
Use `sql_db_schema` with one or more table names (comma-separated) to see column names, types, and sample rows.

### 3. Present Results
- List tables with a short description of each
- Show column names and types clearly
- Note primary/foreign key columns when visible from sample data

## Example: "어떤 테이블들이 있어?"
1. `sql_db_list_tables` → list all tables
2. For each table, `sql_db_schema` to get a brief description

## Example: "orders 테이블 스키마 알려줘"
1. `sql_db_schema("orders")` → show columns and sample rows

## Example: "orders와 customers 테이블 관계가 어떻게 돼?"
1. `sql_db_schema("orders, customers")` → inspect both at once
2. Identify join keys from column names (e.g. customer_id)
