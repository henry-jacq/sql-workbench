-- Lookup by email
SELECT *
FROM users_raw
WHERE email = 'user900000@test.com';

SELECT *
FROM users_optimized
WHERE email = 'user900000@test.com';
