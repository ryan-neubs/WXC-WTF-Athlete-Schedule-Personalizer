from flask import Flask, render_template, request, url_for
from excelsheetscraper import scrape_mileage_sheet, scrape_workout_sheet
from AthleteSchedule import AthleteSchedule
from datetime import datetime
import pandas as pd

app = Flask(__name__)

data = scrape_mileage_sheet("1-22-2024-Mileage.xlsx")
athletes = {}
for row in data:
    if row[1] == 'FMS' or type(row[2]) == float:
        continue
    athletes[row[0]] = AthleteSchedule(row)

workoutdata = scrape_workout_sheet('test.xlsx')

TEMPLATES = ['mon.html', 'tue.html', 'wed.html', 'thu.html', 'fri.html', 'sat.html', 'sun.html']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mileage")
def mileage():
    mileage = scrape_mileage_sheet('1-22-2024-Mileage.xlsx')
    return f"""<p>This page shows milage!</p>
    {mileage}
    """

@app.route("/search", methods=['POST'])
def show_athlete():
    DOW = datetime.today().weekday()
    if request.method == 'POST':
        athlete = request.form['name']
        print(athlete)
        schedule = athletes[athlete]
        return render_template(
            TEMPLATES[1], 
            athletename=schedule.get_name(),
            mileage=schedule.get_days_mileage(DOW),
            fms=schedule.get_fms(),
            notes=schedule.get_notes(),
            total_miles=schedule.get_total_miles(),
            core=schedule.get_core(DOW),
            workoutsheet=workoutdata
            )

