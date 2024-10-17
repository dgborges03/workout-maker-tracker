-- DROP TABLE commands:
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS routine;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS users;

-- CREATE TABLE commands:
-- This table represents users in the workout routine database.
CREATE TABLE users (
    user_id BIGINT  PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    weight DECIMAL(5, 2),
    height DECIMAL(5, 2),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    fitness_level ENUM('Beginner', 'Intermediate', 'Expert') NOT NULL
);

-- This table represents goals in the workout routine database.
CREATE TABLE goals (
    goal_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    goal_type VARCHAR(50) NOT NULL,
    target_date DATE NOT NULL,
    current_status ENUM('In Progress', 'Completed') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- This table represents exercises in the workout routine database.
CREATE TABLE exercises (
    exercise_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    exercise_name VARCHAR(100) NOT NULL,
    exercise_type VARCHAR(100),
    target_group VARCHAR(100),
    equipment VARCHAR(100),
    description VARCHAR(2000),
    difficulty_level VARCHAR(50)
);

-- This table represents routines in the workout routine database.
CREATE TABLE routine (
    routine_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    goal_id BIGINT,
    exercise_id BIGINT NOT NULL,
    routine_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    sets INT,
    reps INT,
    suggested_weight DECIMAL(6, 2),
    duration INT, -- This is in minutes
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (goal_id) REFERENCES goals(goal_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);

-- This table represents workout logs in the workout routine database.
CREATE TABLE logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    routine_id BIGINT NOT NULL,
    log_date DATE NOT NULL,
    sets_completed INT,
    reps_completed INT,
    weight_used DECIMAL(6, 2),
    duration INT, 
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (routine_id) REFERENCES routine(routine_id)
);

-- These are our indexes to improve performance for important queries
CREATE INDEX idx_exercise_type ON exercises(exercise_type);
CREATE INDEX idx_goal_status ON goals(current_status);