-- Load data into the exercises table
LOAD DATA LOCAL INFILE 'data.csv' INTO TABLE exercises
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' 
IGNORE 1 ROWS (@Title, @Desc, @Type, @BodyPart, @Equipment, @Level)
SET
    exercise_name = @Title,
    description = @Desc,
    exercise_type = @Type,
    target_group = @BodyPart,
    equipment = @Equipment,
    difficulty_level = @Level;