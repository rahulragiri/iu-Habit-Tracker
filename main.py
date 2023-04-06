import re
import inquirer
from habit import Habit
from db import connect_db, check_if_habit_exists, get_period, add_predefined_habits
from analytics import return_all_habits_data, return_longest_streak_of_all, return_longest_streak_of_habit, \
    return_habits_with_same_periodicity, return_longest_streak_of_periodicity

print("\n")
print("\n")


def main():
    """launches the main programme allowing you to use the habit tracking tools."""
    print("\n")
    print("------------------------HABIT TRACKER----------------------")
    print("To make your selection, use the arrows. To terminate the application press Ctrl+C")
    print("\n")

    connection = connect_db()
    try:
        add_predefined_habits(connection)

        choice = inquirer.list_input("What do you want to do: ",
                                     choices=["1. Create new habit", "2. Check-off habit", "3. Analyze your habits",
                                              "4. Delete your habit", "5. Exit"])

        # Creates new habit
        if choice == "1. Create new habit":
            habit_name = input("Enter the name of the habit you want to create: ")
            habit_description = input("Enter Description of your habit: ")
            print("\n")

            # checks if the input given by user is empty or numbers
            while not re.match("^[a-z A-Z]+$", habit_name):
                print("\n")
                print('\x1b[6;30;42m' + "Only text is allowed" + '\x1b[0m')
                habit_name = input("Enter the name of the habit you want to create: ")
                print("\n")
                print('\x1b[6;30;42m' + "Now, enter valid description" + '\x1b[0m')
                habit_description = input("Enter Description of your habit: ")
                print("\n")

            periodicity_choice = [
                inquirer.List('period', message="How often you want to do the task", choices=['Daily', 'Weekly']),
            ]

            periodicity = inquirer.prompt(periodicity_choice)
            period = periodicity["period"]
            print('\x1b[6;30;42m' + "you selected", periodicity["period"] + '\x1b[0m')
            print('\x1b[6;30;42m' + f"'{habit_name}' created successfully" + '\x1b[0m')
            print("\n")

            habit = Habit(habit_name, habit_description, period)
            habit.create_new_habit(connection)
            main()

        # check-off habit
        elif choice == "2. Check-off habit":

            habit_name = input("Enter the name of the habit you want to check-off: ")
            period = get_period(connection, habit_name)

            while not re.match("^[a-z A-Z]+$", habit_name):
                print('\x1b[6;30;42m' + "Only text is allowed" + '\x1b[0m')
                habit_name = input("Enter the name of the habit you want to check-off: ")

            if check_if_habit_exists(connection, habit_name):
                print('\x1b[6;30;42m' + "can't check-off, habit you entered doesn't exist" + '\x1b[0m')
                print("\n")
            else:
                habit = Habit(habit_name, "NULL", period)
                habit.checkoff_habit(connection)
                main()

        # analyze your habits
        elif choice == "3. Analyze your habits":

            analytics_choice = [
                inquirer.List('analyze', message="select what you want to know?: ", choices=[
                    '1. Show all of your current habits.',
                    '2. Display all habits with the same periodicity.',
                    '3. Return the longest streak, among all defined habits.',
                    '4. Return the longest streak of specific habit.',
                    '5. Return the longest streak of a habit with same periodicity.'

                ])
            ]
            analytics = inquirer.prompt(analytics_choice)

            if analytics["analyze"] == '1. Show all of your current habits.':
                return return_all_habits_data(connection)

            elif analytics["analyze"] == '2. Display all habits with the same periodicity.':
                periodicity_choice = [
                    inquirer.List('period', message="select periodicity to analyze", choices=['Daily', 'Weekly']),
                ]

                periodicity = inquirer.prompt(periodicity_choice)
                period = periodicity["period"]
                print('\x1b[6;30;42m' + "you selected", periodicity["period"] + '\x1b[0m')
                print("\n")
                return return_habits_with_same_periodicity(connection, period)

            elif analytics["analyze"] == '3. Return the longest streak, among all defined habits.':
                return return_longest_streak_of_all(connection)

            elif analytics["analyze"] == '4. Return the longest streak of specific habit.':

                get_name = [
                    inquirer.Text('name', message="Enter name of the habit")
                ]
                hb_name = inquirer.prompt(get_name)
                habit_name = hb_name["name"]
                return return_longest_streak_of_habit(connection, habit_name)

            elif analytics["analyze"] == '5. Return the longest streak of a habit with same periodicity.':

                periodicity_choice = [
                    inquirer.List('period', message="Select periodicity to analyze", choices=['Daily', 'Weekly']),
                ]

                periodicity = inquirer.prompt(periodicity_choice)
                period = periodicity["period"]
                print('\x1b[6;30;42m' + "you selected", periodicity["period"] + '\x1b[0m')
                print("\n")
                return return_longest_streak_of_periodicity(connection, period)

        # Deletes your habit
        elif choice == "4. Delete your habit":

            habit_name = input("Enter the name of the habit you want to delete: ")

            while not re.match("^[a-z A-Z]+$", habit_name):
                print('\x1b[6;30;42m' + "Only text is allowed" + '\x1b[0m')
                habit_name = input("Enter the name of the habit you want to create: ")

            habit = Habit(habit_name, "NULL", "NULL")

            if check_if_habit_exists(connection, habit_name):
                print('\x1b[6;30;42m' + "habit you entered doesn't exist" + '\x1b[0m')
                main()
            else:
                habit.remove_habit(connection)
                print('\x1b[6;30;42m' + f"'{habit_name}' deleted successfully" + '\x1b[0m')
                main()

        # Exit
        elif choice == "5. Exit":
            print('\x1b[6;30;42m' + 'Successfully exited from application' + '\x1b[0m')
            print("\n")
            exit()

    except (KeyboardInterrupt, TypeError, IndexError):
        print("\n")
        print('\x1b[6;30;42m' + 'User interrupted the application. Please retry!' + '\x1b[0m')


if __name__ == '__main__':
    main()
