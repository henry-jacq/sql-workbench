-- Retrieve the latest users
SELECT *
FROM users_raw
ORDER BY created_at DESC
LIMIT 100;

SELECT *
FROM users_optimized
ORDER BY created_at DESC
LIMIT 100;
