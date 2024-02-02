import os
import pandas as pd


def scrape_mileage_sheet(sheet):
    os.chdir("./MileageSheets/")
    mileage = pd.read_excel(sheet)
    os.chdir("..")
    return mileage.values.tolist()

def scrape_workout_sheet(sheet):
    os.chdir("./WorkoutSheets/")
    workout = pd.read_excel(sheet)
    workout = workout.astype(str)
    os.chdir("..")
    return workout.values.tolist()