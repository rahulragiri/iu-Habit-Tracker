from db import get_habits_data, get_longest_streak, get_longest_streak_of_habit, get_habit_with_periodicity, \
    check_if_habit_exists, get_checked_at, get_longest_streak_of_periodicity


def return_all_habits_data(conn):
    """
    all data of the habits that are currently being tracked
    :param conn: a connection to a sqlite3 database
    :return: list of all habits data
    """

    habits_info = get_habits_data(conn)
    print(f"At present you have {len(habits_info)} habits:")
    print("\n")
    habits_list = []
    for habits in habits_info:
        print(f"Habit Name        : {habits[1]}")
        print(f"Habit description : {habits[2]}")
        print(f"Period            : {habits[3]}")
        print(f"Date Created      : {habits[4]}")
        print(f"Streak            : {habits[5]}")
        print("\n")
        habits_list.append(habits)
    return habits_list


def return_longest_streak_of_all(conn):
    """
    :param conn: a connection to a sqlite3 database
    :return: the longest streak of all habits
    """
    habits_info = get_longest_streak(conn)
    print("----------Longest streak among all habits----------")

    length_of_habits_list = len(habits_info)
    print(f"You have {length_of_habits_list} habit with longest streak")

    longest_streaks = []
    for habits in habits_info:
        streak = habits[1]
        if streak == 0:
            print("No longest streak found")
            break
        else:
            print("\n")
            print(f"Habit Name              : {habits[0]}")
            print(f"Streak                  : {habits[1]}")
            print("\n")
            longest_streaks.append(habits[1])
    return longest_streaks[0]


def return_longest_streak_of_habit(conn, habit_name):
    """
    returns the longest streak of given habit
    :param conn: a connection to a sqlite3 database
    :param habit_name: the name of the habit
    :return: the longest streak of specific habit
    """
    longest_habit_streak = get_longest_streak_of_habit(conn, habit_name)
    streak = longest_habit_streak
    checked_at = get_checked_at(conn, habit_name)

    if check_if_habit_exists(conn, habit_name):
        print('\x1b[6;30;42m' + "Habit doesn't exists please enter correct habit name" + '\x1b[0m')

    elif not checked_at:
        print('\x1b[6;30;42m' + "habit you entered doesn't have any streak" + '\x1b[0m')

    else:
        logs_list = [i[0] for i in checked_at]
        last_checked = logs_list[-1]
        print("\n")
        print('\x1b[6;30;42m' + f"Longest streak of {habit_name} is {streak} which was last checked on {last_checked}" + '\x1b[0m')
        print("\n")
    return streak


def return_habits_with_same_periodicity(conn, period):
    """
    returns the habits with same periodicity
    :param conn: a connection to a sqlite3 database
    :param period: periodicity of the habit
    :return: list of all habits with specific periodicity
    """

    habits_info = get_habit_with_periodicity(conn, period)

    if len(habits_info) == 0:
        print('\x1b[6;30;42m' + f"no '{period}' habits found" + '\x1b[0m')
    else:
        print('\x1b[6;30;42m' + f"Your List of {period} habits are:" + '\x1b[0m')

        habit_names = []

        for habits in habits_info:
            print(f"------------------{habits[1]}-------------------")
            print(f"Habit Description : {habits[2]}")
            print(f"Date Created      : {habits[4]}")
            print(f"Streak            : {habits[5]}")
            print("\n")
            habit_names.append(habits[1])
        return habit_names


def return_longest_streak_of_periodicity(conn, period):
    """
    returns the longest streak of habit with same periodicity
    :param conn: a connection to a sqlite3 database
    :param period: periodicity of the habit
    :return: the longest streak of habit with specific periodicity
    """
    longest_streak_of_periodicity = get_longest_streak_of_periodicity(conn, period)
    streak = longest_streak_of_periodicity[0][0]
    habit_name = longest_streak_of_periodicity[0][1]

    if habit_name is None:
        print('\x1b[6;30;42m' + f"no '{period}' habits found" + '\x1b[0m')

    else:
        if streak == 0:

            print("Selected periodicity doesn't have the longest streak")
            print("\n")
        else:
            print('\x1b[6;30;42m' + f"Among all {period} habits, '{habit_name}' has the longest streak of {streak}" + '\x1b[0m')
    return streak
