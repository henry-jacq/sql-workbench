# Indexing Experiments

Run the workload queries before and after adding indexes, and compare their execution plans and timings.

Suggested experiments:

- Add a unique index on `email` for lookup queries.
- Add single-column indexes on `country`, `status`, and `created_at`.
- Compare separate indexes with a composite `(status, country)` index.
- Compare a covering index with an index that requires table lookups.

Apply one change at a time so each result has a clear cause.

Run `schema/reset_users_indexes.sql` after an indexed experiment to return `users_optimized` to its unindexed state. The script expects all listed experimental indexes to exist.
