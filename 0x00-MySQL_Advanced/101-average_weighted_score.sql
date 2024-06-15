-- This script created a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN

	UPDATE users
	SET average_score = (
		SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
		FROM projects
		JOIN corrections ON projects.id = corrections.project_id
		WHERE corrections.user_id = users.id
	);

END $$
DELIMITER ;
