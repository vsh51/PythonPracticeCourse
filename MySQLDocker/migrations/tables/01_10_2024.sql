-- 1. Create users table
CREATE TABLE IF NOT EXISTS `${MYSQL_DATABASE}`.`users` (
    `id` INT AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `telegram_id` INT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
);

-- 2. Create disciplines table
CREATE TABLE IF NOT EXISTS `${MYSQL_DATABASE}`.`disciplines` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `lecture_total_points` INT NOT NULL,
    `practice_total_points` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

-- 3. Crate points table
CREATE TABLE IF NOT EXISTS `${MYSQL_DATABASE}`.`points` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `discipline_id` INT NOT NULL,
    `type` ENUM('lecture', 'practice') NOT NULL,
    `points` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`discipline_id`) REFERENCES `disciplines`(`id`)
);
