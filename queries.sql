-- This query retrieves the total number of exercises per exercise
-- type.
SELECT exercise_type, COUNT(*) AS total_exercises
FROM exercises
GROUP BY exercise_type;

-- This query lists all users and their respective fitness goals. It also
-- includes the current status of each goal.
SELECT u.username, g.goal_type, g.current_status
FROM users u
JOIN goals g ON u.user_id = g.user_id;

-- This query retrieves detailed workout routine information, including
-- exercise details for a specific user.
SELECT r.routine_name, e.exercise_name, e.target_group, r.sets, r.reps
FROM routine r
JOIN exercises e ON r.exercise_id = e.exercise_id
JOIN users u ON r.user_id = u.user_id
JOIN goals g ON r.goal_id = g.goal_id
WHERE u.username = 'name';
-- Will need to put a username down when testing.

-- This query inserts a new exercise into the exercises table
INSERT INTO exercises 
(exercise_name, exercise_type, target_group, equipment, difficulty_level)
VALUES ('Deadlift', 'Strength', 'Back', 'Barbell', 'Expert');

-- This query updates the weight used in a specific workout log
UPDATE logs
SET weight_used = 60
WHERE log_id = 1;
