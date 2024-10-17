"""
Student name(s): Donavan Borges, Dominic Borges
Student email(s): dborges@caltech.edu, ddborges@caltech.edu

This is the client program for our Workout Routine and Maker. This script allows
for users to interact with the applications using a command-line interface. The
users will be allowed to log in or sign up, create workout routines, log workouts
view their progress, update any needed information, etc.

"""
import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
from login import authenticate_user, create_user_account
import random

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
          user='workoutClient',
          port='3306',
          password='clientPassword',
          database='workoutdb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Logging Users In / Sign up (LOG IN is found within login.py)
# ----------------------------------------------------------------------
def sign_up():
    """
    llows users to sign up for a new account.
    """
    print("\nSign up for a new account")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    email = input("Enter your email: ")
    weight = input("Enter your weight (lbs): ")
    height = input("Enter your height (in): ")
    gender = input("Enter your gender (Male/Female/Other): ")
    fitness_level = input("Enter your fitness level (Beginner/Intermediate/Expert): ")

    # create_user_account still needs to be created within the login.py
    if create_user_account(username, password, email, weight, height, gender, fitness_level):
        print("Account created successfully! Please log in.\n")
    else:
        print("Failed to create account. Please try again.\n")


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print("Welcome to Workout Routine Maker and Tracker!")
    print("  (1) Create a new workout routine")
    print("  (2) Log a workout session")
    print("  (3) View my progress")
    print("  (4) Update my profile")
    print("  (5) View my profile")
    print("  (6) View my workout routine")
    print("  (q) Quit")
    choice = input("What would you like to do? ")
    return choice

# Function to create a new workout routine
def create_workout_routine(conn, user_id):
    """
    Creates a new workout routine based on the user's fitness level.
    """
    cursor = conn.cursor()

    # This gets the user's fitness level
    cursor.execute("SELECT fitness_level FROM users WHERE user_id = %s", (user_id,))
    fitness_level_result = cursor.fetchone()

    if fitness_level_result:
        fitness_level = fitness_level_result[0]
        print(f"Fetched fitness level: {fitness_level}")

        # This fetches exercises that match the user's fitness level
        cursor.execute("""
            SELECT exercise_id FROM exercises
            WHERE difficulty_level = %s
        """, (fitness_level,))
        exercises = cursor.fetchall()

        if len(exercises) >= 3:
            selected_exercises = random.sample(exercises, 3)

            routine_name = input("Enter a name for the new routine: ")
            start_date = input("Enter the start date for the routine (YYYY-MM-DD): ")
            end_date = input("Enter the end date for the routine (YYYY-MM-DD): ")

            for exercise_id_tuple in selected_exercises:
                exercise_id = exercise_id_tuple[0]
                cursor.execute("""
                    INSERT INTO routine (user_id, exercise_id, routine_name, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, exercise_id, routine_name, start_date, end_date))

            conn.commit()
            print("Workout routine created successfully.")
        else:
            print("Not enough exercises available for this fitness level to create a routine.")
    else:
        print("User fitness level not found.")

# Function to view and delete routine
def view_and_delete_workout_routine(conn, user_id):
    """
    Displays and allows the user to delete their workout routines.
    """
    cursor = conn.cursor()

    # Display existing routines with exercises
    cursor.execute("""
        SELECT r.routine_id, r.routine_name, r.start_date, r.end_date, e.exercise_name, e.target_group, r.sets, r.reps, r.suggested_weight, r.duration
        FROM routine r
        JOIN exercises e ON r.exercise_id = e.exercise_id
        WHERE r.user_id = %s
    """, (user_id,))
    routines = cursor.fetchall()

    if not routines:
        print("No workout routines found for this user.")
        return

    print(f"Workout routines for user ID {user_id}:")
    for routine in routines:
        routine_id, routine_name, start_date, end_date, exercise_name,target_group, sets, reps, suggested_weight, duration = routine
        print(f"Routine ID: {routine_id}")
        print(f"Routine Name: {routine_name}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Exercise: {exercise_name}")
        print(f"Target Body Part: {target_group}")
        print(f"Sets: {sets}")
        print(f"Reps: {reps}")
        print(f"Suggested Weight: {suggested_weight}")
        print(f"Duration: {duration} minutes")
        print("------------------------")

    try:
        selected_id = int(input("Enter the ID of the routine you want to delete (0 to cancel): "))
        if selected_id == 0:
            return
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return

    confirm = input(f"Are you sure you want to delete the routine with ID {selected_id}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return

    cursor.execute("""
        DELETE FROM routine
        WHERE user_id = %s AND routine_id = %s
    """, (user_id, selected_id))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"Routine with ID {selected_id} deleted successfully.")
    else:
        print(f"No routine found with ID {selected_id} for this user, or deletion failed.")


# Function to log a workout session
def log_workout_session(conn):
    """
    Logs a workout session for the user.
    """
    print("\nLog a workout session:")
    user_id = input("Enter your user ID: ")
    routine_id = input("Enter your routine ID: ")
    log_date = input("Enter the workout date (YYYY-MM-DD): ")
    sets_completed = input("Enter the number of sets completed: ")
    reps_completed = input("Enter the number of reps completed: ")
    weight_used = input("Enter the weight used (optional, press enter to skip): ")

    sql = """
    INSERT INTO logs (user_id, routine_id, log_date, sets_completed, reps_completed, weight_used)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, routine_id, log_date, sets_completed,
                             reps_completed, weight_used or None))
        conn.commit()
        print("Workout session logged successfully.")
    except mysql.connector.Error as err:
        print(f"Error logging workout session: {err}")

