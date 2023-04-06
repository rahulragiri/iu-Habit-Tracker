from datetime import datetime, timedelta

from db import get_streak, get_period, get_checked_at, insert_habit_into_db, check_off_habit, update_habit_streak, \
    delete_habit


class Habit:
    def __init__(self, habit_name: str, habit_description: str, period: str):
        """
        constructs each new habit
        :param habit_name: the name of the habit
        :param habit_description: description of the habit
        :param period: duration of the habit
        """
        self.habit_name = habit_name
        self.habit_description = habit_description
        self.period = period
        self.streak = 0
        self.checked_at = None

    def __repr__(self):
        """
        :return: printable representation of an object
        """
        return f"{self.habit_name}:{self.habit_description}:{self.period}"

    def increase_streak(self, conn):
        """
        :param conn: a connection to a sqlite3 database
        :return: increment the streak by 1
        """
        self.streak = get_streak(conn, self.habit_name)
        self.streak += 1

    def reset_streak(self):
        """
        :return: brings the streak back to 1
        """
        self.streak = 1

    def create_new_habit(self, conn):
        """
        creates new habit and inserts it into database
        :param conn: a connection to a sqlite3 database
        :return: inserts new habit into database
        """
        insert_habit_into_db(conn, self.habit_name, self.habit_description, self.period)

    def update_habit(self, conn):
        """
        ticks off a habit and increases streak
        :param conn: a connection to a sqlite3 database
        :return: increases habit streak by one
        """
        self.increase_streak(conn)
        check_off_habit(conn, self.habit_name, self.period, self.streak)
        update_habit_streak(conn, self.habit_name, self.streak)

    def reset_habit_streak(self, conn):
        """
        resets streak
        :param conn: a connection to a sqlite3 database
        :return: resets the streak to one
        """
        self.reset_streak()
        update_habit_streak(conn, self.habit_name, self.streak)
        self.checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        check_off_habit(conn, self.habit_name, self.period, self.streak, self.checked_at)

    def checkoff_habit(self, conn, test_date=None):
        """
         if period is daily, cant check-off for next 24hrs and, 7 days if period is weekly, after completing habit
        :param test_date: this parameter is for testing purpose
        :param conn: a connection to a sqlite3 database
        :return: check-off a habit, increments a streak by 1

        """
        streak = get_streak(conn, self.habit_name)
        period = self.period = get_period(conn, self.habit_name)
        checkoff_logs = get_checked_at(conn, self.habit_name)

        if streak == 0:
            self.update_habit(conn)
            print('\x1b[6;30;42m' + f"{self.habit_name} checked-off successfully." + '\x1b[0m')

            # check daily habits
        else:
            if period == "Daily":
                # this line of code makes checkoff_logs into str
                logs_list = [i[0] for i in checkoff_logs]
                last_checked_logs = logs_list[-1]
                last_checked = datetime.strptime(last_checked_logs, "%Y-%m-%d %H:%M:%S").date()

                if test_date is not None:
                    today = test_date
                else:
                    today = datetime.now().date()

                if last_checked == today:
                    print(
                        '\x1b[6;30;42m' + "cannot check-off this habit Since you already completed this habit today, come back tomorrow." + '\x1b[0m')

                else:
                    if (today - last_checked).days == 1:
                        self.update_habit(conn)
                        print('\x1b[6;30;42m' + "Habit checked off successfully." + '\x1b[0m')

                    else:
                        self.reset_habit_streak(conn)
                        print(
                            '\x1b[6;30;42m' + "Habit checked off successfully, but streak reset to 1 because you broke the streak." + '\x1b[0m')

            # checks Weekly habits
            if period == "Weekly":
                logs_list = [i[0] for i in checkoff_logs]
                last_checked_logs = logs_list[-1]
                last_checked = datetime.strptime(last_checked_logs, "%Y-%m-%d %H:%M:%S").date()

                if test_date is not None:
                    today = test_date
                else:
                    today = datetime.now().date()

                if (today - last_checked).days < 7:
                    deadline = last_checked + timedelta(days=6)
                    time_diff = deadline - datetime.now().date()
                    total_seconds = time_diff.total_seconds()
                    days = int(total_seconds // 86400)
                    print(
                        '\x1b[6;30;42m' + f"Habit already checked-off this Week, wait {days} days to check-off again" + '\x1b[0m')

                else:
                    if (today - last_checked).days == 7:
                        self.update_habit(conn)
                        print('\x1b[6;30;42m' + "Weekly habit checked off successfully." + '\x1b[0m')

                    elif (today - last_checked).days > 7:
                        self.reset_habit_streak(conn)
                        print(
                            '\x1b[6;30;42m' + "Habit checked off successfully, but streak reset to 1 because you broke the streak." + '\x1b[0m')

    def remove_habit(self, conn):
        """
        takes a habit out of the database.
        :param conn: a connection to a sqlite3 database
        :return: removes a habit from the database
        """
        delete_habit(conn, self.habit_name)
