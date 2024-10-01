-- 1. Create database if not exists
CREATE DATABASE IF NOT EXISTS `${MYSQL_DATABASE}`;

-- 2. Create user if not exists
CREATE USER IF NOT EXISTS `${MYSQL_USER}`@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';

-- 3. Grant all privileges to user
GRANT ALL PRIVILEGES ON `${MYSQL_DATABASE}`.* TO `${MYSQL_USER}`@'%';

-- 4. Flush privileges
FLUSH PRIVILEGES;

-- 5. Create users table
CREATE TABLE IF NOT EXISTS `${MYSQL_DATABASE}`.`users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL,
    `telegram_id` INT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

