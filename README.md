# The Habit Tracking App
***
## Table of content
- [Introduction](#Introduction)
- [Installation](#Installation)
- [Features](#Features)
- [Usage](#Usage)
- [Tests](#Tests)
- [Contribution](#Contribution)

### Introduction
***
The purpose of a habit tracker is to make it simpler for people to create and maintain good habits by providing them with a way of tracking their development and hold themselves accountable.

With the help of habit tracker, you may develop, track, and analyze any kind of habit.

This habit tracking application was developed as a part of a project I was given by the iu International University of Applied Sciences.

### Installation
***
#### Requirements
The following modules are needed for habit tracker to function:
- Python 3.8 or later 
- Inquirer module
- Python test module

#### Installation Instructions
* Install Python 3.8 or a later version on your computer. To check your current Python version, type the following command into the terminal: 
```commandline
python --version
```
* If you're using a Unix or Linux operating system, open a terminal and type:
```commandline
python3 --version
```
* To clone the repository, navigate to the desired directory.
Use this code to clone the repository and download the habit tracker application:

```commandline
git clone https://github.com/rahulragiri/iu_oofpp_habit_tracker_app.git
```
* To download Inquirer module: 
```commandline
pip install inquirer
```
* To download Pytest module:
```commandline
pip install pytest
```
If you wish to download every module needed for the habit tracker app, then go to the directory where habit tracker app was downloaded and then enter the following code:### Features
```commandline
pip install -r requirements.txt
```
After installing all necessary modules, you are set to go.

### Features
***
* create, update and delete habit
* Track progress for each habit
* Analyze your habits

### Usage
***
To launch the habit tracker application, run the following command in the directory where you downloaded habit tracker app:
```commandline
python main.py
```
The arrow keys can be used to choose create, check-off, analyse, and delete habits on the main screen of the application after it has been launched.

#### create new habit
If you wish to create a new habit, you must input the habit's name, description, and frequency (daily/weekly).

#### check-off your habit
if you want to check-off or mark habit as complete, just enter the name of the habit you want to check-off.

#### Analyze your habits
Choose option #3 and use the arrows to select the analytics you want if you want to analyse your habits.

#### Deleting habit
Choose "Delete your habit" from the main screen and type the name of the habit you wish to remove.

#### exit application
Selecting option #5 on the main screen will exit the application for you.

#### pre-defined habits
The habit tracker has four pre-defined habits that you may view in analyse your habits > see all of your current habits.

### Tests
***
The test module ```pytest``` is used to test the habit tracker's most crucial features. In ```test_project.py``` the habit tracker's key features were all put to the test.

You can enter the following code to test out the habit tracker application:
```commandline
pytest test_project.py
```
### Contribution
***
Contributions are encouraged! Please open an issue or send a pull request if you discover a bug or have a feature request. You can also email me at chinnumjkv16094@gmail.com.


if you want to exit the application, just select option #5 in the main screen, and you will be exited from the app.

the habit tracker comes with a 4 pre-defined habits you can see them in Analyze your habits > show all of your current habits.