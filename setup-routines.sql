-- This function aims to calculate BMI based on weight and height
DELIMITER !
CREATE FUNCTION CalculateBMI(weight DECIMAL(5,2), height DECIMAL(5,2)) 
RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
    RETURN (weight / (height * height)) * 10000;
END !
DELIMITER ;

-- This function calculates workout intensity based off the type and duration
DELIMITER !
CREATE FUNCTION WorkoutIntensity(duration INT, type VARCHAR(50)) 
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    IF type = 'Cardio' AND duration >= 30 THEN
        RETURN 'High';
    ELSEIF type = 'Strength' AND duration >= 60 THEN
        RETURN 'High';
    ELSE
        RETURN 'Moderate';
    END IF;
END !
DELIMITER ;

-- This procedure creates a new workout routine for a user
DELIMITER !
CREATE PROCEDURE CreateWorkoutRoutine(userId BIGINT, routineName VARCHAR(100),
IN exerciseId BIGINT, IN startDate DATE, IN endDate DATE)
BEGIN
    INSERT INTO routine 
    (user_id, exercise_id, routine_name, start_date, end_date)
    VALUES (userId, exerciseId, routineName, startDate, endDate);
END !
DELIMITER ;

-- This trigger updates goal status after a new workout log is inserted. It
-- also checks if the goal's target date is met and updates the status
DELIMITER !
CREATE TRIGGER AfterLogInsert
AFTER INSERT ON logs
FOR EACH ROW
BEGIN
    IF EXISTS(SELECT 1 
              FROM goals 
              WHERE goal_id = NEW.routine_id AND target_date <= NEW.log_date)
              THEN UPDATE goals
        SET current_status = 'Completed'
        WHERE goal_id = NEW.routine_id;
    END IF;
END !
DELIMITER ;