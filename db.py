import sqlite3
from datetime import datetime


def create_tables(conn):
    """
    generates the necessary database tables
    :param conn: a connection to a sqlite3 database
    """
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS habits_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_name TEXT,
    habit_description TEXT,
    period TEXT,
    date_created DATETIME,  
    streak INTEGER )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS habits_tracker (
    habit_name TEXT,
    period TEXT,
    current_streak INTEGER,
    checked_at DATETIME,
    FOREIGN KEY (habit_name) REFERENCES habits_data(habit_name),
    FOREIGN KEY (period) REFERENCES habits_data(period) )
    """)

    conn.commit()


def connect_db(name="main.db"):
    """
    establishes the connection to the sqlite3 database.
    :param name: the database's title
    :return: creates a sqlite3 database and establishes a connection to it.
    """
    conn = sqlite3.connect(name)
    create_tables(conn)
    return conn


def insert_habit_into_db(conn, habit_name, habit_description, period, streak=0):
    """
    inserts a new habit into the database
    :param conn: an association with a sqlite3 database
    :param habit_name: The name of the habit
    :param habit_description: A simple explanation of the habit
    :param period: The duration of the habit
    :param streak: streak of the habit
    """
    c = conn.cursor()
    c.execute("SELECT habit_name FROM habits_data WHERE habit_name=?", (habit_name,))
    record = c.fetchone()
    if record:
        print("Habit already exists in database")
    else:
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO habits_data VALUES (NULL,?,?,?,?,?)",
                  (str(habit_name), str(habit_description), str(period), date_created, streak))
        conn.commit()


def check_off_habit(conn, habit_name, period, current_streak=0, checked_at=None):
    """
    Increases a habit streak by one after checking a habit.
    :param period: period of the habit
    :param checked_at: the time when habit was checked-off
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :param current_streak: current streak of the habit
    """
    if not checked_at:
        checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    c.execute("INSERT INTO habits_tracker VALUES(?,?,?,?)", (habit_name, period, current_streak, checked_at))
    conn.commit()


def update_habit_streak(conn, habit_name, streak):
    """
    updates the streak value in the habits_data table.
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :param streak: streak of the habit to update
    """
    c = conn.cursor()
    c.execute("UPDATE habits_data SET streak=? WHERE habit_name=?", (streak, habit_name))
    conn.commit()


def update_habit_tracker_streak(conn, habit_name, current_streak):
    """

    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :param current_streak: streak of the habit to update
    """
    c = conn.cursor()
    c.execute("UPDATE habits_tracker SET current_streak=? WHERE habit_name=?", (current_streak, habit_name))
    conn.commit()


def delete_habit(conn, habit_name):
    """
    Remove the given habit from the database.
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    """
    c = conn.cursor()
    c.execute("DELETE FROM habits_data WHERE habit_name=?", (habit_name,))
    c.execute("DELETE FROM habits_tracker WHERE habit_name=?", (habit_name,))
    conn.commit()


def check_if_habit_exists(conn, habit_name):
    """
    checks to see if a specific habit is already present in the database.
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :return: True, if the habit is recorded in the database already
    """
    c = conn.cursor()
    c.execute("SELECT habit_name FROM habits_data WHERE habit_name=?", (habit_name,))
    record = c.fetchall()
    if not record:
        return True
    else:
        return False


def get_habits_data(conn):
    """
    retrieves all habits data from database
    :param conn: a connection to a sqlite3 database
    :return: every entry from the habits_data table
    """
    c = conn.cursor()
    c.execute("SELECT * FROM habits_data")
    return c.fetchall()


def get_streak(conn, habit_name):
    """
    retrieve the streak from the habit_data table
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :return: streak from habits_data table
    """
    c = conn.cursor()
    c.execute("SELECT streak FROM habits_data WHERE habit_name=?", (habit_name,))
    streaks = c.fetchall()
    return streaks[0][0]


def get_period(conn, habit_name):
    c = conn.cursor()
    c.execute("SELECT period FROM habits_data WHERE habit_name=?", (habit_name,))
    return c.fetchall()[0][0]


def get_checked_at(conn, habit_name):
    c = conn.cursor()
    c.execute("SELECT checked_at FROM habits_tracker WHERE habit_name=?", [habit_name])
    return c.fetchall()


def get_longest_streak(conn):
    """
    returns the longest streak of all defined habits
    :param conn: a connection to a sqlite3 database
    :return: the longest streak of all habits in the habits_data table.
    """
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT habit_name,current_streak FROM habits_tracker WHERE current_streak=(SELECT MAX(current_streak) FROM habits_tracker)")
    return c.fetchall()


def get_longest_streak_of_habit(conn, habit_name):
    """
    the longest streak of specific habit
    :param conn: a connection to a sqlite3 database
    :param habit_name: The name of the habit
    :return: the longest streak from habits_tracker table
    """
    c = conn.cursor()
    c.execute("SELECT MAX(current_streak) FROM habits_tracker WHERE habit_name=?", (habit_name,))
    return c.fetchall()[0][0]


def get_habit_with_periodicity(conn, period):
    """

    :param conn: a connection to a sqlite3 database
    :param period: periodicity of habit
    :return: habits information with a specific periodicity
    """
    c = conn.cursor()
    c.execute("SELECT * FROM habits_data WHERE period=?", (period,))
    return c.fetchall()


def get_longest_streak_of_periodicity(conn, period):
    """
    returns the longest streak of habit with same periodicity
    :param conn: a connection to a sqlite3 database
    :param period: duration of habit
    :return: the longest streak of habit with specific periodicity
    """
    c = conn.cursor()
    c.execute("SELECT DISTINCT MAX(current_streak),habit_name FROM habits_tracker WHERE period=?", (period,))
    return c.fetchall()


def get_habit_name(conn, habit_name):
    c = conn.cursor()
    c.execute("SELECT habit_name FROM habits_data WHERE habit_name=?", (habit_name,))
    return c.fetchone()


def add_predefined_habits(conn):
    predefined_habits = [
        ("cut off alcohol", "limit consumption of alcohol once per week", "Weekly"),
        ("yoga", "do yoga Weekly", "Weekly"),
        ("meditation", "meditate 10 minutes", "Daily"),
        ("quick nap", "sleep 20 minutes afternoon", "Daily")
    ]
    for habit in predefined_habits:
        if check_if_habit_exists(conn, habit[0]) is True:
            insert_habit_into_db(conn, habit[0], habit[1], habit[2])

            if habit[0] == "cut off alcohol":
                # swim 4-weeks data
                check_off_habit(conn, "cut off alcohol", "Weekly", 1, "2023-03-01 00:00:00")
                check_off_habit(conn, "cut off alcohol", "Weekly", 2, "2023-03-08 00:00:00")
                check_off_habit(conn, "cut off alcohol", "Weekly", 1, "2023-03-20 00:00:00")
                check_off_habit(conn, "cut off alcohol", "Weekly", 1, "2023-03-28 00:00:00")
                update_habit_streak(conn, "cut off alcohol", 1)

            if habit[0] == "yoga":
                # cleaning 4-weeks data
                check_off_habit(conn, "yoga", "Weekly", 1, "2023-03-01 00:00:00")
                check_off_habit(conn, "yoga", "Weekly", 2, "2023-03-08 00:00:00")
                check_off_habit(conn, "yoga", "Weekly", 3, "2023-03-15 00:00:00")
                check_off_habit(conn, "yoga", "Weekly", 1, "2023-03-28 00:00:00")
                update_habit_streak(conn, "yoga", 1)

            if habit[0] == "meditation":
                # meditate 4-weeks data
                check_off_habit(conn, "meditation", "Daily", 1, "2023-03-01 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 2, "2023-03-02 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 3, "2023-03-03 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 4, "2023-03-04 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 1, "2023-03-15 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 1, "2023-03-20 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 1, "2023-03-24 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 2, "2023-03-25 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 3, "2023-03-26 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 1, "2023-03-27 00:00:00")
                check_off_habit(conn, "meditation", "Daily", 2, "2023-03-28 00:00:00")
                update_habit_streak(conn, "meditation", 2)

            if habit[0] == "quick nap":
                # quick nap 4-weeks data
                check_off_habit(conn, "quick nap", "Daily", 1, "2023-03-01 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 2, "2023-03-02 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 3, "2023-03-03 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 4, "2023-03-04 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 5, "2023-03-05 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 6, "2023-03-06 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 1, "2023-03-15 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 1, "2023-03-19 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 1, "2023-03-21 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 2, "2023-03-22 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 1, "2023-03-26 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 2, "2023-03-27 00:00:00")
                check_off_habit(conn, "quick nap", "Daily", 3, "2023-03-28 00:00:00")
                update_habit_streak(conn, "quick nap", 3)
