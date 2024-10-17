README -
This is the final proect for CS 121: Workout Routine and Maker. The goal for
this project was to create a database that can help users create their own
workout routines, track their workouts, and even track their progress. This
database supports a certain number of command-line queries as well as admin
and clinet logins. Folow the insstructions below to try it out for yourself.
Thank you!

Contributors: Dominic Borges and Donavan Borges

Data source: 
https://www.kaggle.com/datasets/niharika41298/gym-exercise-data

NOTE: THIS PROGRAM IS TESTED ON MySQL server version 8.3.0.

Instructions for loading data on command-line:
Make sure you have MySQL downloaded and available through your
device's command-line.

First, launch mySQL:

$ mysql --local-infile=1 -u root -p

Create an appropriate database in mySQL:

mysql> CREATE DATABASE workoutdb;
mysql> USE workoutdb;


Not including the "mysql>" prompt, run the following lines of code on your command-line
after creating and using an appropriate database:

mysql> source setup.sql;
mysql> source load-data.sql;
mysql> source setup-passwords.sql;
mysql> source setup-routines.sql;
mysql> source grant-permissions.sql;
mysql> source queries.sql;

Instructions for Python program:
Please install the Python MySQL Connector using pip3 if not installed already.

After loading the data and verifying you are in the correct database, 
run the following to open the python application:

mysql> quit;

$ python3 app-client.py

OR

$ python3 app-admin.py

Please log in with the following user/passwords:

For app_client.py, the following customers are registered:
    USER            | PASSWORD
    create your own | create your own

For app_admin.py, the following admins are registered:
    USER         | PASSWORD
    workoutAdmin | adminPassword

Here is a suggested guide to using app_client.py:
    1. Create an account (if you dont already have one)
    2. Select option (1) to create a new workout routine
    3. Select option (6) to view your new workout routine
    4. Select option (2) to log a workout session
    5. Select option (3) to view your progress
    6. Select option (5) to view you profile
    7. Select option (4) to update your profile

Here is a suggested guide to using app_admin.py:
    1. Select option (5) to view users using the database
    2. Select option (6) to delete any users
    3. Select option (4) to view system analytics
    4. Select option (1), (2), or (3) to manage the database

Files written to user's system:
- No files are written to the user's system.

Unfinished features:
- Rigorous checks to make sure that all of the functions are running perfectly
- Getting rid of redundant datasets/cleanup in general.
- Some of the functions for both the admin and clients may be a little unfinished with a few bugs
- There might be a few bugs when running create_workout_routine as the database was messy