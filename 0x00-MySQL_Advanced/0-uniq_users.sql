-- This script creates a table called users, with the following 
-- attributes: id (int), email (varchar 255), name (varchar 255)

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	PRIMARY KEY (id)
);
