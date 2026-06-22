# SQL Workbench

SQL Workbench is a MySQL environment for comparing schema design, indexing strategies, and query performance with large datasets.


## Setup

Create the database:

```sql
CREATE DATABASE performance_db;
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create both user tables:

```bash
mysql -u root -p performance_db < schema/users_raw.sql
mysql -u root -p performance_db < schema/users_optimized.sql
```

The loaders use MySQL at `localhost` with `root`/`root` by default. Update their configuration constants if needed.

## Usage

Generate users with the Faker-based loader:

```bash
python scripts/populate_users.py
```

Alternatively, run the producer/consumer loader with live throughput metrics:

```bash
python benchmarks/benchmark_users.py
```

Both loaders insert identical data into `users_raw` and `users_optimized`. Run only one unless you want an additional dataset.

Execute workloads from `queries/`, then use `EXPLAIN` or `EXPLAIN ANALYZE` to compare query plans and execution time.

```sql
EXPLAIN ANALYZE
SELECT *
FROM users_optimized
WHERE email = 'user900000@test.com';
```

Indexing and measurement guidance is available in `docs/`. Use `schema/reset_users_indexes.sql` to remove the named experimental indexes after testing.

## Planned Workloads

- Orders
- Payments
- Inventory
- Booking and ride-sharing systems

