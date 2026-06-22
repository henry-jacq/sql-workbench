# MySQL Tuning Notes

Keep the database environment stable while comparing schemas or indexes. Record the MySQL version, buffer-pool size, dataset size, hardware, and whether the cache was warm.

Measure multiple runs and report the median rather than relying on one execution. Change only one schema, query, or server setting per experiment.
