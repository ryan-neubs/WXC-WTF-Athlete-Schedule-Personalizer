from flask import Flask, render_template
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

@app.route("/")
def hello_world():
    return "<p>This is the index page!</p>"

@app.route("/mileage")
def mileage():
    mileage = scrape_mileage_sheet('1-22-2024-Mileage.xlsx')
    return f"""<p>This page shows milage!</p>
    {mileage}
    """

@app.route("/mileage/<athlete>")
def show_athlete(athlete):
    dow = datetime.today().weekday()
    schedule = athletes[athlete]
    return render_template(
        TEMPLATES[dow], 
        athletename=schedule.get_name(), 
        mileage=schedule.get_days_mileage(dow),
        fms=schedule.get_fms(),
        notes=schedule.get_notes(),
        total_miles=schedule.get_total_miles(),
        core=schedule.get_core(dow)
        )

