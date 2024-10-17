"""
Student name(s): Donavan Borges, Dominic Borges
Student email(s): dborges@caltech.edu, ddborges@caltech.edu

This is the admin program for our Workout Routine and Maker. This script allows
for admins to manage the applications data by allowing access to adding,
updating, deleting exercices. It also allows for admins to view and manage
the application's analytics, and it allows for admin to view and manage users.
"""
import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
from login import authenticate_user
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='workoutAdmin',
          port='3306',
          password='adminPassword',
          database='workoutdb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if DEBUG:
            print(f'Error connecting to database: {err}', file=sys.stderr)
        else:
            print('An error occurred, please contact the administrator.', 
                  file=sys.stderr)
        sys.exit(1)



# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
# Function for the UI
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print("Admin Panel - Workout Routine Maker and Tracker")
    print("  (1) Add a new exercise")
    print("  (2) Update an exercise")
    print("  (3) Delete an exercise")
    print("  (4) View system analytics")
    print("  (5) View Users")
    print("  (6) Delete Users")
    print("  (q) Quit")
    choice = input("Select an option: ")
    return choice

# Function to add new exercise
def add_exercise(conn):
    """
    Adds a new exercise to the database based on user input.
    """
    exercise_name = input("Enter exercise name: ")
    exercise_type = input("Enter exercise type: ")
    target_group = input("Enter target muscle group: ")
    equipment = input("Enter required equipment: ")
    difficulty_level = input("Enter difficulty level: ")

    sql = "INSERT INTO exercises (exercise_name, exercise_type, target_group, equipment, difficulty_level) " \
          "VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (exercise_name, exercise_type, target_group,
         equipment, difficulty_level))
        conn.commit()
        print("Exercise added successfully.")
    except mysql.connector.Error as err:
        print(f"Error adding exercise: {err}") 

# Function to update an exercise
def update_exercise(conn):
    """
    Updates an existing exercise in the database based on user input.
    """
    exercise_id = input("Enter the ID of the exercise to update: ")
    new_name = input("Enter the new name of the exercise: ")

    sql = "UPDATE exercises SET exercise_name = %s WHERE exercise_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (new_name, exercise_id))
        conn.commit()
        print("Exercise updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating exercise: {err}")

# Function to delete an exercise
def delete_exercise(conn):
    """
    Deletes an existing exercise from the database based on user input.
    """
    exercise_id = input("Enter the ID of the exercise to delete: ")

    sql = "DELETE FROM exercises WHERE exercise_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (exercise_id,))
        conn.commit()
        print("Exercise deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting exercise: {err}")

# Function to view analytics
def view_analytics(conn):
    """
    Displays system analytics by executing an example SQL query 
    """
    sql = "SELECT exercise_type, COUNT(*) FROM exercises GROUP BY exercise_type"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error retrieving analytics: {err}")

# Function to view users
def view_users(conn):
    """
    Displays a list of users and their information from the database.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, email, fitness_level FROM users")
        users = cursor.fetchall()
        if users:
            print("List of Users:")
            for user in users:
                user_id, username, email, fitness_level = user
                print(f"User ID: {user_id}, Username: {username}, Email: {email}, Fitness Level: {fitness_level}")
        else:
            print("No users found.")
    except mysql.connector.Error as err:
        print(f"Error retrieving users: {err}")

# Function to delete a user
def delete_user(conn):
    """
    Deletes a user from the database based on user input.
    """
    user_id = input("Enter the ID of the user to delete: ")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        print("User deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error deleting user: {err}")


def main():
    """
    Main function for starting things up.
    """
    print("Admin Panel - Workout Routine Maker and Tracker")
    username = input("Username: ")
    password = input("Password: ")

    # Decided to hard code the username and password for admin
    admin_username = 'workoutAdmin'
    admin_password = 'adminPassword'

    authenticated = False
    if username == admin_username and password == admin_password:
        conn = get_conn()
        if conn.is_connected():
            authenticated = True
            print("Admin login successful.")
        else:
            print("Failed to connect to the database as admin.")
    else:
        authenticated = authenticate_user(username, password)
        if authenticated:
            print("Regular user login successful.")
        else:
            print("Regular user login failed.")

    if authenticated:
        print("Login successful!\n")
        while True:
            choice = show_admin_options()
            if choice == 'q':
                print("Exiting Admin Panel. Goodbye!")
                break
            elif choice == '1':
                add_exercise(conn)
            elif choice == '2':
                update_exercise(conn)
            elif choice == '3':
                delete_exercise(conn)
            elif choice == '4':
                view_analytics(conn)
            elif choice == '5':
                view_users(conn)
            elif choice == '6':
                delete_user(conn)
            else:
                print("Invalid option, please try again.")
    else:
        print("Login failed. Please try again.")


if __name__ == '__main__':
    conn = get_conn()
    main()
