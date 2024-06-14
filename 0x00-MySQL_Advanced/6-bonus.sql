-- This script creates a stored procedure AddBonus that adds a 
-- new correction for a student.
DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
	DECLARE project_id INT;
	SET project_id = (SELECT id
			FROM projects
			WHERE name = project_name);
	IF project_id IS NULL THEN
		INSERT into projects (name) VALUES (project_name);
		SET project_id = (SELECT id
			FROM projects
			WHERE name = project_name);
	END IF;
	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END $$
DELIMITER ;
		
