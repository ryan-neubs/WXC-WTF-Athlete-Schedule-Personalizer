from flask import Flask, render_template, request, url_for, redirect
from excelsheetscraper import scrape_mileage_sheet
from AthleteSchedule import AthleteSchedule
from datetime import datetime

app = Flask(__name__)

data = scrape_mileage_sheet("1-22-2024-Mileage.xlsx")
athletes = {}
for row in data:
    if row[1] == 'FMS' or type(row[2]) == float:
        continue
    athletes[row[0]] = AthleteSchedule(row)

TEMPLATES = ['mon.html', 'tue.html', 'wed.html', 'thu.html', 'fri.html', 'sat.html', 'sun.html']
DOW = datetime.today().weekday()

def fixName(name):
    brokenName = name.split()
    firstName = brokenName[0]
    lastName = brokenName[1]
    return lastName + ', ' + firstName

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
    new_name = fixName(athleteName)
    schedule = athletes[new_name]
    return render_template(
        TEMPLATES[dow], 
        athletename=schedule.get_name(), 
        mileage=schedule.get_days_mileage(dow),
        fms=schedule.get_fms(),
        notes=schedule.get_notes(),
        total_miles=schedule.get_total_miles(),
        core=schedule.get_core(dow)
        )

@app.route("/search", methods=['POST'])
def show_athlete():
    if request.method == 'POST':
        athlete = request.form['name']
        print(athlete)
        schedule = athletes[athlete]
        return render_template(
            TEMPLATES[DOW], 
            athletename=schedule.get_name(), 
            mileage=schedule.get_days_mileage(DOW),
            fms=schedule.get_fms(),
            notes=schedule.get_notes(),
            total_miles=schedule.get_total_miles(),
            core=schedule.get_core(DOW)
            )
