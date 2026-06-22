# EXPLAIN ANALYZE

Prefix a query with `EXPLAIN ANALYZE` to execute it and inspect the actual plan:

```sql
EXPLAIN ANALYZE
SELECT *
FROM users_optimized
WHERE email = 'user900000@test.com';
```

Compare estimated and actual rows, access type, selected indexes, loop counts, and elapsed time. Use plain `EXPLAIN` when the query should not be executed.
