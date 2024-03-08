from flask import Flask, render_template, request, url_for, redirect
from excelsheetscraper import scrape_mileage_sheet, scrape_workout_sheet
from AthleteSchedule import AthleteSchedule
from datetime import datetime
import pandas as pd

app = Flask(__name__)

data = scrape_mileage_sheet("Mileage.xlsx", '1-15')
athletes = {}
for row in data:
    if row[1] == 'FMS' or type(row[2]) == float:
        continue
    athletes[row[0]] = AthleteSchedule(row)

workoutdata = scrape_workout_sheet('Workouts.xlsx', '3-5')

TEMPLATES = ['mon.html', 'tue.html', 'wed.html', 'thu.html', 'fri.html', 'sat.html', 'sun.html']

def switchNameOrder(name):
    brokenName = name.split()
    firstName = brokenName[0]
    lastName = brokenName[1]
    return lastName + ', ' + firstName

def selectAthleteWO(name):
    for row in workoutdata:
        for athlete in row:
            if athlete[0] == name:
                return [x for x in [row[0][0]]+row[0][12:-1] if x != 'nan'], [x for x in [athlete[0]]+athlete[12:-1] if x != 'nan']
    return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mileage")
def mileage():
    mileage = scrape_mileage_sheet('1-22-2024-Mileage.xlsx')
    return f"""<p>This page shows milage!</p>
    {mileage}
    """
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
            workoutsheet=selectAthleteWO(name)
        )

@app.route("/search", methods=['POST'])
def show_athlete():
    DOW = datetime.today().weekday()
    if request.method == 'POST':
        athlete = request.form['name']
        schedule = athletes[athlete]
        return render_template(
            TEMPLATES[DOW], 
            athletename=schedule.get_name(),
            mileage=schedule.get_days_mileage(DOW),
            fms=schedule.get_fms(),
            notes=schedule.get_notes(),
            total_miles=schedule.get_total_miles(),
            core=schedule.get_core(DOW),
            workoutsheet=selectAthleteWO(athlete)
            )
