DROP USER IF EXISTS 'workoutAdmin'@'localhost';
DROP USER IF EXISTS 'workoutClient'@'localhost';

CREATE USER 'workoutAdmin'@'localhost' IDENTIFIED BY 'adminPassword';
CREATE USER 'workoutClient'@'localhost' IDENTIFIED BY 'clientPassword';
GRANT ALL PRIVILEGES ON workoutdb.* TO 'workoutAdmin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON workoutdb.* TO 'workoutClient'@'localhost';
FLUSH PRIVILEGES;