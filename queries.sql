-- Query 1
-- Lookup By Email
SELECT *
FROM users_raw
WHERE email='user900000@test.com';

SELECT *
FROM users_optimized
WHERE email='user900000@test.com';

-- Query 2
-- Lookup By Status
SELECT COUNT(*)
FROM users_raw
WHERE status='ACTIVE';

SELECT COUNT(*)
FROM users_optimized
WHERE status='ACTIVE';

-- Query 3
-- Lookup By Country Filter
SELECT *
FROM users_raw
WHERE country='India';

SELECT *
FROM users_optimized
WHERE country='India';

-- Query 4
-- Lookup By Date Range
SELECT *
FROM users_raw
WHERE created_at >= '2025-01-01';

SELECT *
FROM users_optimized
WHERE created_at >= '2025-01-01';

-- Query 5
-- Composite Index Test
SELECT *
FROM users_raw
WHERE status='ACTIVE'
AND country='India';

SELECT *
FROM users_optimized
WHERE status='ACTIVE'
AND country='India';

-- Query 6
-- Pagination Test
SELECT *
FROM users_raw
ORDER BY created_at DESC
LIMIT 100;

SELECT *
FROM users_optimized
ORDER BY created_at DESC
LIMIT 100;

