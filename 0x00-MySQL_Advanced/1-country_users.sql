-- This script creates a table called users, with the following 
-- attributes: id (int), email (varchar 255), name (varchar 255)
-- country (US, CO, TN)

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country	ENUM('US', 'CO', 'TN') NOT NULL Default 'US',
	PRIMARY KEY (id)
);
