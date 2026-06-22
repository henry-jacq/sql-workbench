-- Count active users
SELECT COUNT(*)
FROM users_raw
WHERE status = 'ACTIVE';

SELECT COUNT(*)
FROM users_optimized
WHERE status = 'ACTIVE';
