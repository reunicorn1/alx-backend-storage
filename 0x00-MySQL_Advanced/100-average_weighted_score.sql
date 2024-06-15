-- This script created a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE average FLOAT;

	SET average = (SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
		FROM projects
		JOIN corrections ON projects.id = corrections.project_id
		WHERE corrections.user_id = user_id);

	UPDATE users
	SET average_score = average
	WHERE id = user_id;

END $$
DELIMITER ;
