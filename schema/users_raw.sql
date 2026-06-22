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
