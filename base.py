from flask import Flask
from excelsheetscraper import scrape_mileage_sheet
from AthleteSchedule import AthleteSchedule

app = Flask(__name__)

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
    mileage = scrape_mileage_sheet('1-22-2024-Mileage.xlsx')
    for row in mileage:
        if athlete in row[0]:
            return f"<p>{row}</p>"
    return "<p>Athlete not found</p>"
