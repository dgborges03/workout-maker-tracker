"""
This file is to create the login process for both the admin and the client.
It is shared with the app-admin.py and app-client.py files.
"""

import mysql.connector
import hashlib
import os


def get_conn():
    """
    Establishes a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host='localhost',
        user='workoutClient',
        password='clientPassword',
        database='workoutdb'
    )


def generate_salt():
    """
    Generates a salt for password hashing.
    """
    return os.urandom(4).hex()


def authenticate_user(username, password):
    """
    Authenticates a user by checking the input password against the stored 
    password hash.
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT salt, password_hash FROM user_info WHERE username = %s", 
                   (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        salt = user['salt']
        stored_hash = user['password_hash']

        hashed_input_password = hashlib.sha256((salt + 
                                                password).encode()).hexdigest()

        if hashed_input_password == stored_hash:
            return True  # Authentication successful
        else:
            return False  # Password does not match
    else:
        return False  # User not found


def create_user_account(username, password, email, weight, height, gender, 
                        fitness_level, role='user'):
    """
    Creates a new user account.
    """
    conn = get_conn()
    cursor = conn.cursor()
    salt = os.urandom(8).hex()
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    
    users_sql = """
    INSERT INTO users (username, email, weight, height, gender, fitness_level)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    user_info_sql = """
    INSERT INTO user_info (username, salt, password_hash, role)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        cursor.execute(users_sql, (username, email, weight, height, gender, 
                                   fitness_level))
        cursor.execute(user_info_sql, (username, salt, hashed_password, role))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating new user: {err}")
        conn.rollback()
        return False