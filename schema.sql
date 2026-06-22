CREATE TABLE users_raw (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    age INT,
    status VARCHAR(20),
    created_at DATETIME,
    last_login DATETIME
);

CREATE TABLE users_optimized (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    city VARCHAR(100),
    country VARCHAR(100),

    age TINYINT UNSIGNED,

    status ENUM(
        'ACTIVE',
        'INACTIVE',
        'BLOCKED'
    ) NOT NULL,

    created_at DATETIME NOT NULL,
    last_login DATETIME
);

ALTER TABLE users_optimized
DROP INDEX idx_country,
DROP INDEX idx_status,
DROP INDEX idx_created,
DROP INDEX idx_last_login,
DROP INDEX idx_status_country;
