# SQL WorkBench

This repository contains examples and exercises for optimizing MySQL queries.

Flow
1. Install MySQL server and set up a database.
2. Run the SQL scripts in the `schema.sql` file to create the necessary tables.
3. Run the appropriate python scripts to populate data in the tables.
4. After populating the data, create indexes based on the queries in the `queries.sql` file to optimize their performance. So that the tables are optimized for the queries you will run. You can use the `EXPLAIN` statement to analyze the query execution plan and identify potential performance bottlenecks.
5. Run the queries in the `queries.sql` file and analyze their performance using EXPLAIN or other profiling tools.
