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
