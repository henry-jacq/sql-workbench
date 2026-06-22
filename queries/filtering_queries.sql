-- Filter by country
SELECT *
FROM users_raw
WHERE country = 'India';

SELECT *
FROM users_optimized
WHERE country = 'India';

-- Filter by creation date
SELECT *
FROM users_raw
WHERE created_at >= '2025-01-01';

SELECT *
FROM users_optimized
WHERE created_at >= '2025-01-01';

-- Filter by status and country
SELECT *
FROM users_raw
WHERE status = 'ACTIVE'
  AND country = 'India';

SELECT *
FROM users_optimized
WHERE status = 'ACTIVE'
  AND country = 'India';