# Function to view workout progress
def view_progress(conn):
    """
    Displays the user's workout progress.
    """
    print("\nView my progress:")
    user_id = input("Enter your user ID: ")

    # Example query
    sql = """
    SELECT routine_name, start_date, end_date
    FROM routine
    WHERE user_id = %s AND end_date <= CURDATE()
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        routines = cursor.fetchall()
        print("Completed routines:")
        for routine in routines:
            print(routine)
    except mysql.connector.Error as err:
        print(f"Error viewing progress: {err}")

# Function to update profile
def update_profile(conn):
    """
    Updates the user's profile information.
    """
    print("\nUpdate my profile:")
    username = input("Enter your username: ")
    new_weight = input("Enter your new weight (lbs, optional, press enter to skip): ")
    new_height = input("Enter your new height (in, optional, press enter to skip): ")
    new_fitness_level = input("Enter your new fitness level (Beginner/Intermediate/Expert, optional, press enter to skip): ")

    updates = []
    parameters = []

    if new_weight:
        updates.append("weight = %s")
        parameters.append(new_weight)

    if new_height:
        updates.append("height = %s")
        parameters.append(new_height)

    if new_fitness_level:
        updates.append("fitness_level = %s")
        parameters.append(new_fitness_level)

    if not updates:
        print("No updates provided.")
        return

    sql = f"UPDATE users SET {', '.join(updates)} WHERE username = %s"
    parameters.append(username)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, parameters)
        conn.commit()
        print("Profile updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating profile: {err}")

# Function to view profile
def view_user_profile(conn, username):
    """
    Displays the user's profile information.
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    profile = cursor.fetchone()

    if profile:
        print("User Profile:")
        for key, value in profile.items():
            print(f"{key}: {value}")
    else:
        print("User profile not found.")

# Helper function
def get_user_id(conn, username):
    """
    Retrieves the user ID based on the username.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def main():
    """
    Main function for starting things up.
    """
    print("Welcome to the Workout Routine Maker and Tracker!")
    action = input("Do you have an account? (yes/no): ").lower()

    if action == 'no':
        sign_up()

    username = input("Username: ")
    password = input("Password: ")
    if authenticate_user(username, password):
        print("Login successful!\n")
        user_id = get_user_id(conn, username)
        while True:
            choice = show_options()
            if choice == 'q':
                print("Exiting Workout Routine Maker and Tracker. Goodbye!")
                break
            elif choice == '1':
                create_workout_routine(conn, user_id)
            elif choice == '2':
                log_workout_session(conn)
            elif choice == '3':
                view_progress(conn)
            elif choice == '4':
                update_profile(conn)
            elif choice == '5':
                view_user_profile(conn, username)
            elif choice == '6':
                view_and_delete_workout_routine(conn, user_id)
            else:
                print("Invalid option, please try again.")
    else:
        print("Login failed. Please try again or sign up if you don't have an account.")



if __name__ == '__main__':
    conn = get_conn()
    main()
