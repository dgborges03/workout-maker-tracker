CREATE TABLE user_info (
    username VARCHAR(20) PRIMARY KEY,
    salt CHAR(16) NOT NULL,
    password_hash CHAR(64) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);

-- Function to generate a salt
DELIMITER !
CREATE FUNCTION make_salt()
RETURNS CHAR(16) DETERMINISTIC
BEGIN
    RETURN SUBSTRING(SHA2(RAND(), 256), 1, 16);
END !
DELIMITER ;

-- Procedure to add a new user
DELIMITER !
CREATE PROCEDURE sp_add_user(IN new_username VARCHAR(20), 
IN new_password VARCHAR(20), IN user_role ENUM('admin', 'user'))
BEGIN
    DECLARE new_salt CHAR(16);
    DECLARE hashed_password CHAR(64);

    SET new_salt = make_salt();
    SET hashed_password = SHA2(CONCAT(new_salt, new_password), 256);

    INSERT INTO user_info (username, salt, password_hash, role) 
    VALUES (new_username, new_salt, hashed_password, user_role);
END !
DELIMITER ;

-- Function to authenticate a user
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE db_salt CHAR(16);
    DECLARE db_hash CHAR(64);
    DECLARE check_hash CHAR(64);

    SELECT salt, password_hash 
    INTO db_salt, db_hash FROM user_info 
    WHERE username = username;
    
    IF db_salt IS NULL THEN
        RETURN 0; 
    END IF;
    
    SET check_hash = SHA2(CONCAT(db_salt, password), 256);
    
    IF check_hash = db_hash THEN
        RETURN 1;
    ELSE
        RETURN 0; 
    END IF;
END !
DELIMITER ;

-- Procedure to change a user's password
DELIMITER !
CREATE PROCEDURE 
sp_change_password(IN in_username VARCHAR(20), IN in_new_password VARCHAR(20))
BEGIN
    DECLARE new_salt CHAR(16);
    DECLARE new_hashed_password CHAR(64);

    SET new_salt = make_salt();
    SET new_hashed_password = SHA2(CONCAT(new_salt, in_new_password), 256);

    UPDATE user_info
    SET salt = new_salt,
        password_hash = new_hashed_password 
    WHERE username = in_username;
END !
DELIMITER ;
