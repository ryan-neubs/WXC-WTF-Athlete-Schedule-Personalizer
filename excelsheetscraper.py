import os
import pandas as pd


def scrape_mileage_sheet(sheet):
    os.chdir("./MileageSheets/")
    mileage = pd.read_excel(sheet)
    os.chdir("..")
    return mileage.values.tolist()

def scrape_workout_sheet(sheet):
    workouts = {}
    os.chdir("./WorkoutSheets/")
    workout = pd.read_excel(sheet)
    workout = workout.astype(str)
    os.chdir("..")
    data = workout.values.tolist()
    
def get_workouts(sheet):
    workouts = {}
    wo = pd.read_excel(sheet)
    rows = wo.values.tolist()
    for row in rows:
        if type(row[-1]) == str:
            workouts[row[-1].split(':')[0]] = row[-1].split(':')[1]
    return workouts