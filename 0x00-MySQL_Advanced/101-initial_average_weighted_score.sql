-- This script created a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE input_user_id INT;
	DECLARE done INT DEFAULT FALSE;
	DECLARE cur CURSOR FOR SELECT id from users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	OPEN cur;
	loop_label: LOOP
		FETCH cur INTO input_user_id;
		IF done THEN 
			LEAVE loop_label;
		END IF;
		UPDATE users
		SET average_score = (SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
			FROM projects
			JOIN corrections ON projects.id = corrections.project_id
			WHERE corrections.user_id = input_user_id)
		WHERE id = input_user_id;

	END LOOP loop_label;
	CLOSE cur;
END $$
DELIMITER ;
