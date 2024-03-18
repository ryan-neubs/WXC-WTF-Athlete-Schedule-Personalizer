from flask import Flask, render_template, request, url_for, redirect
from excelsheetscraper import scrape_mileage_sheet, scrape_workout_sheet, get_workouts, get_roster_list
from AthleteSchedule import AthleteSchedule
from datetime import datetime
import pandas as pd
from datetime import datetime, timedelta
import os

MEN, WOMEN = get_roster_list()
TEMPLATES = ['mon.html', 'tue.html', 'wed.html', 'thu.html', 'fri.html', 'sat.html', 'sun.html']

app = Flask(__name__)

def clean_time_format(time_list):
    cleaned_times = []
    for time_str in time_list:
        print(time_str)
        time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
        cleaned_times.append(time_obj.strftime("%M:%S"))
    return cleaned_times

def get_current_week_dates():
    # Get the current date
    current_date = datetime.now()

    monday_date = current_date - timedelta(days=current_date.weekday())
    tuesday_date = monday_date + timedelta(days=1)
    friday_date = monday_date + timedelta(days=4)

    # Format the dates as "M-D" (Month-Day)
    formatted_monday = monday_date.strftime("%#m-%#d")
    formatted_tuesday = tuesday_date.strftime("%#m-%#d")
    formatted_friday = friday_date.strftime("%#m-%#d")
    # Note: The format string has to use '#' on Windows. On other platforms it needs a hyphen '-'
    # I will look more into this if it causes any issues

    return formatted_monday, formatted_tuesday, formatted_friday

workoutdata = [scrape_workout_sheet('3-12'), scrape_workout_sheet('3-15')]
workoutsW = [get_workouts('3-12')[0], get_workouts('3-15')[0]]
workoutsM = [get_workouts('3-12')[1], get_workouts('3-15')[1]]
# workoutdata = [scrape_workout_sheet(get_current_week_dates()[1]), scrape_workout_sheet(get_current_week_dates()[2])]
# workouts = [dict(sorted(get_workouts(get_current_week_dates()[1]).items())), dict(sorted(get_workouts(get_current_week_dates()[2]).items()))]

# data = scrape_mileage_sheet(get_current_week_dates()[0])
data = scrape_mileage_sheet('3-11')
if data == False:
    raise FileNotFoundError
athletes = {}
for row in data:
    if row[1] == 'FMS' or type(row[2]) == float:
        continue
    athletes[row[0]] = AthleteSchedule(row)

athleteNameList = []
for athlete in athletes:
     athleteNameList.append(athlete)

def get_MorF_workout(name, index):
    if name in WOMEN:
        return workoutsW[index]
    return workoutsM[index]

def switchNameOrder(name):
    brokenName = name.split()
    firstName = brokenName[0]
    lastName = brokenName[1]
    return lastName + ', ' + firstName

def selectAthleteWO(name, workout):
    for row in workout:
        for athlete in row:
            if athlete[0] == name:
                # List comprehensions clean out the nans from the entries
                labels = [x for x in [row[0][0]]+row[0][12:-1] if x != 'nan']
                data = [x for x in [athlete[0]]+athlete[12:-1] if x != 'nan']
                data = [data[1]] + clean_time_format(data[1:-1])+[data[-1]]
                return trimtable(labels, data)
    return False # Athlete isn't found == False

def trimtable(labels, data):
    return labels[:len(data)-1]+["Group"], data

@app.route("/", methods=["POST", "GET"])
def home():
    DOW = datetime.today().weekday()
    if request.method == "GET": 
        return render_template("index.html", athleteList = athleteNameList)
    
    if request.method == "POST":
        athlete = request.form['name']
        if athlete not in athleteNameList:
            return render_template("indexError.html", athleteList = athleteNameList)
        else:
            schedule = athletes[athlete]
            return render_template(
                TEMPLATES[DOW], 
                athletename=schedule.get_name(),
                mileage=schedule.get_days_mileage(DOW),
                fms=schedule.get_fms(),
                notes=schedule.get_notes(),
                total_miles=schedule.get_total_miles(),
                core=schedule.get_core(DOW),
                tueworkoutsheet=selectAthleteWO(athlete, workoutdata[0]),
                friworkoutsheet=selectAthleteWO(athlete, workoutdata[1]),
                tueworkoutinfo=get_MorF_workout(athlete, 0),
                friworkoutinfo=get_MorF_workout(athlete, 1)
                )
        
@app.route("/<athleteName>/<int:dow>")
def weekday(athleteName, dow):
    name = switchNameOrder(athleteName)
    schedule = athletes[name]
    return render_template(
        TEMPLATES[dow], 
        athletename=schedule.get_name(), 
        mileage=schedule.get_days_mileage(dow),
        fms=schedule.get_fms(),
        notes=schedule.get_notes(),
        total_miles=schedule.get_total_miles(),
        core=schedule.get_core(dow),
        tueworkoutsheet=selectAthleteWO(name, workoutdata[0]),
        friworkoutsheet=selectAthleteWO(name, workoutdata[1]),
        tueworkoutinfo=get_MorF_workout(name, 0),
        friworkoutinfo=get_MorF_workout(name, 1)
        )

@app.route("/search", methods=['POST'])
def show_athlete():
    DOW = datetime.today().weekday()
    if request.method == 'POST':
        athlete = request.form['name']
        if athlete not in athleteNameList:
            return render_template("indexError.html", athleteList = athleteNameList)
        else:
            schedule = athletes[athlete]
            return render_template(
                TEMPLATES[DOW], 
                athletename=schedule.get_name(),
                mileage=schedule.get_days_mileage(DOW),
                fms=schedule.get_fms(),
                notes=schedule.get_notes(),
                total_miles=schedule.get_total_miles(),
                core=schedule.get_core(DOW),
                tueworkoutsheet=selectAthleteWO(athlete, workoutdata[0]),
                friworkoutsheet=selectAthleteWO(athlete, workoutdata[1]),
                tueworkoutinfo=get_MorF_workout(athlete, 0),
                friworkoutinfo=get_MorF_workout(athlete, 1)
                )
