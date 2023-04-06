from habit import Habit
from db import connect_db, insert_habit_into_db, check_off_habit, get_streak, get_habit_name, \
    delete_habit, check_if_habit_exists, add_predefined_habits, update_habit_streak
from analytics import return_all_habits_data, return_longest_streak_of_habit, return_longest_streak_of_all, \
    return_habits_with_same_periodicity, return_longest_streak_of_periodicity
import os
from datetime import datetime, timedelta


class TestHabitTracker:

    db = None

    def setup_method(self):
        self.db = connect_db(name="test.db")
        add_predefined_habits(self.db)

    def test_create_checkoff_update(self):
        insert_habit_into_db(self.db, "jogging", "go to jogging daily", "Daily")
        insert_habit_into_db(self.db, "music", "go to music class", "Weekly")

        # checks if habit is successfully inserted into database
        assert check_if_habit_exists(self.db, "jogging") is False
        assert check_if_habit_exists(self.db, "music") is False

        # test check-off and update habit methods in database.py file
        check_off_habit(self.db, "jogging", "Daily", 1, "2023-03-01 00:00:00")
        update_habit_streak(self.db, "jogging", 1)
        check_off_habit(self.db, "music", "Daily", 1, "2023-03-01 00:00:00")
        update_habit_streak(self.db, "music", 1)

        assert get_streak(self.db, "jogging") == 1
        assert get_streak(self.db, "music") == 1

    def test_all_habit_class_methods(self):

        # creating Habit objects with Habit class and testing all habit functions
        daily_habit = Habit("playing", "playing badminton", "Daily")
        daily_habit.create_new_habit(self.db)
        # test if habit is created
        assert get_habit_name(self.db, "playing")

        # tests if streak can be increments twice a day,
        # im calling checkoff_habit method twice but streak gets incremented only 1 time
        daily_habit.checkoff_habit(self.db)
        daily_habit.checkoff_habit(self.db)

        # checkoff_method called twice but streak is only one
        assert get_streak(self.db, "playing") == 1

        # to increments streak again you need to wait 1 day, so change today to tomorrow and test the checkoff_habit method again
        test_date = datetime.now().date() + timedelta(days=1)
        daily_habit.checkoff_habit(self.db, test_date)

        # test if streak of "playing" is 2 now
        assert get_streak(self.db, "playing") == 2

        # TESTING WEEKLY HABITS
        weekly_habit = Habit("books", "reading books", "Weekly")
        weekly_habit.create_new_habit(self.db)
        assert get_habit_name(self.db, "books")

        # tests if streak can be increments twice in a week, expected: increases only once a week
        weekly_habit.checkoff_habit(self.db)
        weekly_habit.checkoff_habit(self.db)

        assert get_streak(self.db, "books") == 1

        # changing date to next week to test if checkoff_method works as expected
        test_date = datetime.now().date() + timedelta(days=7)
        weekly_habit.checkoff_habit(self.db, test_date)

        assert get_streak(self.db, "books") == 2

        # test remove habit
        daily_habit.remove_habit(self.db)
        assert get_habit_name(self.db, "playing") is None

        weekly_habit.remove_habit(self.db)
        assert get_habit_name(self.db, "books") is None

    def test_get_all_defined_habits(self):
        # four habits were already pre-defined in db.py
        all_habits = return_all_habits_data(self.db)
        assert len(all_habits) == 4

    def test_longest_streak(self):
        # the longest streak of all habits
        longest_streak_of_all_habits = return_longest_streak_of_all(self.db)

        # the longest streak of specific habit
        longest_streak_of_habit = return_longest_streak_of_habit(self.db, "yoga")

        # quick nap has the longest streak of all (6)
        assert longest_streak_of_all_habits == 6
        # longest streak of yoga is 3
        assert longest_streak_of_habit == 3

    def test_get_habit_with_period(self):
        # get daily habits
        get_habits_with_same_periodicity_daily = return_habits_with_same_periodicity(self.db, "Daily")
        daily_list = ["quick nap", "meditation"]
        assert set(get_habits_with_same_periodicity_daily) == set(daily_list)

        # get weekly habits
        get_habits_with_same_periodicity_weekly = return_habits_with_same_periodicity(self.db, "Weekly")
        weekly_list = ["yoga", "cut off alcohol"]
        assert set(get_habits_with_same_periodicity_weekly) == set(weekly_list)

    def test_longest_streak_with_same_period(self):
        # quick nap has the longest streak in daily habits which is 6
        longest_streak_of_daily = return_longest_streak_of_periodicity(self.db, "Daily")
        assert longest_streak_of_daily == 6
        # yoga has the longest streak in weekly habits which is 3
        longest_streak_of_weekly = return_longest_streak_of_periodicity(self.db, "Weekly")
        assert longest_streak_of_weekly == 3

    def test_delete_habit(self):
        delete_habit(self.db, "cut off alcohol")
        assert get_habit_name(self.db, "cut off alcohol") is None
        delete_habit(self.db, "quick nap")
        assert get_habit_name(self.db, "quick nap") is None

    def teardown_method(self):
        self.db.close()
        os.remove("test.db")